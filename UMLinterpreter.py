# This class takes in a tokenized UML Classdiagram program and
# converts it into a tokenized Java program

class Interpreter:
    
    def run(self, tokenized_program):
        self.tokenized_program = tokenized_program
        self.java_program = []
        self.terminate = False
        self.ip = 0
        self.num_indents = 0
        self.class_list = []
        self.dict = {"Integer": "int", "String": "String", "Boolean": "boolean", "Double": "double"}
        while not self.terminate:
            self.process_line()
        return self.java_program
        

    def process_line(self):
        line = self.tokenized_program[self.ip]
        match (line[0]):
            case "@startuml":
                self.java_program.append(["class", line[1], "{"])
                self.class_list.append(line[1])
            case "@enduml":
                self.java_program.append(["}"])
                self.terminate = True
            case "class":
                self.java_program.append(["class", line[1], "{"])
                self.class_list.append(line[1])
                if "}" in line: # Case for empty class def (i.e. class Staff { })
                    self.java_program.append(["}"])
            case "}":
                self.java_program.append(["}"])
            case default:
                match (line[0][0]):
                    case "+":
                        self.java_program.append(["public", self.dict[line[1]], line[0][1:-1]+";"])
                    case "-":
                        self.java_program.append(["private", self.dict[line[1]], line[0][1:-1]+";"])
                    case "#":
                        self.java_program.append(["protected", self.dict[line[1]], line[0][1:-1]+";"])
                    case "~":
                        self.java_program.append([self.dict[line[1]], line[0][1:-1]+";"])
                    case default:
                        if "(" in line[0]: # function definition
                            self.parse_function(line)
                        elif line[0] in self.class_list: # Association definition
                            self.parse_association(line)
                        else: # default class member
                            self.java_program.append(["public", self.dict[line[1]], line[0][0:-1]+";"])
        self.advance_statement()
    
    def advance_statement(self):
        self.ip += 1
    
    # Format of functions in UML: func(arg1: Type, arg2: Type, ...)
    # In tokenized format: ["func(arg1:", "Type,", "arg2:", "Type)"]
    def parse_function(self, line):
        func_name = line[0][0:line[0].index("(")]
        line[0] = line[0].replace(func_name, "") # Remove func name from line
        if len(line) == 1:
            self.java_program.append(["public", "void", func_name, "()", "{}"])
        else:
            line_list = ["public", "void", func_name]
            token_list = []
            for word in line:
                token_list.append(word.strip("():,")) # Extract args and types into new list
            for i in range(0, len(token_list), 2):
                arg = token_list[i]
                arg_type = self.dict[token_list[i+1]]
                # Swap order of arg and type
                token_list[i] = arg_type 
                token_list[i+1] = arg + ", " if len(line) - i > 2 else arg
            token_list[0] = "(" + token_list[0]
            token_list[-1] = token_list[-1] + ")"
            line_list += token_list
            self.java_program.append(line_list + ["{}"])
    
    # Format of association in UML: Class1 "name1" --- "name2" Class2
    # In tokenized format: ["Class1", "'name1'", "---", "'name2'", "Class2"]
    def parse_association(self, line):
        source_class = line[0]
        target_class = line[-1]
        is_composition = line[2] == "*--"
        source_name = line[1].strip("\"")
        target_name = line[3].strip("\"")
        ip_source = self.java_program.index(["class", source_class, "{"])
        ip_target = self.java_program.index(["class", target_class, "{"])
        terminate = False
        while not terminate:
            ip_source += 1
            if self.java_program[ip_source] == ["}"]: terminate = True 
        terminate = False
        while not terminate:
            ip_target += 1
            if self.java_program[ip_target] == ["}"]: terminate = True
        
        if is_composition:
            self.java_program.insert(ip_source, ["public", target_class, target_name, "//Composition"])
            self.java_program.insert(ip_target, ["public", source_class, source_name])
        else:
            self.java_program.insert(ip_source, ["public", target_class, target_name])
            self.java_program.insert(ip_target, ["public", source_class, source_name])
        