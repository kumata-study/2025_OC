<<<<<<< HEAD
import streamlit as st
from sidebar_common import show_sidebar 

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="ネットワーク問題体験", layout="centered")

show_sidebar()   

st.title("ネットワークの謎を解け！")
st.subheader("〜最短経路と最大流チャレンジ〜")

st.markdown("ようこそ！次の4つの問題に挑戦できます!")

st.markdown("### 🟢 例題")
st.page_link("pages/shotest_fixed.py", label="最短経路問題（例題）")
st.page_link("pages/maxflow_fixed.py", label="最大流問題（例題）")

st.markdown("### 🔵 実践編")
st.page_link("pages/shotest_free.py", label="最短経路問題（自作グラフ）")
st.page_link("pages/maxflow_free.py", label="最大流問題（自作グラフ）")


=======
import streamlit as st
from sidebar_common import show_sidebar 

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)


st.set_page_config(page_title="ネットワーク問題体験", layout="centered")

show_sidebar()   

st.title("ネットワークの謎を解け！")
st.subheader("〜最短経路と最大流チャレンジ〜")

st.markdown("ようこそ！次の4つの問題に挑戦できます!")

st.markdown("### 🟢 例題")
st.page_link("pages/shotest_fixed.py", label="最短経路問題（例題）")
st.page_link("pages/maxflow_fixed.py", label="最大流問題（例題）")

st.markdown("### 🔵 実践編")
st.page_link("pages/shotest_free.py", label="最短経路問題（自作グラフ）")
st.page_link("pages/maxflow_free.py", label="最大流問題（自作グラフ）")


>>>>>>> a87eb96 (サイドバーの表示修正とリンク追加)
