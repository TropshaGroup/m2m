import argparse
import json
import os
import sys
import requests
import numpy as np
import networkx as nx

#https://rosetta.renci.org/cop/Reslizumab/asthma/

class GraphChar:
   def __init__(self, graph, nodes):
      self.graph = graph
      self.nodes = nodes
      
class Model:

   def __init__(self):
      self.cops = [
         [ 'Reslizumab', 'asthma' ],
         [ 'Mepolizumab', 'asthma' ]
      ]
      self.every_id = "ids.json"
      self.ids = {}
      if os.path.exists (self.every_id):
         with open(self.every_id, "r") as stream:
            self.ids = json.loads(stream.read ())

   def get_uid(self, text):
      if not text in self.ids:
         self.ids[text] = len(self.ids)
      return self.ids[text]

   def close (self):
      with open(self.every_id, "w") as stream:
         self.ids = stream.write (json.dumps (self.ids, indent=2))

   def build_graph (self, source):
      graph = nx.MultiDiGraph()

      nodes = source['nodes'] #[:30]

      id2ident   = { n['id'] : n['identifier'] for n in nodes }
      ident2node = { n['identifier'] : n for n in nodes }
      id2node    = { n['id'] : ident2node[id2ident[n['id']]] for n in nodes }
      id2id      = { n['id'] : ident2node[id2ident[n['id']]]['id'] for n in nodes }

      for e in source['edges']:
         e['subj'] = id2id[e['subj']]
         e['obj']  = id2id[e['obj']]

      for n in ident2node.values ():
         graph.add_node (n['id'], attr_dict=n)
         
      for e in source['edges']:
         graph.add_edge (e['subj'],
                         e['obj'],
                         key=e['pred'],
                         attr_dict=e)
         
      return GraphChar(graph, id2node)

   def get_cops (self):
      for c in self.cops:
         drug, disease = c
         k = f"{drug}-{disease}.json"
         if not os.path.exists (k):
            response = requests.get (f"https://rosetta.renci.org/cop/{drug}/{disease}/").json ()
            query = f"https://rosetta.renci.org/cop/{drug}/{disease}/"
            print (f" query: {query} response: {response}")
            with open(k, 'w') as stream:
               stream.write (json.dumps (response, indent=2))
         else:
            with open(k, 'r') as stream:
               response = json.loads(stream.read ())
               
         graph_char = self.build_graph (response)
         eigencentrality = nx.eigenvector_centrality_numpy (nx.Graph(graph_char.graph))
         for k in eigencentrality:
            print (f" {k} -> {graph_char.nodes[k]} -> {eigencentrality[k]} -> {self.get_uid(graph_char.nodes[k]['identifier'])}")
         #print (f" {eigencentrality}")

         
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Clinical outcome pathway model builder.')
   parser.add_argument('-p', '--port', type=int, help='Port to run service on.', default=None)
   args = parser.parse_args ()

   model = Model ()
   model.get_cops ()
   model.close ()
