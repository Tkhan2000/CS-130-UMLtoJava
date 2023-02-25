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
                        self.java_program.append(["public", line[1], line[0][1:-1]+";"])
                    case "-":
                        self.java_program.append(["private", line[1], line[0][1:-1]+";"])
                    case "#":
                        self.java_program.append(["protected", line[1], line[0][1:-1]+";"])
                    case "~":
                        self.java_program.append([line[1], line[0][1:-1]+";"])
                    case default:
                        if "(" in line[0]: # function definition
                            self.parse_function(line)
                        elif line[0] in self.class_list: # Composition definition
                            pass
                        else: # default class member
                            self.java_program.append(["public", line[1], line[0][0:-1]+";"])
        self.advance_statement()
    
    def advance_statement(self):
        self.ip += 1
    
    # Format of functions in UML: func(arg1: Type, arg2: Type, ...)
    # In tokenized format: ["func(arg1:", "Type,", "arg2", "Type)"]
    def parse_function(self, line):
        func_name = line[0][0:line[0].index("(")]
        line[0] = line[0].replace(func_name, "") # Remove func name from line
        if len(line) == 1:
            self.java_program.append(["public", "void", func_name, "()", "{}"])
        else:
            line_list = [["public", "void", func_name]]
            line_list.append(line)
            self.java_program.append(line_list)