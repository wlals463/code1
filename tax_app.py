import streamlit as st
import requests
from streamlit_folium import st_folium
import folium

# OpenWeatherMap API 키 설정
API_KEY = "YOUR_API_KEY_HERE"

st.title("🌦️ 지도에서 클릭해 날씨 보기")

# 기본 지도 설정 (한국 중심)
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 지도 표시 및 클릭 이벤트 처리
st.write("지도를 클릭하면 해당 위치의 날씨를 표시합니다.")
map_data = st_folium(m, width=700, height=500)

# 클릭 좌표 확인
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"선택된 위치: 위도 {lat:.4f}, 경도 {lon:.4f}")

    # 날씨 API 호출
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        st.subheader("현재 날씨 정보 🌤️")
        st.write(f"**도시:** {data['name']}")
        st.write(f"**날씨:** {data['weather'][0]['description']}")
        st.write(f"**온도:** {data['main']['temp']}°C")
        st.write(f"**습도:** {data['main']['humidity']}%")
        st.write(f"**풍속:** {data['wind']['speed']} m/s")
    else:
        st.error("날씨 데이터를 불러올 수 없습니다. (API Key 확인 필요)")
else:
    st.info("지도를 클릭해주세요.")
