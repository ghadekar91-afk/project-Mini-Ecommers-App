import pandas as pd
from flask import Blueprint, request, redirect, url_for, render_template

EXCEL_FILE = "data_new.xlsx"
PRODUCTS_SHEET = "products"

products_bp = Blueprint("products", __name__, template_folder="../../templates/products")

# ---------- Helper ----------
def read_products():
    return pd.read_excel(EXCEL_FILE, sheet_name=PRODUCTS_SHEET)

def write_products(df):
    with pd.ExcelWriter(EXCEL_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name=PRODUCTS_SHEET, index=False)

# ---------- Display ----------
@products_bp.route("/products/details")
def display_products():
    df = read_products()
    df.columns = df.columns.str.lower()
    return render_template("products/details.html", products=df.to_dict(orient="records"))

# ---------- Add ----------
@products_bp.route("/products/add", methods=["GET","POST"])
def add_product():
    if request.method=="POST":
        name = request.form["name"]
        price = request.form.get("price",0)
        stock = request.form.get("stock",0)
        category = request.form.get("category","")
        details = request.form.get("details","")
        rating = request.form.get("rating",0)
        image_url = request.form.get("image_url")

        df = read_products()
        df.columns = df.columns.str.lower()
        new_id = df["id"].max()+1 if not df.empty else 1
        new_row = pd.DataFrame([[new_id, name, price, stock, category, details, rating,image_url]], columns=df.columns)
        df = pd.concat([df,new_row], ignore_index=True)
        write_products(df)
        return redirect(url_for("products.display_products"))

    return render_template("products/add.html")

# ---------- Update ----------
@products_bp.route("/products/update/<int:id>", methods=["GET","POST"])
def update_product(id):
    df = read_products()
    df.columns = df.columns.str.lower()
    idx = df.index[df["id"]==id].tolist()
    if not idx:
        return "Product not found",404
    row_idx = idx[0]

    if request.method=="POST":
        df.at[row_idx,"name"]=request.form["name"]
        df.at[row_idx,"price"]=request.form.get("price",0)
        df.at[row_idx,"stock"]=request.form.get("stock",0)
        df.at[row_idx,"category"]=request.form.get("category","")
        df.at[row_idx,"details"]=request.form.get("details","")
        df.at[row_idx,"rating"]=request.form.get("rating",0)
        write_products(df)
        return redirect(url_for("products.display_products"))

    product = df.loc[row_idx].to_dict()
    return render_template("products/update.html", product=product)

# ---------- Delete ----------
@products_bp.route("/products/delete/<int:id>", methods=["POST"])
def delete_product(id):
    df = read_products()
    df.columns = df.columns.str.lower()
    df = df[df["id"]!=id]
    write_products(df)
    return redirect(url_for("products.display_products"))
