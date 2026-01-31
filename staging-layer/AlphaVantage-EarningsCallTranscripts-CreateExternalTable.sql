-- Step 1: Drop the existing table to "overwrite" it
DROP TABLE IF EXISTS raw.earnings_call_transcripts_source;

-- Step 2: Create the table with the new schema and dynamic location
CREATE EXTERNAL TABLE raw.earnings_call_transcripts_source (
    symbol STRING,
    quarter STRING,
    transcript ARRAY<STRUCT<speaker: STRING, title: STRING, content: STRING, sentiment: DECIMAL>>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://raw-us-east-1-jngai-dev/alpha_vantage/earnings_call_transcripts/${TICKER}/target/';
