import types


class VectorList(list):
    def get_vectors_by_interpreters(self, shells):
        vect=[]
        for v in self:
            if v.interpreter in shells:
                vect.append(v)
        return vect
    
    def get_vector_by_name(self, name):
        for v in self:
            if v.name == name:
                return v
    
    def order(self, names):
        sorted = [v for v in self for n in names if n == v.name]
        print sorted
    

class Vector:
    def __init__(self,interpreter, name, payloads = []):
        self.interpreter = interpreter
        self.name = name
        if isinstance(payloads, types.ListType):
            self.payloads = payloads
        elif isinstance (payloads, types.StringTypes):
            self.payloads = [payloads]
        else:
            print "[!] Error declaring attack vector"


    def __repr__(self):
        return '[%s, %s, %s]' % (self.name,self.interpreter,  self.payloads)

