import threading
import time
import random
from queue import Queue, Empty


def createCustomersWithPriority(restaurant):
    customer_num = random.randint(0,10)
    customers = []
    i = 0
    for i in range(customer_num):
        customer = Customer(id = i+1, priority= random.randint(0,1), restaurant=restaurant)
        customers.append(customer)

    customers.sort(key=lambda x: x.priority, reverse=True)
    
    return customers

def makeOneLine(newLine, oldLine):
    resultLine = newLine + oldLine
    resultLine.sort(key=lambda x: x.priority, reverse=True)
    return resultLine

def createWaiters(num_waiters):
    waiters = []
    i = 0
    for i in range(num_waiters):
        waiter = Waiter(id=i+1)
        waiters.append(waiter)

    return waiters

def createChefs(num_chefs):
    chefs = []
    i = 0
    for i in range(num_chefs):
        chef = Chef(id=i+1)
        chefs.append(chef)
    
    return chefs

def createCashiers(num_cashiers, restaurant):
    cashiers = []
    i = 0
    for i in range(num_cashiers):
        cashier = Cashier(id=i+1, restaurant=restaurant)
        cashiers.append(cashier)

    return cashiers

class GlobalCounter:
    def __init__(self):
        self.counter = 0
        self.lock = threading.Lock()

    def get_next_id(self):
        with self.lock:
            self.counter += 1
            return self.counter
        

class Restaurant:
  def __init__(self, num_tables, num_waiters, num_chefs, num_cashiers):
        self.tables = Semaphore(num_tables)
        self.available_tables = list(range(1, num_tables + 1))
        self.waiting_line = []
        self.waiters = [[Waiter(i) for i in range(num_waiters)]]
        self.waiters = createWaiters(num_waiters=num_waiters)
        self.chefs = createChefs(num_chefs=num_chefs)
        self.cashiers = createCashiers(num_cashiers=num_cashiers, restaurant=self)
        self.customer_counter = GlobalCounter()

  def start_simulation(self):
        while True:
          newCustomers = createCustomersWithPriority(self)  
          customers = makeOneLine(self.waiting_line, newCustomers)
          self.waiting_line.clear()
          #total_customers = restaurant.customer_counter.get_next_id()

          print("----------------------------------------------")
          for customer in customers:
              print(f"Customer ID: {customer.id}, Customer Priority: {customer.priority}")
          print("----------------------------------------------")

          for customer in customers:
              customer_thread = threading.Thread(target=customer.run)
              customer_thread.start()
              time.sleep(random.uniform(0.1, 0.5))

          for customer in customers:
              customer_thread.join()

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
    def __init__(self, id, priority, restaurant):
        super().__init__()
        self.restaurant = restaurant
        self.priority = priority
        self.id = id 
        #total_customer = restaurant.customer_counter.get_next_id()
        self.table_number = None

    def run(self):
        print(f"Customer-{self.id} is Entered in Restaurant")
        self.restaurant.tables.wait()

        if self.restaurant.available_tables:
          # Rastgele masa seçimi
          self.table_number = random.choice(self.restaurant.available_tables)
          self.restaurant.available_tables.remove(self.table_number)

          print(f"Customer-{self.id} is seated at Table-{self.table_number}")
          #Garson Çağır ve Sipariş Ver
          waiter = random.choice(self.restaurant.waiters)
          waiter_thread = threading.Thread(target=waiter.take_order(self.id))
          waiter_thread.start()
          waiter_thread.join()
          #waiter.take_order(self.id)
          self.restaurant.tables.signal()
            # Müşteri yemek yedikten sonra masayı boşalt
          time.sleep(3)
          #random.uniform(0.1, 0.5)
          print(f"Customer-{self.id} left Table-{self.table_number}")
            # Boşalan masayı tekrar kullanıma aç
          self.restaurant.available_tables.append(self.table_number)
        else:
            self.restaurant.waiting_line.append(self)

class Waiter(threading.Thread):
  def __init__(self, id):
        super().__init__()
        self.id = id

  def take_order(self, customer_id):
        print(f"Waiter-{self.id} took order from Customer-{customer_id}.")
        time.sleep(2) # Sipariş Alma Süresi
        chef = random.choice(restaurant.chefs)
        chef_thread = threading.Thread(target=chef.run(customer_id))
        chef_thread.start()
        chef_thread.join()

class Chef(threading.Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def run(self, customer_id):
        print(f"Chef-{self.id} is preparing the order for Customer-{customer_id}.")
        time.sleep(3) #Yemeğin Pişme Süresi
        #random.uniform(1, 2)
        print(f"Chef-{self.id} finished preparing the order for Customer{customer_id}.")
        cashier = random.choice(restaurant.cashiers)
        cashier_thread = threading.Thread(target=cashier.receive_payment(customer_id))
        cashier_thread.start()
        cashier_thread.join()

class Cashier(threading.Thread):
    def __init__(self, id, restaurant):
        super().__init__()
        self.id = id
        self.restaurant = restaurant

    def receive_payment(self, customer_id):
        total_customers = self.restaurant.customer_counter.get_next_id()
        print(f"Cashier-{self.id} received payment from Customer-{customer_id}.")
        print(f"Total Customer: {total_customers}")
        time.sleep(1)  # Simulate payment processing time
        #random.uniform(0.5, 1)

if __name__ == "__main__":
    restaurant = Restaurant(num_tables=6, num_waiters=3, num_chefs=2, num_cashiers=1)
    restaurant.start_simulation()
