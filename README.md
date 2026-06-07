
## ✨ Features

- **🔐 Custom Authentication** — Email-only signup with OTP registration system inspired by modern authentication patterns
- **📚 Product Catalog** — Browse beautiful anime merchandise organized by categories with powerful search functionality
- **🛒 Smart Shopping Cart** — Session-based cart for seamless product management and checkout experience
- **🎨 Dark Manga Aesthetic** — Striking design with black, white, red, and gold color palette
- **👨‍💼 Admin Dashboard** — Comprehensive Django admin panel for managing products, orders, and user accounts
- **⚡ Optimized Performance** — Built for speed with PostgreSQL backend and efficient query optimization

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.x |
| **Language** | Python 3.8+ |
| **Database** | PostgreSQL |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```
animeshop/
├── animeshop/                    # Main project configuration
│   ├── settings.py               # Django settings & configuration
│   ├── urls.py                   # URL routing & endpoints
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
│
├── accounts/                     # User authentication & management
│   ├── models.py                 # Custom user model with email-based auth
│   ├── views.py                  # Authentication views & logic
│   ├── forms.py                  # User registration & login forms
│   ├── admin.py                  # Admin interface customization
│   └── email.py                  # Email handling & OTP system
│
├── store/                        # Product & shopping cart logic
│   ├── models.py                 # Product, Category, Cart models
│   ├── views.py                  # Store views & shopping logic
│   ├── forms.py                  # Store forms
│   ├── admin.py                  # Store admin interface
│   └── urls.py                   # Store URL patterns
│
├── templates/                    # HTML templates
│   ├── base.html                 # Base template with nav & footer
│   ├── home.html                 # Homepage
│   ├── product_list.html         # Products grid display
│   ├── product_detail.html       # Individual product page
│   ├── cart.html                 # Shopping cart page
│   └── auth/                     # Authentication templates
│       ├── signup.html
│       ├── login.html
│       └── otp_verify.html
│
├── static/                       # Static files
│   ├── css/
│   │   ├── style.css             # Main stylesheet
│   │   └── dark_theme.css        # Dark manga aesthetic
│   ├── js/
│   │   └── script.js             # Client-side logic
│   └── images/
│       ├── logo/
│       └── products/
│
├── media/                        # User uploaded files
│   └── products/                 # Product images
│
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **PostgreSQL** — [Download](https://www.postgresql.org/download/)
- **Git** — [Download](https://git-scm.com/download/)
- **pip** — Usually comes with Python
- **virtualenv** — `pip install virtualenv`

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/animeshop.git
cd animeshop
```

#### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-very-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/animeshop

# Email Configuration (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Email Configuration (for production)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

#### 5. Run Database Migrations

```bash
python manage.py migrate
```

#### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

#### 7. Create Sample Data (Optional)

```bash
python manage.py shell
```

Then in the Python shell:

```python
from store.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

# Create categories
category = Category.objects.create(
    name="Manga",
    description="Manga books and merchandise"
)

# Create a product
product = Product.objects.create(
    name="Attack on Titan Vol. 1",
    description="Start your journey with the first volume",
    price=9.99,
    category=category,
    stock=50
)

exit()
```

#### 8. Run Development Server

```bash
python manage.py runserver
```

Now visit:

- **🌐 Main Application:** http://127.0.0.1:8000/
- **👨‍💼 Admin Panel:** http://127.0.0.1:8000/admin/

Use the superuser credentials you created in step 6 to log in to the admin panel.

---

## 📝 Usage

### For Customers

1. **Browse Products** — Navigate through the product catalog
2. **Search** — Use the search bar to find specific items
3. **View Details** — Click on a product to see more information
4. **Add to Cart** — Add items to your shopping cart
5. **Checkout** — Review cart and proceed with purchase

### For Administrators

1. Go to **http://127.0.0.1:8000/admin/**
2. Log in with your superuser credentials
3. Manage:
   - **Products** — Add, edit, or remove products
   - **Categories** — Organize products by category
   - **Orders** — Track customer orders
   - **Users** — Manage user accounts

---

## 🗺️ Roadmap

- [ ] 💳 **Razorpay Payment Integration** — Enable online payments
- [ ] 📦 **Order History & Tracking** — Let users track their orders
- [ ] ❤️ **Wishlist Functionality** — Users can save favorite items
- [ ] ⭐ **Product Reviews & Ratings** — Customer feedback system
- [ ] 👤 **User Profile Page** — User account settings and details
- [ ] 🔍 **Advanced Filtering** — Filter by price, rating, etc.
- [ ] 📧 **Email Notifications** — Order confirmations and updates
- [ ] 📱 **Mobile App** — React Native mobile application

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy.

### 2. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes

Edit files and add your improvements.

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add: amazing new feature"
```

### 5. Push to Your Branch

```bash
git push origin feature/amazing-feature
```

### 6. Open a Pull Request

Go to GitHub and click "Compare & pull request" to submit your PR.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 animeshop

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🆘 Troubleshooting

### Database Connection Error

**Error:** `could not connect to server: No such file or directory`

**Solution:** Make sure PostgreSQL is running:

```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Windows
# Start the PostgreSQL service from Services
```

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:** Make sure virtual environment is activated and dependencies installed:

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Migration Errors

**Error:** `relation "store_product" does not exist`

**Solution:** Run migrations again:

```bash
python manage.py migrate
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:** Use a different port:

```bash
python manage.py runserver 8080
```

---

## 📚 Additional Resources

- **Django Documentation** — https://docs.djangoproject.com/
- **PostgreSQL Documentation** — https://www.postgresql.org/docs/
- **Python Documentation** — https://docs.python.org/3/
- **Django Rest Framework** — https://www.django-rest-framework.org/
- **Git Basics** — https://git-scm.com/book/en/v2

---

## 👤 Author

**Vivesh** — Anime Enthusiast & Developer

- 🌐 GitHub: [@yourusername](https://github.com/yourusername)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourusername)
- 🐦 Twitter: [@yourhandle](https://twitter.com/yourhandle)

---

## 💬 Support

Have questions or need help?

- 📧 **Email:** your.email@gmail.com
- 💬 **GitHub Discussions:** [Ask a Question](https://github.com/yourusername/animeshop/discussions)
- 🐛 **Report a Bug:** [Create an Issue](https://github.com/yourusername/animeshop/issues)

---

## 🎨 UI Preview

For a detailed visual preview with animations and dark theme styling, check out **[README.html](README.html)** in this repository.

---

## 📊 Project Stats

- **Status:** Active Development
- **Python Version:** 3.8+
- **Django Version:** 4.2+
- **Database:** PostgreSQL
- **License:** MIT

---

<div align="center">

**Built with ❤️ for anime enthusiasts worldwide**

*Designed with dark manga aesthetics | Crafted with Django | Powered by Python*

⭐ If you like this project, please give it a star!

</div>
