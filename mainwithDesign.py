import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject  # Add QObject here
import threading
import time
import random

class GlobalCounter:
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def get_next_id(self):
        with self.lock:
            self.counter += 1
            return self.counter

class Semaphore:
    def __init__(self, initial):
        self.value = initial
        self.mutex = threading.Semaphore(1)
        self.wait_queue = []

    def wait(self):
        self.mutex.acquire()
        if self.value > 0:
            self.value -= 1
            self.mutex.release()
        else:
            self.mutex.release()
            waiter = threading.Semaphore(0)
            self.wait_queue.append(waiter)
            waiter.acquire()

    def signal(self):
        self.mutex.acquire()
        if self.wait_queue:
            waiter = self.wait_queue.pop(0)
            waiter.release()
        else:
            self.value += 1
        self.mutex.release()

class CustomerThread(QThread):
    sitting_signal = pyqtSignal(int)
    standing_signal = pyqtSignal(int)

    def __init__(self, customer, gui):
        super().__init__()
        self.customer = customer
        self.gui = gui

    def run(self):
        print(f"Müşteri-{self.customer.id} Restorana Giriş Yaptı")
        self.customer.restaurant.tables.wait()

        if self.customer.restaurant.available_tables:
            self.customer.table_number = random.choice(self.customer.restaurant.available_tables)
            self.customer.restaurant.available_tables.remove(self.customer.table_number)

            print(f"Müşteri-{self.customer.id} Masa-{self.customer.table_number}'de Oturdu")

            if self.gui:
                self.sitting_signal.emit(self.customer.table_number)

            waiter = random.choice(self.customer.restaurant.waiters)
            waiter_thread = threading.Thread(target=waiter.take_order, args=(self.customer.id,))
            waiter_thread.start()
            waiter_thread.join()

            # Connect the payment_received_signal to updateTableColors
            self.customer.restaurant.cashiers[0].payment_received_signal.connect(
                lambda customer_id=self.customer.id: self.gui.updateTableColors(standing_table=self.customer.table_number)
            )

            self.customer.restaurant.tables.signal()

            time.sleep(3)

            print(f"Müşteri-{self.customer.id} Masa-{self.customer.table_number}'den Kalktı")

            if self.gui:
                self.standing_signal.emit(self.customer.table_number)

            self.customer.restaurant.available_tables.append(self.customer.table_number)
        else:
            self.customer.restaurant.waiting_line.append(self.customer)
            if self.gui:
                self.gui.updateTableColors()

class Waiter(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def take_order(self, customer_id):
        print(f"Garson-{self.id} Müşteri-{customer_id}'den Sipariş Aldı")
        time.sleep(2)

class Cashier(QThread, QObject):  # Inherit from QObject
    payment_received_signal = pyqtSignal(int)

    def __init__(self, id, restaurant):
        super().__init__()
        QObject.__init__(self)  # Initialize QObject
        self.id = id
        self.restaurant = restaurant

    def receive_payment(self, customer_id):
        total_customers = self.restaurant.customer_counter.get_next_id()
        print(f"Kasiyer-{self.id} Müşteri-{customer_id}'den ödeme aldı.")
        print(f"Toplam Müşteri: {total_customers}")
        time.sleep(1)
        self.payment_received_signal.emit(customer_id)

class RestaurantGUI(QWidget):
    def __init__(self, restaurant):
        super().__init__()

        self.restaurant = restaurant
        self.table_labels = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        for table_num in self.restaurant.available_tables:
            label = QLabel(f"Masa {table_num}")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: green;")
            self.table_labels.append(label)
            layout.addWidget(label)

        self.setGeometry(300, 300, 200, 200)
        self.setLayout(layout)
        self.setWindowTitle('Restoran Simülasyonu')

        self.show()

    def updateTableColors(self, sitting_table=None, standing_table=None):
        for table_label in self.table_labels:
            table_label.setStyleSheet("background-color: green;")
            table_label.setText("")

        if self.restaurant.waiting_line:
            selected_table = self.restaurant.waiting_line[0].table_number
            if 1 <= selected_table <= len(self.table_labels):
                self.table_labels[selected_table - 1].setStyleSheet("background-color: red;")

        if sitting_table is not None and 1 <= sitting_table <= len(self.table_labels):
            self.table_labels[sitting_table - 1].setStyleSheet("background-color: blue;")
            if self.restaurant.waiting_line:
                self.table_labels[sitting_table - 1].setText(f"Masa {sitting_table} - Müşteri {self.restaurant.waiting_line[0].id}")

        if standing_table is not None and 1 <= standing_table <= len(self.table_labels):
            self.table_labels[standing_table - 1].setStyleSheet("background-color: green;")

    def startTimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.updateTableColors)
        timer.start(1000)  # Her saniyede bir güncelleme

