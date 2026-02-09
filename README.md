# Spotify-End-to-End Data Engineering Project
### Description
Built an end-to-end ETL pipeline on AWS using the Spotify API. The pipeline extracts music metadata from Spotify, transforms raw JSON into structured datasets, and loads the data into AWS S3 for querying and analysis using Glue and Athena
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
   AWS Lambda fetches music metadata (artists, albums, songs) from the Spotify API.

2. **Raw Data Storage:**  
   Extracted JSON data is stored in Amazon S3 under the `raw_data/` directory.

3. **Transformation Trigger:**  
   An S3 ObjectCreated event triggers the transformation Lambda function.

4. **Data Transformation:**  
   The transformation Lambda processes raw data using Python and Pandas, creating structured datasets for albums, artists, and songs.

5. **Processed Data Storage:**  
   Transformed CSV files are saved to Amazon S3 under the `transformed_data/` directory, while raw files are moved to `raw_data/processed/`.

6. **Schema Inference:**  
   AWS Glue Crawler scans the transformed data and updates table schemas in the Glue Data Catalog.

7. **Analytics & Querying:**  
   Amazon Athena queries the transformed data directly from S3 using SQL for analytics and insights.
