from controllers.stock_controller import StockController
from controllers.transaction_controller import TransactionController
from data.db import (createDatabase, loadData, saveData)
from models.vending_machine import VendingMachine
from models.coin import Coin
from utils.initial_values import (initialSlots, initialCoins)

def menu():
    while True:
        print("\n--- Vending Machine ---")
        print("1. Insert Coin")
        print("2. Buy Product")
        print("3. Cancel Transaction")
        print("4. Load Stock")
        print("5. Load Coins")
        print("6. Check Stock")
        print("7. Import Initial Values")
        
        choice = input("Please select an option (1-7): ")

        actions = {
            '1': insertCoin,
            '2': buyProduct,
            '3': cancelTransaction,
            '4': loadStock,
            '5': loadCoins,
            '6': checkStock,
            '7': importInitialValues
        }
        
        action = actions.get(choice)
        if action:
            action()
        else:
            break

def insertCoin():
    for index, coin in enumerate(Coin, start = 1):
        print(f"{index}. {coin.name.replace('_', ' ').title()} - €{coin.value:.2f}")
    choice = int(input("Choose a coin: "))
    selectedCoin = list(Coin)[choice - 1]
    transactionController.insertCoin(selectedCoin)
    saveData(vm)

def buyProduct():
    choice = int(input("Choose a product between slot 1 and 30: "))
    transactionController.buyProduct(choice)
    saveData(vm)

def cancelTransaction():
    transactionController.cancelTransaction()
    saveData(vm)

def loadStock():
    slot = int(input("Choose a slot: "))
    quantity = int(input("How many: "))
    stockController.addStock(slot, quantity)
    saveData(vm)

def loadCoins():
    for index, coin in enumerate(Coin, start=1):
        print(f"{index}. {coin.name.replace('_', ' ').title()} - €{coin.value:.2f}")
    choice = int(input("Choose a coin: "))
    selectedCoin = list(Coin)[choice - 1]
    quantity = int(input("How many: "))
    stockController.addCoin(selectedCoin, quantity)
    saveData(vm)

def checkStock():
    print("Coins in the vending machine:")
    for coin, count in vm.coins.items():
        print(f"{coin.name}: {count}")
    print("Current product stock:")
    for slotNumber, slot in vm.slots.items():
        print(f"Slot {slotNumber}: {slot.stock}")

def importInitialValues():
    print("Importing vending machine initial values")
    vm.slots = initialSlots
    vm.coins = initialCoins
    saveData(vm)

createDatabase()

vm = VendingMachine()

loadData(vm)
if len(vm.coins) == 0 or len(vm.slots) == 0:
    importInitialValues()

stockController = StockController(vm)
transactionController = TransactionController(vm, stockController)

menu()
