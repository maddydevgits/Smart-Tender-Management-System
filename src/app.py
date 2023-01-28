from flask import Flask,render_template,request,redirect,session
import json
from web3 import Web3,HTTPProvider
import zeptoemail as z
import time

register_contract_address='0x9dcD0B1e944d405E0e4b50Ad93E5A3FDD72C9A1E'
tender_contract_address=''

######## To connect with Register Contract in Blockchain
def connect_blockchain_register(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/register.json'
    contract_address=register_contract_address
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

######## To connect with Tender Contract in Blockchain
def connect_blockchain_tender(wallet):
    blockchain='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchain))
    if wallet==0:
        wallet=web3.eth.accounts[0]
    web3.eth.defaultAccount=wallet
    artifact_path='../build/contracts/tender.json'
    contract_address=tender_contract_address
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)

app=Flask(__name__)
app.secret_key="sacetb8"

@app.route('/')
def homepage():
    return render_template('Home.html')

@app.route('/description')
def descriptionpage():
    return render_template('description.html')

@app.route('/head')
def headpage():
    return render_template('Head.html')

@app.route('/loginbidder')
def loginbidderpage():
    return render_template('loginbidder.html')

@app.route('/logintender')
def logintenderpage():
    return render_template('logintender.html')

@app.route('/registrationbidder')
def registrationbidderpage():
    return render_template('registrationbidder.html')

@app.route('/registrationtender')
def registrationtenderpage():
    return render_template('registrationtender.html')

@app.route('/tenderloginsuccess')
def tenderloginsuccesspage():
    return render_template('Tenderloginsuccess.html')

@app.route('/bidderloginsuccess')
def bidderloginsuccesspage():
    return render_template('Bidderloginsuccess.html')

@app.route('/createtender')
def createtenderpage():
    return render_template('Createtender.html')

@app.route('/createbid')
def createbidpage():
    return render_template('Createbid.html')

@app.route('/viewtenders1')
def viewtenders1page():
    contract,web3=connect_blockchain_register(0)
    _usernames,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_tender(0)
    _tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders=contract.functions.viewtenders().call()

    data=[]
    for i in range(len(_tenderowners)):
        if _tenderstates[i]==True:
            dummy=[]
            dummy.append(_tenderids[i])
            dummy.append(_tenderowners[i])
            dummy.append(_tenderinfos[i])
            data.append(dummy)
    return render_template('Viewtenders1.html',dashboard_data=data,l=len(data))

@app.route('/viewtenders')
def viewtenderspage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_tender(0)
    _tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders=contract.functions.viewtenders().call()
    
    data=[]
    for i in range(len(_tenderowners)):
        if session['username']==_tenderowners[i]:
            dummy=[]
            dummy.append(_tenderids[i])
            dummy.append(_tenderinfos[i])
            if(_tenderstates[i]==True):
                dummy.append('Tender Open')
            else:
                dummy.append('Tender Close')
            if _tenderbidders[i]==session['username']:
                dummy.append('Tender Not Closed')
            else:
                dummy.append(_tenderbidders[i])
            data.append(dummy)

    return render_template('Viewtenders.html',dashboard_data=data,l=len(data))

@app.route('/viewbids1')
def viewbids1page():
    contract,web3=connect_blockchain_register(0)
    _usernames,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_tender(0)
    _bidtenderids,_bidamounts,_bidemails,_bidders=contract.functions.viewbids().call()
    _tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders=contract.functions.viewtenders().call()

    data=[]
    for i in range(len(_bidtenderids)):
        if _bidders[i]==session['username']:
            dummy=[]
            dummy.append(_bidtenderids[i])
            dummy.append(_bidamounts[i])
            k=_bidtenderids[i]
            kindex=_tenderids.index(k)
            if(_tenderstates[kindex]==True):
                dummy.append('Tender is Still Open')
            else:
                dummy.append('Tender Closed')
            if(_tenderstates[kindex]==True):
                dummy.append('InProgress')
            else:
                if _tenderbidders[kindex]==session['username']:
                    dummy.append('You won the Tender')
                else:
                    dummy.append('You have lost')
            data.append(dummy)

    return render_template('viewbids1.html',dashboard_data=data,l=len(data))

