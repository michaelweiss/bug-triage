import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from pyvis.network import Network

# model

@st.cache()
def load_commits():
	commits = pd.read_csv("data/commits.csv")
	commits = commits[["source", "target", "weight", "start_date", "end_date", "year"]]
	return commits

def bipartite_graph(commits):
	graph = Network("600px", "100%", notebook=True, heading='')
	contributors = set(commits["source"])
	bug_types = set(commits["target"])
	id = 1
	for contributor in contributors:
		graph.add_node(id, label=contributor, color="#00ee00")
		id = id + 1
	for bug_type in bug_types:
		graph.add_node(id, label=bug_type, color="#ee0000", shape="square")
		id = id + 1
	return graph

	# for i in range(commits):
	# 	graph.add_node(i, label=keywords[i], size=4*10*math.sqrt(total_topic_weights[i]),
	# 		title="Topic {}".format(i))
	# edge = np.zeros((number_of_topics, number_of_topics))
	# for topic_weights in dtm:
	# 	topics = [k for k in range(number_of_topics) if topic_weights[k] >= min_weight]
	# 	for i, j in list(itertools.combinations(topics, 2)):
	# 		edge[i, j] = edge[i, j] + 1
	# for i in range(number_of_topics):
	# 	for j in range(number_of_topics):
	# 		if edge[i, j] >= min_edges:
	# 			graph.add_edge(i, j, value=edge[i, j], smooth=smooth_edges)
	# return graph

# view

def show_commits():
	st.title("Commits")
	commits = load_commits()
	st.dataframe(commits)

def show_bipartite_graph():
	st.title("Contributors-Bug type graph")
	commits = load_commits()
	graph = bipartite_graph(commits)
	graph.show("contributor-bug-type.html")
	with st.beta_container():
		components.html(open("contributor-bug-type.html", 'r', encoding='utf-8').read(), height=625)

# controller

st.sidebar.title("Bug triage")

show_commits()
show_bipartite_graph()


