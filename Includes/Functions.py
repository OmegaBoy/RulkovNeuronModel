class Functions:
    def __init__(self, sym):
        self.sym = sym
    def Derivate(self,functions,variables):
        df = []
        for f in functions:
            for v in variables:
                df.append({"Function": f, "Variable": v, "Derivate": self.sym.diff(f,v)})
        return df