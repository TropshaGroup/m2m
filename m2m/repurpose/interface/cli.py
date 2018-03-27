from m2m.hypothesis import TrivialHypothesis

class CLIInterface:
    """ Stub for an interface generating repurposing hypotheses. """
    def __init__(self):
        self.hypotheses = [
            TrivialHypothesis ("imatinib", "asthma"),
            TrivialHypothesis ("aspirin", "asthma")
        ]
        self.last = 0
    def get_hypothesis(self):
        result = self.hypotheses [self.last]
        self.last = self.last + 1 % 2
        return result
