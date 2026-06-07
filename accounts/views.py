import base64
import hashlib
import json
import random
import secrets
import time
from datetime import timedelta
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .email import send_otp_email
from .models import OTPRecord, User


_otp_rate_limit = {}  # {email: [timestamp, ...]}; resets on server restart.


def _rate_limited(email: str, limit=3, window_seconds=60) -> bool:
	now = time.time()
	timestamps = _otp_rate_limit.get(email, [])
	timestamps = [ts for ts in timestamps if now - ts < window_seconds]
	if len(timestamps) >= limit:
		_otp_rate_limit[email] = timestamps
		return True
	timestamps.append(now)
	_otp_rate_limit[email] = timestamps
	return False


def _mask_email(email: str) -> str:
	if "@" not in email:
		return email
	name, domain = email.split("@", 1)
	if len(name) <= 2:
		masked = name[0] + "*"
	else:
		masked = name[0] + ("*" * (len(name) - 2)) + name[-1]
	return f"{masked}@{domain}"


def _decode_jwt_payload(token: str) -> dict:
	try:
		parts = token.split(".")
		if len(parts) != 3:
			return {}
		payload = parts[1]
		padding = "=" * (-len(payload) % 4)
		payload_bytes = base64.urlsafe_b64decode(payload + padding)
		return json.loads(payload_bytes.decode("utf-8"))
	except Exception:
		return {}


def login_view(request):
	if request.method == "POST":
		email = request.POST.get("email", "").strip().lower()
		password = request.POST.get("password", "")

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			user = None

		if not user or not user.is_email_verified or not user.check_password(password):
			messages.error(request, "Invalid credentials.")
			return render(request, "accounts/login.html", {"email": email})

		session_cart = request.session.get("cart", {}).copy()
		login(request, user, backend="accounts.backends.EmailBackend")
		request.session["cart"] = session_cart
		next_url = request.GET.get("next") or reverse("store:home")
		return redirect(next_url)

	return render(request, "accounts/login.html")


def logout_view(request):
	if request.method != "POST":
		return redirect("store:home")
	logout(request)
	return redirect("store:home")


def register_step1(request):
	if request.method == "POST":
		email = request.POST.get("email", "").strip().lower()
		name = request.POST.get("name", "").strip()
		password = request.POST.get("password", "")
		confirm_password = request.POST.get("confirm_password", "")

		errors = {}
		if not email or "@" not in email:
			errors["email"] = "Please enter a valid email address."
		if not name:
			errors["name"] = "Please enter your name."
		if len(password) < 8:
			errors["password"] = "Password must be at least 8 characters."
		if password != confirm_password:
			errors["confirm_password"] = "Passwords do not match."

		if errors:
			for msg in errors.values():
				messages.error(request, msg)
			return render(
				request,
				"accounts/register.html",
				{"errors": errors, "email": email, "name": name},
			)

		if _rate_limited(email):
			messages.error(request, "Too many OTP requests. Please wait a minute.")
			return render(request, "accounts/register.html", {"email": email, "name": name})

		existing = User.objects.filter(email=email, is_email_verified=True).first()
		if existing:
			messages.error(request, "An account with this email already exists.")
			return render(request, "accounts/register.html", {"email": email, "name": name})

		otp = str(random.randint(100000, 999999))
		otp_hash = hashlib.sha256(otp.encode()).hexdigest()
		expires_at = timezone.now() + timedelta(minutes=10)

		OTPRecord.objects.update_or_create(
			email=email,
			defaults={
				"otp_hash": otp_hash,
				"expires_at": expires_at,
				"pending_name": name,
				"pending_password": password,  # Plain temporarily; cleared after use.
			},
		)

		if not send_otp_email(email, otp, name):
			messages.error(request, "Failed to send OTP email. Please try again.")
			return render(request, "accounts/register.html", {"email": email, "name": name})

		request.session["pending_email"] = email
		messages.success(request, "OTP sent! Please check your email.")
		return redirect("accounts:register_verify")

	return render(request, "accounts/register.html")


