import sqlite3
from models.coin import Coin
from models.slot import Slot
from models.vending_machine import VendingMachine

DB_FILE = './data/database.db'

def createDatabase():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            slot_number INTEGER PRIMARY KEY,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS coins (
            denomination REAL PRIMARY KEY,
            count INTEGER NOT NULL
        )
        ''')

def saveData(machine: VendingMachine):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.executemany('''
        INSERT OR REPLACE INTO slots (slot_number, price, stock) VALUES (?, ?, ?)
        ''', [(slot.number, slot.price, slot.stock) for slot in machine.slots.values()])

        cursor.executemany('''
        INSERT OR REPLACE INTO coins (denomination, count) VALUES (?, ?)
        ''', [(coin.value, count) for coin, count in machine.coins.items()])

def loadCoins():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT slot_number, price, stock FROM slots')
        slots_data = cursor.fetchall()
        return {
            slot_number: Slot(slot_number, price, stock)
            for slot_number, price, stock in slots_data
        }

def loadSlots():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT denomination, count FROM coins')
        coins_data = cursor.fetchall()
        return {Coin(denomination): count for denomination, count in coins_data}
    
def loadData(machine: VendingMachine):
    """Load the VendingMachine state from the SQLite database."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT slot_number, price, stock FROM slots')
        slots_data = cursor.fetchall()
        machine.slots = {
            slot_number: Slot(slot_number, price, stock)
            for slot_number, price, stock in slots_data
        }

        cursor.execute('SELECT denomination, count FROM coins')
        coins_data = cursor.fetchall()
        machine.coins = {Coin(denomination): count for denomination, count in coins_data}
