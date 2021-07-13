from app.constants import ROPSTEN, NETWORK_URLS, LEAK_CONTRACT_ADDRESS, LEAK_ABI_RAW, FILE
import json
from web3 import Web3

class CallBuyBackLeak:
    def __init__(self):
        contract_abi = json.loads(LEAK_ABI_RAW)
        f = open(FILE)
        self.data = json.load(f)
        url = NETWORK_URLS[ROPSTEN] + self.data['infuraProjId']
        self.web3 = Web3(Web3.HTTPProvider(url))
        self.contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(LEAK_CONTRACT_ADDRESS),
            abi=contract_abi
        )

    def run(self):
        wallet_address, wallet_private_key, wallet_mnemonic = self._get_wallet(self.data, 0)
        self.web3.eth.defaultAddress = wallet_address
        nounce = self.web3.eth.getTransactionCount(wallet_address)
        transaction = self.contract.functions.attemptBuyBack().buildTransaction(
            {'chainId': 3, 'gas': 1000000, 'nonce': nounce}
        )
        signed_txn = self.web3.eth.account.signTransaction(transaction, wallet_private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        print(txn_hash)

    def _get_wallet(self, data, index):
        wallet = data['accounts'][index]
        return wallet['address'], wallet['private_key'], wallet['mnemonic']

CallBuyBackLeak().run()