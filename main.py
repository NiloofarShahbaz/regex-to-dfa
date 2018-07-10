from tree import SyntaxTree
from convert_to_dfa import ConvertToDfa


file=open('input.txt','r')

inputs=file.read()
inputs=inputs.split('\n')
print(inputs)

for input in inputs:
    regex=input
    tree=SyntaxTree(regex)
    tree.findfollowpos(tree.root)
    print(tree.followpos)
    converttree=ConvertToDfa(tree=tree)
    dfa=converttree.convert()
    outputfile=open('output.txt','a')
    converttree.write_in_file(outputfile)
