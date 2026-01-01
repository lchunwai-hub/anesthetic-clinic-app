import streamlit as st
import json
import os
import pandas as pd

# --- Page Configuration ---
# Version 2.0: Mobile-optimized card layout
st.set_page_config(
    page_title="Product Catalog",
    page_icon="💉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS Styling for Mobile ---
st.markdown("""
    <style>
    /* Mobile responsive styling */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #2e8b57;
        text-align: center;
        margin-bottom: 15px;
        padding: 10px;
    }
    
    .category-button {
        background-color: #f0f8f0;
        border: 2px solid #2e8b57;
        border-radius: 8px;
        padding: 12px;
        margin: 6px 0;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: #2e8b57;
        font-size: 16px;
    }
    
    .category-button:hover {
        background-color: #2e8b57;
        color: white;
    }
    
    .table-container {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
    }
    
    /* Expandable card styling */
    .streamlit-expanderHeader {
        background-color: #e8f5e9 !important;
        border: 2px solid #2e8b57 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        margin: 8px 0 !important;
        font-weight: bold !important;
    }
    
    .streamlit-expanderContent {
        background-color: #f9f9f9 !important;
        padding: 15px !important;
    }
    
    /* Mobile-friendly table styling */
    [data-testid="stDataFrame"] {
        font-size: 12px !important;
        overflow-x: hidden !important;
    }
    
    [data-testid="stDataFrame"] table {
        width: 100% !important;
        border-collapse: collapse !important;
        table-layout: fixed !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #2e8b57 !important;
        color: white !important;
        padding: 8px 6px !important;
        text-align: left !important;
        font-weight: bold !important;
        border: 1px solid #1d5e3f !important;
        font-size: 11px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    [data-testid="stDataFrame"] td {
        padding: 8px 6px !important;
        border: 1px solid #ddd !important;
        text-align: left !important;
        font-size: 12px !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }
    
    [data-testid="stDataFrame"] tr:nth-child(even) {
        background-color: #f9f9f9 !important;
    }
    
    [data-testid="stDataFrame"] tr:nth-child(odd) {
        background-color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] tr:hover {
        background-color: #e8f5e9 !important;
    }
    
    /* Button styling for mobile */
    .stButton > button {
        width: 100%;
        padding: 12px !important;
        font-size: 16px !important;
        border-radius: 8px !important;
        margin: 5px 0 !important;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        font-size: 16px !important;
        padding: 10px !important;
        border-radius: 5px !important;
    }
    
    /* Tabs */
    .stTabs [role="tablist"] button {
        font-size: 14px !important;
        padding: 10px 15px !important;
    }
    
    /* Reduce margin */
    .block-container {
        padding: 10px !important;
    }
    
    /* Better spacing for mobile */
    h1, h2, h3 {
        margin-top: 15px !important;
        margin-bottom: 10px !important;
    }
    
    /* Product info text styling */
    p {
        font-size: 14px !important;
        line-height: 1.6 !important;
    }
    
    /* Better divider */
    hr {
        margin: 10px 0 !important;
        border: none !important;
        border-top: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Data Management ---
DATA_FILE = "clinic_data.json"

@st.cache_data(ttl=5)
def load_data():
    """Load clinic data from JSON file with short cache (5 seconds)"""
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

    # Top bar with category selector, refresh and logout button
    header_cols = st.columns([2, 0.5, 0.5])
    
    categories = ["填充", "水光", "溶脂"]
    
    # Category selector box
    with header_cols[0]:
        selected = st.selectbox(
            "Select Category",
            categories,
            index=categories.index(st.session_state.selected_category),
            key="category_selector",
            label_visibility="collapsed"
        )
        st.session_state.selected_category = selected
    
    # Refresh button
    with header_cols[1]:
        if st.button("🔄", key="refresh_btn", help="Refresh data"):
            st.cache_data.clear()
            st.rerun()
    
    # Logout button
    with header_cols[2]:
        if st.button("Logout", key="user_logout", use_container_width=True):
            st.session_state.user_logged_in = False
            st.rerun()

    st.markdown("---")

    # Product table (full width, no side panel)
    st.markdown(f"### 📊 {st.session_state.selected_category} Products")

    if st.session_state.selected_category in data["products"]:
        products = data["products"][st.session_state.selected_category]

        if products:
            # Convert to DataFrame for table display
            table_data = []
            for product_name, product_info in products.items():
                table_data.append({
                    "Product Name": product_name,
                    "Price ($)": f"{product_info.get('price', 0):.2f}",
                    "Type": "行" if product_info.get("is_genuine", True) else "水",
                    "Source": product_info.get("source", "N/A")
                })

            df = pd.DataFrame(table_data)

            # Display table with mobile-friendly styling (no horizontal scroll)
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Product Name": st.column_config.TextColumn("Product Name", width="medium"),
                    "Price ($)": st.column_config.TextColumn("Price", width="small"),
                    "Type": st.column_config.TextColumn("Type", width="small"),
                    "Source": st.column_config.TextColumn("Source", width="small")
                }
            )

        else:
            st.info(f"📭 No products found in {st.session_state.selected_category} category.")
    else:
        st.info("📭 No products available in this category.")

# --- Main App Logic ---
def main():
    # Check if login is enabled
    if st.session_state.enable_login and not st.session_state.user_logged_in:
        login_page()
    else:
        main_interface()

if __name__ == "__main__":
    main()