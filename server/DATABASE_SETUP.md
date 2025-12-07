# MySQL Database Setup Guide

## Step 1: Create Database

You need to create the MySQL database first. Choose one method:

### Method 1: Using MySQL Workbench (GUI)
1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Run this SQL:
```sql
CREATE DATABASE IF NOT EXISTS ecommerce_chat_assistant;
```

### Method 2: Using Command Line
```bash
# If you have password
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS ecommerce_chat_assistant;"

# If no password (like your .env)
mysql -u root -e "CREATE DATABASE IF NOT EXISTS ecommerce_chat_assistant;"
```

### Method 3: Using phpMyAdmin
1. Open phpMyAdmin
2. Click "New" in left sidebar
3. Database name: `ecommerce_chat_assistant`
4. Click "Create"

---

## Step 2: Initialize Tables

After database is created, run:

```bash
cd server
source .venv/bin/activate
python scripts/init_db.py
```

This will create all tables:
- users
- addresses
- categories
- products
- cart_items
- orders
- order_items

---

## Step 3: Seed Data

```bash
python scripts/seed_database.py
```

This will add:
- Sample categories
- 50+ products with tags
- Sample users
- Test data

---

## Troubleshooting

### Error: "Access denied for user 'root'@'localhost'"
**Solution**: Your MySQL root user needs password. Either:
1. Set password in `.env`: `DB_PASSWORD=your_password`
2. Or create new MySQL user:
```sql
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_chat_assistant.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```
Then update `.env`:
```
DB_USER=ecommerce_user
DB_PASSWORD=your_password
```

### Error: "Can't connect to MySQL server"
**Solution**: Make sure MySQL is running:
```bash
# Check MySQL status
sudo systemctl status mysql

# Start MySQL if not running
sudo systemctl start mysql
```

### Error: "Unknown database"
**Solution**: Database not created yet. Follow Step 1 above.

---

## Verify Setup

```bash
# Check if database exists
mysql -u root -e "SHOW DATABASES LIKE 'ecommerce%';"

# Check tables
mysql -u root ecommerce_chat_assistant -e "SHOW TABLES;"

# Count products
mysql -u root ecommerce_chat_assistant -e "SELECT COUNT(*) FROM products;"
```

---

## Next Steps

After database is set up:
1. Restart backend server
2. Test authentication endpoints
3. Test product search
4. Test cart operations
