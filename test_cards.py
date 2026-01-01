"""
Test script to verify product card layout is working
Run this with: streamlit run test_cards.py
"""

import streamlit as st
import json
import os

st.set_page_config(
    page_title="Product Cards Test",
    page_icon="💉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Sample data
data = {
    "products": {
        "填充": {
            "VOLUMA": {
                "source": "SINOPHARM",
                "is_genuine": False,
                "price": 820.0,
                "unit": "per syringe",
                "date_added": "2026-01-01 09:38"
            },
            "Restylane": {
                "source": "Global Med",
                "is_genuine": True,
                "price": 750.0,
                "unit": "per syringe",
                "date_added": "2026-01-01 10:00"
            }
        },
        "水光": {
            "Hyaluronic Acid Solution 5ml": {
                "source": "Local Supplier",
                "is_genuine": True,
                "price": 120.0,
                "unit": "per bottle",
                "date_added": "2024-01-01 10:30"
            }
        }
    }
}

st.title("💉 Product Cards Test")
st.write("This tests if the expandable card layout is working correctly.")

# Test category
category = "填充"
st.subheader(f"📊 {category} Products")

products = data["products"][category]

if products:
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
            
            st.divider()

st.success("✅ If you see expandable cards above with product details, the layout is working!")
