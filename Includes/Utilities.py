class Utilities:
    def ChangeParameter(par, self, parName):
        if par != None:
            setattr(self, parName, par)
        else:
            if hasattr(self, parName):
                value = getattr(self, parName)
                if value != None:
                    return value
                else:
                    raise Exception(parName + " esta vacio")    
            else:
                raise Exception(parName + " necesario")