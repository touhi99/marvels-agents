import os 
import urllib.parse
import secrets
import requests

# OAuth setup
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = 'http://localhost:8501/'
ENCODED_REDIRECT_URI = urllib.parse.quote(REDIRECT_URI, safe='')

def get_auth_url():
    playerSessionSecret = secrets.token_urlsafe()
    AUTH_URL = (
        f"https://hydra-public.prod.m3.scopelypv.com/oauth2/auth?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={ENCODED_REDIRECT_URI}&"
        f"state={playerSessionSecret}&"
        f"scope=openid+offline+m3p.f.pr.pro+m3p.f.pr.act+m3p.f.pr.ros"
    )
    return AUTH_URL


def get_access_token(code):
    token_url = 'https://hydra-public.prod.m3.scopelypv.com/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    response = requests.post(token_url, data=data)
    return response.json()

