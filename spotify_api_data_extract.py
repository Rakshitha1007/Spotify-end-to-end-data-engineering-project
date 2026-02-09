import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):

    # 1️⃣ Credentials from env variables
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')

    # 2️⃣ Spotify client (Lambda-safe)
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )

    sp = spotipy.Spotify(
        client_credentials_manager=client_credentials_manager
    )

    # 3️⃣ Playlist extraction
    playlist_link = "https://open.spotify.com/playlist/0Ozuve71TWqmFQ5XQGzUO9"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    spotify_data = sp.playlist_tracks(playlist_URI)

    # 4️⃣ Create timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"spotify_raw_{timestamp}.json"

    # 5️⃣ Upload to S3
    s3 = boto3.client('s3')

    s3.put_object(
        Bucket="spotify-etl-project-raksha",
        Key=f"raw_data/to_processed/{filename}",
        Body=json.dumps(spotify_data)
    )

    return {
        "statusCode": 200,
        "body": f"Uploaded {filename} successfully"
    }
