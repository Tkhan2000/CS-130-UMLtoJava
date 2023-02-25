import os.path
from UMLinterpreter import Interpreter
from JavaCodeGenerator import JavaCodeGenerator

#-----------UMLtoJavaConverter-----------------
# This python script converts a .clasdiagram file
# to a .java file. Assumes no syntax errors.

# Get the current directory of the file
scriptdir = os.path.dirname(os.path.abspath(__file__))

# print("Enter name of the classdiagram file (i.e. UML.classdiagram): ")
# file_name = str(input())
file_name = "UML.classdiagram"
uml_file = open(os.path.join(scriptdir, './' + file_name))

# This function that converts text to list of strings, where index of 
# string is the line number, for example:
# [
#     ["@startuml", "Graph"]
#     ["@enduml"]
# ]
def tokenize_program():
    tokenized_program = []
    line_list = []
    for line in uml_file:
        line = remove_comment(line)
        line_list = line.split()
        if line_list: tokenized_program.append(line_list)
    return tokenized_program

def remove_comment(line):
    if "//" in line:
        return line[0:line.index("//")]
    return line

tokenized_program = tokenize_program()

uml_interpreter = Interpreter()
java_program = uml_interpreter.run(tokenized_program)

java_writer = JavaCodeGenerator()
java_writer.run(java_program, file_name[0:file_name.index(".")])
