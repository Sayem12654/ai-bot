from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import os
import logging

logger = logging.getLogger(__name__)

def create_post(title, content, image_url=None):
    try:
        # টোকেন লোড করুন
        if not os.path.exists('token.json'):
            return {'success': False, 'error': 'টোকেন ফাইল পাওয়া যায়নি'}
            
        with open('token.json') as f:
            token_data = json.load(f)
            creds = Credentials(
                token=token_data['token'],
                refresh_token=token_data['refresh_token'],
                token_uri=token_data['token_uri'],
                client_id=token_data['client_id'],
                client_secret=token_data['client_secret'],
                scopes=token_data['scopes']
            )
        
        # সার্ভিস তৈরি
        service = build('blogger', 'v3', credentials=creds)
        
        # ইমেজ যোগ করুন
        html_content = content
        if image_url:
            html_content = f'<img src="{image_url}" alt="{title}" style="max-width:100%"><br>{content}'
        
        # পোস্ট বডি
        body = {
            "title": title,
            "content": html_content,
            "labels": ["AI-Generated", "News"]
        }
        
        # পোস্ট তৈরি
        post = service.posts().insert(
            blogId=config.BLOGGER_ID,
            body=body
        ).execute()
        
        return {
            'success': True,
            'url': post['url'],
            'title': title
        }
        
    except Exception as e:
        logger.error(f"ব্লগার ত্রুটি: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
