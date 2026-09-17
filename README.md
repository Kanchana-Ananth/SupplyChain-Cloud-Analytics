# Supply Chain Cloud Analytics

A cloud-based Supply Chain Analytics application developed using **Python, Flask, and AWS**.  
The application stores supply-chain data in Amazon RDS and Amazon S3 and displays the analysis through a web dashboard.

## Technologies Used

- Python
- Flask
- MySQL
- Plotly
- Amazon EC2
- Amazon RDS
- Amazon S3
- IAM
- Amazon VPC

## Application Flow

<img width="644" height="734" alt="image" src="https://github.com/user-attachments/assets/3321b0da-8d15-4b59-a19b-2838d7921b86" />


**User → Web Browser → EC2 (Flask) → RDS + S3 → Data Processing → Analytics → Dashboard**

## Dashboard

<img width="940" height="617" alt="image" src="https://github.com/user-attachments/assets/c0cdda8d-fb07-40e7-8982-4659fc5edc1f" />


The dashboard shows:

- Total Orders
- Total Sales
- Total Customers
- Total Profit
- Average Order Value
- Late Delivery Rate

## Analytics

<img width="940" height="723" alt="image" src="https://github.com/user-attachments/assets/1dd6f10a-8a49-4d44-892b-a513e57201be" />


The application provides charts for:

- Monthly Sales
- Product Categories
- Sales by Region
- Shipping Mode
- Delivery Performance

## Project Structure

```text
SupplyChain-Cloud-Analytics/
├── app.py
├── analysis.py
├── database.py
├── load_data.py
├── s3_utils.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
└── static/

```
## AWS Services

- **Amazon VPC** – Provides the cloud network.
- **Amazon EC2** – Runs the Flask web application.
- **Amazon RDS** – Stores the supply-chain data in MySQL.
- **Amazon S3** – Stores the raw and processed datasets.
- **IAM** – Provides secure access from EC2 to S3.
- **Security Groups** – Controls inbound and outbound traffic.

## Database

**Database:** `supply_chain`  
**Table:** `supply_chain_data`  
**Records:** 180,519

## S3 Storage

```text
supplychain-cloud-data-bda/
├── raw/
│   └── DataCoSupplyChainDataset.csv
└── processed/
```
## Result

The cloud-based Supply Chain Analytics application was successfully deployed on AWS using EC2, RDS, S3, VPC, and IAM. The application provides an interactive dashboard for analyzing supply-chain data and displaying key business insights.
