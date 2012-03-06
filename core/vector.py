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

    def get_names_list(self):
        
        return [v.name for v in self]

    def order(self, names):
        sorted = [v for v in self for n in names if n == v.name]
        print sorted
    
    def __repr__(self):
        for v in self:
            print v

class Vector:
    def __init__(self, interpreter, name, payloads):
        self.interpreter = interpreter
        self.name = name
        self.payloads = {}
        if isinstance(payloads, types.DictionaryType):
            self.payloads = payloads
        elif isinstance(payloads, types.ListType):
            pos = 0
            for p in payloads:
               self.payloads[pos] = p
               pos+=1
        elif isinstance (payloads, types.StringTypes):
            self.payloads[0] = payloads
        else:
            print "[!] Error declaring attack vector"

    def __repr__(self):
        return '[%s, %s, %s]' % (self.name,self.interpreter,  self.payloads)

