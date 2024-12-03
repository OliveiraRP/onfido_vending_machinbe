import pytest
from tests.test_values import (testCoins, testSlots)
from controllers.stock_controller import StockController
from models.coin import Coin
from models.vending_machine import VendingMachine

@pytest.fixture
def mockVendingMachine():
    mockVM = VendingMachine()
    mockVM.slots = testSlots
    mockVM.coins = testCoins
    return mockVM

@pytest.fixture
def mockStockController(mockVendingMachine):
    return StockController(mockVendingMachine)

"""
GIVEN StockControler WHEN addStock is called with valid inputs
THEN should update the stock in the specified slot correctly
"""
def testAddStock(mockStockController, mockVendingMachine):
    expectedStock = mockVendingMachine.slots[1].stock
    mockStockController.addStock(1, 2)
    assert mockVendingMachine.slots[1].stock == expectedStock + 2
    mockStockController.addStock(1, 3)
    assert mockVendingMachine.slots[1].stock == expectedStock + 5

"""
GIVEN StockControler WHEN addStock is called with invalid slot
THEN error log should be printed
"""
def testAddStockInvalidSlot(mockStockController, capsys):
    mockStockController.addStock(31, 3)
    log = capsys.readouterr()
    assert "Invalid slot number" in log.out

"""
GIVEN StockControler WHEN dispenseProduct is called with available stock
THEN the stock in vending machine should go down by 1
"""
def testDispenseProduct(mockStockController, mockVendingMachine):
    expectedStock = mockVendingMachine.slots[1].stock - 1
    mockStockController.dispenseProduct(1)
    assert mockVendingMachine.slots[1].stock == expectedStock

"""
GIVEN StockControler WHEN dispenseProduct is called with no stock
THEN error log should be printed
"""
def testDispenseProductNoStock(mockStockController, mockVendingMachine, capsys):
    mockVendingMachine.slots[1].stock = 0
    mockStockController.dispenseProduct(1)
    log = capsys.readouterr()
    assert "This slot is empty" in log.out

"""
GIVEN StockControler WHEN setPrice is called
THEN price of specified slot should be updated
"""
def testSetSlotPrice(mockStockController, mockVendingMachine):
    mockStockController.setSlotPrice(1, 2.0)
    assert mockVendingMachine.slots[1].price == 2.0

"""
GIVEN StockControler WHEN addCoin is called
THEN quantity of specified coin should be updated
"""
def testAddCoin(mockStockController, mockVendingMachine):
    expectedResult = mockVendingMachine.coins[Coin.TWO_EURO]
    mockStockController.addCoin(Coin.TWO_EURO, 5)
    assert mockVendingMachine.coins[Coin.TWO_EURO] == expectedResult + 5

"""
GIVEN StockControler WHEN dispenseCoin is called
THEN quantity of specified coin should lower by specified quantity
"""
def testDispenseCoin(mockStockController, mockVendingMachine):
    expectedResult = mockVendingMachine.coins[Coin.FIFTY_CENT]
    mockStockController.dispenseCoins(Coin.FIFTY_CENT, 3)
    assert mockVendingMachine.coins[Coin.FIFTY_CENT] == expectedResult - 3

"""
GIVEN StockControler WHEN dispenseCoin is called but there are no coins specified
THEN error log should be printed
"""
def testDispenseCoinNoCoins(mockStockController, mockVendingMachine, capsys):
    mockVendingMachine.coins[Coin.FIVE_CENT] = 0
    mockStockController.dispenseCoins(Coin.FIVE_CENT, 1)
    log = capsys.readouterr()
    assert "Not enough coins in storage" in log.out
