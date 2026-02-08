#!/usr/bin/env python3
"""
Standalone YouTube OAuth2 authentication script.
Run this once to generate youtube_token.pickle.
Requires browser access - run on a machine with a browser.
"""
import pickle
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl',
]

CLIENT_SECRET = Path(__file__).parent / 'client_secret.json'
TOKEN_FILE = Path(__file__).parent / 'youtube_token.pickle'

def main():
    if not CLIENT_SECRET.exists():
        print(f"❌ Client secret not found at {CLIENT_SECRET}")
        print("Copy it from ~/Projects/youtube-analytics/client_secret.json")
        return

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
    credentials = flow.run_local_server(port=8090, prompt='consent')

    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(credentials, f)

    print(f"✅ Token saved to {TOKEN_FILE}")

if __name__ == '__main__':
    main()
