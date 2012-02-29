import ast

class Parameter:
    
    def __init__(self, arg, help='', required = False, pos=-1, default = None, choices = [], type = None, mutual_exclusion=[]):
        self.arg = arg
        self.help = help
        self.required = required
        self.default = default
        self.choices = choices
        self.type = type
        self.pos = pos
        self.mutual_exclusion = mutual_exclusion
        
        self.value = default
        
    def set_value(self, value):
        value = self.value
    
    
    def __repr__(self):
        
        choices = ''
        if self.choices:
            choices = '(%s)' % (', '.join(self.choices))
            
        type = ''
        if self.type:
            type = 'Type: %s' % repr(self.type.__name__)                    
            if isinstance(True, self.type):
                type += ' (True, False)'
            
            
        value = ''
        if self.value:
            value = str(self.value)
        
        exclusions = ''
        if self.mutual_exclusion:
            exclusions = '(Mutual exclusions: \'%s\')' % '\', \''.join(self.mutual_exclusion)
        
            
        tabs = '\t'*(3-((len(self.arg)+len(value) + 4)/8))
            
        return '%s = %s %s %s %s %s %s' % (self.arg, value, tabs, self.help, choices, type, exclusions)
        
class ParametersList:
    
    def __init__(self, module_description, vectors, *parameters):
        
        self.module_description = module_description
        self.parameters = list(parameters)
        self.vectors = vectors
        if vectors and len(vectors)>1:
            self.parameters.append(Parameter(arg='vector', help='Specify vector', choices = vectors.get_names_list()))
      
#        for param in self.parameters:
#            setattr(self, param.arg, param.default)
        
      
    def param_summary(self):
    
        output=''
        
        for parameter in self.parameters:
                
            if parameter.required:
                formatarg = '<%s%s%s>' 
            else:
                formatarg = '[%s%s%s]' 
                
            output += '%s ' % (formatarg % ( parameter.arg, '=', parameter.value))                
        
        return output
        
        
      
    def summary(self):
        
        output=''
        
        for parameter in self.parameters:
            
            # Skip printing vectors from summaries
            if parameter.arg == 'vector':
                continue
            
            if parameter.required:
                formatarg = '<%s%s>' 
            else:
                formatarg = '[%s%s]' 
                
            if parameter.pos != -1:
                output += '%s ' % (formatarg % ( parameter.arg, ''))
            else:
                output += '%s ' % (formatarg % ( parameter.arg, '='))                
        
        return output
    
    def help(self):
        
        output = ''
        for parameter in self.parameters:
            output += '\n%s' % (parameter)
        return output

    def __print_namepos(self,s):
        try: 
            int(s)
            return 'at position %s' % s
        except ValueError:
            return 'in parameter \'%s\'' % s
        
        
    def __repr__(self):
        
        return self.summary() + self.help()
        
        
    def set_and_check_parameters(self, args, oneshot = True):
        
        check=True
        
        oneshot_parameters = {}
        
        for namepos in args:
            param = self.__get_parameter(namepos)
            
            if param:
                value = args[namepos]
                
                if value:

                    if param.choices and (value not in param.choices):
                        print '[!] Error using \'%s\' %s. Options: \'%s\'' % (value, self.__print_namepos(namepos), '\', \''.join(param.choices))             
                        check=False
                    
                    if param.type:
                        try:
                            value = ast.literal_eval(value)
                        except ValueError:
                            print '[!] Error, parameter invalid type (%s)' % (repr(param.type))             
                            check=False
    
                        if not isinstance(value, param.type):
                            print '[!] Error, parameter invalid type (%s)' % (repr(param.type)) 
                            check=False
                        
                    if param.mutual_exclusion:
                        
                        for excluded in param.mutual_exclusion:
                            if self.get_parameter_value(excluded):
                                print '[!] Error, parameters \'%s\' and \'%s\' are mutually exclusive' % (param.arg, excluded) 
                                check=False
                
            else:
                print '[!] Error, invalid parameter %s' % (self.__print_namepos(namepos))  
                check=False
                
            if check:
                if not oneshot:
                    param.value = value    
                    #setattr(self, param.arg, param.value)
        
                oneshot_parameters[param.arg] = value
                
                
        if not check:
            print '[!] Usage: %s' % self.summary()
        
        return check, oneshot_parameters
                
                
                
    def __get_parameter(self, namepos):
        
        for par in self.parameters:
            if namepos == par.arg or namepos == par.pos:
                return par
        
        
    def get_parameter_value(self, namepos):
        
        par = self.__get_parameter(namepos)
        if par and par.value:
            return par.value
        return None

    def get_parameter_choices(self, namepos):
        
        par = self.__get_parameter(namepos)
        if par and par.choices:
            return par.choices
        return None


                
    def get_parameters_list(self, argdict):
        
        args_list =  []
        
        error_required = []
        
        for param in self.parameters:
            
            best_value = None
            
            oneshot_value = None
            if param.arg in argdict:
                oneshot_value = argdict[param.arg]
            
            perm_value = param.value
            
            if oneshot_value:
                best_value = oneshot_value
            elif perm_value:
                best_value = perm_value
            else:
                if param.required:
                   error_required.append(param.arg)
                   continue               
            
            if best_value != None:
                args_list.append(best_value)
            
        if error_required:
            print '[!] Error, required parameters: \'%s\'\n[!] Usage: %s' % ('\', \''.join(error_required), self.summary())
            return False, args_list
        
        return True, args_list
            
        
