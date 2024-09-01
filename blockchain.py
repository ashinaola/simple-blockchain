'''
Class to manage the blockchain
transactions:
    -
blocks:
    - index, timestamp, list of trans, proof, hash of prev block
'''

import hashlib
import json
from urllib.parse import urlparse
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.blocks = []
        self.transactions = []

        # ensures all address on the list is unique
        self.nodes = set()

        # create the genesis block
        self.init_block(prev_hash=1, proof=100)

    '''
    Adds a node to list of nodes so it has all nodes on network
    :param: <str> ip address of node
    '''
    def register_node(self, address):
        url_parsed = urlparse(address)
        
        if url_parsed.netloc:
            self.nodes.add(url_parsed.netloc)
        elif url_parsed.path:
            self.nodes.add(url_parsed.path)
        else:
            raise ValueError('URL invalid')

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
    def init_trans(self, sender, recipient, amount):
        self.transactions.append({
            'sender' : sender,
            'recepient' : recipient,
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
        block_hash = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_hash).hexdigest()

    # returns the last block on the chain
    @property
    def get_last_block(self):
        return self.blocks[-1]

    '''
    function to implement proof of work
    find x s.t. the hash of x produces 4 leading 0s
    :param: <int>last_proof, 
    :return: <string>proof
    '''
    def proof_of_work(self, last_proof):
        proof = 0

        while not self.validate_pow(last_proof, proof):
            proof += 1
        return proof

    '''
    function to validate the proof of work checks if the hash of the guess
    has 4 leading zeroes (adjust number of zeroes for harder algo)
    :param: <int>last_proof
    :return: <int>proof
    '''
    def validate_pow(self, proof, last_proof):
        guess = f"{proof}{last_proof}".encode()
        guess_hashd = hashlib.sha256(guess).hexdigest()
        return guess_hashd[:4] == "0000"
    
    '''
    Iterates down the chain to validate
    :param: <list>blocks 
    :return: <bool>valid chain := true, non-valid chain := false
    '''
    def validate_chain(self, blocks):
        # get last block and set index
        last_block = blocks[0]
        index = 1

        # iterate down chain
        while index < len(blocks):
            block = blocks[index]            
            print(f'previous block: {last_block}')
            print(f'current block: {block}')

            # check current block's hash is correct
            if block['prev_hash'] != self.hash(last_block):
                return False
            
            # check if p.o.w is correct
            if not self.validate_pow(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            index += 1

        return True
    
    '''
    Consensus algorithm which will replace the chain with the longest
    chain on the network
    :return: <bool> true if the chain was replace, false otherwise
    '''
    def conflict_resolution(self):
        # get neighboring nodes and initiate var for longest chain
        neighbors = self.nodes
        new_blocks = None

        # need the longest chain
        max_chain = len(self.blocks)

        # grab each node on list and compare to length of nodes
        for node in neighbors:
            response = request.get(f'{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_chain and self.validate_chain(chain):
                    max_chain = length
                    new_blocks = chain

        # replace chain with longer chain if found
        if new_blocks:
            self.blocks = new_blocks
            return True
        
        return False


# initiate node
app = Flask(__name__)

# generate unique address for the node
node_id = str(uuid4()).replace('-', '')

# Instantiate the blockchain
blockchain = Blockchain()

# define functions /transactions/new /mine /chain
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POSTd data
    required = ['recipient', 'sender', 'amount']
    if not all(x in values for x in required):
        return 'Missing values', 400

    # Create a new transaction and return response message
    index = blockchain.init_trans(values['sender'], values['recipient'], values['amount'])
    response = {'message' : f'Adding transaction to block {index}'}
    return response, 201


@app.route('/mine', methods=['GET'])
def mine():
    # run proof of work algo
    last_block = blockchain.get_last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # award the miner which completes the proof
    blockchain.init_trans (
        sender="0",
        recipient=node_id,
        amount=1,
    )

    # add the new block to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.init_block(proof, previous_hash)

    # build and return response
    response = {
        'message' : "New block added to chain",
        'index' : block['index'],
        'transaction' : block['transactions'],
        'proof' : block['proof'],
        'prev_hash' : block['prev_hash'],
    }
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain' : blockchain.blocks,
        'length' : len(blockchain.blocks)
    }
    return jsonify(response), 200

@app.route('nodes/register', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: No valid node list", 400
    
    for node in nodes:
        blockchain.register_node(node)
    
    response = {
        'message' : 'Chain replaced',
        'total_nodes' : list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    changed_block = blockchain.conflict_resolution()

    if changed_block:
        response = {
            'message' : 'Block resolved',
            'chain' : blockchain.blocks,
        }
    else:
        response = {
            'message' : 'Unchanged chain',
            'chain' : blockchain.blocks,
        }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)