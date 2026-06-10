import re
import tldextract

def extract_features(url):
    # 9 features generate kar rahe hain (dataset ke columns ke count ke barabar)

    having_ip = 1 if re.match(r"\d+\.\d+\.\d+\.\d+", url) else -1
    url_length = 1 if len(url) > 75 else -1
    short_url = -1 if "bit.ly" in url or "tinyurl" in url else 1
    at_symbol = -1 if "@" in url else 1
    double_slash = -1 if "//" in url[7:] else 1
    prefix_suffix = -1 if "-" in url else 1
    sub_domain = 1 if url.count(".") > 2 else -1
    ssl_state = 1 if url.startswith("https") else -1
    domain_length = 1 if len(tldextract.extract(url).domain) > 7 else -1

    return [
        having_ip,
        url_length,
        short_url,
        at_symbol,
        double_slash,
        prefix_suffix,
        sub_domain,
        ssl_state,
        domain_length
    ]
