import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

def album(data):
    album_list = []
    for row in data['items']:
        album = row['track']['album']
        album_list.append({
            'album_id': album['id'],
            'name': album['name'],
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'url': album['external_urls']['spotify']
        })
    return album_list

def artist(data):
    artist_list = []
    for row in data['items']:
        for artist in row['track']['artists']:
            artist_list.append({
                'artist_id': artist['id'],
                'artist_name': artist['name'],
                'external_url': artist['href']
            })
    return artist_list

def songs(data):
    song_list = []
    for row in data['items']:
        track = row['track']
        song_list.append({
            'song_id': track['id'],
            'song_name': track['name'],
            'duration_ms': track['duration_ms'],
            'url': track['external_urls']['spotify'],
            'song_popularity': track['popularity'],
            'song_added': row['added_at'],
            'album_id': track['album']['id'],
            'artist_id': track['album']['artists'][0]['id']
        })
    return song_list

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')

    Bucket = 'spotify-etl-project-raksha'
    RawPrefix = "raw_data/to_processed/"

    response = s3.list_objects_v2(Bucket=Bucket, Prefix=RawPrefix)

    if "Contents" not in response:
        print("No files found to process")
        return {"statusCode": 200, "body": "No raw files found"}

    for file in response["Contents"]:
        raw_key = file["Key"]

        if not raw_key.endswith(".json"):
            continue

        print(f"Processing file: {raw_key}")

        obj = s3.get_object(Bucket=Bucket, Key=raw_key)
        data = json.loads(obj["Body"].read())

        album_df = pd.DataFrame(album(data)).drop_duplicates(subset=['album_id'])
        artist_df = pd.DataFrame(artist(data)).drop_duplicates(subset=['artist_id'])
        song_df = pd.DataFrame(songs(data))

        album_df['release_date'] = pd.to_datetime(album_df['release_date'])
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Songs
        song_buffer = StringIO()
        song_df.to_csv(song_buffer, index=False)
        s3.put_object(
            Bucket=Bucket,
            Key=f"transformed_data/songs_data/song_{timestamp}.csv",
            Body=song_buffer.getvalue()
        )

        # Albums
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index=False)
        s3.put_object(
            Bucket=Bucket,
            Key=f"transformed_data/album_data/album_{timestamp}.csv",
            Body=album_buffer.getvalue()
        )

        # Artists
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        s3.put_object(
            Bucket=Bucket,
            Key=f"transformed_data/artist_data/artist_{timestamp}.csv",
            Body=artist_buffer.getvalue()
        )

        # Move raw file to processed
    copy_source = {'Bucket': Bucket, 'Key': raw_key}
    s3_resource.meta.client.copy(
        copy_source,
        Bucket,
        f"raw_data/processed/{raw_key.split('/')[-1]}"
    )
    s3_resource.Object(Bucket, raw_key).delete()

    print(f"Moved and deleted raw file: {raw_key}")

    return {
        "statusCode": 200,
        "body": "Transformation completed successfully"
    }