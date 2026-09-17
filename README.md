\# Supply Chain Cloud Analytics



A cloud-based Supply Chain Analytics application developed using Flask and AWS.



\## Technologies



\- Python

\- Flask

\- MySQL

\- Amazon EC2

\- Amazon RDS

\- Amazon S3

\- IAM

\- VPC

\- Plotly



\## Architecture



User → Web Browser → EC2 (Flask) → RDS + S3 → Analytics Dashboard



\## AWS Components



\- VPC with public and private subnets

\- Internet Gateway

\- EC2 application server

\- RDS MySQL database

\- S3 dataset storage

\- IAM role for EC2-S3 access

\- Security Groups for network control



\## Dataset



The original dataset is stored in Amazon S3.



S3 bucket:

`supplychain-cloud-data-bda`



Folder:

`raw/`



\## Database



Database:

`supply\_chain`



Table:

`supply\_chain\_data`



Rows loaded:

180,519



\## Running the application



1\. Create `.env` from `.env.example`

2\. Configure the RDS endpoint and credentials

3\. Install dependencies:



```bash

pip install -r requirements.txt

