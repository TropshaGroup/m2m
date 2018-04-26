import argparse
import json
import os
import requests
import numpy as np
from sklearn.manifold import TSNE
import networkx as nx
from flask import Flask, jsonify, g, Response
from flasgger import Swagger
app = Flask(__name__)

template = {
   "swagger": "2.0",
  "info": {
    "title": "M2M API",
    "description": "API",
    "contact": {
      "responsibleOrganization": "renci.org",
      "responsibleDeveloper": "scox@renci.org",
      "email": "scox@renci.org",
      "url": "www.renci.org",
    },
    "termsOfService": "http://renci.org/terms",
    "version": "0.0.1"
  },
  "schemes": [
    "http",
    "https"
  ]
}
app.config['SWAGGER'] = {
   'title': 'Rosetta Service',
   'bag_source' : '/.'
}

swagger = Swagger(app, template=template)

class Core:
   
   def get_tsne_shape(self):
      """ http://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html """
      X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
      X_embedded = TSNE(n_components=2).fit_transform(X)
      return X_embedded.shape
   
   def build_graph (self, source):
      graph = nx.MultiDiGraph()
      nodes = { n['id'] : n for n in source['nodes'] }
      for n in source['nodes']:
         graph.add_node (n['id'], attr_dict=n)
      for e in source['edges']:
         graph.add_edge (e['subj'],
                         e['obj'],
                         key=e['pred'],
                         attr_dict=e)
      print (f" num connected: {graph.to_undirected().number_connected_components ()}")
      return nx.eigenvector_centrality_numpy (nx.Graph(graph))
   
core = None
def get_core ():
   global core
   if not core:
      core = Core ()
   return core

@app.route('/tsne/<arg1>/<arg2>/', methods=['GET'])
def tsne (arg1="v1", arg2="v2"):
   """ Get service metadata 
   ---
   parameters:
     - name: arg1
       in: path
       type: string
       required: false
       default: v1
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /query?drug={{ input }}
     - name: arg2
       in: path
       type: string
       required: false
       default: v2
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /query?disease={{ input }}
   responses:
     200:
       description: ...
   """
   core = get_core ()
   shape = core.get_tsne_shape ()
   print (f"{shape}")
   return jsonify (shape)

@app.route('/graph/<drug>/<disease>/', methods=['GET'])
def graph (drug="imatinib", disease="asthma"):
   """ Get service metadata 
   ---
   parameters:
     - name: drug
       in: path
       type: string
       required: false
       default: imatinib
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /query?drug={{ input }}
     - name: disease
       in: path
       type: string
       required: false
       default: asthma
       x-valueType:
         - http://schema.org/string
       x-requestTemplate:
         - valueType: http://schema.org/string
           template: /query?disease={{ input }}
   responses:
     200:
       description: ...
   """
   response = requests.get (f"https://rosetta.renci.org/cop/{drug}/{disease}/").json ()
   core = get_core ()
   print (json.dumps (response['edges'][0], indent=2))
   print (json.dumps (response['nodes'][0], indent=2))
   laplacian_spectrum = core.build_graph (response)
   return jsonify (laplacian_spectrum)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Rosetta Server')
   parser.add_argument('-p', '--port', type=int, help='Port to run service on.', default=None)
   args = parser.parse_args ()
   app.run(host='0.0.0.0', port=args.port, debug=True, threaded=True)
