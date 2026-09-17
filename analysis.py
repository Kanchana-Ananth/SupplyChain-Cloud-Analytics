import pandas as pd
import os

# ============================================================
# SUPPLY CHAIN DATA PROCESSING
# ============================================================

DATA_PATH = "data/DataCoSupplyChainDataset.csv"
OUTPUT_DIR = "data/processed"

# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("SUPPLY CHAIN DATA PROCESSING")
print("=" * 70)

# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n[1/7] Loading dataset...")

df = pd.read_csv(
    DATA_PATH,
    encoding="latin1"
)

print(f"Dataset loaded: {len(df):,} rows")


# ============================================================
# 2. SELECT REQUIRED COLUMNS
# ============================================================

print("\n[2/7] Selecting required columns...")

required_columns = [
    "Type",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Delivery Status",
    "Late_delivery_risk",
    "Category Name",
    "Customer Id",
    "Customer Segment",
    "Department Name",
    "Market",
    "Order City",
    "Order Country",
    "Order Customer Id",
    "order date (DateOrders)",
    "Order Id",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Id",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Order Region",
    "Order State",
    "Order Status",
    "Product Name",
    "Product Price",
    "shipping date (DateOrders)",
    "Shipping Mode"
]

df = df[required_columns].copy()

print(f"Selected {len(required_columns)} useful columns")


# ============================================================
# 3. PROCESS DATES
# ============================================================

print("\n[3/7] Processing dates...")

df["order_date"] = pd.to_datetime(
    df["order date (DateOrders)"],
    errors="coerce"
)

df["shipping_date"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    errors="coerce"
)

# Extract date information

df["order_year"] = df["order_date"].dt.year

df["order_month"] = df["order_date"].dt.month

df["order_month_name"] = (
    df["order_date"].dt.strftime("%b")
)

df["order_day"] = df["order_date"].dt.day


# ============================================================
# 4. CLEAN NUMERIC DATA
# ============================================================

print("\n[4/7] Cleaning numeric values...")

numeric_columns = [
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Late_delivery_risk",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Product Price"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Replace missing numeric values with 0

df[numeric_columns] = (
    df[numeric_columns].fillna(0)
)


# ============================================================
# 5. CREATE ANALYTICS COLUMNS
# ============================================================

print("\n[5/7] Creating analytics columns...")

# Delivery delay

df["delivery_delay_days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

# Delivery performance

df["delivery_performance"] = df[
    "Delivery Status"
].apply(
    lambda x:
        "Late"
        if "Late" in str(x)
        else "On Time"
)

# Profit

df["profit"] = df[
    "Order Profit Per Order"
]


# ============================================================
# 6. RENAME COLUMNS
# ============================================================

print("\n[6/7] Renaming columns...")

rename_columns = {

    "Type":
        "payment_type",

    "Days for shipping (real)":
        "actual_shipping_days",

    "Days for shipment (scheduled)":
        "scheduled_shipping_days",

    "Benefit per order":
        "benefit_per_order",

    "Sales per customer":
        "sales_per_customer",

    "Delivery Status":
        "delivery_status",

    "Late_delivery_risk":
        "late_delivery_risk",

    "Category Name":
        "category",

    "Customer Id":
        "customer_id",

    "Customer Segment":
        "customer_segment",

    "Department Name":
        "department",

    "Market":
        "market",

    "Order City":
        "order_city",

    "Order Country":
        "order_country",

    "Order Customer Id":
        "order_customer_id",

    "Order Id":
        "order_id",

    "Order Item Discount":
        "discount",

    "Order Item Discount Rate":
        "discount_rate",

    "Order Item Id":
        "order_item_id",

    "Order Item Product Price":
        "item_product_price",

    "Order Item Profit Ratio":
        "profit_ratio",

    "Order Item Quantity":
        "quantity",

    "Sales":
        "sales",

    "Order Item Total":
        "order_item_total",

    "Order Profit Per Order":
        "order_profit",

    "Order Region":
        "region",

    "Order State":
        "order_state",

    "Order Status":
        "order_status",

    "Product Name":
        "product_name",

    "Product Price":
        "product_price",

    "Shipping Mode":
        "shipping_mode"
}

df.rename(
    columns=rename_columns,
    inplace=True
)


# ============================================================
# 7. SAVE PROCESSED DATA
# ============================================================

print("\n[7/7] Saving processed data...")

final_columns = [

    "order_id",
    "order_item_id",

    "order_date",
    "shipping_date",

    "order_year",
    "order_month",
    "order_month_name",
    "order_day",

    "payment_type",

    "customer_id",
    "customer_segment",

    "category",
    "department",

    "market",

    "order_city",
    "order_country",

    "region",
    "order_state",

    "product_name",

    "quantity",

    "product_price",
    "item_product_price",

    "discount",
    "discount_rate",

    "sales",
    "order_item_total",
    "order_profit",
    "profit_ratio",

    "actual_shipping_days",
    "scheduled_shipping_days",
    "delivery_delay_days",

    "delivery_status",
    "delivery_performance",

    "shipping_mode",
    "late_delivery_risk"
]

df = df[final_columns]


# Save processed dataset

processed_path = os.path.join(
    OUTPUT_DIR,
    "processed_supply_chain.csv"
)

df.to_csv(
    processed_path,
    index=False
)


# ============================================================
# KPI SUMMARY
# ============================================================

print("\nCreating KPI summary...")

total_orders = df["order_id"].nunique()

total_order_items = df[
    "order_item_id"
].nunique()

total_customers = df[
    "customer_id"
].nunique()

total_sales = df[
    "sales"
].sum()

total_profit = df[
    "order_profit"
].sum()

average_order_value = (
    total_sales / total_orders
)

late_delivery_rate = (
    (df["delivery_performance"] == "Late")
    .mean()
    * 100
)


kpi = pd.DataFrame({

    "metric": [

        "total_orders",
        "total_order_items",
        "total_customers",
        "total_sales",
        "total_profit",
        "average_order_value",
        "late_delivery_rate"

    ],

    "value": [

        total_orders,
        total_order_items,
        total_customers,
        total_sales,
        total_profit,
        average_order_value,
        late_delivery_rate

    ]

})


kpi.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "kpi_summary.csv"
    ),
    index=False
)