@app.route('/viewbids')
def viewbidspage():
    contract,web3=connect_blockchain_register(0)
    _usernames,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_tender(0)
    _bidtenderids,_bidamounts,_bidemails,_bidders=contract.functions.viewbids().call()
    _tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders=contract.functions.viewtenders().call()

    data=[]
    for i in range(len(_bidtenderids)):
        k=_bidtenderids[i]
        kindex=_tenderids.index(k)
        kowner=_tenderowners[kindex]
        if kowner==session['username']:
            dummy=[]
            dummy.append(_bidtenderids[i])
            dummy.append(_bidamounts[i])
            dummy.append(_bidemails[i])
            dummy.append(_bidders[i])
            data.append(dummy)

    return render_template('Viewbids.html',dashboard_data=data,l=len(data))

@app.route('/logout')
def logoutpage():
    session['username']=None
    return redirect('/')

@app.route('/tender/<id>')
def finalbid(id):
    tenderid=int(id)
    contract,web3=connect_blockchain_register(0)
    _usernames,_passwords=contract.functions.viewusers().call()
    contract,web3=connect_blockchain_tender(0)
    _tenderowners,_tenderids,_tenderinfos,_tenderstates,_tenderbidders=contract.functions.viewtenders().call()
    _bidtenderids,_bidamounts,_bidemails,_bidders=contract.functions.viewbids().call()

    kbidamounts=[]
    kbidders=[]
    kbidemails=[]
    for i in range(0,len(_bidtenderids)):
        if _bidtenderids[i]==tenderid:
            kbidamounts.append(_bidamounts[i])
            kbidders.append(_bidders[i])
            kbidemails.append(_bidemails[i])
    
    minamount=min(kbidamounts)
    minindex=kbidamounts.index(minamount)
    minbidder=kbidders[minindex]
    minemail=kbidemails[minindex]

    tx_hash=contract.functions.allocatetender(int(tenderid),minbidder).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    while True:
        try:
            a=z.sendEmail('Your bid is Finalized',minemail)
            if a:
                break
            else:
                continue
        except:
            time.sleep(10)
    return redirect('/viewtenders')

@app.route('/registerbidder',methods=['POST'])
def registerbidder():
    username=request.form['username']
    password=request.form['password']
    email=request.form['email']
    print(username,password,email)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registerbiduser(username,int(password),email).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/loginbidder')

@app.route('/loginbidderform', methods=['POST'])
def loginbidderform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginbiduser(username,int(password)).call()
    if state==True:
        session['username']=username
        return(render_template('Bidderloginsuccess.html'))
    else:
        return(render_template('loginbidder.html',err='Invalid credentials'))

@app.route('/registertender',methods=['POST'])
def registertender():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    tx_hash=contract.functions.registeruser(username,int(password)).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/logintender')

@app.route('/logintenderform',methods=['POST'])
def logintenderform():
    username=request.form['username']
    password=request.form['password']
    print(username,password)
    contract,web3=connect_blockchain_register(0)
    state=contract.functions.loginuser(username,int(password)).call()
    if state==True:
        session['username']=username
        return(render_template('Tenderloginsuccess.html'))
    else:
        return(render_template('logintender.html',err='Invalid credentials'))

@app.route('/createtenderform',methods=['post'])
def createtenderform():
    tenderid=int(request.form['tenderid'])
    tenderowner=session['username']
    tenderinfo=request.form['tenderinfo']
    print(tenderid,tenderowner,tenderinfo)
    contract,web3=connect_blockchain_tender(0)
    tx_hash=contract.functions.createtender(tenderowner,tenderid,tenderinfo).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return (render_template('Createtender.html',res='Tender created'))

@app.route('/createbidform',methods=['post'])
def createbidform():
    tenderid=int(request.form['tenderid'])
    bidamount=int(request.form['bidamount'])
    bidemail=request.form['bidemail']
    print(tenderid,bidamount,bidemail)
    contract,web3=connect_blockchain_tender(session['username'])
    tx_hash=contract.functions.bidtender(tenderid,bidamount,bidemail).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return render_template('Createbid.html',res='Bid Sent')

if __name__=="__main__":
    app.run(debug=True)