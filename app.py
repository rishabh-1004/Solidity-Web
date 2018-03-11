from flask import Flask , render_template
import requests
import json

address="0x92dc2a20693cdee59841e8a5f16007ecc3c8dcb3"
apikeytoken='2SRCB667VGR2MNZQ6U4SHAYUA7MB61ZA6P'
	


def getbalance(payload):
	r= requests.get("https://api-rinkeby.etherscan.io/api",params=payload).json()
	return r

def totalTransactions(payload):
	r=requests.get("https://api-rinkeby.etherscan.io/api",params=payload).json()
	return r

def getTransactions(payload):
	r=requests.get("https://api-rinkeby.etherscan.io/api",params=payload).json()
	return r

def getSingleTransaction(payload):
	r=requests.get("https://api-rinkeby.etherscan.io/api",params=payload).json()
	return r

def getgasPrice():
	r= requests.get("https://api-rinkeby.etherscan.io/api?module=proxy&action=eth_gasPrice&apikey=YourApiKeyToken")
	return r


app = Flask(__name__)

@app.route('/')
def index():
	
	balance_payload={"module":"account","action":"balance","address":address,'tag':'latest',"apikey":apikeytoken}
	balance= getbalance(balance_payload)
	tot_transaction_payload={'module':'proxy','action':'eth_getTransactionCount','address':address,'tag':'latest','apikey':apikeytoken}
	balance=balance['result']
	total_no_of_transactions = totalTransactions(tot_transaction_payload)
	total_no_of_transactions= total_no_of_transactions['result']
	transaction_payload={'module':'account','action':'txlist','address':address,'startblock':'0','endblock':'2702578','page':'1','offset':'10','sort':'asc','apikey':apikeytoken}
	transactions= getTransactions(transaction_payload)
	transactions = transactions['result']

	data={'balance':balance,'total_no_of_transactions':total_no_of_transactions,'transactions':transactions}
	return render_template('home.html',data=data)


@app.route('/transactions')
def transactions():
	balance_payload={"module":"account","action":"balance","address":address,'tag':'latest','apikey':apikeytoken}
	balance= getbalance(balance_payload)
	balance=balance['result']
	transaction_payload={'module':'account','action':'txlist','address':address,'startblock':'0','endblock':'99999999','sort':'asc','apikey':apikeytoken}
	transactions= getTransactions(transaction_payload)
	transactions = transactions['result']
	data={'balance':balance,'transactions':transactions}
	return render_template('transaction.html',data=data)

@app.route('/transactions/<string:id>/')
def transaction(id):
	
	transaction_payload={'module':'proxy','action':'eth_getTransactionByHash','txhash':id,'apikey':apikeytoken}
	transaction_details= getSingleTransaction(transaction_payload)
	transaction_details=transaction_details['result']
	return render_template('transaction_details.html',data=transaction_details)
	
@app.route('/test/')
def test():
	return render_template('test.html')
	

if __name__=='__main__':
	app.run(debug=True)
