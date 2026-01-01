import streamlit as st
import json
import os
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Clinic Product Catalog",
    page_icon="💉",
    layout="wide"
)

# --- CSS Styling ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #2e8b57;
        text-align: center;
        margin-bottom: 30px;
    }
    .category-button {
        background-color: #f0f8f0;
        border: 2px solid #2e8b57;
        border-radius: 10px;
        padding: 15px;
        margin: 5px 0;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: #2e8b57;
    }
    .category-button:hover {
        background-color: #2e8b57;
        color: white;
    }
    .table-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .login-container {
        background-color: #f9f9f9;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #2e8b57;
        max-width: 400px;
        margin: 50px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Management ---
DATA_FILE = "clinic_data.json"

def load_data():
    """Load clinic data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"products": {}, "sources": [], "users": {}}

# --- Session State ---
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "填充"
if 'enable_login' not in st.session_state:
    st.session_state.enable_login = False  # Set to False for testing convenience

# --- Login Page ---
def login_page():
    """Optional login page for user access"""
    st.markdown('<h1 class="main-header">💉 Clinic Product Catalog</h1>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 User Login")

        with st.form("user_login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")

            if st.form_submit_button("Login", use_container_width=True):
                data = load_data()
                # Simple login - you can modify this logic
                if username and password:  # Basic validation
                    st.session_state.user_logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter valid credentials")

        st.markdown('</div>', unsafe_allow_html=True)

        # Skip login option for testing
        st.markdown("---")
        if st.button("🚀 Skip Login (Testing)", use_container_width=True):
            st.session_state.user_logged_in = True
            st.rerun()

# --- Main Interface ---
def main_interface():
    """Main user interface with categories and product table"""
    data = load_data()

    # Header
    st.markdown('<h1 class="main-header">💉 Anesthetic Clinic Product Catalog</h1>', unsafe_allow_html=True)

    # Logout button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Logout", key="user_logout"):
            st.session_state.user_logged_in = False
            st.rerun()

    # Main layout
    col_left, col_right = st.columns([1, 3])

    # Left column - Category selection
    with col_left:
        st.markdown("### 📁 Product Categories")

        categories = ["填充", "水光", "溶脂"]
        for category in categories:
            if st.button(f"📦 {category}",
                        key=f"user_cat_{category}",
                        use_container_width=True,
                        help=f"View {category} products"):
                st.session_state.selected_category = category

        # Show selected category
        st.markdown("---")
        st.markdown(f"**Selected:** {st.session_state.selected_category}")

        # Show category stats
        if st.session_state.selected_category in data["products"]:
            products_count = len(data["products"][st.session_state.selected_category])
            st.markdown(f"**Products:** {products_count}")

        # Total products across all categories
        total_products = sum(len(products) for products in data["products"].values())
        st.markdown(f"**Total Products:** {total_products}")

    # Right column - Product table
    with col_right:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.markdown(f"### 📊 {st.session_state.selected_category} Products")

        if st.session_state.selected_category in data["products"]:
            products = data["products"][st.session_state.selected_category]

            if products:
                # Convert to DataFrame for table display
                table_data = []
                for product_name, product_info in products.items():
                    table_data.append({
                        "Product Name": product_name,
                        "Source": product_info.get("source", "N/A"),
                        "Type": "行貨" if product_info.get("is_genuine", True) else "水貨",
                        "Price ($)": f"{product_info.get('price', 0):.2f}",
                        "Unit": product_info.get("unit", "N/A"),
                        "Date Added": product_info.get("date_added", "N/A")
                    })

                df = pd.DataFrame(table_data)

                # Display table with custom styling
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                        "Source": st.column_config.TextColumn("Source", width="medium"),
                        "Type": st.column_config.TextColumn("Type", width="small"),
                        "Price ($)": st.column_config.TextColumn("Price ($)", width="small"),
                        "Unit": st.column_config.TextColumn("Unit", width="small"),
                        "Date Added": st.column_config.TextColumn("Date Added", width="medium")
                    }
                )

            else:
                st.info(f"No products found in {st.session_state.selected_category} category.")
        else:
            st.info("No products available in this category.")

        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    # Check if login is enabled
    if st.session_state.enable_login and not st.session_state.user_logged_in:
        login_page()
    else:
        main_interface()

if __name__ == "__main__":
    main()