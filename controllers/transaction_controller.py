from controllers.stock_controller import StockController
from models.coin import Coin
from models.vending_machine import VendingMachine
from utils.constants import MAX_SLOTS

"""
Controller class for business logic related to the transaction interactions
"""
class TransactionController:
    def __init__(self, vendingMachine: VendingMachine, stockController: StockController):
        self.vendingMachine = vendingMachine
        self.stockController = stockController
        self.coinsInserted = {coin: 0 for coin in Coin}

    def insertCoin(self, coinType: Coin):
        self.coinsInserted[coinType] += 1
        print(f"Inserted {coinType.name}")
        self.stockController.addCoin(coinType, 1)
        currentAmount = self.__totalInsertedValue()
        print(f"Current inserted amount is €{currentAmount}")

    def buyProduct(self, slotNumber):
        print("Initiating transaction")

        if slotNumber < 1 or slotNumber > MAX_SLOTS:
            print("Invalid slot number")
            return
        
        selectedSlot = self.vendingMachine.slots[slotNumber]
        
        if selectedSlot.stock < 1:
            print("The selected slot is empty")
            return
        
        print(f"The price of this product is €{selectedSlot.price}")
        
        if self.__totalInsertedValue() < selectedSlot.price:
            print("Not enough money in machine")
            return
        
        self.__giveChange(selectedSlot.price)
        print(f"Dispensing product from slot {slotNumber}")
        self.stockController.dispenseProduct(slotNumber)
        self.__resetInsertedCoins()

    def __giveChange(self, price):
        changeToGive = self.__totalInsertedValue() - price

        if changeToGive <= 0:
            print("No change to give")
            return
        
        # Round change value to 2 decimal places to avoid floating point issues
        changeToGive = round(changeToGive, 2)

        print(f"Change to give is €{changeToGive}. Dispensing change")
        change = self.__selectCoinsForChange(changeToGive, self.vendingMachine.coins)
        for coin, count in change.items():
            if count > 0:
                print(f"{count}x {coin.name} (€{coin.value:.2f})")
                self.stockController.dispenseCoins(coin, count)

    def __selectCoinsForChange(self, changeValue, storedCoins):
        changeToGive = dict({coin: 0 for coin in Coin})
        _storedCoins = storedCoins.copy()

        for coin in Coin:
            while changeValue >= coin.value and _storedCoins[coin] > 0:
                changeToGive[coin] += 1
                _storedCoins[coin] -= 1
                changeValue = round(changeValue - coin.value, 2)
            
            if changeValue <= 0:
                break
        
        if changeValue > 0:
            print(f"Unable to give exact change. Remaining amount: €{changeValue:.2f}")

        return dict(changeToGive)

    def cancelTransaction(self):
        for coin, count in self.coinsInserted.items():
            if count > 0:
                self.stockController.dispenseCoins(coin, count)

        self.__resetInsertedCoins()
        print("Transaction cancelled. All inserted coins have been returned.")
        
    def __totalInsertedValue(self):
        return sum(coin.value * count for coin, count in self.coinsInserted.items())
    
    def __resetInsertedCoins(self):
        self.coinsInserted = {coin: 0 for coin in Coin}
