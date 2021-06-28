import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import math
from pyvis.network import Network

# model

@st.cache()
def load_commits():
	commits = pd.read_csv("data/commits.csv")
	commits = commits[["source", "target", "weight", "start_date", "end_date", "year"]]
	return commits

def bipartite_graph(commits, min_contribs):
	graph = Network("600px", "100%", notebook=True, heading='')
	contributors = set(commits["source"])
	bug_types = set(commits["target"])
	id = 1
	reverse_node_index = {}
	for contributor in contributors:
		graph.add_node(id, label=contributor, color="#00ee00")
		reverse_node_index[contributor] = id
		id = id + 1
	for bug_type in bug_types:
		graph.add_node(id, label=bug_type, color="#ee0000", shape="square")
		reverse_node_index[bug_type] = id
		id = id + 1
	for i, row in commits.iterrows():
		# st.write(i, row["source"], row["target"])
		if row["weight"] > min_contribs:
			graph.add_edge(reverse_node_index[row["source"]], reverse_node_index[row["target"]],
				value=1 + math.log10(row["weight"]))
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
	st.title("Contributors-bug type graph")
	min_contribs = st.number_input("weight", 0)
	commits = load_commits()
	graph = bipartite_graph(commits, min_contribs)
	graph.show("contributor-bug-type.html")
	with st.beta_container():
		components.html(open("contributor-bug-type.html", 'r', encoding='utf-8').read(), height=625)

# controller

st.sidebar.title("Bug triage")

show_commits()
show_bipartite_graph()


