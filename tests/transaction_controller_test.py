import pytest
from tests.test_values import (testCoins, testSlots)
from controllers.stock_controller import StockController
from controllers.transaction_controller import TransactionController
from models.coin import Coin
from models.vending_machine import VendingMachine
from unittest.mock import MagicMock
from unittest.mock import call


@pytest.fixture
def mockVendingMachine():
    mockVM = VendingMachine()
    mockVM.slots = testSlots
    mockVM.coins = testCoins
    return mockVM

@pytest.fixture
def mockStockController(mockVendingMachine):
    return MagicMock(spec = StockController, vendingMachine = mockVendingMachine)

@pytest.fixture
def mockTransactionController(mockVendingMachine, mockStockController):
    return TransactionController(mockVendingMachine, mockStockController)

"""
GIVEN TransactionController WHEN insertCoin is called
THEN should update the inserted coins and stock controller adds the coin
"""
def testInsertCoin(mockTransactionController, mockStockController):
    mockTransactionController.insertCoin(Coin.TEN_CENT)
    assert mockTransactionController.coinsInserted[Coin.TEN_CENT] == 1
    mockStockController.addCoin.assert_called_once_with(Coin.TEN_CENT, 1)

"""
GIVEN TransactionController WHEN buyProduct is called with exact money
THEN should dispense the product and give no change
"""
def testBuyProductExactMoney(mockTransactionController, mockStockController):
    mockTransactionController.cancelTransaction()
    mockTransactionController.insertCoin(Coin.ONE_EURO)
    assert mockTransactionController.coinsInserted[Coin.ONE_EURO] == 1
    mockTransactionController.buyProduct(2)
    mockStockController.dispenseProduct.assert_called_once_with(2)
    mockStockController.dispenseCoins.assert_not_called()

"""
GIVEN TransactionController WHEN buyProduct is called with more money than price
THEN should dispense the product and give correct
"""
def testBuyProductWithChange(mockTransactionController, mockStockController):
    mockTransactionController.cancelTransaction()
    mockTransactionController.insertCoin(Coin.ONE_EURO)
    mockTransactionController.insertCoin(Coin.FIVE_CENT)
    mockTransactionController.buyProduct(2)
    expected_calls = [
        call(Coin.TWO_CENT, 2),
        call(Coin.ONE_CENT, 1)
    ]
    mockStockController.dispenseCoins.assert_has_calls(expected_calls)
    mockStockController.dispenseProduct.assert_called_once_with(2)

"""
GIVEN TransactionController WHEN buyProduct is called for a invalid slot
THEN error log should be printed
"""
def testBuyProductInvalidSlot(mockTransactionController, capsys):
    mockTransactionController.buyProduct(31)
    log = capsys.readouterr()
    assert "Invalid slot number" in log.out

"""
GIVEN TransactionController WHEN buyProduct is called for a slot with no stock
THEN error log should be printed
"""
def testBuyProductNoStock(mockTransactionController, mockVendingMachine, capsys):
    mockVendingMachine.slots[3].stock = 0
    mockTransactionController.buyProduct(3)
    log = capsys.readouterr()
    assert "The selected slot is empty" in log.out

"""
GIVEN TransactionController WHEN buyProduct is called with insufficient money
THEN error log should be printed
"""
def testBuyProductInsufficientMoney(mockTransactionController, capsys):
    mockTransactionController.cancelTransaction()
    mockTransactionController.insertCoin(Coin.ONE_CENT)
    mockTransactionController.buyProduct(4)
    log = capsys.readouterr()
    assert "Not enough money in machine" in log.out
