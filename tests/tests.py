'''
CBP Token tests
created by Delerex.com
(c) 2018 Delerex Pte Ltd
'''


import json
import sys
from web3 import Web3

#path to contract ABI. tested with Emabrk 3.10
contract_json_api_interface = "ComBoxToken.json"
decimals=4

def FloatToDecimal(value):
    return int(value * 10**decimals)

def DecimalToFloat(value):
    return float(  value / 10**decimals )


class Balances:
    def __init__(self, accounts):
        self.accounts = accounts
    def fetchbalances(self):
        self.balances = []
        for a in accounts:
            self.balances.append( ComBoxToken.functions.balanceOf(a).call() )

    def checkbalances(self, changesarray):
        for a in changesarray:
            if ComBoxToken.functions.balanceOf(self.accounts[a[0]]).call() != self.balances[a[0]] + a[1]:
                return False
        return True

    def checkfixedbalances(self, changesarray):
        for a in changesarray:
            if ComBoxToken.functions.balanceOf(self.accounts[a[0]]).call() != self.balances[a[0]]:
                return False
        return True


w3 = Web3( Web3.HTTPProvider("http://127.0.0.1:8545") )
print( w3.eth.accounts )


accounts = w3.eth.accounts
test_balances= Balances(accounts)


w3.eth.defaultAccount = w3.eth.accounts[0]

json_data=open(contract_json_api_interface).read()
contract_interface = json.loads(json_data)
ComBoxToken = w3.eth.contract(abi=contract_interface['abiDefinition'], address=contract_interface["deployedAddress"])

print( ComBoxToken.functions.totalSupply().call() )
print( ComBoxToken.functions.balanceOf(w3.eth.defaultAccount).call())

print("\nSimple transfer test account[0] account[1] #1")
try:
    test_amount = FloatToDecimal(45.5)
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.transfer(accounts[1], test_amount).transact()
    if test_balances.checkbalances([(0, -test_amount),(1, test_amount)]) == True:
        print("--Passed")
    else:
        print("--Failed")
except:
    print("------Failed")

print("\nSimple transfer test account[0] account[1] #2")
try:
    test_amount = FloatToDecimal(56.2345645)
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.transfer(accounts[1], test_amount).transact()
    if test_balances.checkbalances([(0, -test_amount), (1, test_amount)]) == True:
        print("--Passed")
    else:
        print("--Failed")
except:
    print("------Failed")

print("\nSimple approve/transferFrom test account[0] account[1] #2")

try:
    test_amount = FloatToDecimal(20)
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.approve(accounts[2], test_amount).transact()

    w3.eth.defaultAccount = w3.eth.accounts[1]
    try:
        tx_hash = ComBoxToken.functions.transferFrom(accounts[0], accounts[3], test_amount).transact()
    except:
        pass

    w3.eth.defaultAccount = w3.eth.accounts[2]
    try:
        tx_hash = ComBoxToken.functions.transferFrom(accounts[0], accounts[4], test_amount-1).transact()
    except:
        pass

    try:
        tx_hash = ComBoxToken.functions.transferFrom(accounts[0], accounts[4], 2).transact()
    except:
        pass

    if test_balances.checkbalances([(0, -test_amount+1), (3, 0), (4, test_amount-1)]) == True:
        print("--Passed")
    else:
        print("--Failed")

except:
    print("------Failed")


print("\nMassSend test account[0] account[5] account[6] account[7] #1")

try:
    w3.eth.defaultAccount = w3.eth.accounts[0]

    to_addr = [accounts[5], accounts[6], accounts[7] ]
    to_values = [FloatToDecimal(10), FloatToDecimal(20), FloatToDecimal(30)]
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.masssend(to_addr, to_values).transact()
    if test_balances.checkbalances([(0, -sum(to_values)), (5, to_values[0]), (6, to_values[1]), (7, to_values[2])]) == True:
        print("--Passed")
    else:
        print("--Failed")

except:
    print(sys.exc_info())
    print("------Failed")


print("\nMassSend test account[0] account[5] account[6] account[7] #2")

try:
    w3.eth.defaultAccount = w3.eth.accounts[0]

    to_addr = [accounts[5], accounts[6], accounts[7] ]
    to_values = [FloatToDecimal(10), FloatToDecimal(20), FloatToDecimal(30)]
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.masssend(to_addr, to_values).transact()
    if test_balances.checkbalances([(0, -sum(to_values)), (5, to_values[0]), (6, to_values[1]), (7, to_values[2])]) == True:
        print("--Passed")
    else:
        print("--Failed")

except:
    print(sys.exc_info())
    print("------Failed")


print("\nMassSend test account[5] account[6] account[7] account[8] #1")

try:
    w3.eth.defaultAccount = w3.eth.accounts[5]
    test_amount = FloatToDecimal(20)

    test_balances.fetchbalances()
    move_balance = ComBoxToken.functions.balanceOf(w3.eth.defaultAccount).call()
    if move_balance > 0:
        tx_hash = ComBoxToken.functions.transfer(accounts[0], move_balance).transact()
    if test_balances.checkbalances([(0, move_balance), (5, -move_balance)]) == False:
        print("--Failed #1")
        raise Exception("Test failed")

    w3.eth.defaultAccount = w3.eth.accounts[0]
    test_balances.fetchbalances()
    tx_hash = ComBoxToken.functions.transfer(accounts[5], test_amount).transact()
    w3.eth.defaultAccount = w3.eth.accounts[5]
    test_balances.fetchbalances()
    if test_balances.checkfixedbalances([ (5, test_amount)]) == False:
        print("--Failed #2")
        raise Exception("Test failed")


    to_addr = [accounts[6], accounts[7], accounts[7] ]
    to_values = [FloatToDecimal(10), FloatToDecimal(20), FloatToDecimal(30)]
    test_balances.fetchbalances()
    try:
        tx_hash = ComBoxToken.functions.masssend(to_addr, to_values).transact()
    except:
        pass

    if test_balances.checkbalances([(5, 0), (6, 0), (7, 0), (8, 0)]) == True:
        print("--Passed")
    else:
        print("--Failed #3")
