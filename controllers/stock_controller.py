from models.coin import Coin
from models.vending_machine import VendingMachine
from utils.constants import MAX_SLOTS

"""
Controller class for business logic related to the vending machine stock
"""
class StockController:
    def __init__(self, vendingMachine: VendingMachine):
        self.vendingMachine = vendingMachine

    def addStock(self, slotNumber, quantity):
        if slotNumber < 1 or slotNumber > MAX_SLOTS:
            print("Invalid slot number")
            return
        
        self.vendingMachine.slots[slotNumber].stock += quantity
        print(f"Added {quantity} products in slot {slotNumber}")

    def dispenseProduct(self, slotNumber):
        if slotNumber < 1 or slotNumber > MAX_SLOTS:
            print("Invalid slot number")
            return
        
        if self.vendingMachine.slots[slotNumber].stock < 1:
            print("This slot is empty")
            return
        
        self.vendingMachine.slots[slotNumber].stock -= 1
        print(f"Dispensed 1 product from slot {slotNumber}")

    def setSlotPrice(self, slotNumber, price):
        if slotNumber < 1 or slotNumber > MAX_SLOTS:
            print("Invalid slot number")
            return
        
        self.vendingMachine.slots[slotNumber].price = price
        print(f"Set slot {slotNumber} price to {price}")


    def addCoin(self, coinType: Coin, quantity):
        self.vendingMachine.coins[coinType] += quantity
        print(f"Added {quantity} {coinType.name} into coin storage")

    def dispenseCoins(self, coinType: Coin, quantity):
        if self.vendingMachine.coins[coinType] < quantity:
            print("Not enough coins in storage")
            return
        
        self.vendingMachine.coins[coinType] -= quantity
        print(f"Dispensed {quantity} {coinType.name} from coin storage")
