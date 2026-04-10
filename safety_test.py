import streamlit as st
import requests
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator

# 1. 앱 페이지 설정 (제목, 아이콘)
st.set_page_config(page_title="글로벌 안전 사고 분석기", page_icon="⚠️")

st.title("🌍 글로벌 안전 사고 실시간 분석")
st.write("미국 구글 뉴스를 분석하여 최신 산업 사고 소식을 한국어로 요약합니다.")

# 2. 사이드바 (필터 설정)
st.sidebar.header("설정")
news_count = st.sidebar.slider("수집할 뉴스 개수", 5, 20, 10)

# 3. 데이터 수집 및 분석 함수
def get_safety_news(count):
    url = "https://news.google.com/rss/search?q=industrial+accident&hl=en-US&gl=US&ceid=US:en"
    translator = GoogleTranslator(source='en', target='ko')
    
    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)
        news_list = []
        
        for item in root.findall('.//item')[:count]:
            eng_title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            kor_title = translator.translate(eng_title)
            
            news_list.append({
                "title": kor_title,
                "date": pub_date,
                "link": link
            })
        return news_list
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return []

# 4. 앱 화면 구성
if st.button("🔄 최신 사고 소식 업데이트"):
    with st.spinner('뉴스를 분석 중입니다... 잠시만 기다려주세요.'):
        results = get_safety_news(news_count)
        
        if results:
            for idx, news in enumerate(results):
                # 예쁜 상자(Card) 안에 뉴스 표시
                with st.container():
                    st.subheader(f"{idx+1}. {news['title']}")
                    st.write(f"📅 발생일: {news['date']}")
                    st.markdown(f"[🔗 원문 기사 보기]({news['link']})")
                    st.divider() # 구분선
            st.success("모든 뉴스를 성공적으로 분석했습니다!")