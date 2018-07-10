class Node:
    firstpos = None
    lastpos = None
    nullable = None

    def __init__(self, parent):
        self.parent = parent

    def create_subtree(self, nodestack):
        pass

    def isnullable(self):
        pass

    def findfirstpos(self):
        pass

    def findlastpos(self):
        pass


class ConcatNode(Node):
    def __init__(self, parent):
        super().__init__(parent)
        self.lchild = None
        self.rchild = None

    def create_subtree(self, nodestack):
        operand2 = nodestack.pop()
        operand1 = nodestack.pop()

        if isinstance(operand1, Node):
            self.lchild = operand1
            operand1.parent = self
        else:
            self.lchild = LeafNode(parent=self, string=operand1)

        if isinstance(operand2, Node):
            self.rchild = operand2
            operand2.parent = self
        else:
            self.rchild = LeafNode(parent=self, string=operand2)

    def __str__(self):
        return '[' + str(self.lchild) + '.' + str(self.rchild) + ']'

    def isnullable(self):
        a = self.lchild.isnullable()
        b = self.rchild.isnullable()
        self.nullable = a and b
        return self.nullable

    def findfirstpos(self):
        a = self.lchild.findfirstpos()
        b = self.rchild.findfirstpos()
        if self.lchild.nullable:
            self.firstpos = list(set(a + b))
        else:
            self.firstpos = a
        return self.firstpos

    def findlastpos(self):
        a=self.lchild.findlastpos()
        b=self.rchild.findlastpos()
        if self.rchild.nullable:
            self.lastpos = list(set( a+ b))
        else:
            self.lastpos = b
        return self.lastpos


class StarNode(Node):
    def __init__(self, parent):
        super().__init__(parent)
        self.child = None

    def create_subtree(self, nodestack):
        operand = nodestack.pop()
        if isinstance(operand, Node):
            self.child = operand
        else:
            self.child = LeafNode(parent=self, string=operand)

    def __str__(self):
        return '[ (' + str(self.child) + ') * ]'

    def isnullable(self):
        self.child.isnullable()
        self.nullable = True
        return True

    def findfirstpos(self):
        self.firstpos = self.child.findfirstpos()
        return self.firstpos

    def findlastpos(self):
        self.lastpos = self.child.findlastpos()
        return self.lastpos


class OrNode(Node):
    def __init__(self, parent):
        super().__init__(parent)
        self.lchild = None
        self.rchild = None

    def create_subtree(self, nodestack):
        operand2 = nodestack.pop()
        operand1 = nodestack.pop()

        if isinstance(operand1, Node):
            self.lchild = operand1
            operand1.parent = self
        else:
            self.lchild = LeafNode(parent=self, string=operand1)

        if isinstance(operand2, Node):
            self.rchild = operand2
            operand2.parent = self
        else:
            self.rchild = LeafNode(parent=self, string=operand2)

    def __str__(self):
        return '[' + str(self.lchild) + '|' + str(self.rchild) + ']'

    def isnullable(self):
        a = self.lchild.isnullable()
        b = self.rchild.isnullable()
        self.nullable = a or b
        return self.nullable

    def findfirstpos(self):
        self.firstpos = list(set(self.lchild.findfirstpos() + self.rchild.findfirstpos()))
        return self.firstpos

    def findlastpos(self):
        self.lastpos = list(set(self.lchild.findlastpos() + self.rchild.findlastpos()))
        return self.lastpos


class LeafNode(Node):
    num_of_instances = 0

    def __init__(self, parent, string):
        super().__init__(parent)
        self.string = string

        LeafNode.num_of_instances += 1
        self.number = LeafNode.num_of_instances

    def __str__(self):
        return '[' + self.string + ']'

    def isnullable(self):
        if self.string == 'e':  # lambda node
            self.nullable = True
            return True
        else:
            self.nullable = False
            return False

    def findfirstpos(self):
        if self.string == 'e':  # lambda node
            self.firstpos = []
            return self.firstpos
        else:
            self.firstpos = [self.number, ]
            return self.firstpos

    def findlastpos(self):
        if self.string == 'e':  # lambda node
            self.lastpos = []
            return self.lastpos
        else:
            self.lastpos = [self.number, ]
            return self.lastpos
