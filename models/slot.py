"""
Defines the object Slot
@param number: Number of the slot inside the VM
@param price: Price set for this slot
@param stock: Amount of products in this slot
"""
class Slot:
    def __init__(self, number, price, stock):
        self.number = number
        self.price = price
        self.stock = stock
