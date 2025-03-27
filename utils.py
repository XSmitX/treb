# Stickers for bot responses
STICKERS = {
    'welcome': 'CAACAgQAAxkBAAEWpZpn5Ga_FS36Uc8kSiuAc_6LmQGDugACqgsAAsDqEFDQ3jt1DpvhoDYE',
    'processing': 'CAACAgUAAxkBAAEV_8RnkPiFEzAKWVUgzWeNcLTOWjsBkAACpwgAAtu6GFQ4oUoIL-_BgzYE'
}

def process_terabox_url(url):
    """Process TeraBox URL and extract ID"""
    try:
        if '/s/' in url:
            # For URLs with /s/ pattern
            surl = url.split('/s/')[1].split('?')[0].split('#')[0]
        elif 'surl=' in url:
            # For URLs with surl parameter
            surl = url.split('surl=')[1].split('&')[0].split('?')[0].split('#')[0]
        elif 'id=' in url:
            # For URLs with id parameter
            surl = url.split('id=')[1].split('&')[0].split('?')[0].split('#')[0]
        else:
            # Get the last part of the URL
            surl = url.split('/')[-1].split('?')[0].split('#')[0]
        
        return surl
    except Exception as e:
        print(f"Error processing URL: {e}")
        return None

def create_streaming_url(surl):
    """Create streaming URL from TeraBox ID"""
    return f"https://muddy-flower-20ec.arjunavai273.workers.dev/?id={surl}" 