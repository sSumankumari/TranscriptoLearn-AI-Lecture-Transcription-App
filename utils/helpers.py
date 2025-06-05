from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    try:
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc:
            return parse_qs(parsed_url.query)['v'][0]
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path[1:]
        else:
            return None
    except Exception:
        return None