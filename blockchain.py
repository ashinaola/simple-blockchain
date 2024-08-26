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
from uuid import uuid4

class blockchain(object):
    def __init__(self):
        self.blocks = []
        self.transactions = []
        # create the genesis block
        self.init_block(prev_hash=1, proof=100)

    '''
    function to initiate a new block and add to chain
    :param: <string>prev_hash, <int>proof
    :return: <dict>newly created block
    '''
    def init_block(self, prev_hash, proof):
        block = ({
            'index' : len(self.blocks) + 1,
            'timestamp' : time(),
            'transactions' : self.transactions,
            'proof' : proof,
            'prev_hash' : prev_hash,
        })
        #reset the transactions
        self.transactions = []
        self.blocks.append(block)
        return block

    '''
    function to create a new transaction and add to chain
    :param: <string>sender, <string>recepient, <double>amount
    :return: <int>index of block to hold the transaction
    '''
    def init_trans(self, sender, recepient, amount):
        self.transactions.append({
            'sender' : sender,
            'recepient' : recepient,
            'amount' : amount,
        })

        return self.get_last_block['index'] + 1

    '''
    turn block into json which will then be serialized into a hash
    :param: <dict>block
    :return: <string>hash
    '''
    @staticmethod
    def hash(block):
        block_hash = json.dumps(block, key=True)
        return hashlib.sha256(block_hash).hexdigest()

    # returns the last block on the chain
    @property
    def get_last_block(self):
        return self.blocks[len(self.blocks) - 1]

    '''
    function to implement proof of work
    find x s.t. the hash of x produces 4 leading 0s
    :param: <int>last_proof, 
    :return: <string>proof
    '''
    def proof_of_work(self, last_proof):
        proof = 0
        while not self.validate_pow(last_proof):
            proof += 1
        return proof

    '''
    function to validate the proof of work
    :param: <int>last_proof
    :return: <int>proof
    '''
    def validate_pow(self, last_proof):
        pass