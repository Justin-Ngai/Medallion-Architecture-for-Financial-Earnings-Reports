import json
import boto3
import urllib3

# Configuration
# Keep your existing Secret ARN and S3 Bucket
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:629904435132:secret:dev/alpha_vantage-wbLVgz"
S3_BUCKET = "raw-us-east-1-jngai-dev"
# Updated to FMP Articles endpoint
BASE_URL = "https://financialmodelingprep.com/api/v3/fmp/articles"

# Clients
http = urllib3.PoolManager()
s3 = boto3.client("s3")
secrets = boto3.client("secretsmanager")

def lambda_handler(event, context):
    # FMP Articles uses 'page' and 'size' instead of symbols
    page = event.get("page", 0)
    size = event.get("size", 5)
    
    # Get API key from Secrets Manager
    res = secrets.get_secret_value(SecretId=SECRET_ARN)
    api_key = json.loads(res["SecretString"])["FreeApiKey"]
    
    # FMP query parameters
    params = {
        "page": page,
        "size": size,
        "apikey": api_key
    }
    
    # Build URL string
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE_URL}?{query_string}"
    print(f"Request URL: {url}")
    
    try:
        raw_res = http.request("GET", url)
        data = json.loads(raw_res.data.decode("utf-8"))
        
        # FMP returns an error message in a "Error Message" key if the key is invalid
        if isinstance(data, dict) and "Error Message" in data:
            return {
                "statusCode": 401,
                "body": json.dumps({
                    "error": "FMP API error",
                    "details": data["Error Message"]
                })
            }
        
        json_content = json.dumps(data)
        
        # Define S3 keys for FMP news articles
        target_key = f"fmp/news_articles/latest/articles.json"
        historic_key = f"fmp/news_articles/historic/page_{page}_size_{size}.json"
        
        # Save to latest/target folder
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=target_key,
            Body=json_content,
            ContentType="application/json"
        )
        
        # Save to historic folder
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=historic_key,
            Body=json_content,
            ContentType="application/json"
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "FMP Articles saved successfully",
                "page": page,
                "size": size,
                "target_key": target_key,
                "historic_key": historic_key
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
