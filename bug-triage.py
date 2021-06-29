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

def bipartite_graph(commits, min_contribs, max_contribs, min_total_contribs):
	contribs = tally_contribs(commits)
	graph = Network("600px", "100%", notebook=True, heading='')
	id = 1
	reverse_node_index = {}

	# compute the subset of contributors and bug types within range
	contributors, bug_types = set(), set()
	for i, row in commits.iterrows():
		total_contribs = sum(contribs.loc[row["source"], :])
		if total_contribs >= min_total_contribs:
			if row["weight"] >= min_contribs: 
				if min_contribs > max_contribs or row["weight"] <= max_contribs:
					contributors.add(row["source"])
					bug_types.add(row["target"])

	# add nodes to the graph
	for contributor in contributors:
		total_contribs = sum(contribs.loc[contributor, :])
		size = 10 * (1 + math.log10(total_contribs/max(1, min_contribs)))
		graph.add_node(id, label=contributor, color="#00ee00", size=size, 
			title="{}".format(total_contribs))
		reverse_node_index[contributor] = id
		id = id + 1
	for bug_type in bug_types:
		graph.add_node(id, label=bug_type, color="#ee0000", shape="square", size=10)
		reverse_node_index[bug_type] = id
		id = id + 1

	# add edges to the graph
	for i, row in commits.iterrows():
		total_contribs = sum(contribs.loc[row["source"], :])
		if total_contribs >= min_total_contribs:
			if row["weight"] >= min_contribs: 
				if min_contribs > max_contribs or row["weight"] <= max_contribs:
					edge_width = 1 + math.log10(row["weight"])
					graph.add_edge(reverse_node_index[row["source"]], reverse_node_index[row["target"]],
						value=edge_width, title="{}".format(row["weight"]))
	return graph

def tally_contribs(commits):
	contribs = {}
	for i, row in commits.iterrows():
		contributor = row["source"]
		bug_type = row["target"]
		number_of_contribs = row["weight"]
		if contributor not in contribs:
			contribs[contributor] = {}
		contribs[contributor][bug_type] = number_of_contribs
	for contributor in contribs:
		row = [contribs[contributor][bug_type] if bug_type in contribs[contributor] else 0 
			for bug_type in bug_types(commits)]
		contribs[contributor] = row
	return pd.DataFrame.from_dict(contribs, orient="index", columns=bug_types(commits))

@st.cache()
def bug_types(commits):
	return sorted(list(set(commits["target"])))

# view

def show_commits():
	st.title("Commits")
	with st.beta_expander("More", expanded=False):
		commits = load_commits()
		st.dataframe(commits)

def show_bipartite_graph():
	st.title("Contributors-bug type graph")
	col1, col2, col3 = st.beta_columns(3)
	min_contribs = col1.number_input("Min contributions (bug type", 0)
	max_contribs = col2.number_input("Max contributions (bug type)", 0)
	min_total_contribs = col3.number_input("Min total contributions", 0)
	commits = load_commits()
	graph = bipartite_graph(commits, min_contribs, max_contribs, min_total_contribs)
	graph.show("contributor-bug-type.html")
	with st.beta_container():
		components.html(open("contributor-bug-type.html", 'r', encoding='utf-8').read(), height=625)

def show_tally_contribs():
	st.title("Tally contributions")
	with st.beta_expander("More", expanded=False):
		commits = load_commits()
		st.dataframe(tally_contribs(commits))

# controller

st.sidebar.title("Bug triage")

show_commits()
show_tally_contribs()
show_bipartite_graph()


