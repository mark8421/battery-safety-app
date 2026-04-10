import streamlit as st
import requests
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
import pandas as pd

st.set_page_config(page_title="배터리 제조 안전 모니터링", page_icon="🔋", layout="wide")

st.title("🔋 배터리 제조업 글로벌 사고 모니터링 (KR/US/CN)")
st.write("한국, 미국, 중국의 배터리 공장 화재, 폭발, 화학 사고 소식을 집중 추적합니다.")

# 1. 국가별 정밀 검색 키워드 설정 (배터리 제조업 특화)
# 'OR'를 써서 여러 키워드를 한꺼번에 검색합니다.
keywords = {
    "한국": "(South Korea OR Samsung SDI OR LG Energy Solution OR SK On) AND (battery factory OR plant) AND (fire OR explosion OR accident OR chemical leak)",
    "미국": "(USA OR America) AND (battery plant OR gigafactory) AND (fire OR explosion OR injury OR toxic)",
    "중국": "(China OR CATL OR BYD) AND (battery factory OR manufacturing) AND (fire OR blast OR accident)"
}

selected_country = st.sidebar.selectbox("대상 국가 선택", ["한국", "미국", "중국"])
news_count = st.sidebar.slider("수집 개수", 5, 30, 10)

def get_battery_safety_news(country, count):
    query = keywords[country]
    # 뉴스 수집 (배터리 산업에 집중하기 위해 최신순 정렬)
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    translator = GoogleTranslator(source='en', target='ko')
    
    try:
        response = requests.get(url)
        root = ET.fromstring(response.text)
        news_list = []
        
        for item in root.findall('.//item')[:count]:
            eng_title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            
            # 🇺🇸 -> 🇰🇷 번역
            kor_title = translator.translate(eng_title)
            
            news_list.append({
                "발생일": pub_date,
                "사고 소식": kor_title,
                "원문 링크": link
            })
        return news_list
    except:
        return []

# 2. 실행 버튼
if st.button(f"🚀 {selected_country} 배터리 사고 데이터 업데이트"):
    with st.spinner(f'{selected_country}의 데이터를 분석 중입니다...'):
        data = get_battery_safety_news(selected_country, news_count)
        
        if data:
            df = pd.DataFrame(data)
            st.success(f"최신 {len(data)}건의 소식을 가져왔습니다.")
            
            # 표로 보여주기
            st.dataframe(df, use_container_width=True)
            
            # 카드 형태로 상세 보기
            for res in data:
                with st.expander(res['사고 소식']):
                    st.write(f"📅 날짜: {res['발생일']}")
                    st.markdown(f"[🔗 기사 원문 확인하기]({res['원문 링크']})")
        else:
            st.error("관련 소식을 찾지 못했습니다. 키워드를 조정해보세요.")