class Restaurant:
    def __init__(self, num_tables, num_waiters, num_chefs, num_cashiers):
        self.tables = Semaphore(num_tables)
        self.available_tables = list(range(1, num_tables + 1))
        self.waiting_line = []
        self.waiters = createWaiters(num_waiters=num_waiters)
        self.chefs = createChefs(num_chefs=num_chefs)
        self.cashiers = createCashiers(num_cashiers=num_cashiers, restaurant=self)
        self.customer_counter = GlobalCounter()

    def start_simulation(self):
        while True:
            new_customers = createCustomersWithPriority(self)
            customers = makeOneLine(self.waiting_line, new_customers)
            self.waiting_line.clear()

            print("----------------------------------------------")
            for customer in customers:
                print(f"Müşteri ID: {customer.id}, Müşteri Öncelik: {customer.priority}")
            print("----------------------------------------------")

            threads = []
            for customer in customers:
                customer_thread = CustomerThread(customer, gui)
                customer_thread.sitting_signal.connect(gui.updateTableColors)
                customer_thread.standing_signal.connect(gui.updateTableColors)
                threads.append(customer_thread)
                customer_thread.start()
                customer_thread.wait()  # Wait for the thread to finish before moving on

            time.sleep(2)

def createCustomersWithPriority(restaurant):
    customer_num = random.randint(0, 10)
    customers = []
    i = 0
    for i in range(customer_num):
        customer = Customer(id=i + 1, priority=random.randint(0, 1), restaurant=restaurant)
        customers.append(customer)

    customers.sort(key=lambda x: x.priority, reverse=True)
    return customers

def makeOneLine(new_line, old_line):
    result_line = new_line + old_line
    result_line.sort(key=lambda x: x.priority, reverse=True)
    return result_line

def createWaiters(num_waiters):
    waiters = []
    i = 0
    for i in range(num_waiters):
        waiter = Waiter(id=i + 1)
        waiters.append(waiter)

    return waiters

def createChefs(num_chefs):
    chefs = []
    i = 0
    for i in range(num_chefs):
        chef = Chef(id=i + 1)
        chefs.append(chef)

    return chefs

def createCashiers(num_cashiers, restaurant):
    cashiers = []
    i = 0
    for i in range(num_cashiers):
        cashier = Cashier(id=i + 1, restaurant=restaurant)
        cashiers.append(cashier)

    return cashiers

class Chef(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self, customer_id):
        print(f"Aşçı-{self.id} Müşteri-{customer_id} için siparişi hazırlıyor.")
        time.sleep(3)
        print(f"Aşçı-{self.id} Müşteri-{customer_id}'in siparişini hazırladı.")

class Customer:
    def __init__(self, id, priority, restaurant):
        self.restaurant = restaurant
        self.priority = priority
        self.id = id
        self.table_number = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    restaurant = Restaurant(num_tables=6, num_waiters=3, num_chefs=2, num_cashiers=1)
    gui = RestaurantGUI(restaurant)
    gui.startTimer()
    restaurant_gui_thread = threading.Thread(target=restaurant.start_simulation)
    restaurant_gui_thread.start()
    sys.exit(app.exec_())
