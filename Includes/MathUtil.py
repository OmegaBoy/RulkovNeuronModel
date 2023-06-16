class MathUtil:
    def __init__(self):
        import numpy as np
        import math
        self.np = np
        self.math = math

    def StdDev(self, signal):
        return self.np.std(signal)
    
    def Mean(self, signal):
        return self.np.mean(signal)