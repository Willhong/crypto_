from datetime import timedelta
from flask import Flask, redirect, render_template, request, jsonify, url_for, session
from flask_sqlalchemy import SQLAlchemy
import crypto
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key="i am a secret key"
db = SQLAlchemy(app) 

wallet = crypto.EthereumWallet(
    provider_url="https://mainnet.infura.io/v3/c59975fd414e4c3298ecc67a8b951c65",
    contract_abi_file="usdt.json",
    contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7"
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)



class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float)
    total = db.Column(db.Float)
    type = db.Column(db.String(50))  # 'cash_to_coin' or 'coin_to_cash'
    address_or_account = db.Column(db.String(255))
    

@app.cli.command("create-db")
def create_db():
    db.create_all()
    print("Database initialized!")



@app.route('/')
def index():
    if session.get('username'):
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard' ))

        else:

            return render_template('alert.html', message="Invalid username or password")
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout', methods=['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        user = User(username=username, password=password, email=email)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            return render_template('alert.html', message="Username or email already exists", url=url_for('register'))
        session['username'] = username

        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    #get transactions from db
    try:
        transactions = Transaction.query.filter_by(user_id=User.query.filter_by(username=username).first().id).all()
    except:
        session.pop('username', None)
        return render_template('alert.html', message="No transactions found", url=url_for('dashboard'))
    #change timezone to korea
    for transaction in transactions:
       transaction.created_at+=timedelta(hours=9)
       transaction.amount=round(transaction.amount,2)
       transaction.fee=round(transaction.fee,2)
       
    if request.method == 'POST':
        username = request.json.get('username')

    return render_template('dashboard.html',username=username,transactions=transactions)

@app.route('/exchange', methods=['POST'])
def exchange():
# user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
# amount = db.Column(db.Float, nullable=False)
# fee = db.Column(db.Float)
# total = db.Column(db.Float)
# type = db.Column(db.String(50))  # 'cash_to_coin' or 'coin_to_cash'
# address_or_account = db.Column(db.String(255))
    username = session.get('username')
    amount = request.form.get('amount')
    fee = float(amount) * 0.05 #5% 수수료
    total = float(amount) - fee
    type = request.form.get('exchangeType')
    address_or_account = request.form.get('coinAddress') if type=="cash_to_coin" else request.form.get('bankAccount')
    user = User.query.filter_by(username=username).first()
    transaction = Transaction(user_id=user.id, amount=amount, fee=fee, total=total, type=type, address_or_account=address_or_account)
    db.session.add(transaction)
    db.session.commit()
    
    return render_template('alert.html', message="요청이 완료되었습니다.", url=url_for('dashboard'))



@app.route('/admin')
def admin():
    return render_template('admin.html', users=User.query.all(), transactions=Transaction.query.all())

@app.route('/crypto')
def crypto():
    return render_template('index.html')

#get_ether_balance
@app.route('/get_ether_balance', methods=['POST'])
def get_ether_balance():
    address = request.json.get('address')
    if(address is not None):
        address=wallet.w3.to_checksum_address(address)
        return jsonify({"message": str(wallet.get_ether_balance(address))+" ether"})
    return jsonify({"message": "Not connected to Ethereum Mainnet"})
#get_tether_balance
@app.route('/get_tether_balance', methods=['POST'])
def get_tether_balance():
    address = request.json.get('address')
    if(address is not None):
        address=wallet.w3.to_checksum_address(address)
        return jsonify({"message": str(wallet.get_usdt_balance(address))+" USDT"})
    return jsonify({"message": "Not connected to Ethereum Mainnet"})
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
