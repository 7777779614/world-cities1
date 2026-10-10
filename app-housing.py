import streamlit as st
import pandas as pd
import plotly.express as px

st.title("California Housing Data (1990) by 王镱舒")  # 页面主标题，已填入你的名字
value = st.slider("Minimal Median House Value", 0, 500001, 200000)  # 主页面滑块：范围0~500001，默认200000
df = pd.read_csv("housing.csv")  # 读取同目录下的 housing.csv
df = df[df["median_house_value"] >= value]  # 第一步筛选：只保留房价≥滑块值的区域
st.subheader("See more filters in the sidebar:")  # 副标题，提示用户去侧边栏
locations = ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"]  # 五种临海类型，必须和CSV里写的一致
chosen = st.sidebar.multiselect("Choose the location type", locations, default=locations)  # 侧边栏多选，默认全选
df = df[df["ocean_proximity"].isin(chosen)]  # 第二步筛选：只保留用户勾选的临海类型
income = st.sidebar.radio("Choose income level", ["Low", "Medium", "High"])  # 侧边栏单选按钮，三个收入档位
if income == "Low":  # 如果选 Low
    df = df[df["median_income"] <= 2.5]  # 筛选收入≤2.5（单位：万美元）
elif income == "Medium":  # 如果选 Medium
    df = df[(df["median_income"] > 2.5) & (df["median_income"] < 4.5)]  # 筛选 2.5 < 收入 < 4.5
else:  # 否则就是 High
    df = df[df["median_income"] >= 4.5]  # 筛选收入≥4.5
st.map(df)  # 在主页面用地图画筛选后的区域，自动取 latitude/longitude 列
fig = px.histogram(df, x="median_house_value", nbins=30)  # 用 plotly 画房价直方图，30个柱子
st.plotly_chart(fig)  # 把直方图渲染到页面上，放在地图下方
