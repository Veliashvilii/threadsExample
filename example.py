import threading
import time
import random
from queue import Queue, Empty, PriorityQueue
from threading import Semaphore

class Restaurant:
    def __init__(self, num_tables, num_waiters, num_chefs, num_cashiers):
        self.tables = Semaphore(num_tables)
        self.waiters = [Waiter(f'Waiter-{i}') for i in range(num_waiters)]
        self.chefs = [Chef(f'Chef-{i}') for i in range(num_chefs)]
        self.cashier = Cashier('Cashier')
        self.customer_queue = Queue()  # PriorityQueue kullanarak öncelik kuyruğu oluşturuyoruz

    def start_simulation(self):
        while True:    
            customers = []
            num_customers = random.randint(1, 10)
            for i in range(num_customers):
                customer = Customer(f"Customer-{i+1}", self, random.randint(0, 1))
                customers.append(customer)

            customers.sort(key=lambda x: x.priority, reverse=True)

            for customer in customers:
                self.customer_queue.put(customer)

            while not self.customer_queue.empty():
                customer = self.customer_queue.get()
                customer.start()

            for customer in customers:
                customer.join()
            
            print("--------------------------------")


            time.sleep(2)

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

class Customer(threading.Thread):
    def __init__(self, name, restaurant, priority):
        super().__init__(name=name)
        self.restaurant = restaurant
        self.priority = priority

    def run(self):
        time.sleep(3)  # Simulate customer arriving at random time
        #random.uniform(0, 1)
        #priority = random.randint(0, 1)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"{self.name} entered the restaurant with priority {self.priority}.")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        self.restaurant.customer_queue.put(self.name)
        self.restaurant.tables.wait()  # Wait for an available table
        waiter = random.choice(self.restaurant.waiters)
        waiter.take_order(self.name)
        self.restaurant.tables.signal()  # Release the table
        self.restaurant.customer_queue.get()  # Remove from the queue
        time.sleep(random.uniform(1, 2))  # Simulate customer eating time

class Waiter(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def take_order(self, customer_name):
        print(f"{self.name} took order from {customer_name}.")
        chef = random.choice(restaurant.chefs)
        chef.prepare_order(customer_name)

class Chef(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def prepare_order(self, customer_name):
        print(f"{self.name} is preparing the order for {customer_name}.")
        time.sleep(random.uniform(1, 2))  # Simulate cooking time
        print(f"{self.name} finished preparing the order for {customer_name}.")
        restaurant.cashier.receive_payment(customer_name)

class Cashier(threading.Thread):
    def __init__(self, name):
        super().__init__(name=name)

    def receive_payment(self, customer_name):
        print(f"{self.name} received payment from {customer_name}.")
        time.sleep(3)  # Simulate payment processing time
        #random.uniform(0.5, 1)

if __name__ == "__main__":
    restaurant = Restaurant(num_tables=6, num_waiters=3, num_chefs=2, num_cashiers=1)
    restaurant.start_simulation()