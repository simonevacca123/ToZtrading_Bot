import os
from google import genai
from dotenv import load_dotenv
from market_data import get_real_ticker_data

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_market_opportunities(news_text):
    prompt = f"""
    Sei un educatore finanziario. Analizza queste notizie: {news_text}
    Struttura:
    1️⃣ DOVE INVESTIRE (I 3 migliori del momento) - Azione e Rischio %.
    2️⃣ RUMORE vs SEGNALE VERO - L'hype inutile vs la notizia vera.
    3️⃣ IL CATALIZZATORE - Quale evento imminente muoverà il mercato.
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text

def butterfly_effect(evento):
    prompt = f"""
    Sei un geniale analista macroeconomico. Calcola "l'effetto farfalla" per questo evento: {evento}.
    Spiega le conseguenze di secondo e terzo livello che la massa non vede.
    Formato:
    🦋 **L'EFFETTO FARFALLA: {evento.upper()}**
    🏆 **Vincitori Inaspettati (2 asset):** Spiega il collegamento logico occulto.
    💀 **Vittime Collaterali (2 asset):** Chi ci rimetterà senza che nessuno se lo aspetti.
    🧠 **Il Rischio Cigno Nero:** Cosa potrebbe succedere di totalmente imprevedibile.
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text

def analyze_fomo(ticker):
    real_data = get_real_ticker_data(ticker)
    
    if "error" in real_data or real_data.get("price") == "N/A":
        return f"⚠️ Impossibile recuperare dati reali per '{ticker}'. Verifica il simbolo (es. NVDA, VWCE.DE, AAPL)."

    prompt = f"""
    Sei un analista quantitativo. Analizza questo asset basandoti RIGOROSAMENTE su questi dati reali di mercato:
    
    📌 Asset: {real_data['symbol']}
    💵 Prezzo Attuale: {real_data['price']} {real_data['currency']}
    📊 Rapporto Prezzo/Utili (P/E): {real_data['pe_ratio']}
    📉 Distanza dai Massimi a 52 Settimane: {real_data['distance_from_52wk_high']}

    REGOLE RIGIDE:
    1. L'Indice di Bolla % deve basarsi su dati reali (un P/E basso o un ETF globale ben diversificato NON possono avere indici di bolla altissimi).
    2. Spiega se il prezzo attuale è giustificato dai fondamentali numerici forniti.

    Formato:
    🫧 **FOMO METER REALE: {real_data['symbol']}**
    📈 **Dati di Mercato:** Prezzo {real_data['price']} {real_data['currency']} | P/E: {real_data['pe_ratio']} | Var. Massimi: {real_data['distance_from_52wk_high']}
    🌡️ **Indice di Bolla Realistico:** [Valutazione % basata sui numeri sopra]
    🎯 **Verdetto sui Fondamentali:** [Analisi oggettiva basata sui dati]
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text

def roast_portfolio(portfolio):
    prompt = f"""
    Sei un cinico gestore di hedge fund. Fai il roast di questo portafoglio: {portfolio}.
    Formato:
    🔥 **ROAST DEL PORTAFOGLIO**
    🤡 **Il tuo più grande errore:** Trova la mancanza di diversificazione.
    📉 **Stress Test:** Cosa succede se l'inflazione sale al 5%?
    💡 **Il consiglio spietato:** Cosa faresti per sistemare questo disastro.
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text

def plan_investment(importo, news_text):
    prompt = f"""
    Sei un Wealth Manager di alto livello. Il tuo cliente ha un capitale di {importo} e ti chiede come allocarlo OGGI.
    
    Ecco il contesto di mercato attuale in tempo reale: 
    {news_text}
    
    COMPITO: Crea un portafoglio su misura applicando simultaneamente:
    1. Logica Anti-Bolla (Evita asset in FOMO pura sui massimi).
    2. L'Effetto Farfalla (Cerca asset che beneficeranno indirettamente delle notizie fornite).
    
    Formato tassativo:
    💼 **MASTER PLAN PER: {importo}**
    
    🍰 **L'Allocazione:** Dividi l'importo in % precise su 3 o 4 asset/ETF. Spiega brevemente la logica per ciascuno.
    
    📈 **Rendimento Annuo Stimato:** [Es: 7.5% - 9%] Calcola una stima realistica basata sulla media storica degli asset scelti.
    
    ⚖️ **Max Drawdown (Rischio Peggiore):** [Es: -15%] Quanto potrebbe perdere questo portafoglio in un anno di recessione.
    
    ⚠️ Concludi con un disclaimer di una riga: "Le stime sono basate su medie storiche e logica algoritmica, non sono garanzie future."
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
    return response.text