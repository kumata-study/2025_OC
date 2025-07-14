import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from sidebar_common import show_sidebar 

st.set_page_config(page_title="最大流問題（自作）")

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

show_sidebar()

st.title("🔵 最大流問題（自作）")
st.markdown("ノードと容量付きの有向辺を追加して、自分だけのネットワークを作ってみよう！")

# --- 初期化 ---
if "digraph_mf" not in st.session_state:
    st.session_state.digraph_mf = nx.DiGraph()
if "node_counter_mf" not in st.session_state:
    st.session_state.node_counter_mf = 0  # A=0, B=1, ...

G = st.session_state.digraph_mf



# --- ノード追加 ---
if st.button("＋ ノードを追加"):
    if st.session_state.node_counter_mf < 26:
        node_name = chr(65 + st.session_state.node_counter_mf)
        if node_name not in G:
            G.add_node(node_name)
            st.session_state.node_counter_mf += 1
            st.success(f"ノード「{node_name}」を追加しました。")
        else:
            st.warning(f"ノード「{node_name}」はすでに存在しています。")
    else:
        st.error("Zまで追加済みです。これ以上のノードは追加できません。")

# --- 辺追加（容量指定） ---
if len(G.nodes) >= 2:
    with st.form("add_edge_form_mf"):
        col1, col2, col3 = st.columns(3)
        with col1:
            node1 = st.selectbox("始点ノード", list(G.nodes), key="maxflowfree_e1")
        with col2:
            node2 = st.selectbox("終点ノード", list(G.nodes), key="maxflowfree_e2")
        with col3:
            capacity = st.number_input("容量（flow capacity）", min_value=1, value=1, step=1, key="maxflowfree_cap")
        submitted = st.form_submit_button("有向辺を追加")
        if submitted:
            G.add_edge(node1, node2, capacity=capacity)
            st.success(f"辺 {node1} → {node2}（容量: {capacity}）を追加しました。")

# --- グラフ描画 ---
if G.nodes:
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, node_color='lightyellow', edge_color='gray', arrows=True)
    edge_labels = {(u, v): f"{d['capacity']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    st.pyplot(plt)


# --- 回答クイズ形式 ---
if len(G.nodes) >= 2 and len(G.edges) > 0:
    if "maxflow_quiz_answered" not in st.session_state:
        st.session_state.maxflow_quiz_answered = False

    with st.form("maxflow_quiz_form"):
        col1, col2, col3 = st.columns([1, 1, 1.2])
        with col1:
            source = st.selectbox("出発点", list(G.nodes), key="maxflowfree_src")
        with col2:
            target = st.selectbox("終点", list(G.nodes), key="maxflowfree_tgt")
        with col3:
            user_flow = st.number_input("最大流量（予想）", min_value=0, step=1, key="maxflowfree_user_flow")
        submitted = st.form_submit_button("回答")
        if submitted:
            st.session_state.maxflow_quiz_answered = True
            st.session_state.maxflowfree_source = source
            st.session_state.maxflowfree_target = target

    if not st.session_state.maxflow_quiz_answered:
        st.info("出発点・終点を選び、最大流量を予想して入力し『回答』ボタンを押してください。")

    if st.session_state.maxflow_quiz_answered:
        source = st.session_state.maxflowfree_source
        target = st.session_state.maxflowfree_target
        user_flow = st.session_state.maxflowfree_user_flow
        if source != target:
            try:
                flow_value, flow_dict = nx.maximum_flow(G, source, target, capacity="capacity")
                # 正誤判定
                if user_flow == flow_value:
                    st.success("正解です！🎉")
                else:
                    st.error(f"不正解です。 正解: {flow_value}")

                st.info(f"【最大流の流量】{flow_value}")

                # グラフ描画（最大流をラベルで表示）
                plt.figure(figsize=(6, 4))
                nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
                edge_labels = {(u, v): f"{flow_dict[u][v]}/{G[u][v]['capacity']}" for u, v in G.edges}
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                st.pyplot(plt)

            except nx.NetworkXError as e:
                st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("出発点と終点は異なるノードを選んでください。")

    st.markdown("###  ")
    st.markdown("---")  
    st.markdown(" ")    

    colA, spacer, colB = st.columns([1, 0.4, 1])

    with colA:
        if st.button("同じ問題で挑戦する"):
            for k in [
                "maxflowfree_src", "maxflowfree_tgt", "maxflowfree_user_flow",
                "maxflow_quiz_answered",  # 追加
                "maxflowfree_source", "maxflowfree_target"
            ]:
                if k in st.session_state:
                    del st.session_state[k]
            st.session_state.maxflow_quiz_answered = False   # ここでFalseに
            st.rerun()   # 強制再描画

    with colB:
        if st.button("問題を作り直す"):
            st.session_state.digraph_mf = nx.DiGraph()
            st.session_state.node_counter_mf = 0
            for k in list(st.session_state.keys()):
                if k.startswith("maxflowfree_"):
                    del st.session_state[k]
            st.info("ノード・辺が全てリセットされました。新たにグラフを作成してください。")

