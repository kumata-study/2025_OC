import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
from sidebar_common import show_sidebar

st.set_page_config(page_title="最大流問題（ランダム）")

# --- スタイルとサイドバー表示 ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
show_sidebar()

st.title("🟡 最大流問題（ランダム）")
st.markdown("\u30ce\u30fc\u30c9\u6570\u3092\u5165\u529b\u3057\u3066\u3001\u30e9\u30f3\u30c0\u30e0\u751f\u6210\u3055\u308c\u305f **\u6709\u5411\u30b0\u30e9\u30d5** \u306e\u6700\u5927\u6d41\u91cf\u3092\u4e88\u60f3\u3057\u3066\u307f\u3088\u3046！")

# --- ノード数の設定 ---
num_nodes = st.number_input("ノード数（5〜12）を入力", min_value=5, max_value=12, value=6, step=1)

# --- セッション初期化 ---
if "random_digraph" not in st.session_state:
    st.session_state.random_digraph = None
    st.session_state.flow_value = None
    st.session_state.flow_dict = None
    st.session_state.source = None
    st.session_state.target = None
    st.session_state.graph_generated = False
    st.session_state.graph_message_shown = False

if st.button("グラフを生成する"):
    nodes = [chr(65 + i) for i in range(num_nodes)]
    UG = nx.Graph()
    UG.add_nodes_from(nodes)

    # 最小全域木で連結グラフを構成（無向）
    available = [nodes[0]]
    remaining = nodes[1:]
    while remaining:
        u = random.choice(available)
        v = remaining.pop(0)
        w = random.randint(5, 20)
        UG.add_edge(u, v, capacity=w)
        available.append(v)

    # ランダムに辺を追加
    extra_edges = random.randint(num_nodes // 2, num_nodes)
    for _ in range(extra_edges):
        u, v = random.sample(nodes, 2)
        if not UG.has_edge(u, v):
            w = random.randint(5, 20)
            UG.add_edge(u, v, capacity=w)

    # 無向グラフを有向グラフに変換（ランダムな向きに）
    DG = nx.DiGraph()
    for u, v, data in UG.edges(data=True):
        if random.random() < 0.5:
            DG.add_edge(u, v, capacity=data['capacity'])
        else:
            DG.add_edge(v, u, capacity=data['capacity'])

    st.session_state.random_digraph = DG
    st.session_state.graph_generated = True
    st.session_state.graph_message_shown = True
    st.rerun()


# --- メッセージ・グラフ表示（グラフ生成後は常に表示） ---
if st.session_state.graph_generated:
    DG = st.session_state.random_digraph
    nodes = list(DG.nodes)

    if st.session_state.graph_message_shown:
        st.success("グラフが生成されました！出発点と終点を選択してください。")

    source = st.selectbox("出発点（source）を選択", nodes, key="source_select")
    target = st.selectbox("終点（sink）を選択", nodes, key="target_select")

    # 🔽 終点選択の直後に表示されるように、ここに警告を入れる
    if source == target:
        st.warning("⚠️ 出発点と終点は異なるノードを選んでください。")
    elif not nx.has_path(DG, source, target):
        st.error("選択したノード間にパスが存在しません。他のノードを選んでください。")


    pos = nx.spring_layout(DG, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(DG, pos, with_labels=True, node_color='lightyellow', edge_color='gray', arrows=True, ax=ax)
    edge_labels = {(u, v): f"{d['capacity']}" for u, v, d in DG.edges(data=True)}
    nx.draw_networkx_edge_labels(DG, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

    edge_data = [(u, v, d['capacity']) for u, v, d in DG.edges(data=True)]
    df_edges = pd.DataFrame(edge_data, columns=["始点", "終点", "容量"])
    st.markdown("### グラフの辺と容量一覧")
    st.dataframe(df_edges)

    if source == target:
        pass
    elif not nx.has_path(DG, source, target):
        st.error("選択したノード間にパスが存在しません。他のノードを選んでください。")
    else:
        # 最大流計算
        flow_value, flow_dict = nx.maximum_flow(DG, source, target, capacity="capacity")
        st.session_state.flow_value = flow_value
        st.session_state.flow_dict = flow_dict
        st.session_state.source = source
        st.session_state.target = target

        st.markdown(f"#### 出発点: 🚩 {source}　→　終点: 🎯 {target}")

        # ✅ 🔼 ここに移動：最大流の予想と解答ボタン
        user_guess = st.number_input("最大流量の予想を入力", min_value=0, step=1)
        if st.button("解答する"):
            correct = st.session_state.flow_value
            if user_guess == correct:
                st.success("正解です！🎉")
            else:
                st.error(f"不正解です。正解は {correct} です。")

            st.info(f"【最大流の流量】{correct}")

            # グラフ再描画
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            nx.draw(DG, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True, ax=ax2)
            flow_labels = {(u, v): f"{flow_dict[u][v]}/{DG[u][v]['capacity']}" for u, v in DG.edges()}
            nx.draw_networkx_edge_labels(DG, pos, edge_labels=flow_labels, ax=ax2)
            st.pyplot(fig2)




        # ✅ 再挑戦ボタン（常に表示）
        if st.button("🔁 もう一度挑戦する"):
            for k in list(st.session_state.keys()):
                if k.startswith("random_") or k in ["flow_value", "flow_dict", "source", "target", "graph_generated", "graph_message_shown"]:
                    del st.session_state[k]
            st.rerun()


            # テーブル表示
            edge_data = [(u, v, d['capacity']) for u, v, d in DG.edges(data=True)]
            df_edges = pd.DataFrame(edge_data, columns=["始点", "終点", "容量"])
            st.markdown("### グラフの辺と容量一覧")
            st.dataframe(df_edges)
