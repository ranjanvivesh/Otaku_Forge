from django.contrib import admin
from .models import User, OTPRecord


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ["email", "name", "is_email_verified", "google_id", "is_admin", "created_at"]
	list_filter = ["is_email_verified", "is_admin"]
	search_fields = ["email", "name"]
	readonly_fields = ["created_at"]


@admin.register(OTPRecord)
class OTPAdmin(admin.ModelAdmin):
	list_display = ["email", "expires_at", "created_at"]
