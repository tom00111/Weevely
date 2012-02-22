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
    
    
    def __repr__(self):
        
        choices = ''
        if self.choices:
            choices = '(%s)' % (', '.join(self.choices))
            
        value = ''
        if self.value:
            value = str(self.value)
            
        tabs = '\t'*(3-((len(self.arg)+len(value) + 4)/8))
            
        return '%s = %s %s %s %s' % (self.arg, value, tabs, self.help, choices)
        
class ParametersList:
    
    def __init__(self, module_description, vectors, *parameters):
        
        self.module_description = module_description
        self.parameters = list(parameters)
        self.vectors = vectors
        if vectors and len(vectors)>1:
            self.parameters.append(Parameter(arg='vector', help='Specify vector', choices = vectors.get_names_list(), oneshot = False))
        
    def __repr__(self):
        
        output=''
        
        for parameter in self.parameters:
            
            if parameter.required:
                formatarg = '<%s%s>' 
            else:
                formatarg = '[%s%s]' 
                
            if parameter.pos != -1:
                output += '%s ' % (formatarg % ( parameter.arg, ''))
            else:
                output += '%s ' % (formatarg % ( parameter.arg, '='))                
            
        output += '\n'
        for parameter in self.parameters:
            output += '\n%s' % (parameter)
        return output
        
        
    def set_check_args(self, args):
        
        check=True
        
        
        for namepos in args:
            param = self.__get_parameter(namepos)
            
            if param:
                print param
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
                        if self.get_parameter_value(excluded):
                            print '[!] Error, parameter \'%s\' and \'%s\' are mutually exclusive' % (param.arg, excluded) 
                            check=False
                            continue     
                    
                param.value = value
                
            else:
                print '[!] Error, invalid parameter %s' % (namepos)  
                check=False
                
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
            
        
