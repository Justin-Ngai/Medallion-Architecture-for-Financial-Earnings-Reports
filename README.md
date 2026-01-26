**Financial Text Ingestion and Staging Pipeline**

---

**Overview**

This repository contains an AWS-based pipeline for ingesting, staging, and structuring financial text data from Alpha Vantage and Financial Modeling Prep. The system automates the collection of earnings transcripts and news articles and loads them into Apache Iceberg tables for analytics.

---

**Architecture**

The pipeline uses AWS managed services and follows a layered design with Bronze and Silver stages.

**Scheduling (EventBridge)**

- Earnings transcripts are scheduled quarterly
- News articles are scheduled daily at 7:00 AM
- Each schedule triggers a Step Functions workflow
- An input parameter provides a list of stock tickers for processing

**Ingestion – Bronze Layer**

Earnings transcripts and news articles are collected using AWS Lambda functions, which fetch data from external APIs and store the results as JSON files in S3.

**Orchestration (Step Functions)**

Step Functions workflows iterate over the list of stock tickers and reporting periods. For each iteration, ingestion is executed, data is staged in S3, Athena tables are created, and records are upserted into Iceberg.

**Staging – Silver Layer**

Athena external tables are created on top of raw JSON files. The data is transformed and merged into Apache Iceberg tables.

**Analytical Storage (Iceberg)**

Apache Iceberg tables are stored in S3 and support incremental upserts and analytical queries.

---

**Folder Structure and Repository Contents**

The repository is organized into four main folders based on pipeline responsibilities.

/raw_processing
/environment_setup
/staging_processing
/orchestration

1. raw_processing

Contains AWS Lambda functions for data ingestion.

- Earnings transcript ingestion from Alpha Vantage  
- News article ingestion from Financial Modeling Prep  

These functions fetch external data and write raw JSON files to S3.

2. environment_setup

Contains Athena queries for environment initialization.

- Create Apache Iceberg tables  
- Define table schemas and properties  

This layer prepares the analytical storage environment.

3. staging_processing

Contains Athena queries for staging and merging data.

- Create external tables on raw JSON files  
- Upsert staged data into Iceberg tables  

This layer handles transformation and merge logic.

4. orchestration

Contains Step Functions workflows.

- Quarterly earnings transcript workflow  
- Daily news article workflow  

These workflows coordinate ingestion, staging, and merge operations across the pipeline.
