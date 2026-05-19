# =========================================================
# BUDGETFLOW - FULLY CORRECTED WITH EDIT & DELETE
# Save as: bud.py
# Run: streamlit run bud.py
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="BudgetFlow",
    page_icon="💸",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.main {
    background: #0f172a;
    color: white;
}

.block-container {
    padding-top: 1rem;
    max-width: 1250px;
}

.big-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
}

.subtitle {
    color: #94a3b8;
    font-size: 18px;
}

.login-card {
    background: #111827;
    padding: 40px;
    border-radius: 25px;
    border: 1px solid #334155;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(135deg,#3b82f6,#2563eb);
    color: white;
    border: none;
    height: 50px;
    border-radius: 14px;
    font-size: 16px;
    font-weight: 600;
}

.stButton>button:hover {
    transform: scale(1.02);
}

.stTextInput input,
.stNumberInput input,
.stDateInput input {

    background: #1e293b !important;
    color: white !important;
    border-radius: 14px !important;
    border: 1px solid #334155 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #1e293b !important;
    color: white !important;
}

.stSelectbox svg {
    fill: white !important;
}

div[data-baseweb="popover"] {
    background-color: #1e293b !important;
}

div[role="listbox"] ul {
    background-color: #1e293b !important;
}

div[role="option"] {
    color: white !important;
    background-color: #1e293b !important;
}

div[role="option"]:hover {
    background-color: #334155 !important;
}

[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 20px;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: white;
}

