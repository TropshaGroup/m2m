class Hypothesis:
    pass
class TrivialHypothesis:
    def __init__(self, substance, condition):
        self.substance = substance
        self.condition = condition    
    def __repr__(self):
        return f"hypothesis(substance:{self.substance}=>condition:{self.condition})"
        
        
