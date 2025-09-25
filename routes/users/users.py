import pandas as pd
from flask import Blueprint, request, redirect, url_for, render_template, session

EXCEL_FILE = "data_new.xlsx"
USERS_SHEET = "users"
CUSTOMERS_SHEET = "customers"

users_bp = Blueprint("users", __name__, template_folder="../../templates/users")

# ---------- Helper ----------
def read_users():
    df = pd.read_excel(EXCEL_FILE, sheet_name=USERS_SHEET)
    df.columns = df.columns.str.strip().str.lower()  # strip spaces & lowercase
    return df

def write_users(df):
    with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=USERS_SHEET, index=False)

def read_customers():
    df = pd.read_excel(EXCEL_FILE, sheet_name=CUSTOMERS_SHEET)
    df.columns = df.columns.str.strip().str.lower()
    return df

def write_customers(df):
    with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=CUSTOMERS_SHEET, index=False)

# ---------- Register ----------
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        email = request.form.get("email","").strip()
        phone = request.form.get("phone","").strip()
        address = request.form.get("address","").strip()

        users_df = read_users()
        new_user_id = int(users_df["id"].max()) + 1 if not users_df.empty else 1

        # Append user
        new_user = pd.DataFrame([[new_user_id, username, password]], columns=users_df.columns)
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        write_users(users_df)

        # Append customer record with same new ID
        customers_df = read_customers()
        new_customer = pd.DataFrame([[new_user_id, username, email, phone, address]], columns=customers_df.columns)
        customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
        write_customers(customers_df)

        return redirect(url_for("users.login"))

    return render_template("users/register.html")

# ---------- Login ----------
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # read users safely
        users_df = pd.read_excel(EXCEL_FILE, sheet_name=USERS_SHEET)
        users_df.columns = users_df.columns.str.strip().str.lower()
        users_df["username"] = users_df["username"].astype(str).str.strip()
        users_df["password"] = users_df["password"].astype(str).str.strip()

        # match exactly
        user = users_df[(users_df["username"] == username) & (users_df["password"] == password)]

        if not user.empty:
            session["user_id"] = int(user.iloc[0]["id"])
            session["username"] = username
            return redirect(url_for("products.display_products"))

        return "Invalid credentials", 401

    return render_template("users/login.html")


# ---------- Logout ----------
@users_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("users.login"))
