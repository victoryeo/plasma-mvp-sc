from plasma_core.block import Block
from plasma_core.chain import Chain
from plasma_core.utils.transactions import get_deposit_tx, encode_utxo_id
from .root_event_listener import RootEventListener
from plasma_core.constants import NULL_SIGNATURE
from plasma_core.constants import NULL_ADDRESS
from plasma_core.transaction import Transaction
from ethereum import utils
import pickle


class ChildChain(object):

    def __init__(self, operator, root_chain):
        self.operator = operator
        self.root_chain = root_chain
        self.chain = Chain(self.operator)
        self.current_block = Block(number=self.chain.next_child_block)
        print("self.current_block {0}".format(self.current_block.number))
        # Listen for events
        self.event_listener = RootEventListener(root_chain, confirmations=0)
        self.event_listener.on('Deposit', self.apply_deposit)
        self.event_listener.on('ExitStarted', self.apply_exit)
        self.event_listener.on('MsgSender', self.msgsender)
        self.event_listener.on('FinalState', self.finalstate)
        self.event_listener.on('forDebug01', self.debug01)

    def debug01(self, event):
        print("debug01 {0}".format(event['args']))

    def finalstate(self, event):
        print("finalstate {0}".format(event['args']))
        event_args = event['args']
        dmapping = event_args['dmapping']
        print("pickle {}".format(pickle.loads(dmapping)))

    def msgsender(self, event):
        print("msgsender {0}".format(event['args']))

    def apply_exit(self, event):
        print("exit started {0}".format(event['args']))
        event_args = event['args']
        utxo_id = event_args['utxoPos']
        blknum = utxo_id/1000000000
        print("blknum {0}".format(blknum))
        block = self.chain.get_block(blknum)
        print("Files {}".format(block.transaction_set[0].files))
        self.chain.mark_utxo_spent(utxo_id)

    def apply_deposit(self, event):
        print("apply deposit {0}".format(event['args']))
        event_args = event['args']
        owner = event_args['depositor']
        amount = event_args['amount']
        blknum = event_args['depositBlock']

        deposit_tx = get_deposit_tx(owner, amount)
        deposit_block = Block([deposit_tx], number=blknum)
        self.chain.add_block(deposit_block)

    def apply_transaction(self, tx):
        print("spent_utxos {0} {1}".format(self.current_block.spent_utxos, self.current_block.number))
        self.chain.validate_transaction(tx, self.current_block.spent_utxos)
        self.current_block.add_transaction(tx)
        return encode_utxo_id(self.current_block.number, len(self.current_block.transaction_set) - 1, 0)

    def submit_block(self, block):
        self.chain.add_block(block)
        self.root_chain.transact({
            'from': self.operator
        }).submitBlock(block.merkle.root)
        self.current_block = Block(number=self.chain.next_child_block)

    def get_transaction(self, tx_id):
        return self.chain.get_transaction(tx_id)

    def get_block(self, blknum):
        return self.chain.get_block(blknum)

    def get_current_block(self):
        print("current block")
        return self.current_block

    def get_current_block_num(self):
        print("current block num")
        return self.current_block.number

    def get_test(self):
        print("get test")
        return self.chain.get_test()

    def set_test(self, num):
        print("set test")
        print("Data type of argument:",type(num))
        blknum = self.chain.next_deposit_block
        file_block = Block(None, blknum, NULL_SIGNATURE)
        self.chain.add_block(file_block)
        print("Number {} {} {}".format(num, file_block.number, self.chain.next_deposit_block))
        tx = Transaction(blknum, 0, 0,
                0, 0, 0,
                utils.normalize_address(0x0),
                utils.normalize_address('0xfd02EcEE62797e75D86BCff1642EB0844afB28c7'), 1,
                utils.normalize_address(NULL_ADDRESS), 1,
                NULL_SIGNATURE,
                NULL_SIGNATURE,
                num)
        key1 = '3bb369fecdc16b93b99514d8ed9c2e87c5824cf4a6a98d2e8e91b7dd0c063304'
        print("Data type of key1:",type(key1))
        tx.sign1(utils.normalize_key(key1))
        self.current_block.add_transaction(tx)
        print("Added {}".format(self.current_block.transaction_set[0]))
        print("Added {}".format(self.current_block.transaction_set[0].files))
        self.chain.set_test(num)

    def set_dict(self, **num):
        print("set test")
        print("Data type of argument:",type(num))
        for key, value in num.items():
            print("{} is {}".format(key,value))
        #self.root_chain.deposit(transact={'from': owner, 'value': amount})
        mapping = {}
        mapping.update(num)
        for key, value in mapping.items():
            print("{} is {}".format(key,value))
        #convert dict to binary string
        bin_mapping = pickle.dumps(mapping)
        blknum = self.chain.next_deposit_block
        new_block = Block(None, blknum, NULL_SIGNATURE)
        new_block.add_mapping(mapping)
        self.chain.add_block(new_block)
        print("Number {} {}".format(new_block.number, self.chain.next_deposit_block))
        tx = Transaction(blknum, 0, 0,
                0, 0, 0,
                utils.normalize_address(0x0),
                utils.normalize_address('0xfd02EcEE62797e75D86BCff1642EB0844afB28c7'), 1,
                utils.normalize_address(NULL_ADDRESS), 1,
                NULL_SIGNATURE,
                NULL_SIGNATURE,
                0,
                bin_mapping)
        key1 = '3bb369fecdc16b93b99514d8ed9c2e87c5824cf4a6a98d2e8e91b7dd0c063304'
        print("Data type of key1:",type(key1))
        tx.sign1(utils.normalize_key(key1))
        self.current_block.add_transaction(tx)
        print("Added {}".format(self.current_block.transaction_set[0]))
        print("Added {}".format(self.current_block.transaction_set[0].mapping))
        self.chain.set_dict(**num)

    def hello(self):
        print("hello")
