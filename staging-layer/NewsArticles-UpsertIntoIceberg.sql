MERGE INTO "s3tablescatalog/stage-us-east-1-jngai-dev".equity_research.fmp_articles AS target
USING AwsDataCatalog.raw.fmp_articles_source AS source
ON (target.link = source.link)
WHEN MATCHED THEN
    UPDATE SET 
        title = source.title,
        date = source.date,
        content = source.content,
        tickers = source.tickers,
        image = source.image,
        author = source.author,
        site = source.site,
        last_updated = CAST(current_timestamp AS TIMESTAMP(6))
WHEN NOT MATCHED THEN
    INSERT (title, date, content, tickers, image, link, author, site, ingestion_date, last_updated)
    VALUES (
        source.title,
        source.date,
        source.content,
        source.tickers,
        source.image,
        source.link,
        source.author,
        source.site,
        current_date,
        CAST(current_timestamp AS TIMESTAMP(6))
    );
