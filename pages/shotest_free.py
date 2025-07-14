import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from sidebar_common import show_sidebar 



st.set_page_config(page_title="最短経路問題（自作）")


st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)


show_sidebar()

st.title("🔵 最短経路問題（自作）")
st.markdown("ノードと辺を自由に追加して、自分だけのグラフを作ろう！")


# --- 初期化 ---
if "graph_sp" not in st.session_state:
    st.session_state.graph_sp = nx.Graph()
if "node_counter_sp" not in st.session_state:
    st.session_state.node_counter_sp = 0

G = st.session_state.graph_sp

# --- ノード追加 ---
if st.button("＋ ノードを追加"):
    if st.session_state.node_counter_sp < 26:
        node_name = chr(65 + st.session_state.node_counter_sp)
        if node_name not in G:
            G.add_node(node_name)
            st.session_state.node_counter_sp += 1
            st.success(f"ノード「{node_name}」を追加しました。")
        else:
            st.warning(f"ノード「{node_name}」はすでに存在しています。")
    else:
        st.error("Zまで追加済みです。これ以上のノードは追加できません。")

# --- 辺追加 ---
if len(G.nodes) >= 2:
    with st.form("add_edge_form_shortestfree"):
        col1, col2, col3 = st.columns(3)
        with col1:
            node1 = st.selectbox("始点ノード", list(G.nodes), key="shortestfree_e1")
        with col2:
            node2 = st.selectbox("終点ノード", list(G.nodes), key="shortestfree_e2")
        with col3:
            weight = st.number_input("距離（重み）", min_value=1.0, value=1.0, step=1.0, key="shortestfree_weight")
        submitted = st.form_submit_button("辺を追加")
        if submitted:
            G.add_edge(node1, node2, weight=weight)
            st.success(f"辺 {node1} ↔ {node2}（重み: {weight}）を追加しました。")

# --- グラフ描画 ---
if G.nodes:
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='gray', ax=ax)
    edge_labels = {(u, v): f"{d['weight']:.0f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

# --- 最短経路クイズ ---
if len(G.nodes) >= 2 and len(G.edges) > 0:
    quiz_answered_key = "shortestfree_quiz_answered"
    src_key = "shortestfree_quiz_src"
    tgt_key = "shortestfree_quiz_tgt"
    userlen_key = "shortestfree_quiz_userlen"

    if quiz_answered_key not in st.session_state:
        st.session_state[quiz_answered_key] = False

    with st.form("shortestfree_quiz_form"):
        col1, col2, col3 = st.columns([1, 1, 1.2])
        with col1:
            source = st.selectbox("出発点", list(G.nodes), key=src_key)
        with col2:
            target = st.selectbox("到達点", list(G.nodes), key=tgt_key)
        with col3:
            user_length = st.number_input("最短経路の長さ（予想）", min_value=0, step=1, key=userlen_key)
        submitted = st.form_submit_button("回答")
        if submitted:
            st.session_state[quiz_answered_key] = True
            st.session_state["shortestfree_result_src"] = source
            st.session_state["shortestfree_result_tgt"] = target

    if not st.session_state[quiz_answered_key]:
        st.info("出発点・到達点を選び、最短経路の長さを予想して入力し『回答』ボタンを押してください。")

    if st.session_state[quiz_answered_key]:
        source = st.session_state["shortestfree_result_src"]
        target = st.session_state["shortestfree_result_tgt"]
        user_length = st.session_state[userlen_key]
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

        # リセットボタン
        colA, spacer, colB = st.columns([1, 0.4, 1])
        with colA:
            if st.button("同じ問題で挑戦する"):
                for k in [quiz_answered_key, src_key, tgt_key, userlen_key, "shortestfree_result_src", "shortestfree_result_tgt"]:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()
        with colB:
            if st.button("問題を作り直す"):
                st.session_state.graph_sp = nx.Graph()
                st.session_state.node_counter_sp = 0
                for k in list(st.session_state.keys()):
                    if k.startswith("shortestfree_"):
                        del st.session_state[k]
                st.rerun()
