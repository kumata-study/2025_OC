import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
from sidebar_common import show_sidebar
import pandas as pd


st.set_page_config(page_title="最短経路問題（ランダム）")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

show_sidebar()

st.title("🟡 最短経路問題（ランダム）")
st.markdown("ノード数を入力して、ランダム生成されたグラフの最短経路を解いてみよう！")

# --- ノード数の設定（スライダーからテキスト入力へ変更） ---
num_nodes = st.number_input("ノード数（5〜26）を入力", min_value=5, max_value=26, value=6, step=1)

# --- セッション初期化 ---
if "random_graph" not in st.session_state:
    st.session_state.random_graph = None
    st.session_state.correct_length = None
    st.session_state.path = None
    st.session_state.graph_generated = False

if st.button("グラフを生成する") or not st.session_state.graph_generated:
    G = nx.Graph()
    nodes = [chr(65 + i) for i in range(num_nodes)]
    G.add_nodes_from(nodes)

    # 最小全域木で連結グラフを構成
    edges = []
    available = [nodes[0]]
    remaining = nodes[1:]
    while remaining:
        u = random.choice(available)
        v = remaining.pop(0)
        w = random.randint(5, 99)
        edges.append((u, v, w))
        available.append(v)

    # ランダムに追加の辺を加える
    extra_edges = random.randint(num_nodes // 2, num_nodes)
    for _ in range(extra_edges):
        u, v = random.sample(nodes, 2)
        if not G.has_edge(u, v):
            w = random.randint(5, 99)
            edges.append((u, v, w))

    G.add_weighted_edges_from(edges)

    st.session_state.random_graph = G
    st.session_state.graph_generated = True

# --- 表示部分 ---
if st.session_state.graph_generated:
    G = st.session_state.random_graph
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightyellow', edge_color='gray', ax=ax)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

    st.markdown("#### 出発点と到達点を選んでください")
    nodes = list(G.nodes)
    src = st.selectbox("出発点", nodes)
    tgt = st.selectbox("到達点", nodes, index=1 if len(nodes) > 1 else 0)

    if src != tgt:
        try:
            path = nx.shortest_path(G, source=src, target=tgt, weight="weight")
            length = nx.shortest_path_length(G, source=src, target=tgt, weight="weight")

            st.session_state.correct_length = length
            st.session_state.path = path

            st.markdown(f"#### 出発点:  {src}　→　到達点:  {tgt}")

            # 解答フォーム
            user_guess = st.number_input("最短経路の長さ（予想）", min_value=0, step=1)
            if st.button("解答する"):
                if user_guess == length:
                    st.success("正解です！🎉")
                else:
                    st.error(f"不正解です。正解は {length} です。")

                st.info(f"【最短経路】 {' → '.join(path)}")

                # 経路表示
                plt.figure(figsize=(6, 4))
                nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                path_edges = list(zip(path[:-1], path[1:]))
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
                st.pyplot(plt)

                st.markdown("---")
                if st.button("もう一度挑戦する"):
                    for k in list(st.session_state.keys()):
                        if k.startswith("random_") or k in ["correct_length", "path", "graph_generated"]:
                            del st.session_state[k]
                    st.rerun()
        except nx.NetworkXNoPath:
            st.error("選択されたノード間に経路がありません。他のノードを選んでください。")
    else:
        st.warning("出発点と到達点は異なるノードを選んでください。")

    # 辺と重みの一覧を表示
    edge_data = [(u, v, d['weight']) for u, v, d in G.edges(data=True)]
    df_edges = pd.DataFrame(edge_data, columns=["ノードA", "ノードB", "距離（重み）"])
    st.markdown("### グラフの辺と距離一覧")
    st.dataframe(df_edges)
