from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import csv
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = "data.csv"
FORMAT = "%d-%m-%Y"
COLUMNS = ["date", "amount", "category", "description"]
CATEGORIES = {"I": "INCOME", "E": "EXPENSE"}


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)


def read_data():
    initialize_csv()
    df = pd.read_csv(CSV_FILE)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], format=FORMAT)
    return df


def add_entry(date_str, amount, category, description):
    
    try:
        if len(date_str) == 10 and date_str[4] == '-':
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            date_str = dt.strftime(FORMAT)
    except:
        pass
    
    description = description.replace(",", " -")
    
    new_entry = {
        "date": date_str,
        "amount": amount,
        "category": category,
        "description": description
    }
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS, quoting=csv.QUOTE_ALL)
        writer.writerow(new_entry)


@app.route("/")
def index():
    df = read_data()
    total_income = 0
    total_expense = 0
    total_save = 0
    recent = []
    
    if not df.empty:
        total_income = df[df["category"] == "INCOME"]["amount"].sum()
        total_expense = df[df["category"] == "EXPENSE"]["amount"].sum()
        total_save = total_income - total_expense
        recent = df.sort_values("date", ascending=False).head(5)
        recent = recent.to_dict("records")
        for r in recent:
            r["date"] = r["date"].strftime(FORMAT)
    
    return render_template(
        "index.html",
        total_income=f"{total_income:.2f}",
        total_expense=f"{total_expense:.2f}",
        total_save=f"{total_save:.2f}",
        recent=recent,
        has_data=not df.empty
    )


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date_str = request.form.get("date")
        amount = float(request.form.get("amount"))
        category = request.form.get("category")
        description = request.form.get("description", "")
        
        if not date_str:
            date_str = datetime.today().strftime(FORMAT)
        
        add_entry(date_str, amount, category, description)
        return redirect(url_for("index"))
    
    return render_template("add.html")


@app.route("/report", methods=["GET", "POST"])
def report():
    df = read_data()
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    
    if df.empty:
        return render_template("report.html", has_data=False, transactions=[])
    
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        mask = (df["date"] >= start_dt) & (df["date"] <= end_dt)
        filtered = df.loc[mask]
    else:
        filtered = df
        start_date = df["date"].min().strftime("%Y-%m-%d")
        end_date = df["date"].max().strftime("%Y-%m-%d")
    
    if filtered.empty:
        return render_template("report.html", has_data=False, transactions=[])
    
    # Prepare data for charts
    income_data = filtered[filtered["category"] == "INCOME"].copy()
    expense_data = filtered[filtered["category"] == "EXPENSE"].copy()
    
    monthly_income = income_data.set_index("date").resample("ME")["amount"].sum()
    monthly_expense = expense_data.set_index("date").resample("ME")["amount"].sum()
    
    months = monthly_income.index.strftime("%b %Y").tolist()
    income_values = monthly_income.tolist()
    expense_values = monthly_expense.tolist()
    
    # Category breakdown for expenses
    category_breakdown = expense_data.groupby("category")["amount"].sum()
    cat_labels = category_breakdown.index.tolist()
    cat_values = category_breakdown.values.tolist()
    
    total_income = income_data["amount"].sum()
    total_expense = expense_data["amount"].sum()
    total_save = total_income - total_expense
    
    transactions = filtered.sort_values("date", ascending=False).to_dict("records")
    for t in transactions:
        t["date"] = t["date"].strftime(FORMAT)
        t["amount"] = f"{t['amount']:.2f}"
    
    return render_template(
        "report.html",
        has_data=True,
        transactions=transactions,
        total_income=f"{total_income:.2f}",
        total_expense=f"{total_expense:.2f}",
        total_save=f"{total_save:.2f}",
        months=months,
        income_values=income_values,
        expense_values=expense_values,
        cat_labels=cat_labels,
        cat_values=cat_values,
        start_date=start_date,
        end_date=end_date
    )


@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    df = pd.read_csv(CSV_FILE)
    if index < len(df):
        df = df.drop(index).reset_index(drop=True)
        df.to_csv(CSV_FILE, index=False)
    return redirect(url_for("report"))


if __name__ == "__main__":
    initialize_csv()
    app.run(debug=True)