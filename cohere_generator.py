import cohere
import config

co = cohere.Client(config.COHERE_API_KEY)

def generate_seo_article(title, summary, region):
    # রিজন ভিত্তিক প্রম্পট
    region_prompt = {
        'usa': "Focus on US audience and Google SEO guidelines",
        'eu': "Focus on European audience and GDPR compliance"
    }.get(region, "")
    
    prompt = f"""
    নিউজ টাইটেল: {title}
    নিউজ সামারি: {summary}
    
    SEO-অপটিমাইজড আর্টিকেল লিখুন (800-1000 শব্দ) নিম্নলিখিত বিষয়বস্তু অনুসারে:
    - {region.upper()} মার্কেটের জন্য উপযোগী
    - {region_prompt}
    - প্রাসঙ্গিক কীওয়ার্ড ব্যবহার করুন
    - H2/H3 হেডিংসহ স্ট্রাকচারড আর্টিকেল
    - মানববান্ধব ভাষায় লিখুন
    """
    
    response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7
    )
    return response.generations[0].text
