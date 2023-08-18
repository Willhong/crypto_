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
        return self.usdt_contract.functions.balanceOf(address).call()




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
