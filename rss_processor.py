import feedparser
import random
import database
import logging

logger = logging.getLogger(__name__)

def get_latest_news():
    try:
        # ডাটাবেস থেকে ফিড পাওয়া
        feeds = database.get_feeds()
        if not feeds:
            return None
            
        # র‍্যান্ডম ফিড সিলেক্ট
        feed_url, region = random.choice(feeds)
        
        # ফিড পার্স করুন
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            return None
            
        # র‍্যান্ডম নিউজ আইটেম
        entry = random.choice(feed.entries[:5])
        
        # ইমেজ এক্সট্রাক্ট
        image_url = None
        if hasattr(entry, 'media_content'):
            for media in entry.media_content:
                if media.get('type', '').startswith('image/'):
                    image_url = media['url']
                    break
        
        return {
            'title': entry.title,
            'summary': entry.description,
            'link': entry.link,
            'image': image_url,
            'region': region
        }
        
    except Exception as e:
        logger.error(f"RSS প্রসেসিং ত্রুটি: {str(e)}")
        return None
