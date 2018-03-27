import argparse
from m2m.repurpose.algorithm.core import AlgorithmFactory
from m2m.repurpose.interface.core import InterfaceFactory
from m2m.knowledge import KnowledgeMap

class M2MApp:
    """ The application level instantiating and integrating interface and algorithm components. """

    def __init__(self):
        """ Configure the pieces. Should eventually be dynamically parameterized. """
        self.interface_factory = InterfaceFactory ()
        self.algorithm_factory = AlgorithmFactory ()
        self.knowledge_map = KnowledgeMap ()
        self.interface = self.interface_factory.get_interface (name="CLI")
        self.algorithm = self.algorithm_factory.get_algorithm ("literature_similarity")
        
    def evaluate_hypothesis(self, hypothesis=None):
        """ Run the configured components. """
        if not hypothesis:
            hypothesis = self.interface.get_hypothesis ()
        knowledge_graph = self.knowledge_map.get_knowledge_graph (hypothesis)
        evaluation = self.algorithm.evaluate (hypothesis)
        print (f"Hypothesis: {hypothesis} => Evaluation: {evaluation}")
        return evaluation
        
if __name__ == "__main__":
    """ Parse arguments and invoke the application. """
    parser = argparse.ArgumentParser(description='M2M Repurpsing App')
    parser.add_argument('-c', '--conf', help='Config file to use.', default=None)
    args = parser.parse_args ()

    m2m = M2MApp ()
    m2m.evaluate_hypothesis ()
   
