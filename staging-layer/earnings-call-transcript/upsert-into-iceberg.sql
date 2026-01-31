MERGE INTO "s3tablescatalog/stage-us-east-1-jngai-dev".equity_research.earnings_call_transcripts AS target
USING AwsDataCatalog.raw.earnings_call_transcripts_source AS source
ON (target.symbol = source.symbol AND target.quarter = source.quarter)
WHEN MATCHED THEN
    UPDATE SET 
        transcript = CAST(source.transcript AS ARRAY(ROW(speaker VARCHAR, title VARCHAR, content VARCHAR, sentiment DECIMAL))),
        last_updated = CAST(current_timestamp AS TIMESTAMP(6))
WHEN NOT MATCHED THEN
    INSERT (symbol, quarter, transcript, ingestion_date, last_updated)
    VALUES (
        source.symbol, 
        source.quarter, 
        CAST(source.transcript AS ARRAY(ROW(speaker VARCHAR, title VARCHAR, content VARCHAR, sentiment DECIMAL))), 
        current_date, 
        CAST(current_timestamp AS TIMESTAMP(6))
    );
