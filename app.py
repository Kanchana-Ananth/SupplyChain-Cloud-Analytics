from flask import Flask, render_template
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    connection = get_connection()

    try:

        with connection.cursor() as cursor:

            # ------------------------------------------------
            # KPI 1 - TOTAL ORDERS
            # ------------------------------------------------

            cursor.execute("""
                SELECT COUNT(DISTINCT order_id) AS total_orders
                FROM supply_chain_orders
            """)

            total_orders = cursor.fetchone()["total_orders"]


            # ------------------------------------------------
            # KPI 2 - TOTAL SALES
            # ------------------------------------------------

            cursor.execute("""
                SELECT SUM(sales) AS total_sales
                FROM supply_chain_orders
            """)

            total_sales = cursor.fetchone()["total_sales"] or 0


            # ------------------------------------------------
            # KPI 3 - TOTAL CUSTOMERS
            # ------------------------------------------------

            cursor.execute("""
                SELECT COUNT(DISTINCT customer_id) AS total_customers
                FROM supply_chain_orders
            """)

            total_customers = cursor.fetchone()["total_customers"]


            # ------------------------------------------------
            # KPI 4 - TOTAL PROFIT
            # ------------------------------------------------

            cursor.execute("""
                SELECT SUM(order_profit) AS total_profit
                FROM supply_chain_orders
            """)

            total_profit = cursor.fetchone()["total_profit"] or 0


            # ------------------------------------------------
            # KPI 5 - AVERAGE ORDER VALUE
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    SUM(sales) /
                    NULLIF(COUNT(DISTINCT order_id), 0)
                    AS average_order_value
                FROM supply_chain_orders
            """)

            average_order_value = (
                cursor.fetchone()["average_order_value"]
                or 0
            )


            # ------------------------------------------------
            # KPI 6 - LATE DELIVERY RATE
            # ------------------------------------------------

            cursor.execute("""
                SELECT
                    (
                        SUM(
                            CASE
                                WHEN delivery_performance = 'Late'
                                THEN 1
                                ELSE 0
                            END
                        )
                        /
                        COUNT(*)
                    ) * 100 AS late_delivery_rate

                FROM supply_chain_orders
            """)

            late_delivery_rate = (
                cursor.fetchone()["late_delivery_rate"]
                or 0
            )


            # =================================================
            # MONTHLY SALES
            # =================================================

            cursor.execute("""
                SELECT
                    order_year,
                    order_month,
                    SUM(sales) AS total_sales

                FROM supply_chain_orders

                GROUP BY
                    order_year,
                    order_month

                ORDER BY
                    order_year,
                    order_month
            """)

            monthly_data = cursor.fetchall()

            monthly_labels = [
                f"{row['order_year']}-{row['order_month']:02d}"
                for row in monthly_data
            ]

            monthly_sales = [
                float(row["total_sales"])
                for row in monthly_data
            ]


            # =================================================
            # CATEGORY SALES
            # =================================================

            cursor.execute("""
                SELECT
                    category,
                    SUM(sales) AS total_sales

                FROM supply_chain_orders

                GROUP BY category

                ORDER BY total_sales DESC

                LIMIT 10
            """)

            category_data = cursor.fetchall()

            category_labels = [
                row["category"]
                for row in category_data
            ]

            category_sales = [
                float(row["total_sales"])
                for row in category_data
            ]


            # =================================================
            # REGION SALES
            # =================================================

            cursor.execute("""
                SELECT
                    region,
                    SUM(sales) AS total_sales

                FROM supply_chain_orders

                GROUP BY region

                ORDER BY total_sales DESC
            """)

            region_data = cursor.fetchall()

            region_labels = [
                row["region"]
                for row in region_data
            ]

            region_sales = [
                float(row["total_sales"])
                for row in region_data
            ]


            # =================================================
            # SHIPPING MODE
            # =================================================

            cursor.execute("""
                SELECT
                    shipping_mode,
                    COUNT(DISTINCT order_id)
                    AS total_orders

                FROM supply_chain_orders

                GROUP BY shipping_mode

                ORDER BY total_orders DESC
            """)

            shipping_data = cursor.fetchall()

            shipping_labels = [
                row["shipping_mode"]
                for row in shipping_data
            ]

            shipping_orders = [
                int(row["total_orders"])
                for row in shipping_data
            ]


            # =================================================
            # DELIVERY PERFORMANCE
            # =================================================

            cursor.execute("""
                SELECT
                    delivery_performance,
                    COUNT(DISTINCT order_id)
                    AS total_orders

                FROM supply_chain_orders

                GROUP BY delivery_performance
            """)

            delivery_data = cursor.fetchall()

            delivery_labels = [
                row["delivery_performance"]
                for row in delivery_data
            ]

            delivery_orders = [
                int(row["total_orders"])
                for row in delivery_data
            ]


        # ====================================================
        # SEND DATA TO HTML
        # ====================================================

        return render_template(
            "dashboard.html",

            total_orders=total_orders,

            total_customers=total_customers,

            total_sales=float(total_sales),

            total_profit=float(total_profit),

            average_order_value=float(
                average_order_value
            ),

            late_delivery_rate=float(
                late_delivery_rate
            ),

            monthly_labels=monthly_labels,

            monthly_sales=monthly_sales,

            category_labels=category_labels,

            category_sales=category_sales,

            region_labels=region_labels,

            region_sales=region_sales,

            shipping_labels=shipping_labels,

            shipping_orders=shipping_orders,

            delivery_labels=delivery_labels,

            delivery_orders=delivery_orders
        )

    finally:

        connection.close()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )