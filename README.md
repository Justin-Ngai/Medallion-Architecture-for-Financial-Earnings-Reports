**Financial Text Ingestion & Staging Pipeline**

This repository contains an AWS-based pipeline for ingesting, staging, and structuring financial text data from Alpha Vantage and Financial Modeling Prep (FMP). The system automates collection of earnings transcripts and news articles and loads them into Apache Iceberg tables for analytics.

**Architecture**

The pipeline uses AWS managed services and follows a layered (Bronze → Silver) design.
	1.	Scheduling (EventBridge)

	•	Two schedules run daily at 7:00 AM.
	•	Each triggers a Step Functions workflow.
	•	Workflows receive a list of stock tickers.
	
	2.	Ingestion – Bronze Layer (Raw)
	•	Earnings transcripts (quarterly) from Alpha Vantage.
	•	News articles (daily) from FMP.
	•	AWS Lambda fetches data and stores JSON in S3.
	
	3.	Orchestration (Step Functions)
	•	Loops over tickers and periods.
	•	For each iteration:
	
	1.	Run ingestion Lambda.
	2.	Store JSON in S3.
	3.	Create Athena tables.
	4.	Upsert into Iceberg.
	
	4.	Staging – Silver Layer
	•	Athena external tables on raw JSON.
	•	Transformed and merged into Iceberg tables.
	
	5.	Analytical Storage (Iceberg)
	•	Stored in S3.
	•	Supports incremental upserts and analytics.

**Data Layers**

Layer	Purpose	Components
Bronze	Raw ingestion	EventBridge, Lambda, S3 (JSON)
Silver	Staging & merge	Athena, Iceberg

**Scheduling**

Dataset	Frequency	Trigger
Earnings Transcripts	Quarterly	EventBridge → Step Functions
News Articles	Daily (7 AM)	EventBridge → Step Functions

Both pipelines follow the same orchestration pattern.

**Repository Contents**

1. Lambda – Earnings Transcript Ingestion
	•	Fetches transcripts from Alpha Vantage.
	•	Stores results in S3 as JSON.

2. Lambda – News Article Ingestion
	•	Fetches news from Financial Modeling Prep.
	•	Writes normalized JSON to S3.

3. Athena – Create Iceberg Table
	•	Creates Apache Iceberg tables in S3.
	•	Defines schema and properties.

4. Athena – Create External JSON Table
	•	Creates Athena tables over raw JSON files.
	•	Enables querying of ingestion data.

5. Athena – Upsert into Iceberg
	•	Merges staged data into Iceberg tables.
	•	Handles inserts and updates.

6. Step Functions Workflow
	•	JSON state machine definition.
	•	Orchestrates ingestion and transformation per ticker and quarter.

Workflow:
	1.	Receive parameters.
	2.	Invoke Lambda.
	3.	Create Athena tables.
	4.	Run Iceberg upsert.

**Summary**

This project provides a scalable, serverless pipeline for financial text data. It separates raw ingestion from structured storage, supports automated scheduling, and enables reliable analytics using Apache Iceberg.
