from roles import Waiter, Cashier, Chef, Customer, Table
import threading, time, random, queue

def createCustomer():
    # Bu method ile gelen müşterilerin gelmesi sağlanıyor ve öncelik sıralamsına göre sıraya sokuluyorlar.
    customer_num = random.randint(1, 10)
    customers = []

    i = 0
    for i in range(customer_num):
        customer = Customer(id=i+1, priority=random.randint(0,1))
        customers.append(customer)
    
    customers.sort(key=lambda x: x.priority, reverse=True)
    
    return customers

def createChef(length):
    # Bu method ile simülasyonda kaç şef olması gerekiyorsa alınan sayıya göre yaratıyor.
    chefs = []
    i = 0
    for i in range(length):
        chef = Chef(i+1)
        chefs.append(chef)
    return chefs

def createWaiter(length):
    # Bu method ile simülasyonda kaç garson olması gerekiyorsa alınan sayıya göre yaratıyor.
    waiters = []
    i = 0
    for i in range(length):
        waiter = Waiter(i+1)
        waiters.append(waiter)
    return waiters

def createCashier(length):
    # Bu method ile simülasyonda kaç kasa olması gerekiyorsa alınan sayıya göre yaratıyor.
    cashiers = []
    i = 0
    for i in range(length):
        cashier = Cashier(i+1)
        cashiers.append(cashier)
    return cashiers

def createTable(length):
    # Bu method ile simülasyonda kaç masa olması gerekiyorsa alınan sayıya göre yaratıyor.
    tables = []
    i = 0
    for i in range(length):
        table = Table(i+1)
        tables.append(table)
    return tables

def customer_activity(customer, table):
    print(f"Customer {customer.id} is seated at Table {table.id}.")
    time.sleep(3)  # Müşteri belirli bir süre oturuyor
    table.freeTable()
    print(f"Customer {customer.id} left Table {table.id}.")

def makeLinePriority(oldLine, newLine):
    result = list(zip(oldLine, newLine))
    result.sort(key=lambda x: x.priority, reverse=True)
    return result


def main():
    # Başlangıçtaki restoran özelliklerinin belirlenmesi
    waiters = createWaiter(3)
    chefs = createChef(2)
    cashiers = createCashier(1)
    tables = createTable(6) # Masaların tam olarak nasıl tasarlanması ve tanımlanması gerektiğini çözemedim.
    
    for table in tables:
        print(f"Table ID: {table.id} and Table is Available: {table.isAvailable}")

    customers_line = queue.Queue()
    extra_line = []
    while True:
        queue_copy = []

        for oldCustomer in extra_line:
            queue_copy.append(oldCustomer)

        extra_line.clear()

        customers = createCustomer()
        for customer in customers:
            queue_copy.append(customer)

        queue_copy.sort(key=lambda x: x.priority, reverse=True)

        for customer in queue_copy:
            print(f"Customer ID: {customer.id} and Customer Priority: {customer.priority}") 
            customers_line.put(customer) 

        print("------------------------------------------------------")  
        
        while not customers_line.empty():
            customer = customers_line.get()

            # Müşteriye uygun masa bul
            available_table = None
            for table in tables:
                if table.isAvailable:
                    available_table = table
                    break

            if available_table:
                available_table.seatTable(customer)
                threading.Thread(target=customer_activity, args=(customer, available_table)).start()
            else:
                print(f"Müsait masa yok for Müşteri {customer.id}.")
                extra_line.append(customer)
        time.sleep(5)  # Belirli bir süre sonra yeni müşterilerin gelmesini bekle


if __name__ == "__main__":
    main()