# ============================================================
# MONTHLY SALES
# ============================================================

print("Creating monthly sales analysis...")

monthly_sales = (

    df.groupby(
        [
            "order_year",
            "order_month"
        ]
    )

    .agg(

        total_sales=(
            "sales",
            "sum"
        ),

        total_orders=(
            "order_id",
            "nunique"
        )

    )

    .reset_index()

)


monthly_sales.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "monthly_sales.csv"
    ),
    index=False
)


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

print("Creating category analysis...")

category_analysis = (

    df.groupby("category")

    .agg(

        total_sales=(
            "sales",
            "sum"
        ),

        total_orders=(
            "order_id",
            "nunique"
        ),

        total_quantity=(
            "quantity",
            "sum"
        ),

        total_profit=(
            "order_profit",
            "sum"
        )

    )

    .reset_index()

    .sort_values(
        "total_sales",
        ascending=False
    )

)


category_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "category_analysis.csv"
    ),
    index=False
)


# ============================================================
# REGION ANALYSIS
# ============================================================

print("Creating region analysis...")

region_analysis = (

    df.groupby("region")

    .agg(

        total_sales=(
            "sales",
            "sum"
        ),

        total_orders=(
            "order_id",
            "nunique"
        ),

        total_profit=(
            "order_profit",
            "sum"
        )

    )

    .reset_index()

    .sort_values(
        "total_sales",
        ascending=False
    )

)


region_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "region_analysis.csv"
    ),
    index=False
)


# ============================================================
# SHIPPING MODE ANALYSIS
# ============================================================

print("Creating shipping analysis...")

shipping_analysis = (

    df.groupby("shipping_mode")

    .agg(

        total_orders=(
            "order_id",
            "nunique"
        ),

        average_shipping_days=(
            "actual_shipping_days",
            "mean"
        ),

        late_orders=(
            "delivery_performance",
            lambda x:
            (x == "Late").sum()
        )

    )

    .reset_index()

)


shipping_analysis["late_rate"] = (

    shipping_analysis["late_orders"]

    /

    shipping_analysis["total_orders"]

    * 100

)


shipping_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "shipping_analysis.csv"
    ),
    index=False
)


# ============================================================
# DELIVERY ANALYSIS
# ============================================================

print("Creating delivery analysis...")

delivery_analysis = (

    df.groupby(
        "delivery_performance"
    )

    .agg(

        total_orders=(
            "order_id",
            "nunique"
        )

    )

    .reset_index()

)


delivery_analysis.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "delivery_analysis.csv"
    ),
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n")
print("=" * 70)
print("PROCESSING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nProcessed rows : {len(df):,}"
)

print(
    f"Unique orders  : {total_orders:,}"
)

print(
    f"Customers      : {total_customers:,}"
)

print(
    f"Total sales    : ${total_sales:,.2f}"
)

print(
    f"Total profit   : ${total_profit:,.2f}"
)

print(
    f"Late delivery  : {late_delivery_rate:.2f}%"
)

print("\nGenerated files:")

for file in sorted(
    os.listdir(OUTPUT_DIR)
):

    print(f"  ✓ {file}")

print("\nProcessed data saved to:")

print(processed_path)

print("\n" + "=" * 70)