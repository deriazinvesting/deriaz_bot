import os
import FinanceDataReader as fdr
import requests
from datetime import datetime
import time

# 깃허브 설정(Secrets)에서 불러올 변수들
BOT_TOKEN = os.environ.get('TG_TOKEN')
CHAT_ID = os.environ.get('TG_CHAT_ID')

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def get_price_message():
    # 원하는 종목 리스트 (이름: 티커)
    # 한국주식: 종목코드, 미국주식: 티커, 지수: KS11(코스피), KQ11(코스닥), US500(S&P500)
    target_stocks = {
        "코스피": "KS11",
        "코스닥": "KQ11",
        "S&P 500": "US500",
        "나스닥": "IXIC",
        "삼성전자": "005930",
        "SK하이닉스": "000660",
        "알파벳": "GOOGL",
        "테슬라": "TSLA",
        "엔비디아": "NVDA",
        "마이크론": "MU",
        "샌디스크": "SNDK",
        "비트코인": "BTC/USDT",
        "이더리움": "ETH/USDT",
        "달러/원": "USD/KRW"
    }
    
    msg = f"📊 [{datetime.now().strftime('%Y-%m-%d')}] 종가 알림\n\n"
    
    for name, code in target_stocks.items():
        try:
            # 데이터 가져오기 (최근 2일치 가져와서 마지막꺼 사용)
            df = fdr.DataReader(code)
            if df.empty:
                continue
                
            close_val = df['Close'].iloc[-1]
            
            # 보기 좋게 꾸미기
            if code == "USD/KRW":
                price_str = f"{close_val:.2f}원"
            elif isinstance(close_val, float) and close_val < 5000: # 미국주식 등
                price_str = f"${close_val:.2f}"
            else: # 한국주식 및 지수
                price_str = f"{int(close_val):,}pt/원"
                
            msg += f"✅ {name}: {price_str}\n"
        except Exception as e:
            msg += f"❌ {name}: 에러 발생\n"
            
    return msg

if __name__ == "__main__":
    text = get_price_message()
    send_msg(text)

    print("전송 완료")
