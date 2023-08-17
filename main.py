from flask import Flask, render_template, request, jsonify
import crypto
app = Flask(__name__)

address=None
wallet = crypto.EthereumWallet(
    provider_url="https://mainnet.infura.io/v3/c59975fd414e4c3298ecc67a8b951c65",
    contract_abi_file="usdt.json",
    contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7"
)
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/store_address', methods=['POST'])
def store_address():
    global address
    address = request.json.get('address')
    # 여기서 주소를 처리하거나 저장
    print(f"Connected Ethereum address: {address}")
    #send message to client then redirect to index
    return jsonify({"message": "Connected to Ethereum Mainnet"})

#check metamask connection
@app.route('/check_connection', methods=['GET'])
def check_connection():
    global address
    if(address is not None):
        return jsonify({"message": "Connected to Ethereum Mainnet"})
    return jsonify({"message": "Not connected to Ethereum Mainnet"})

#get_ether_balance
@app.route('/get_ether_balance', methods=['POST'])
def get_ether_balance():
    global address
    if(address is not None):
        return jsonify({"balance": str(wallet.get_ether_balance(address))})
    return jsonify({"message": "Not connected to Ethereum Mainnet"})
if __name__ == '__main__':
    app.run(debug=True)