.small-text {
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FILES
# =========================================================

USER_FILE = "users.json"
DATA_FILE = "budget_data.csv"
CATEGORY_FILE = "categories.txt"
CURRENCY_FILE = "currencies.json"

# =========================================================
# CREATE USER FILES
# =========================================================

if not os.path.exists(USER_FILE):

    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

if not os.path.exists(CURRENCY_FILE):

    with open(CURRENCY_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

# =========================================================
# DEFAULT CATEGORIES
# =========================================================

default_categories = [
    "🍔 Food",
    "🏠 Rent",
    "🛍️ Shopping",
    "🚕 Travel",
    "🎮 Entertainment",
    "🏥 Healthcare",
    "📚 Education",
    "💡 Bills",
    "💼 Salary",
    "📈 Investments",
    "📦 Others"
]

# =========================================================
# CREATE CATEGORY FILE
# =========================================================

if not os.path.exists(CATEGORY_FILE):

    with open(CATEGORY_FILE, "w", encoding="utf-8") as f:

        for item in default_categories:
            f.write(item + "\n")

# =========================================================
# LOAD CATEGORIES
# =========================================================

with open(CATEGORY_FILE, "r", encoding="utf-8") as f:

    file_categories = [
        line.strip()
        for line in f.readlines()
        if line.strip()
    ]

categories = default_categories.copy()

for item in file_categories:

    if item not in categories:
        categories.append(item)

with open(CATEGORY_FILE, "w", encoding="utf-8") as f:

    for item in categories:
        f.write(item + "\n")

# =========================================================
# CREATE DATA FILE
# =========================================================

if not os.path.exists(DATA_FILE):

    df = pd.DataFrame(columns=[
        "User",
        "Date",
        "Category",
        "Amount",
        "Type",
        "Description"
    ])

    df.to_csv(DATA_FILE, index=False)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(DATA_FILE)

required_columns = [
    "User",
    "Date",
    "Category",
    "Amount",
    "Type",
    "Description"
]

for col in required_columns:

    if col not in df.columns:
        df[col] = ""

df = df[required_columns]

df.to_csv(DATA_FILE, index=False)

with open(USER_FILE, "r", encoding="utf-8") as f:
    users = json.load(f)

with open(CURRENCY_FILE, "r", encoding="utf-8") as f:
    user_currencies = json.load(f)

# =========================================================
# CURRENCY OPTIONS
# =========================================================

currency_options = {
    "India (₹)": "₹",
    "USA ($)": "$",
    "Europe (€)": "€",
    "UK (£)": "£",
    "Japan (¥)": "¥",
    "UAE (AED)": "AED",
    "Canada (C$)": "C$",
    "Australia (A$)": "A$"
}

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.markdown("""
    <center>
    <div class='big-title'>
    💸 BudgetFlow
    </div>

    <div class='subtitle'>
    Smart Budget Management System
    </div>
    </center>
    """, unsafe_allow_html=True)

    st.markdown("")

    col1, col2, col3 = st.columns([1,1.2,1])

    with col2:

        st.markdown("<div class='login-card'>", unsafe_allow_html=True)

        menu = st.radio(
            "Choose",
            ["Login", "Create Account"],
            horizontal=True
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        selected_currency = st.selectbox(
            "Select Your Currency",
            list(currency_options.keys())
        )

        if menu == "Login":

            if st.button("Login"):

                if username in users:

                    if users[username] == password:

                        st.session_state.logged_in = True
                        st.session_state.username = username

                        st.success("Login Successful")
                        st.rerun()

                    else:
                        st.error("Wrong Password")

                else:
                    st.error("User Not Found")

        else:

            if st.button("Create Account"):

                if username in users:

                    st.warning("Username already exists")

                else:

                    users[username] = password

                    user_currencies[username] = currency_options[selected_currency]

                    with open(USER_FILE, "w", encoding="utf-8") as f:
                        json.dump(users, f)

                    with open(CURRENCY_FILE, "w", encoding="utf-8") as f:
                        json.dump(user_currencies, f)

                    st.success("Account Created Successfully")

        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# MAIN APP
# =========================================================

else:

    current_user = st.session_state.username

    currency_symbol = user_currencies.get(current_user, "₹")

    user_df = df[df["User"] == current_user]

    # =====================================================
    # HEADER
    # =====================================================

    col1, col2 = st.columns([5,1])

    with col1:

        st.markdown(f"""
        <div class='big-title'>
        💸 BudgetFlow
        </div>

        <div class='small-text'>
        Welcome back, {current_user}
        </div>
        """, unsafe_allow_html=True)

    with col2:

        if st.button("Logout"):

            st.session_state.logged_in = False
            st.rerun()

    st.markdown("")

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Dashboard",
        "➕ Add",
        "📊 Analytics",
        "📅 Reports"
    ])

    # =====================================================
    # DASHBOARD
    # =====================================================

    with tab1:

        income = user_df[user_df["Type"] == "Income"]["Amount"].sum()

        expense = user_df[user_df["Type"] == "Expense"]["Amount"].sum()

        balance = income - expense

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Income", f"{currency_symbol} {income:,.0f}")

        with c2:
            st.metric("Expense", f"{currency_symbol} {expense:,.0f}")

        with c3:
            st.metric("Balance", f"{currency_symbol} {balance:,.0f}")

        st.markdown("")

        expense_df = user_df[user_df["Type"] == "Expense"]

        if not expense_df.empty:

            category_sum = expense_df.groupby(
                "Category"
            )["Amount"].sum().reset_index()

            fig = px.pie(
                category_sum,
                names="Category",
                values="Amount",
                hole=0.7
            )

            fig.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font_color="white",
                height=500
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =====================================================
        # RECENT TRANSACTIONS
        # =====================================================

        st.markdown("## Recent Transactions")

        if not user_df.empty:

            recent_transactions = user_df.tail(10).reset_index()

            st.dataframe(
                recent_transactions,
                use_container_width=True,
                height=400
            )

            # =================================================
            # EDIT TRANSACTION
            # =================================================

            st.markdown("## ✏️ Edit Transaction")

            edit_index = st.selectbox(
                "Select Transaction To Edit",
                recent_transactions.index,
                format_func=lambda x:
                f"{recent_transactions.loc[x, 'Category']} | "
                f"{currency_symbol} {recent_transactions.loc[x, 'Amount']} | "
                f"{recent_transactions.loc[x, 'Description']}"
            )

            selected_row = recent_transactions.loc[edit_index]

            actual_index = selected_row["index"]

            original_row = df.loc[actual_index]

            with st.form("edit_transaction_form"):

                edit_date = st.date_input(
                    "Edit Date",
                    pd.to_datetime(original_row["Date"]).date()
                )

                edit_type = st.radio(
                    "Edit Type",
                    ["Expense", "Income"],
                    index=0 if original_row["Type"] == "Expense" else 1,
                    horizontal=True
                )

                edit_category = st.selectbox(
                    "Edit Category",
                    categories,
                    index=categories.index(original_row["Category"])
                    if original_row["Category"] in categories else 0
                )

                edit_amount = st.number_input(
                    "Edit Amount",
                    value=float(original_row["Amount"]),
                    min_value=0.0,
                    format="%.2f"
                )

                edit_description = st.text_input(
                    "Edit Description",
                    value=original_row["Description"]
                )

                update_btn = st.form_submit_button(
                    "Update Transaction"
                )

                if update_btn:

                    df.loc[actual_index, "Date"] = edit_date.strftime("%Y-%m-%d")
                    df.loc[actual_index, "Category"] = edit_category
                    df.loc[actual_index, "Amount"] = edit_amount
                    df.loc[actual_index, "Type"] = edit_type
                    df.loc[actual_index, "Description"] = edit_description

                    df.to_csv(DATA_FILE, index=False)

                    st.success("Transaction Updated Successfully")

                    st.rerun()

            # =================================================
            # DELETE TRANSACTION
            # =================================================

            st.markdown("## 🗑 Delete Transaction")

            delete_index = st.selectbox(
                "Select Transaction To Delete",
                recent_transactions.index,
                key="delete_select",
                format_func=lambda x:
                f"{recent_transactions.loc[x, 'Category']} | "
                f"{currency_symbol} {recent_transactions.loc[x, 'Amount']} | "
                f"{recent_transactions.loc[x, 'Description']}"
            )

            if st.button("Delete Transaction"):

                actual_delete_index = recent_transactions.loc[
                    delete_index,
                    "index"
                ]

                df = df.drop(actual_delete_index)

                df.to_csv(DATA_FILE, index=False)

                st.success("Transaction Deleted Successfully")

                st.rerun()

    # =====================================================
    # ADD TRANSACTION
    # =====================================================

    with tab2:

        st.markdown("## Add Transaction")

        with st.form("transaction_form"):

            date = st.date_input(
                "Date",
                datetime.today()
            )

            transaction_type = st.radio(
                "Transaction Type",
                ["Expense", "Income"],
                horizontal=True
            )

            category = st.selectbox(
                "Category",
                categories
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                format="%.2f"
            )

            description = st.text_input(
                "Description"
            )

            submit = st.form_submit_button(
                "Save Transaction"
            )

            if submit:

                new_data = pd.DataFrame({
                    "User": [current_user],
                    "Date": [date.strftime("%Y-%m-%d")],
                    "Category": [category],
                    "Amount": [amount],
                    "Type": [transaction_type],
                    "Description": [description]
                })

                df = pd.concat([df, new_data], ignore_index=True)

                df.to_csv(DATA_FILE, index=False)

                st.success("Transaction Added Successfully")

                st.rerun()

        st.markdown("## Create Category")

        new_category = st.text_input("New Category")

        if st.button("Add Category"):

            if new_category:

                if new_category not in categories:

                    categories.append(new_category)

                    with open(CATEGORY_FILE, "w", encoding="utf-8") as f:

                        for item in categories:
                            f.write(item + "\n")

                    st.success("Category Added Successfully")

                    st.rerun()

                else:
                    st.warning("Category already exists")

    # =====================================================
    # ANALYTICS
    # =====================================================

    with tab3:

        expense_df = user_df[user_df["Type"] == "Expense"]

        if not expense_df.empty:

            category_expense = expense_df.groupby(
                "Category"
            )["Amount"].sum().reset_index()

            fig = px.bar(
                category_expense,
                x="Category",
                y="Amount",
                text_auto=True
            )

            fig.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font_color="white",
                height=550
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # =====================================================
    # REPORTS
    # =====================================================

    with tab4:

        if not user_df.empty:

            report_df = user_df.copy()

            report_df["Date"] = pd.to_datetime(
                report_df["Date"]
            )

            report_df["Month"] = report_df["Date"].dt.strftime("%B")

            monthly = report_df.groupby(
                ["Month", "Type"]
            )["Amount"].sum().unstack().fillna(0)

            monthly["Savings"] = (
                monthly.get("Income", 0)
                - monthly.get("Expense", 0)
            )

            st.dataframe(
                monthly,
                use_container_width=True
            )

            csv = report_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Download Report",
                csv,
                "budget_report.csv",
                "text/csv"
            )

