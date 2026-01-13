# 💉 Anesthetic Clinic Management System

A comprehensive web application for managing and viewing anesthetic clinic product costs with dual interfaces for administrators and users.

## 📋 Features

### Admin Interface (`admin_app.py`)
- 🔐 **Secure Login**: Username/password authentication
- 📦 **Product Categories**: Organized by 填充, 水光, 溶脂
- ➕ **Add Products**: Complete product information management
- 🏪 **Source Management**: Add new product sources dynamically
- 💰 **Pricing Control**: Set prices with different units
- ✅ **Product Types**: Distinguish between 行貨 (genuine) and 水貨 (parallel imports)

### User Interface (`user_app.py`)
- 📖 **Product Catalog**: View all clinic products
- 🔍 **Search Functionality**: Find products by name
- 🏷️ **Category Filtering**: Browse by product categories
- 💵 **Price Display**: Clear pricing information
- 🎯 **Genuine/Parallel Filter**: Filter by product type

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. 🎯 簡易啟動方式（推薦）

使用提供的啟動腳本，一個命令即可運行：

#### 啟動用戶介面
```bash
./start_user.sh
```
- 端口: 8501
- 自動清理舊進程
- 顯示訪問地址

#### 啟動管理介面
```bash
./start_admin.sh
```
- 端口: 8502
- 自動清理舊進程
- 顯示登入資訊

#### 同時啟動兩個介面
```bash
./start_both.sh
```
- 在後台運行兩個服務
- 自動顯示所有訪問地址
- 查看日誌: `tail -f user_app.log` 或 `tail -f admin_app.log`

#### 停止所有服務
```bash
./stop_all.sh
```

### 3. 手動運行方式

**管理介面:**
```bash
streamlit run admin_app.py --server.port 8502
```

**用戶介面:**
```bash
streamlit run user_app.py --server.port 8501
```

### 📱 從其他設備訪問 (不同 WiFi 網路)

應用程式已配置為可從任何設備訪問。啟動後:

1. **查看你的 IP 地址:**
   ```bash
   hostname -I
   # 或
   ip addr show | grep "inet " | grep -v 127.0.0.1
   ```

2. **在瀏覽器訪問:**
   - 用戶介面: `http://你的IP:8501`
   - 管理介面: `http://你的IP:8502`
   - 範例: `http://192.168.1.100:8501`

3. **確保防火牆允許連接:**
   ```bash
   # 如需要,開放端口 (Linux)
   sudo ufw allow 8501
   sudo ufw allow 8502
   ```

**注意:** 配置檔案位於 `.streamlit/config.toml`,已設定 `address = "0.0.0.0"` 允許遠端訪問。

## 👥 User Accounts

### Admin Access
- **Username:** `admin`
- **Password:** `admin123`

### Partner Access
- **Username:** `partner`
- **Password:** `partner123`

## 📁 Project Structure

```
Anesthetic_Clinic_App/
├── admin_app.py          # Admin interface for managing products
├── user_app.py           # User interface for viewing products
├── clinic_data.json      # Product database and user credentials
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 💡 Usage Guide

### Adding New Products (Admin)

1. **Login** with admin credentials
2. **Select Category** from left panel (填充, 水光, 溶脂)
3. **Fill Product Details**:
   - Product name
   - Select or add new source
   - Choose 行貨/水貨 type
   - Set price and unit
4. **Click "Add Product"**

### Viewing Products (User)

1. **Open** user interface
2. **Browse** products by category
3. **Search** for specific products
4. **Filter** by genuine goods only if needed

## 🔧 Customization

### Adding New Categories
Edit the `categories` list in both `admin_app.py` and `user_app.py`:
```python
categories = ["填充", "水光", "溶脂", "新分類"]
```

### Adding New Units
Edit the `unit_options` in `admin_app.py`:
```python
unit_options = ["per 支", "per 盒", "per part", "per ml", "per vial", "新單位"]
```

### Changing Login Credentials
Edit the `users` section in `clinic_data.json`:
```json
{
    "users": {
        "admin": "newpassword",
        "partner": "newpassword"
    }
}
```

## 📊 Data Storage

All product data is stored in `clinic_data.json`:
- **Products**: Organized by category with full details
- **Sources**: List of available product sources
- **Users**: Login credentials for admin and partner access

## 🔒 Security Notes

- Default passwords should be changed for production use
- The app uses local JSON storage (suitable for single-user scenarios)
- For multi-user production deployment, consider database integration

## 🆘 Support

For technical issues or feature requests, please check the code comments or modify the source files directly.

---

**Developed for Anesthetic Clinic Management** 💉📊