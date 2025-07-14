import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="最大流問題（固定）")

st.title("🟢 最大流問題（例題）")
st.markdown("以下の**有向グラフ**で、**出発点（source）から終点（sink）まで送れる最大の流量**を予想して入力し、「回答」ボタンを押してください。")

# 有向グラフ + 容量付き
G = nx.DiGraph()
edges = [
    ("S", "A", 10),
    ("S", "B", 5),
    ("A", "B", 15),
    ("A", "C", 9),
    ("B", "D", 8),
    ("B", "C", 5),
    ("C", "T", 10),
    ("D", "T", 10),
]
G.add_weighted_edges_from(edges, weight="capacity")
nodes = list(G.nodes)

# グラフ描画
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['capacity'] for u, v, d in G.edges(data=True)})
st.pyplot(plt)

# セッション管理
if "maxflow_answered" not in st.session_state:
    st.session_state.maxflow_answered = False

with st.form("maxflow_form"):
    col1, col2, col3 = st.columns([1, 1, 1.2])
    with col1:
        source = st.selectbox("出発点（source）", nodes, index=0, key="maxflow_src")
    with col2:
        target = st.selectbox("終点（sink）", nodes, index=len(nodes)-1, key="maxflow_tgt")
    with col3:
        user_flow = st.number_input("最大流量（予想）", min_value=0, step=1, key="maxflow_user_flow")
    submitted = st.form_submit_button("回答")
    if submitted:
        st.session_state.maxflow_answered = True
        st.session_state.maxflow_source = source
        st.session_state.maxflow_target = target

if not st.session_state.maxflow_answered:
    st.info("最大流量を予想して入力し、『回答』ボタンを押してください。")

if st.session_state.maxflow_answered:
    source = st.session_state.maxflow_source
    target = st.session_state.maxflow_target
    user_flow = st.session_state.maxflow_user_flow
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

    # リセットボタン（セッション変数を削除し、案内のみ）
    if st.button("もう一度挑戦する"):
        for k in [
            "maxflow_src", "maxflow_tgt", "maxflow_user_flow", "maxflow_answered",
            "maxflow_source", "maxflow_target"
        ]:
            if k in st.session_state:
                del st.session_state[k]
        st.warning("もう一度ボタンを押してください。")
