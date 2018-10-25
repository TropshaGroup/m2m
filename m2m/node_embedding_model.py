import json
import logging
import os
from ros.client import Client
from ros.csvargs import CSVArgs
from node2vec import Node2Vec
import networkx as nx

logger = logging.getLogger("node_embedding_model")
logger.setLevel(logging.DEBUG)

class NodeEmbeddingModelDriver:
    
    def __init__(self, workflow, libpath, parameter_set):
        self.args_list = CSVArgs (parameter_set)
        self.workflow = workflow 
        self.libpath = libpath
        logger.debug (f" created driver wf: {self.workflow} args: {self.args_list} libpath: {self.libpath}")
        
    def run (self):
        logger.debug ("running")
        
        """ Build graph. """
        g = nx.MultiDiGraph ()
        for args in self.args_list.vals:
            logger.debug (f"running workflow with args: {json.dumps(args,indent=2)}")
            ros = Client (url="http://localhost:5002")
            response = ros.run (workflow=self.workflow,
                                args = args,
                                library_path = self.libpath)
        
            print (json.dumps (response.result, indent=2))
            response_nx = response.to_nx ()
            print (f"read {len(response_nx.nodes())} nodes and {len(response_nx.edges())} edges.")
            g = nx.compose (g, response.to_nx ())

        """ Calulate node embeddings. """
        n2v = Node2Vec (g, dimensions=128, walk_length=80,
                        num_walks=10, p=1, q=1, weight_key='weight',
                        workers=1, sampling_strategy=None, quiet=False)
        return n2v.fit ()
    
if __name__ == "__main__":
    nemd = NodeEmbeddingModelDriver (
        workflow = os.path.join ('workflows', 'm2m_models_v1.ros'),
        libpath = "workflows",
        parameter_set = os.path.join ("workflows", "ros_m2m_wf1.csv"))
    nemd.run ()
