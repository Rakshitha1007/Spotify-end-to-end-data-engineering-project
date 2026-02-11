# Spotify-End-to-End Data Engineering Project
### Description
This project implements a fully automated, serverless end-to-end ETL (Extract, Transform, Load) pipeline on AWS using the Spotify Web API. The pipeline programmatically extracts playlist track metadata including song details, album information, and artist attributes using the Spotify Client Credentials authentication flow. Raw API responses are stored as timestamped JSON files in Amazon S3 to maintain data lineage, traceability, and reprocessing capability. An event-driven transformation layer, powered by AWS Lambda and Python (Pandas), reads unprocessed raw files, normalizes nested JSON structures, deduplicates records, and generates structured analytical datasets for albums, artists, and songs.The transformed data is written back to Amazon S3 in structured CSV format, organized into separate data zones to prevent duplicate processing and maintain clean data separation. AWS Glue Crawlers automatically infer schema and update the Glue Data Catalog, enabling Amazon Athena to perform serverless SQL queries directly on the S3 data lake.This project demonstrates cloud-native data engineering principles including serverless orchestration, event-driven architecture, automated schema management, and scalable analytics-ready data modeling.

### Architecture
![Architecture](https://github.com/Rakshitha1007/Spotify-end-to-end-data-engineering-project/blob/main/Spotify%20Architecture%20ETL.png)
### About Dataset/API
This API containes information about music artists, albums and songs - [Spotify API](https://developer.spotify.com/documentation/web-api)
### Services Used
1. **Amazon S3 (Simple Storage Service):** Serves as the central data lake for the pipeline, storing raw Spotify API responses, processed files, and transformed datasets used for analytics.
2. **AWS Lambda:** Executes serverless functions to extract data from the Spotify API, transform it using Python and Pandas, and load the processed data into Amazon S3.
3. **Amazon EventBridge (CloudWatch Events):** Automates and schedules the execution of the data extraction Lambda function at regular intervals.
4. **AWS Glue Crawler:** Automatically scans transformed data in Amazon S3, infers schemas, and updates table definitions in the Glue Data Catalog.
5. **AWS Glue Data Catalog:** Stores metadata for all datasets, enabling structured querying and seamless integration with Amazon Athena.
6. **Amazon Athena:** Enables serverless SQL-based querying of transformed data stored in Amazon S3 for analytics and insights.


### Install Packages

```
pip install pandas
pip install numpy
pip install spotipy
```
## Project Execution Flow

1. **Data Extraction:**  
- Uses Spotify Client Credentials authentication flow  
- Fetches playlist track metadata via Spotify Web API  
- Stores full API response as timestamped JSON files in S3  
- Preserves raw data for traceability and future reprocessing  
- Fully automated via scheduled Amazon EventBridge trigger  

2. **Raw Data Storage:**  
Amazon S3 (`raw_data/to_processed/`)

```
spotify-etl-project-bucket/
├── raw_data/
│   ├── to_processed/     → Newly ingested Spotify JSON files
│   └── processed/        → Raw files already transformed
│
└── transformed_data/
    ├── album_data/       → Cleaned album datasets (CSV)
    ├── artist_data/      → Cleaned artist datasets (CSV)
    └── songs_data/       → Cleaned song datasets (CSV)
```

4. **Transformation Trigger:**  
- Amazon EventBridge (rate schedule) triggers extraction Lambda periodically  
- Amazon S3 ObjectCreated event triggers transformation Lambda  
- Pipeline executes end-to-end without manual intervention  
- Raw files are automatically moved after successful processing  
- Ensures a fully event-driven architecture  

5. **Data Transformation:**  The transformation Lambda:
- Reads all unprocessed raw JSON files from S3  
- Parses and normalizes nested Spotify API structures  
- Converts semi-structured JSON into structured tabular datasets  

6. **Processed Data Storage:**  
- Writes transformed datasets as CSV files to S3  
- Uses timestamped filenames for version control  
- Moves processed raw files to `raw_data/processed/`  
- Prevents duplicate reprocessing
  
7. **Schema Inference:**  
- AWS Glue Crawler infers schema from transformed CSV files  
- Tables stored in AWS Glue Data Catalog  
- Amazon Athena enables SQL querying directly on S3  

8. **Analytics & Querying:**  
   Amazon Athena queries the transformed data directly from S3 using SQL for analytics and insights.

