import streamlit as st

def show_sidebar():
    st.sidebar.title("🔗 メニュー")

    # ✅ Home に戻るリンク
    st.sidebar.page_link("Home.py", label="🏠 ホームに戻る")

    st.sidebar.markdown("## 🟢 例題")
    st.sidebar.page_link("pages/shotest_fixed.py", label="最短経路問題（例題）")
    st.sidebar.page_link("pages/maxflow_fixed.py", label="最大流問題（例題）")
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔵 実践編")
    st.sidebar.page_link("pages/shotest_free.py", label="最短経路問題（自作グラフ）")
    st.sidebar.page_link("pages/maxflow_free.py", label="最大流問題（自作グラフ）")