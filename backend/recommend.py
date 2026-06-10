def recommend_sites(url):
    url = url.lower()

    if "bank" in url:
        return ["sbi.co.in", "hdfcbank.com", "icicibank.com"]
    elif "shop" in url or "buy" in url:
        return ["amazon.in", "flipkart.com", "myntra.com"]
    elif "social" in url:
        return ["facebook.com", "instagram.com", "twitter.com"]
    else:
        return ["google.com", "wikipedia.org", "microsoft.com"]
