import streamlit as st
import json
import os
import pandas as pd

# --- Page Configuration ---
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

    # Right column - Product cards (mobile-friendly)
    with col_right:
        st.markdown(f"### 📊 {st.session_state.selected_category} Products")

        if st.session_state.selected_category in data["products"]:
            products = data["products"][st.session_state.selected_category]

            if products:
                # Display as expandable cards instead of table
                for idx, (product_name, product_info) in enumerate(products.items()):
                    product_type = "✅ 行貨 (Genuine)" if product_info.get("is_genuine", True) else "⚠️ 水貨 (Non-Genuine)"
                    price = f"${product_info.get('price', 0):.2f}"
                    unit = product_info.get("unit", "N/A")
                    source = product_info.get("source", "N/A")
                    date_added = product_info.get("date_added", "N/A")
                    
                    # Create expandable product card
                    with st.expander(f"💊 {product_name} - {price}", expanded=(idx == 0)):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Product:** {product_name}")
                            st.markdown(f"**Price:** {price}")
                            st.markdown(f"**Unit:** {unit}")
                        
                        with col2:
                            st.markdown(f"**Type:** {product_type}")
                            st.markdown(f"**Source:** {source}")
                            st.markdown(f"**Added:** {date_added}")
                        
                        # Divider line
                        st.divider()

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