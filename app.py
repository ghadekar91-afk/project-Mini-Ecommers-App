from flask import Flask, render_template
from routes.users.users import users_bp
from routes.customers.customers import customers_bp
from routes.products.products import products_bp
from routes.orders.orders import orders_bp
import pandas as pd

EXCEL_FILE = "data_new.xlsx"

# ---------- Helper ----------
def read_sheet(sheet_name):
    """Read Excel sheet safely and normalize column names"""
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
    df.columns = df.columns.str.strip().str.lower()  # remove extra spaces, lowercase
    return df

# ---------- Flask App ----------
app = Flask(__name__, template_folder="templates")
app.secret_key = "your_secret_key"

# ---------- Register Blueprints ----------
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(customers_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)

# ---------- Home Route ----------
@app.route("/")
def home():
    return render_template("home.html")

# ---------- Admin Route: View All Data ----------
from flask import session

@app.route("/admin/data")
def view_admin_data():
    customers_df = read_sheet("customers")
    products_df = read_sheet("products")
    orders_df = read_sheet("orders")

    logged_in_user_id = session.get("user_id")

    # Merge orders with products to get price for each order
    merged_df = pd.merge(orders_df, products_df, left_on="productid", right_on="id", suffixes=("_order", "_product"))

    # Calculate total revenue per order
    merged_df["total_price"] = merged_df["quantity"] * merged_df["price"]

    # Total quantity sold
    total_quantity = merged_df["quantity"].sum() if not merged_df.empty else 0
    # Total revenue
    total_revenue = merged_df["total_price"].sum() if not merged_df.empty else 0
    total_profit = (merged_df["total_price"].sum())*8/100 if not merged_df.empty else 0
    context = {
        "customers": customers_df.to_dict(orient="records"),
        "products": products_df.to_dict(orient="records"),
        "orders": merged_df.to_dict(orient="records"),
        "logged_in_user_id": logged_in_user_id,
        "total_quantity": total_quantity,
        "total_revenue": total_revenue,
        "total_profit": total_profit
    }

    return render_template("admin/data.html", **context)

if __name__ == "__main__":
    app.run(debug=True)
