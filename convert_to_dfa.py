from node import LeafNode,StarNode

class State:
    def __init__(self,name,statenumber):
        self.name=name
        self.statenumber=statenumber
        self.Dtran={}

    def __str__(self):
        s= '<' + self.name + ' ,'+str(self.statenumber) + ' ,'
        for transition in self.Dtran:
            s=s+ 'Dtran(' + transition + ')='+ self.Dtran[transition].name
            s=s+'\t'
        s=s+ '>\n'
        return s



class ConvertToDfa:
    def __init__(self,tree):
        self.tree = tree
        self.followpos = tree.followpos
        self.initial_statenumber = tree.root.firstpos
        self.initial_state=None
        self.leaf_nodes={}

    def find_leaf_nodes(self,node):
        if isinstance(node,LeafNode):
            if node.string!='#' and node.string!='e':
                try:
                    self.leaf_nodes[node.string] += [node.number, ]
                except:
                    self.leaf_nodes[node.string]=[node.number,]
        elif isinstance(node,StarNode):
            self.find_leaf_nodes(node.child)
        else:
            self.find_leaf_nodes(node.lchild)
            self.find_leaf_nodes(node.rchild)

        return

    def convert(self):
        state_dic={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',
                   11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',
                   21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}

        self.find_leaf_nodes(self.tree.root)
        print(self.leaf_nodes)

        self.initial_state=State(name='A',statenumber=self.initial_statenumber)
        x=2

        left_states=[self.initial_state,]
        seen_states=[]
        while len(left_states)!=0:
            state=left_states.pop()
            if state not in seen_states:
                seen_states.append(state)
                print('state=', str(state))
                for string in self.leaf_nodes:
                    i=[elem for elem in state.statenumber if elem in self.leaf_nodes[string]]
                    print('str=',string,'i=',i)
                    if len(i)!=0:
                        next_statenumber = []

                        for item in list(i):
                            next_statenumber= list(set(next_statenumber+ self.followpos[item-1]))

                        for seen in seen_states:
                            if next_statenumber == seen.statenumber:
                                state.Dtran[string] = seen
                                print('tran=', string, str(seen))
                                break
                        else:
                            next_state=State(name=state_dic[x],statenumber=next_statenumber)
                            x=x+1
                            state.Dtran[string] = next_state
                            print('tran=', string, str(next_state))
                            left_states.append(next_state)


        return self.initial_state

    def write_in_file(self,file):
        left_states=[self.initial_state,]
        seen_states=[]

        while len(left_states)!=0:
            state=left_states.pop()
            if state not in seen_states:
                seen_states.append(state)
                file.write(str(state))
                for transition in state.Dtran:
                    next_state=state.Dtran[transition]
                    left_states.append(next_state)
        file.write('\n\n\n')




