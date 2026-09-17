import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "supply_chain")


# ============================================================
# CONNECT TO MYSQL
# ============================================================

def get_connection(database=None):

    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                f"""
                CREATE DATABASE IF NOT EXISTS `{DB_NAME}`
                """
            )

        connection.commit()

        print(f"Database '{DB_NAME}' created successfully.")

    finally:

        connection.close()


# ============================================================
# CREATE TABLE
# ============================================================

def create_tables():

    connection = get_connection(DB_NAME)

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS supply_chain_orders (

                    id BIGINT AUTO_INCREMENT PRIMARY KEY,

                    order_id BIGINT NOT NULL,

                    order_item_id BIGINT NOT NULL,

                    order_date DATETIME,

                    shipping_date DATETIME,

                    order_year INT,

                    order_month INT,

                    order_month_name VARCHAR(10),

                    order_day INT,

                    payment_type VARCHAR(50),

                    customer_id BIGINT,

                    customer_segment VARCHAR(50),

                    category VARCHAR(150),

                    department VARCHAR(100),

                    market VARCHAR(100),

                    order_city VARCHAR(150),

                    order_country VARCHAR(100),

                    region VARCHAR(100),

                    order_state VARCHAR(150),

                    product_name VARCHAR(255),

                    quantity INT,

                    product_price DECIMAL(12,2),

                    item_product_price DECIMAL(12,2),

                    discount DECIMAL(12,2),

                    discount_rate DECIMAL(8,4),

                    sales DECIMAL(14,2),

                    order_item_total DECIMAL(14,2),

                    order_profit DECIMAL(14,2),

                    profit_ratio DECIMAL(8,4),

                    actual_shipping_days INT,

                    scheduled_shipping_days INT,

                    delivery_delay_days INT,

                    delivery_status VARCHAR(100),

                    delivery_performance VARCHAR(30),

                    shipping_mode VARCHAR(50),

                    late_delivery_risk INT,

                    INDEX idx_order_id (order_id),

                    INDEX idx_order_date (order_date),

                    INDEX idx_category (category),

                    INDEX idx_region (region),

                    INDEX idx_customer (customer_id),

                    INDEX idx_delivery (delivery_performance)

                )
                """
            )

        connection.commit()

        print(
            "supply_chain_orders table created successfully."
        )

    finally:

        connection.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SUPPLY CHAIN DATABASE SETUP")
    print("=" * 60)

    create_database()

    create_tables()

    print("=" * 60)
    print("DATABASE SETUP COMPLETED")
    print("=" * 60)