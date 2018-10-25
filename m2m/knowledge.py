class KnowledgeMap:
    """ A map of knowledge sources able to generate a graph of entities and relations between them. """
    def __init__(self):
        pass
    def get_knowledge_graph(self, hypothesis):
        pass

class TrivialKnowledgeMap(KnowledgeMap):
    """ Return the hypothesis contents as the knowledge. A development stub. """
    def __init__(self):
        super(TrivialKnowledgeMap, self).__init__()
    def get_knowledge_graph(self, hypothesis):
        return [
            hypothesis.substance,
            hypothesis.condition
        ]