def register_step2(request):
	pending_email = request.session.get("pending_email")
	if not pending_email:
		return redirect("accounts:register")

	if request.method == "POST":
		otp = request.POST.get("otp", "").strip()
		if not otp:
			messages.error(request, "Please enter the OTP sent to your email.")
			return render(
				request,
				"accounts/register_verify.html",
				{"masked_email": _mask_email(pending_email)},
			)

		otp_record = OTPRecord.objects.filter(email=pending_email).first()
		if not otp_record:
			messages.error(request, "OTP expired or invalid. Please register again.")
			return redirect("accounts:register")

		if otp_record.expires_at <= timezone.now():
			otp_record.delete()
			messages.error(request, "OTP has expired. Please register again.")
			return redirect("accounts:register")

		if hashlib.sha256(otp.encode()).hexdigest() != otp_record.otp_hash:
			messages.error(request, "Incorrect OTP. Please try again.")
			return render(
				request,
				"accounts/register_verify.html",
				{"masked_email": _mask_email(pending_email)},
			)

		if User.objects.filter(email=pending_email).exists():
			messages.error(request, "An account with this email already exists.")
			otp_record.delete()
			return redirect("accounts:login")

		user = User.objects.create_user(
			email=pending_email,
			name=otp_record.pending_name,
			password=otp_record.pending_password,
		)
		user.is_email_verified = True
		user.save()

		otp_record.delete()
		del request.session["pending_email"]

		session_cart = request.session.get("cart", {}).copy()
		login(request, user, backend="accounts.backends.EmailBackend")
		request.session["cart"] = session_cart

		messages.success(request, "Account created successfully! Welcome to AnimeShop.")
		return redirect("store:home")

	return render(
		request,
		"accounts/register_verify.html",
		{"masked_email": _mask_email(pending_email)},
	)


def resend_otp(request):
	if request.method != "POST":
		return redirect("accounts:register")

	pending_email = request.session.get("pending_email")
	if not pending_email:
		return redirect("accounts:register")

	if _rate_limited(pending_email):
		messages.error(request, "Too many OTP requests. Please wait a minute.")
		return redirect("accounts:register_verify")

	otp_record = OTPRecord.objects.filter(email=pending_email).first()
	if not otp_record:
		messages.error(request, "OTP expired or invalid. Please register again.")
		return redirect("accounts:register")

	otp = str(random.randint(100000, 999999))
	otp_hash = hashlib.sha256(otp.encode()).hexdigest()
	otp_record.otp_hash = otp_hash
	otp_record.expires_at = timezone.now() + timedelta(minutes=10)
	otp_record.save()

	send_otp_email(pending_email, otp, otp_record.pending_name)
	messages.success(request, "A new OTP has been sent to your email.")
	return redirect("accounts:register_verify")


def google_login(request):
	if not settings.GOOGLE_CLIENT_ID:
		messages.error(request, "Google login is not configured yet.")
		return redirect("accounts:login")

	redirect_uri = request.build_absolute_uri(reverse("accounts:google_callback"))
	state = secrets.token_urlsafe(16)
	request.session["google_oauth_state"] = state

	params = {
		"client_id": settings.GOOGLE_CLIENT_ID,
		"redirect_uri": redirect_uri,
		"response_type": "code",
		"scope": "openid email profile",
		"state": state,
		"prompt": "select_account",
	}
	return redirect("https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params))


def google_callback(request):
	state = request.GET.get("state")
	code = request.GET.get("code")
	expected_state = request.session.get("google_oauth_state")
	if not state or not expected_state or state != expected_state:
		messages.error(request, "Invalid OAuth state. Please try again.")
		return redirect("accounts:login")

	del request.session["google_oauth_state"]

	if not code:
		messages.error(request, "Google login failed. Please try again.")
		return redirect("accounts:login")

	redirect_uri = request.build_absolute_uri(reverse("accounts:google_callback"))
	token_resp = requests.post(
		"https://oauth2.googleapis.com/token",
		data={
			"code": code,
			"client_id": settings.GOOGLE_CLIENT_ID,
			"client_secret": settings.GOOGLE_CLIENT_SECRET,
			"redirect_uri": redirect_uri,
			"grant_type": "authorization_code",
		},
		timeout=10,
	)

	if token_resp.status_code != 200:
		messages.error(request, "Google login failed. Please try again.")
		return redirect("accounts:login")

	token_data = token_resp.json()
	id_token = token_data.get("id_token")
	if not id_token:
		messages.error(request, "Google login failed. Please try again.")
		return redirect("accounts:login")

	payload = _decode_jwt_payload(id_token)
	email = (payload.get("email") or "").lower()
	name = payload.get("name") or ""
	google_id = payload.get("sub")
	email_verified = payload.get("email_verified", False)

	if not email or not google_id:
		messages.error(request, "Google login failed. Please try again.")
		return redirect("accounts:login")

	user = User.objects.filter(email=email).first()
	if user:
		if not user.google_id:
			user.google_id = google_id
		if email_verified:
			user.is_email_verified = True
		user.save()
	else:
		user = User.objects.create(
			email=email,
			name=name or email.split("@")[0],
			google_id=google_id,
			is_email_verified=True,
		)

	session_cart = request.session.get("cart", {}).copy()
	login(request, user, backend="accounts.backends.EmailBackend")
	request.session["cart"] = session_cart

	messages.success(request, "Welcome back to AnimeShop!")
	return redirect("store:home")


@login_required(login_url="accounts:login")
def profile_view(request):
	return render(request, "accounts/profile.html")
