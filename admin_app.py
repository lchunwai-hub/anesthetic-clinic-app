import streamlit as st
import json
import os
from datetime import datetime
import uuid

# --- Page Configuration ---
st.set_page_config(
    page_title="Clinic Management",
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
        color: #1f77b4;
        text-align: center;
        margin-bottom: 20px;
        padding: 10px;
    }
    
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        background-color: #f9f9f9;
    }
    
    .admin-panel {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #1f77b4;
        margin: 10px 0;
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
        padding: 10px 20px !important;
    }
    
    /* Reduce margin */
    .block-container {
        padding: 10px !important;
    }
    
    /* Better spacing */
    h1, h2, h3 {
        margin-top: 15px !important;
        margin-bottom: 10px !important;
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
    return {
        "products": {"填充": [], "水光": [], "溶脂": []},
        "sources": ["本地供應商", "香港代理", "台灣進口", "其他"],
        "users": {
            "admin": "admin123",
            "partner": "partner123"
        }
    }

def save_data(data):
    """Save clinic data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Note: On Streamlit Cloud, you need to manually commit clinic_data.json 
    # to GitHub or use the Upload to Cloud button after making changes

# --- Session State Initialization ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'current_category' not in st.session_state:
    st.session_state.current_category = "填充"

# --- Authentication ---
def login_page():
    """Login page for admin access"""
    st.markdown('<h1 class="main-header">💉 Anesthetic Clinic Management</h1>', unsafe_allow_html=True)
    st.markdown("### Admin Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login", use_container_width=True):
                data = load_data()
                if username in data["users"] and data["users"][username] == password:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "admin" if username == "admin" else "partner"
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

# --- Admin Interface ---
def admin_interface():
    """Main admin interface for managing products"""
    data = load_data()

    # Header
    st.markdown('<h1 class="main-header">💉 Clinic Product Management</h1>', unsafe_allow_html=True)

    # Top bar with upload and logout buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("☁️ Upload to Cloud", key="upload_btn", use_container_width=True, help="Save all changes to cloud"):
            save_data(data)
            st.success("✅ All data uploaded successfully!")
    
    with col3:
        if st.button("Logout", key="logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.rerun()

    # Main layout
    col_left, col_right = st.columns([1, 2])

    # Left column - Product categories
    with col_left:
        st.markdown("### 📁 Product Categories")
        categories = ["填充", "水光", "溶脂", "肉毒", "生髮"]

        for category in categories:
            if st.button(f"📦 {category}",
                        key=f"cat_{category}",
                        use_container_width=True,
                        help=f"View {category} products"):
                st.session_state.current_category = category

        # Show current category
        st.markdown("---")
        st.markdown(f"**Current Category:** {st.session_state.current_category}")

        # Show existing products in current category
        if st.session_state.current_category in data["products"]:
            products = data["products"][st.session_state.current_category]
            
            # Handle migration from dict to list format
            if isinstance(products, dict):
                # Convert old dict format to new list format
                products_list = []
                for prod_name, prod_info in products.items():
                    product_type_suffix = "_g" if prod_info.get('is_genuine', True) else "_ng"
                    products_list.append({
                        'id': f"{prod_name.lower().replace(' ', '_')}{product_type_suffix}",
                        'name': prod_name,
                        **prod_info
                    })
                data["products"][st.session_state.current_category] = products_list
                save_data(data)  # Save the migrated format
                products = products_list
            
            st.markdown(f"**Products in {st.session_state.current_category}:** {len(products)}")

            for idx, product_info in enumerate(products):
                product_id = product_info.get('id', f'product_{idx}')
                key_suffix = f"{product_id}_{idx}"
                product_name = product_info['name']
                product_type = '行' if product_info['is_genuine'] else '水'
                display_name = f"{product_name} ({product_type})"
                
                with st.expander(f"💰 {display_name}"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**Source:** {product_info['source']}")
                        st.write(f"**Type:** {'行貨' if product_info['is_genuine'] else '水貨'}")
                        st.write(f"**Price:** ${product_info['price']}")
                        st.write(f"**Unit:** {product_info['unit']}")
                        st.write(f"**Added:** {product_info['date_added']}")
                    with col2:
                        # Edit button
                        edit_key = f"edit_{st.session_state.current_category}_{key_suffix}"
                        if st.button("✏️ Edit", key=edit_key, help=f"Edit {product_name}"):
                            st.session_state[f"editing_{key_suffix}"] = True

                        # Delete button
                        delete_key = f"delete_{st.session_state.current_category}_{key_suffix}"
                        if st.button("🗑️ Delete", key=delete_key, help=f"Delete {product_name}"):
                            st.session_state[f"confirm_delete_{key_suffix}"] = True

                # Edit form (shown when edit button is clicked)
                if st.session_state.get(f"editing_{key_suffix}", False):
                    st.markdown("---")
                    with st.container():
                        st.markdown(f"### ✏️ Edit Product: {display_name}")

                        with st.form(f"edit_form_{key_suffix}"):
                            # Product name (editable)
                            new_product_name = st.text_input("Product Name", value=product_name, key=f"name_{key_suffix}")

                            # Source selection
                            source_options = data["sources"] + ["+ Add New Source"]
                            current_source_index = data["sources"].index(product_info['source']) if product_info['source'] in data["sources"] else 0
                            selected_source = st.selectbox("Product Source", source_options, index=current_source_index, key=f"source_{key_suffix}")

                            # Handle new source addition
                            if selected_source == "+ Add New Source":
                                new_source = st.text_input("New Source Name", placeholder="Enter new source", key=f"new_src_{key_suffix}")
                                if new_source and new_source not in data["sources"]:
                                    selected_source = new_source

                            # Genuine/Parallel import
                            is_genuine = st.checkbox("行貨 (Genuine Goods)", value=product_info['is_genuine'], key=f"genuine_{key_suffix}")

                            # Price and Unit
                            col3, col4 = st.columns(2)
                            with col3:
                                price = st.number_input("Price ($)", value=float(product_info['price']), min_value=0.0, step=0.01, format="%.2f", key=f"price_{key_suffix}")
                            with col4:
                                unit_options = ["per 支", "per 盒", "per part", "per ml", "per vial"]
                                current_unit_index = unit_options.index(product_info['unit']) if product_info['unit'] in unit_options else 0
                                unit = st.selectbox("Unit", unit_options, index=current_unit_index, key=f"unit_{key_suffix}")

                            # Form buttons
                            col_save, col_cancel = st.columns(2)
                            with col_save:
                                save_submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)
                            with col_cancel:
                                cancel_submitted = st.form_submit_button("❌ Cancel", use_container_width=True)

                            if save_submitted:
                                if not new_product_name.strip():
                                    st.error("Product name cannot be empty")
                                elif price <= 0:
                                    st.error("Price must be greater than 0")
                                else:
                                    # Add/update new source if needed
                                    if selected_source not in data["sources"] and selected_source != "+ Add New Source":
                                        data["sources"].append(selected_source)

                                    # Update product at this index
                                    data["products"][st.session_state.current_category][idx] = {
                                        "id": product_id,
                                        "name": new_product_name.strip(),
                                        "source": selected_source if selected_source != "+ Add New Source" else new_source,
                                        "is_genuine": is_genuine,
                                        "price": price,
                                        "unit": unit,
                                        "date_added": product_info['date_added']  # Keep original date
                                    }

                                    save_data(data)
                                    st.success(f"✅ Product updated successfully!")
                                    st.session_state[f"editing_{key_suffix}"] = False
                                    st.rerun()

                            if cancel_submitted:
                                st.session_state[f"editing_{key_suffix}"] = False
                                st.rerun()

                # Delete confirmation (shown when delete button is clicked)
                if st.session_state.get(f"confirm_delete_{key_suffix}", False):
                    st.markdown("---")
                    with st.container():
                        st.error(f"🗑️ Are you sure you want to delete **{display_name}**?")
                        st.warning("This action cannot be undone!")

                        col_confirm, col_cancel_del = st.columns(2)
                        with col_confirm:
                            if st.button("🗑️ Yes, Delete", key=f"confirm_del_{key_suffix}", use_container_width=True):
                                data["products"][st.session_state.current_category].pop(idx)
                                save_data(data)
                                st.success(f"✅ Product deleted successfully!")
                                st.session_state[f"confirm_delete_{key_suffix}"] = False
                                st.rerun()
                        with col_cancel_del:
                            if st.button("❌ Cancel", key=f"cancel_del_{key_suffix}", use_container_width=True):
                                st.session_state[f"confirm_delete_{key_suffix}"] = False
                                st.rerun()

    # Right column - Add new product form
    with col_right:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        st.markdown(f"### ➕ Add New Product - {st.session_state.current_category}")

        # Source management (outside form for immediate updates)
        st.markdown("#### Product Source")
        source_options = data["sources"] + ["+ Add New Source"]
        selected_source = st.selectbox("Select Source", source_options, key="source_select")

        new_source_name = ""
        if selected_source == "+ Add New Source":
            new_source_name = st.text_input("New Source Name", placeholder="Enter new source name", key="new_source_input")
            if st.button("➕ Add Source", key="add_source_btn"):
                if new_source_name.strip():
                    if new_source_name not in data["sources"]:
                        data["sources"].append(new_source_name.strip())
                        save_data(data)
                        st.success(f"✅ Added new source: {new_source_name}")
                        st.rerun()
                    else:
                        st.warning("Source already exists")
                else:
                    st.error("Please enter a source name")

        # Determine final source for product
        final_source = new_source_name if selected_source == "+ Add New Source" and new_source_name else selected_source

        with st.form("add_product_form"):
            # Product name
            product_name = st.text_input("Product Name", placeholder="e.g., Juvederm Ultra 1ml")

            # Display selected source (read-only in form)
            if final_source and final_source != "+ Add New Source":
                st.text_input("Selected Source", value=final_source, disabled=True)
            else:
                st.info("Please select or add a source above")

            # Genuine/Parallel import
            is_genuine = st.checkbox("行貨 (Genuine Goods)", value=True)
            if not is_genuine:
                st.info("水貨 (Parallel Import)")

            # Price and Unit
            col3, col4 = st.columns(2)
            with col3:
                price = st.number_input("Price ($)", min_value=0.0, step=0.01, format="%.2f")
            with col4:
                unit_options = ["per 支", "per 盒", "per part", "per ml", "per vial"]
                unit = st.selectbox("Unit", unit_options)

            # Submit button
            submitted = st.form_submit_button("➕ Add Product", use_container_width=True)

            if submitted:
                if not product_name.strip():
                    st.error("Please enter a product name")
                elif not final_source or final_source == "+ Add New Source":
                    st.error("Please select a valid product source")
                elif price <= 0:
                    st.error("Please enter a valid price")
                else:
                    # Initialize category if it doesn't exist
                    if st.session_state.current_category not in data["products"]:
                        data["products"][st.session_state.current_category] = []

                    # Generate unique ID based on product name, type, and timestamp to avoid duplicates
                    product_type_suffix = "_g" if is_genuine else "_ng"
                    product_id = f"{product_name.lower().replace(' ', '_')}{product_type_suffix}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                    
                    # Add product to list
                    data["products"][st.session_state.current_category].append({
                        "id": product_id,
                        "name": product_name.strip(),
                        "source": final_source,
                        "is_genuine": is_genuine,
                        "price": price,
                        "unit": unit,
                        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })

                    save_data(data)
                    st.success(f"✅ Product '{product_name}' added successfully!")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        admin_interface()

if __name__ == "__main__":
    main()