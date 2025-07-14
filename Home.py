import streamlit as st

st.set_page_config(page_title="ネットワーク問題体験", layout="centered")

st.title("ネットワークの謎を解け！")
st.subheader("〜最短経路と最大流チャレンジ〜")

st.markdown("ようこそ！次の4つの問題に挑戦できます!")

st.markdown("### 🟢 例題")
st.page_link("pages/shotest_fixed.py", label="最短経路問題（例題）")
st.page_link("pages/maxflow_fixed.py", label="最大流問題（例題）")

st.markdown("### 🔵 実践編")
st.page_link("pages/shotest_free.py", label="最短経路問題（自作グラフ）")
st.page_link("pages/maxflow_free.py", label="最大流問題（自作グラフ）")

#st.info("ページ上部の「≡」アイコンからも各ページに移動できます。")

# --- サイドバーのデフォルト「ページリスト」を非表示にするCSS ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- サイドバー独自メニュー
st.sidebar.title("🔗 メニュー")
st.sidebar.markdown("## 🟢 例題")
st.sidebar.page_link("pages/shotest_fixed.py", label="最短経路問題（例題）")
st.sidebar.page_link("pages/maxflow_fixed.py", label="最大流問題（例題）")
st.sidebar.markdown("---")
st.sidebar.markdown("## 🔵 実践編")
st.sidebar.page_link("pages/shotest_free.py", label="最短経路問題（自作グラフ）")
st.sidebar.page_link("pages/maxflow_free.py", label="最大流問題（自作グラフ）")
