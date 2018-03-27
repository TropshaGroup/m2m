from m2m.similarity.pmc import PMCW2VModel
from m2m.evaluation import TrivialEvaluation

class LiteratureSimilarityAlgorithm:
    """ An algorithm to evaluate a hypothesis based on literary sources.
    These might include word2vec, medline annotations, or other literature derived sources. """
    def __init__(self):
        """ For now we start with word2vec. """
        self.pmc_w2v = PMCW2VModel ()

    def evaluate(self, hypothesis):
        return TrivialEvaluation(self.pmc_w2v.get_similarity (term_a=hypothesis.substance,
                                                              term_b=hypothesis.condition))