except:
    print(sys.exc_info())
    print("------Failed")


print("\nMassSend test account[5] account[6] account[7] account[8] #2")

try:

    to_addr = [accounts[6], accounts[7], accounts[8] ]
    to_values = [FloatToDecimal(2), FloatToDecimal(3), FloatToDecimal(5)]
    test_balances.fetchbalances()
    try:
        tx_hash = ComBoxToken.functions.masssend(to_addr, to_values).transact()
    except:
        pass

    if test_balances.checkbalances([(5, -sum(to_values)), (6, to_values[0]), (7, to_values[1]), (8, to_values[2]) ]) == True:
        print("--Passed")
    else:
        print("--Failed #1")


except:
    print(sys.exc_info())
    print("------Failed")



print("\nPause test")

try:
    test_amount = FloatToDecimal(20)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    try:
        paused = ComBoxToken.functions.paused().call()
#        print(f"Paused : {paused}")
    except:
        print("--Failed #1")

    try:
        tx_hash = ComBoxToken.functions.pause().transact()
    except:
        print("--Failed #2")

    try:
        paused = ComBoxToken.functions.paused().call()
#        print(f"Paused : {paused}")
    except:
        print("--Failed #3")
        raise Exception("Test failed")

    if paused != True:
        print("--Failed #4")
        raise Exception("Test failed")

    try:
        w3.eth.defaultAccount = w3.eth.accounts[1]
        test_balances.fetchbalances()
        tx_hash = ComBoxToken.functions.transfer(accounts[5], test_amount).transact()
        print("Failed #5-0")
    except:
        print("Pass #5-0")

    try:
        w3.eth.defaultAccount = w3.eth.accounts[0]
        tx_hash = ComBoxToken.functions.transfer(accounts[6], test_amount).transact()
        print("Pass #5-1")
    except:
        print("Failed #5-1")
        raise Exception("Test failed")



    if test_balances.checkbalances([(0, -test_amount), (1, 0), (5, 0), (6, test_amount)  ]) == True:
        print("--Passed")
    else:
        print("--Failed #6")

    w3.eth.defaultAccount = w3.eth.accounts[0]
    try:
        tx_hash = ComBoxToken.functions.resume().transact()
    except:
        print("--Failed #7")

    try:
        paused = ComBoxToken.functions.paused().call()
#        print(f"Paused : {paused}")
    except:
        print("--Failed #8")
        raise Exception("Test failed")
except:
    print(sys.exc_info())
    print("------Failed")


print("\nTransfer ownership test")

try:
    test_amount = FloatToDecimal(20)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    test_balances.fetchbalances()

    print(f"Owner : {ComBoxToken.functions.owner().call()}")

    if ComBoxToken.functions.owner().call() != accounts[0]:
        print("--Failed #1")

    if ComBoxToken.functions.newOwner().call() != '0x0000000000000000000000000000000000000000' and ComBoxToken.functions.newOwner().call() != accounts[0]:
        print("--Failed #2")


    try:
        tx_hash = ComBoxToken.functions.transferOwnership( accounts[9] ).transact()
    except:
        print(sys.exc_info())
        print("--Failed #3")

    if ComBoxToken.functions.owner().call() != accounts[0]:
        print("--Failed #4")

    if ComBoxToken.functions.newOwner().call() != accounts[9]:
        print("--Failed #4")



    w3.eth.defaultAccount = w3.eth.accounts[9]
    try:
        tx_hash = ComBoxToken.functions.acceptOwnership( ).transact()
    except:
        print(sys.exc_info())
        print("--Failed #5")


    if ComBoxToken.functions.owner().call() != accounts[9]:
        print("--Failed #6")

    if ComBoxToken.functions.newOwner().call() != '0x0000000000000000000000000000000000000000':
        print("--Failed #7")

    try:
        tx_hash = ComBoxToken.functions.transferOwnership( accounts[0] ).transact()
    except:
        print(sys.exc_info())
        print("--Failed #8")

    if ComBoxToken.functions.owner().call() != accounts[9]:
        print("--Failed #9")

    if ComBoxToken.functions.newOwner().call() != accounts[0]:
        print("--Failed #10")

    w3.eth.defaultAccount = w3.eth.accounts[0]
    try:
        tx_hash = ComBoxToken.functions.acceptOwnership( ).transact()
    except:
        print(sys.exc_info())
        print("--Failed #11")



    if ComBoxToken.functions.newOwner().call() != '0x0000000000000000000000000000000000000000':
        print("--Failed #13")

    if ComBoxToken.functions.owner().call() == accounts[0]:
        print("--Passed")


except:
    print(sys.exc_info())
    print("------Failed")


print("--------Balances--------")
for i in range(0,len(accounts)):
    print(f" {i}  {accounts[i]}  {DecimalToFloat(ComBoxToken.functions.balanceOf(accounts[i]).call())}" )


