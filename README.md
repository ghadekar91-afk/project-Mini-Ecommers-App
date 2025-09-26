Mini E-Commerce Web Application


* Directory Structure
ECOMMERCE_APP/
│── app.py # Main entry point
│── requirements.txt # Dependencies
│── data_new.xlsx # Excel file (if using Excel DB)
│── ecommerce.db # SQLite database (if using SQL DB)
│
├── routes/ # All routes organized
│ ├── users/ # Customer/Seller/Admin routes
│ │ └── users.py
│ ├── products/ # Product related routes
│ │ └── products.py
│ └── orders/ # Order management
│ └── orders.py
│
├── templates/ # HTML files
│ ├── users/
│ │ ├── register.html
│ │ ├── login.html
│ │ └── dashboard.html
│ ├── products/
│ │ └── products.html
│ └── orders/
│ └── orders.html
│
└── static/

*By default, the app runs at:
👉 http://127.0.0.1:5000/



὆ User Roles
● Customer: Register/Login, View products, Place orders
● Seller: Login, Add new products, Update stock and price
● Admin: Manage users, Manage products, View all orders

📷 UI Overview

Users

register.html → New user registration

login.html → User login

dashboard.html → User-specific dashboard

Products

products.html → View/add products

Orders

orders.html → Place/view orders

Admin

/admin/data → Dashboard to view all Customers, Products, Orders, Revenue, and Profit


📖 Example Usage
User Flow:

A new user registers on /users/register.

The user logs in via /users/login.

After login, they access their dashboard.

Customers browse products, add items to cart, and place orders.

Admin checks /admin/data to see analytics



📌 Features

User Management: Register, login, and dashboard for customers/sellers/admins.

Product Management: Add, view, and update products.

Order Management: Place and track customer orders.


🔮 Future Enhancements

✅ Add Authentication with Flask-Login

✅ Replace Excel storage with SQLAlchemy ORM

✅ Add Payment Gateway Integration (Stripe/PayPal)

✅ Add product categories & search functionality

✅ Implement REST API endpoints for mobile apps




📌 Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, Jinja2 templates

Database Options: Excel (pandas) / SQLite (sqlalchemy or sqlite3)

Libraries: pandas, flask, openpyxl

Flexible Storage: Supports Excel (data_new.xlsx) or SQLite (ecommerce.db).
