import feedparser

# Fonti: Mercati tradizionali, Crypto e Macroeconomia
RSS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "MarketWatch": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "CNBC": "https://search.cnbc.com/rs/search/combinednews/view.xml?partnerId=wr2k&id=15839069",
    "Investing.com": "https://it.investing.com/rss/news.rss",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/"
}

def fetch_all_news(limit_per_feed=3):
    """Scarica le notizie più recenti da tutti i feed."""
    compiled_news = []
    
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:limit_per_feed]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            compiled_news.append(f"[{source}] {title}: {summary[:150]}...")
            
    return "\n".join(compiled_news)