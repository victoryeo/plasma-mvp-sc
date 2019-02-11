import requests
import rlp
from plasma.child_chain.child_chain import ChildChain
from plasma_core.transaction import Transaction
from plasma_core.block import Block
from .exceptions import ChildChainServiceError


class ChildChainService(object):

    def __init__(self, url):
        self.url = url
        #print("before call {0}".format(url))
        self.methods = [func for func in dir(ChildChain) if callable(getattr(ChildChain, func)) and not func.startswith("__")]
        #print("after call {0}".format(url))

    def send_request(self, method, args):
        payload = {
            "method": method,
            "params": args,
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(self.url, json=payload).json()
        if 'error' in response.keys():
            raise ChildChainServiceError(response["error"])

        return response["result"]

    def apply_transaction(self, transaction):
        return self.send_request("apply_transaction", [rlp.encode(transaction, Transaction).hex()])

    def submit_block(self, block):
        return self.send_request("submit_block", [rlp.encode(block, Block).hex()])

    def get_transaction(self, blknum, txindex):
        return self.send_request("get_transaction", [blknum, txindex])

    def get_current_block(self):
        return self.send_request("get_current_block", [])

    def get_block(self, blknum):
        return self.send_request("get_block", [blknum])

    def get_current_block_num(self):
        print("get_current_block_num")
        return self.send_request("get_current_block_num", [])

    def get_test(self):
        print("get_test")

    def set_test(self, num):
        print("set_test")
        return self.send_request("set_test", num)

    def set_dict(self, **num):
        print("set_dict")
        return self.send_request("set_dict", **num)

    def hello(self):
        print("hello")
        return self.send_request("hello", [])        
