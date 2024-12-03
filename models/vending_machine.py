from models.coin import Coin
from models.slot import Slot
from utils.constants import MAX_SLOTS

"""
Defines a singleton object of VendingMachine
@param slots: Tracks the stock for each slot of the vm
@param coins: Coins the vm has stored per coin type
"""
class VendingMachine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'slots'):
            self.slots = { slot: Slot(slot, 0.0, 0) for slot in range(1, MAX_SLOTS + 1) }
        if not hasattr(self, 'coins'):
            self.coins = { coin: 0 for coin in Coin }
