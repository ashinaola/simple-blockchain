'''
Class to manage the blockchain
transactions:
    -
blocks:
    - index, timestamp, list of trans, proof, hash of prev block
'''

import hashlib
import json
from time import time

class blockchain(object):
    def __init__(self):
        self.blocks = []
        self.transactions = []
        # create the genesis block
        self.init_block(prev_hash=1, proof=100)

    # function to initiate a new block and add to chain
    def init_block(self, prev_hash, proof):
        pass

    '''
    function to create a new transaction and add to chain
    :param: <string>sender, <string>recepient, <double>amount
    :return: <int>index of block to hold the transaction
    '''
    def init_trans(self, sender, recepient, amount):
        self.transactions.append({
            'sender' : sender,
            'recepient' : recepient,
            'amount' : amount
        })

        return self.get_last_block['index'] + 1

    # hashes a block
    @staticmethod
    def hash(block):
        pass

    # returns the last block on the chain
    @property
    def get_last_block(self):
        pass