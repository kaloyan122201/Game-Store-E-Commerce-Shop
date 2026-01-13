# Game-Store-E-Commerce-Shop
Quest Haven - E-commerce Game Store
A full-featured Django e-commerce platform for selling video games, consoles, and gaming accessories.

Project Overview
Quest Haven is a modern e-commerce solution built with Django that provides a complete online shopping experience for gamers. The platform includes user authentication, product catalog management, shopping cart functionality, order processing with email confirmation, and an administrative dashboard.

Features:
  User Features
  User registration and authentication
  User profiles with shipping information
  Password reset functionality
  Order history tracking
  Shopping Features
  Product browsing by categories
  Detailed product pages
  Shopping cart with quantity management
  Real-time cart updates
  Secure checkout process
  Multiple payment methods (Cash on Delivery, Bank Transfer, Card)
  Order confirmation emails with HTML templates

Admin Features
  Django admin panel for product management
  Order management system
  User management
  Inventory tracking
  Sales reporting

Technology Stack:
  Backend:
    Framework: Django 6.0
    Database: SQLite3 (development) - Built into Python
    Authentication: Django built-in auth system
    Email: Django SMTP backend with TLS support
    Image Processing: Pillow 12.1.0
  
  Frontend:
    Templates: Django template language
    Styling: Custom CSS with responsive design
    Images: ImageField with Pillow support

Development Tools:
  Environment: Virtual environment with pip
  Version Control: Git
  Dependency Management: requirements.txt

Project Structure
text
quest-haven/
│
├── accounts/                          # User authentication app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Extended user profile model
│   ├── views.py                       # Login, register, profile views
│   ├── urls.py                        # Authentication URLs
│   └── templates/accounts/            # Auth templates
│
├── products_and_categories/           # Main store functionality
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                      # Product, Category, Cart, Order models
│   ├── views.py                       # Store views and logic
│   ├── urls.py                        # Store URLs
│   └── templates/products_and_categories/  # Store templates
│       ├── home.html                  # Homepage with categories
│       ├── category_products.html     # Products by category
│       ├── cart.html                  # Shopping cart
│       ├── checkout.html              # Checkout page
│       └── checkout_success.html      # Order confirmation
│
├── store/                             # Main project configuration
│   ├── __init__.py
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py                        # WSGI configuration
│   └── asgi.py                        # ASGI configuration
│
├── static/                            # Static files
│   └── css/
│       └── style.css                  # Main stylesheet
│
├── templates/                         # Base templates
│   └── base.html                      # Base template structure
│
├── media/                             # Uploaded media files
│   ├── categories/                    # Category images
│   └── products/                      # Product images
│
├── requirements.txt                   # Python dependencies
├── manage.py                          # Django management script
└── README.md                          # This file
Dependencies
The project requires the following Python packages (see requirements.txt):

text
Django==6.0
Pillow==12.1.0
asgiref==3.11.0
sqlparse==0.5.5
tzdata==2025.3
Note: SQLite3 database is built into Python and does not require separate installation.

Installation Guide
Prerequisites
Python 3.8 or higher

pip (Python package manager)
Git (for version control)

Step-by-Step Installation

Clone the Repository
  git clone https://github.com/yourusername/quest-haven.git
  cd quest-haven

Create Virtual Environment
  python -m venv venv

Activate virtual enviroment on Windows:
  venv\Scripts\activate

Activate virtual enviroment on Mac/Linux:
  source venv/bin/activate

Install the required modules in order for the program to work properly
  pip install -r requirements.txt
  
Apply Database Migrations
  Save changes (after python manage.py makemigrations)
  python manage.py migrate

Create Superuser (Admin)
  Creating superuser so you can make changes, add products, categories
  python manage.py createsuperuser
  Follow the prompts to create an admin account.

Run Development Server
  python manage.py runserver
  
Access the Application
  Main site: http://127.0.0.1:8000
  Admin panel: http://127.0.0.1:8000/admin

Database Configuration
Development Database - The project uses SQLite3 by default, which is included with Python:

python
# store/settings.py - Default configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SQLite3 Advantages:
  No installation required (built into Python)
  Single file database (easy to backup and transfer)
  Fast and reliable for development
  Zero configuration needed
