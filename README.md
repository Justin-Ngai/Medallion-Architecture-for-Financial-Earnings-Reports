**Financial Text Ingestion and Staging Pipeline**

---

**Overview**

This repository contains an AWS-based pipeline for ingesting, staging, and structuring financial text data from Alpha Vantage and Financial Modeling Prep. The system automates the collection of earnings transcripts and news articles and loads them into Apache Iceberg tables for analytics.

---

**Architecture**

The pipeline uses AWS managed services and follows a layered design with Bronze and Silver stages.

**Scheduling (EventBridge)**

- Two schedules run daily at 7:00 AM
- Each schedule triggers a Step Functions workflow
- Workflows receive a list of stock tickers

**Ingestion – Bronze Layer**

- Earnings transcripts collected quarterly from Alpha Vantage
- News articles collected daily from Financial Modeling Prep
- AWS Lambda fetches data and stores JSON in S3

**Orchestration (Step Functions)**

- Loops over tickers and reporting periods
- For each iteration:
  - Run ingestion Lambda
  - Store JSON in S3
  - Create Athena tables
  - Upsert into Iceberg

**Staging – Silver Layer**

- Athena external tables on raw JSON
- Data transformed and merged into Iceberg

**Analytical Storage (Iceberg)**

- Stored in S3
- Supports incremental upserts and analytics

---

**Data Layers**

| Layer  | Purpose          | Components                         |
|--------|------------------|------------------------------------|
| Bronze | Raw ingestion    | EventBridge, Lambda, S3 (JSON)      |
| Silver | Staging and merge| Athena, Iceberg                    |

---

**Scheduling**

| Dataset              | Frequency   | Trigger                         |
|----------------------|-------------|---------------------------------|
| Earnings Transcripts | Quarterly   | EventBridge → Step Functions    |
| News Articles        | Daily 7 AM  | EventBridge → Step Functions    |

Both pipelines follow the same orchestration pattern.

---

**Repository Contents**

1. Lambda – Earnings Transcript Ingestion  
   Fetches transcripts from Alpha Vantage and stores results in S3 as JSON.

2. Lambda – News Article Ingestion  
   Fetches news from Financial Modeling Prep and writes normalized JSON to S3.

3. Athena – Create Iceberg Table  
   Creates Apache Iceberg tables in S3 and defines schemas and properties.

4. Athena – Create External JSON Table  
   Creates Athena tables over raw JSON files.

5. Athena – Upsert into Iceberg  
   Merges staged data into Iceberg tables and handles inserts and updates.

6. Step Functions Workflow  
   JSON state machine definitions that orchestrate ingestion and transformation.

**Workflow Steps**

1. Receive parameters  
2. Invoke Lambda  
3. Create Athena tables  
4. Run Iceberg upsert

---

**Summary**

This project provides a scalable, serverless pipeline for financial text data. It separates raw ingestion from structured storage, supports automated scheduling, and enables reliable analytics using Apache Iceberg.
