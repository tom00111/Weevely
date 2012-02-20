import ast

class Parameter:
    
    def __init__(self, arg, help='', required = False, pos=-1, default = None, choices = [], type = None, mutual_exclusion=[], oneshot = True, hidden = False):
        self.arg = arg
        self.help = help
        self.required = required
        self.default = default
        self.choices = choices
        self.type = type
        self.pos = pos
        self.mutual_exclusion = mutual_exclusion
        self.oneshot = oneshot
        self.hidden = hidden
        
        self.value = default
        
    def set_value(self, value):
        value = self.value

        
class ParametersList:
    
    def __init__(self, module_description, vectors_list, *parameters):
        
        self.module_description = module_description
        self.parameters = list(parameters)
        if vectors_list:
            self.parameters.append(Parameter(arg='vector', help='Force vector', choices = vectors_list, oneshot = False))
        
        
    def set_check_args(self, args):
        
        check=True
        
        
        for namepos in args:
            param = self.__get_parameter(namepos)
            
            if param:
                
                value = args[namepos]
                
                if param.choices and (value not in param.choices):
                    print '[!] Error, invalid choice \'%s\' for \'%s\'\n[!] Choose from \'%s\'' % (value, namepos, '\', \''.join(param.choices))             
                    check=False
                    continue
                
                if param.type:
                    try:
                        value = ast.literal_eval(value)
                    except ValueError:
                        print '[!] Error, parameter invalid type (%s)' % (repr(param.type))             
                        check=False
                        continue
                    if not isinstance(value, param.type):
                        print '[!] Error, parameter invalid type (%s)' % (repr(param.type)) 
                        check=False
                        continue
                    
                if param.mutual_exclusion:
                    
                    for excluded in param.mutual_exclusion:
                        p = self.__get_parameter(excluded)
                        if p.value != None:
                            print '[!] Error, parameter %s is mutually exclusive with %s' % (p.name, param.name) 
                            check=False
                            continue     
                    
                param.value = value
                
            else:
                print '[!] Error, invalid parameter %s' % (namepos)  
                check=False
        print args
                
        return check    
                
                
                
    def __get_parameter(self, namepos):
        
        for par in self.parameters:
            if namepos == par.arg or namepos == par.pos:
                return par
        
        
    def get_parameter_value(self, namepos):
        
        
        
        par = self.__get_parameter(namepos)
        
        if par and par.value:
            return par.value
        
        return None


    def clean(self):
        
        for param in self.parameters:
            if param.oneshot:
                if param.default:
                    param.value = param.default
                else:
                    param.value = None
                
                
    def get_check_args_list(self):
        
        check = True
        args_list =  []
        
        for param in self.parameters:
            if param.value == None:
                
                if param.required:
                    print '[!] Error, parameter %s required' % (param.arg)
                    check = False
                    continue
  
            if param.oneshot:
                args_list.append(param.value)
            else:
                setattr(self, param.arg, param.value)
        
        return check, args_list
            
        
