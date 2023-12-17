import threading
import time

class Customer(threading.Thread):
    def __init__(self, id, priority):
        super().__init__()
        self.id = id
        self.priority = priority

    def run(self):
        # Müşteri işlemleri
        print(f"Customer {self.id} is seated.")

class Waiter(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        # Garson işlemleri
        print(f"Waiter {self.id} is taking an order.")

class Chef(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        # Aşçı işlemleri
        print(f"Chef {self.id} is preparing a dish.")

class Cashier(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self):
        # Kasa işlemleri
        print(f"Cashier {self.id} is processing a payment.")
        #time.sleep(10)
        #table_number = input("What's your table number?\n")
        #time.sleep(0.5)
        print("Payment will starts")

class Table():
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.isAvailable = True #Masanın dolu olup olmadığını kontrol etmek adına kullanılıyor.
        self.customer = None # Masadaki müşterinin takibi için

    def freeTable(self):
        self.isAvailable = True
        self.customer = None

    def seatTable(self, customer):
        self.isAvailable = False
        self.customer = customer