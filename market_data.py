import yfinance as yf

def get_real_ticker_data(ticker_symbol):
    """Estrae metriche finanziarie reali da Yahoo Finance."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        # Estraiamo indicatori di prezzo e valutazione
        current_price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")
        fifty_two_high = info.get("fiftyTwoWeekHigh", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        market_cap = info.get("marketCap", "N/A")
        
        # Calcolo distanza dai massimi
        distance_from_high = "N/A"
        if isinstance(current_price, (int, float)) and isinstance(fifty_two_high, (int, float)):
            diff = ((current_price - fifty_two_high) / fifty_two_high) * 100
            distance_from_high = f"{diff:.2f}%"

        return {
            "symbol": ticker_symbol,
            "price": current_price,
            "pe_ratio": pe_ratio,
            "distance_from_52wk_high": distance_from_high,
            "currency": info.get("currency", "USD")
        }
    except Exception as e:
        return {"error": str(e)}