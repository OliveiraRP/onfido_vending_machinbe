from models.coin import Coin
from models.slot import Slot
from utils.constants import MAX_SLOTS

testSlots = {slot: Slot(number = slot, stock = 3, price = 1.00) for slot in range(1, MAX_SLOTS + 1)}
testCoins = {coin: 5 for coin in Coin}
