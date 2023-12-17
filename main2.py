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


def main():
    # Başlangıçtaki restoran özelliklerinin belirlenmesi
    waiters = createWaiter(3)
    chefs = createChef(2)
    cashiers = createCashier(1)
    tables = createTable(6) # Masaların tam olarak nasıl tasarlanması ve tanımlanması gerektiğini çözemedim.

    customers = createCustomer()
    for customer in customers:
        print(f"Customer ID: {customer.id} and Customer Priority: {customer.priority}")
    
    for table in tables:
        print(f"Table ID: {table.id} and Table is Available: {table.isAvailable}")

   # print("!Change Available situation!")
   # for table in tables:
   #     if table.id == 4:
   #         table.isAvailable = False
   #     print(f"Table ID: {table.id} and Table is Available: {table.isAvailable}")


    # Gelen birinci müşteri dalgasını masalara yerleştiren bir simülasyon gerçekleştiriyor.
    """ customers_line = queue.Queue()
    for customer in customers:
        customers_line.put(customer)

    while not customers_line.empty():
        customer = customers_line.get()
        available_table = None
        for table in tables:
            if table.isAvailable:
                available_table = table
                break
        
        if available_table:
            available_table.isAvailable = False
            customer.start()
            print(f"Customer ID: {customer.id}, Available Table ID: {available_table.id} seated.")
        else:
            print(f"Available Table None, please wait!")
    """

    customers_line = queue.Queue()
    while True:
        customers = createCustomer()
        for customer in customers:
            customers_line.put(customer)

        while not customers_line.empty():
            customer = customers_line.get()

            # Müşteriye uygun masa bul
            available_table = None
            for table in tables:
                if table.isAvailable:
                    available_table = table
                    break

            if available_table:
                available_table.isAvailable = False
                available_table.customer = customer
                threading.Thread(target=customer_activity, args=(customer, available_table)).start()
            else:
                print(f"Müsait masa yok for Müşteri {customer.id}.")

        time.sleep(5)  # Belirli bir süre sonra yeni müşterilerin gelmesini bekle

    # aktif sıra dizisi tutmak mantıklı olabilir. Çünkü örneğin masalar dolu olunca bu sefer 
    # gelen kişileri silmek yerine sırada olduklarını bu şekilde takip edebiliriz.
    # Ayrıyeten burada şunu unutmamak gerekli. Örneğin 2. müşteri dalgası gelidiğinde bu sefer
    # öncelik sıralaması kayacak. Örneğin birinci dalgada öncelik sıralaması 1100 olsun. İkincide
    # 1010 olsun. Biz bunu burada yeniden sort etmeliyizki önceliklilier öne gelsin. Yani sıra şöyle olmalı
    # 11110000 bu şekle girmesi için kullanmamız gereken kod parçacığı aşağıda:
    # active_line.sort(key=lambda x: x.priority, reverse=True)
    active_line = []


if __name__ == "__main__":
    main()
