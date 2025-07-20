import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from sidebar_common import show_sidebar 




st.set_page_config(page_title="最短経路問題（固定）")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

show_sidebar()

st.title("🟢 最短経路問題（例題）")
st.markdown("以下のグラフ上で、**最短経路**を見つけ、その長さ（重みの合計）を入力してください。")

# 固定グラフの定義
G = nx.Graph()
edges = [
    ("Start", "Senboku", 15),
    ("Senboku","Akita",75),
    ("Senboku","Daisen",40),
    ("Akita","Daisen",56),
    ("Daisen","Yuzawa",45),
    ("Akita","Goal",42),
    ("Daisen","Goal",50),
    ("Yuzawa", "Goal", 58)
]
G.add_weighted_edges_from(edges)
nodes = list(G.nodes)

# グラフ全体を常に表示
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
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
    submitted = st.form_submit_button("解答")
    if submitted:
        st.session_state.shortest_answered = True
        st.session_state.shortest_source = source
        st.session_state.shortest_target = target

if not st.session_state.shortest_answered:
    st.info("グラフを見て、最短経路の長さを計算し、入力してから『解答』ボタンを押してください。")

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
