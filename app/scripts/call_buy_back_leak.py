import json
from web3 import Web3
from datetime import datetime

FILE = '/home/ConspiracyLabStudio1/secrets.json'

# Decentralized network
MAINNET = 'mainnet'
ROPSTEN = 'ropsten'

NETWORK_URLS = {
    ROPSTEN: 'https://ropsten.infura.io/v3/'
}

# Leak specifics
BOT_CONTRACT_ADDRESS = '0x89885d835741f6e3b53Ed9157084387342373835'
BOT_ABI_RAW = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"estimatedPrice","type":"uint256"}],"name":"debugger","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"senderAddress","type":"address"}],"name":"msgSenderChecker","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"num","type":"uint256"}],"name":"randomNumGenerated","type":"event"},{"inputs":[],"name":"attemptBuyBack","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"buyback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"ethAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"generateNextThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"isReady","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minBuyBack","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nextThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pairAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"previousRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenAddress_","type":"address"},{"internalType":"address","name":"pairAddress_","type":"address"}],"name":"registerToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"setAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"minThreshold","type":"uint256"},{"internalType":"uint256","name":"allowedDeviation","type":"uint256"}],"name":"setThresholdRange","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"isReady_","type":"bool"}],"name":"toggleReady","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"tokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"upperDiviation","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'


class CallBuyBackLeak:
    def __init__(self):
        contract_abi = json.loads(BOT_ABI_RAW)
        f = open(FILE)
        self.data = json.load(f)
        url = NETWORK_URLS[ROPSTEN] + self.data['infuraProjId']
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(BOT_CONTRACT_ADDRESS),
            abi=contract_abi
        )

    def run(self):
        wallet_address, wallet_private_key, wallet_mnemonic = self._get_wallet(self.data, 0)
        self.web3.eth.defaultAddress = wallet_address
        nounce = self.web3.eth.getTransactionCount(wallet_address)
        transaction = self.contract.functions.attemptBuyBack().buildTransaction(
            {'chainId': 3, 'gas': 1000000, 'nonce': nounce}
        )
        print('txn created')
        signed_txn = self.web3.eth.account.signTransaction(transaction, wallet_private_key)
        print('txn signed')
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print('txn hash: ' + txn_hash)

    def _get_wallet(self, data, index):
        wallet = data['accounts'][index]
        return wallet['address'], wallet['private_key'], wallet['mnemonic']

print('Buy back attempts started...')
caller = CallBuyBackLeak()
caller.run()
print('completed at ' + now.strftime("%m/%d/%Y, %H:%M:%S"))



