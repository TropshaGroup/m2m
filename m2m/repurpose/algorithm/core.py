from m2m.repurpose.algorithm.literature import LiteratureSimilarityAlgorithm

class AlgorithmFactory:
    """ A central place for creating similarity algorithms supporting repurposing hypotheses. """
    def __init__(self):
        self.algorithms = {
            "literature_similarity" : LiteratureSimilarityAlgorithm ()
        }
    def get_algorithm(self, name):
        return self.algorithms[name]

