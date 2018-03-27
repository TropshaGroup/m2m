class Evaluation:
    """ This is an abstractio of the result of a hypothesis evaluation.
    As we develop ideas of what constitutes a good evaluation, we should add these here."""
    def __init__(self, score):
        self.score = score

class TrivialEvaluation(Evaluation):
    def __init__(self, score):
        super(TrivialEvaluation,self).__init__(score)
    def __repr__(self):
        return f"eval(score={self.score})"
    
