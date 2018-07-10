from node import LeafNode,ConcatNode,OrNode,StarNode,Node


class SyntaxTree:

    def __init__(self, string):
        LeafNode.num_of_instances=0
        self.regex = self.add_concat(string) + '.#'
        print('regex= ',self.regex)
        self.root=self.convert_regex_to_syntaxtree()
        print('tree= ',str(self.root))

        # determines which node is nullable
        # starting from root to leaves
        # and saves the result in the 'nullable' attribute
        self.root.isnullable()

        # determines the firstpos  and lastpos of each node
        # starting from root to leaves
        # and saves the result in the 'firstpos' and 'lastpos' attribute
        self.root.findfirstpos()
        self.root.findlastpos()

        self.followpos=[]
        for i in range(0,LeafNode.num_of_instances):
            self.followpos.append(None)

        self.print_firstpos(self.root)


    def print_firstpos(self,node):
        if isinstance(node,ConcatNode):
            print('cat', node.firstpos,node.lastpos,node.nullable)
            self.print_firstpos(node.lchild)
            self.print_firstpos(node.rchild)

        elif isinstance(node,StarNode):
            print('star', node.firstpos,node.lastpos,node.nullable)
            self.print_firstpos(node.child)

        elif isinstance(node,OrNode):
            print('or',node.firstpos,node.lastpos,node.nullable)
            self.print_firstpos(node.lchild)
            self.print_firstpos(node.rchild)
        else:
            print(node.string,node.number,node.firstpos,node.lastpos,node.nullable)
            return



    def add_concat(self,string):
        opstack=[]
        nodestack=[]

        result=''

        #  consider a , b are characters in the Σ
        # and the set: {'(', ')', '*', '.', '|'} are the operators
        # then, if '.' is the concat symbol, we have to concatenate such expressions:
        # a . b
        # a . (
        # ) . a
        # * . a
        # * . (
        # ) . (
        for i in range(0,len(string)-1):
            result=result+string[i]
            if (string[i].isalpha() and string[i+1].isalpha()) or \
                    (string[i].isalpha() and string[i+1]=='(') or \
                    (string[i]==')' and string[i+1].isalpha()) or \
                    (string[i]=='*' and string[i+1].isalpha()) or \
                    (string[i]=='*' and string[i+1]=='(') or \
                    (string[i]==')' and string[i+1]=='('):
                result += '.'
        result = result + string[-1]
        return result


    def not_greater(self, i, j):
        prioriy = {'*': 3, '.':2 ,'|': 1}
        try:
            a = prioriy[i]
            b = prioriy[j]
            return True if a <= b else False
        except KeyError:
            return False

    def convert_regex_to_syntaxtree(self):
        nodestack = []
        opstack=[]

        for r in self.regex:
            if r.isalpha() or r=='#':
                nodestack.append(r)

            elif r == '(':
                opstack.append(r)
            elif r == ')':
                while len(opstack) != 0 and opstack[-1] != '(':
                    self.convert_substr_to_subtree(opstack,nodestack)
                opstack.pop() #pop the '('

            else:
                while len(opstack) != 0 and self.not_greater(r, opstack[-1]):
                    self.convert_substr_to_subtree(opstack,nodestack)
                opstack.append(r)

        while len(opstack) != 0:
            self.convert_substr_to_subtree(opstack,nodestack)

        root=nodestack.pop()
        return root



    def convert_substr_to_subtree(self,opstack,nodestack):
        op=opstack.pop()

        if op=='*':
            op=StarNode(parent=None)
        elif op=='.':
            op=ConcatNode(parent=None)
        elif op=='|':
            op=OrNode(parent=None)
        else:
            raise Exception('Unknown Operator!')

        op.create_subtree(nodestack)
        nodestack.append(op)

    def findfollowpos(self,node):

        # if n is a ‘.’ (concat) Node, with a left child C1 and
        # right child C2 and i is a position in the Lastpos(C1),
        # then all positions in Firstpos(C2) are in Followpos(i)
        if isinstance(node,ConcatNode):
            for i in node.lchild.lastpos:
                if self.followpos[i-1]:
                    self.followpos[i-1]= list(set(self.followpos[i-1]+node.rchild.firstpos))
                else:
                    self.followpos[i-1]=node.rchild.firstpos

            self.findfollowpos(node.lchild)
            self.findfollowpos(node.rchild)

        # if n is a * (closure) Node and i is a position in the
        # Lastpos(n), then all positions in Firstpos(n) are Followpos(i)
        elif isinstance(node,StarNode):
            for i in node.lastpos:
                if self.followpos[i-1]:
                    self.followpos[i-1]=list(set(self.followpos[i-1]+node.firstpos))
                else:
                    self.followpos[i-1]=node.firstpos
            self.findfollowpos(node.child)

        return



