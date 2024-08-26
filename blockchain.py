class blockchain:
    def blockchain(self):
        self.blocks = []
        self.transactions = []

    # function to initiate a new block and add to chain
    def init_block(self):
        pass

    # function to create a new transaction and add to chain
    def init_trans(self):
        pass

    # hashes a block
    @staticmethod
    def hash(block):
        pass

    # returns the last block on the chain
    @property
    def get_last_block(self):
        pass