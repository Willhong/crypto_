import json
from web3 import Web3, exceptions

class EthereumWallet:
    def __init__(self, provider_url, contract_abi_file, contract_address):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.USDT_address = contract_address

        with open(contract_abi_file) as f:
            usdt_abi = json.load(f)

        self.USDT_ABI = usdt_abi
        self.usdt_contract = self.w3.eth.contract(address=self.USDT_address, abi=self.USDT_ABI)

    def is_connected(self):
        return self.w3.is_connected()

    def current_block(self):
        return self.w3.eth.block_number

    def get_ether_balance(self, address):
        balance = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance, "ether")

    def get_usdt_balance(self, address):
        address = Web3.to_checksum_address(address)
        return self.usdt_contract.functions.balanceOf(address).call()

    import json
from web3 import Web3, exceptions

class EthereumWallet:
    def __init__(self, provider_url, contract_abi_file, contract_address):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.USDT_address = contract_address

        with open(contract_abi_file) as f:
            usdt_abi = json.load(f)

        self.USDT_ABI = usdt_abi
        self.usdt_contract = self.w3.eth.contract(address=self.USDT_address, abi=self.USDT_ABI)

    def is_connected(self):
        return self.w3.is_connected()

    def current_block(self):
        return self.w3.eth.block_number

    def get_ether_balance(self, address):
        balance = self.w3.eth.get_balance(address)
        return self.w3.from_wei(balance, "ether")

    def get_usdt_balance(self, address):
        address = Web3.to_checksum_address(address)
        balance= self.usdt_contract.functions.balanceOf(address).call()
        return self.w3.from_wei(balance, "mwei")
    
    def send_ether(self, from_address, private_key, to_address, amount_in_ether):
        # Convert Ether amount to Wei
        amount_in_wei = self.w3.to_wei(amount_in_ether, 'ether')

        # Get the current gas price
        current_gas_price_wei = self.w3.eth.gas_price

        # Construct a transaction
        transaction = {
            'to': to_address,
            'value': amount_in_wei,
            'gas': 2000000,
            'gasPrice': current_gas_price_wei,  # Use the real-time gas price here
            'nonce': self.w3.eth.get_transaction_count(from_address),
            'chainId': 1  # 1 for mainnet, 3 for Ropsten, 4 for Rinkeby, etc.
        }

        # Sign the transaction
        signed_transaction = self.w3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction
        try:
            tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return tx_hash.hex()
        except exceptions.TransactionNotFound:
            return "Error: Transaction not found"




if __name__ == "__main__":
    wallet = EthereumWallet(
        provider_url="https://mainnet.infura.io/v3/c59975fd414e4c3298ecc67a8b951c65",
        contract_abi_file="usdt.json",
        contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7"
    )

    # Check connection
    if wallet.is_connected():
        print("Connected to Ethereum Mainnet")
    else:
        print("Not connected to Ethereum Mainnet")

    # Print current block
    print(f"Current block number: {wallet.current_block()}")

    # Get and print ether balance
    address = "주소입력"
    print(f"Balance of {address} is {wallet.get_ether_balance(address)} ether")

    # Get and print USDT balance
    print(f"Balance of {address} is {wallet.get_usdt_balance(address)} USDT")
