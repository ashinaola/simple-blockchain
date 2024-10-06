class merkle_tree:
    '''
    merkle tree node to hold block hash
    merkle tree:
        Node root
        int size
        string nonce


    '''
    class node:
        def __init__(self):
            self.key = 0
            self.value = ""
            self.hash_prev = ""
            self.tx_data = ""
            self.left = None
            self.right = None

        def node_tostring(self):
            return (f"Node key: {self.key} \n"
                    f"Node value: {self.value} \n"
                    f"Previous hash: {self.hash_prev} \n"
                    f"Transaction: {self.tx_data} \n")

    '''
    initiate merkle tree
    '''
    def __init__(self):
        self.node_root = None
        self.tree_size = 0
        self.nonce = ""
        self.path = []

    '''
    generate hash value for merkel tree node
    '''
    def generate_hash(self):
        pass

    '''
    insert a new node into the merkle tree
    '''
    def insert_node(self, new_node):
        pass

    '''
    to verify the addition of a new node to the tree
    before adding a new node
    '''
    def verify(self, node):
        pass

    
