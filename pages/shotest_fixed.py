import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib  # rcParams設定のため
import platform
from sidebar_common import show_sidebar

# --- Streamlit ページ設定 ---
st.set_page_config(page_title="最短経路問題（固定）")

# --- サイドバー非表示スタイル（任意）---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- サイドバー表示 ---
show_sidebar()

# --- フォント設定（OSごとに分岐） ---
try:
    if platform.system() == "Windows":
        font_path = "C:/Windows/Fonts/YuGothR.ttc"
    elif platform.system() == "Linux":
        # Streamlit Cloudではこのあたりが入ってることが多い
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    else:
        font_path = None

    if font_path:
        font_prop = fm.FontProperties(fname=font_path)
        matplotlib.rcParams['font.family'] = font_prop.get_name()
    else:
        matplotlib.rcParams['font.family'] = 'sans-serif'

except Exception as e:
    st.warning(f"フォント設定に失敗しました。fallbackフォントを使用します。\n\n詳細: {e}")
    matplotlib.rcParams['font.family'] = 'sans-serif'


# --- タイトル表示 ---
st.title("🟢 最短経路問題（例題）")
st.markdown("以下のグラフ上で、**最短経路**を見つけ、その長さ（重みの合計）を入力してください。")

# --- 固定グラフ定義 ---
G = nx.Graph()
edges = [
    ("出発地点", "仙北市", 15),
    ("仙北市", "秋田市", 75),
    ("仙北市", "大仙市", 40),
    ("秋田市", "大仙市", 56),
    ("大仙市", "湯沢市", 45),
    ("秋田市", "目的地", 42),
    ("大仙市", "目的地", 50),
    ("湯沢市", "目的地", 58)
]
G.add_weighted_edges_from(edges)
nodes = list(G.nodes)

# --- グラフ描画 ---
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 4))
nx.draw(
    G, pos, with_labels=True, node_color='lightblue', edge_color='gray',
    font_family=font_prop.get_name()
)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)},
    font_family=font_prop.get_name()
)
st.pyplot(plt)


# セッション初期化
if "shortest_answered" not in st.session_state:
    st.session_state.shortest_answered = False
if "shortest_src" not in st.session_state:
    st.session_state.shortest_src = nodes[0]
if "shortest_tgt" not in st.session_state:
    st.session_state.shortest_tgt = nodes[-1]
if "shortest_user_length" not in st.session_state:
    st.session_state.shortest_user_length = 0

with st.form("shortest_path_form"):
    col1, col2, col3 = st.columns([1, 1, 1.2])
    with col1:
        source = st.selectbox("出発点", nodes, key="shortest_src")
    with col2:
        target = st.selectbox("到達点", nodes, key="shortest_tgt")
    with col3:
        user_length = st.number_input(
            "最短経路の長さ（予想）",
            min_value=0,
            step=1,
            key="shortest_user_length"
        )
    submitted = st.form_submit_button("回答")
    if submitted:
        st.session_state.shortest_answered = True
        st.session_state.shortest_source = source
        st.session_state.shortest_target = target

if not st.session_state.shortest_answered:
    st.info("グラフを見て、最短経路の長さを計算し、入力してから『回答』ボタンを押してください。")

if st.session_state.shortest_answered:
    source = st.session_state.shortest_source
    target = st.session_state.shortest_target
    user_length = st.session_state.shortest_user_length
    if source != target:
        try:
            path = nx.shortest_path(G, source=source, target=target, weight="weight")
            length = nx.shortest_path_length(G, source=source, target=target, weight="weight")
            # 正誤判定
            if user_length == length:
                st.success("正解です！🎉")
            else:
                st.error(f"不正解です。 正解: {length}")

            st.info(f"【最短経路】{' → '.join(path)}")

            # グラフ描画（最短経路を赤で表示）
            plt.figure(figsize=(6, 4))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
            nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
            st.pyplot(plt)

        except nx.NetworkXNoPath:
            st.error("選択されたノード間に経路がありません。")
    else:
        st.warning("出発点と到達点は異なるノードを選んでください。")

    # リセットボタン（ページ手動リロード案内方式）
    if st.button("もう一度挑戦する"):
        for k in [
            "shortest_src", "shortest_tgt", "shortest_user_length", "shortest_answered",
            "shortest_source", "shortest_target"
        ]:
            if k in st.session_state:
                del st.session_state[k]
        st.warning("もう一度ボタンを押してください。")
