from roles import Waiter, Cashier, Chef, Customer, Table
import threading, time, random

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
        table = Table()
        tables.append(table)
    return tables


def main():
    # Başlangıçtaki restoran özelliklerinin belirlenmesi
    waiters = createWaiter(3)
    chefs = createChef(2)
    cashiers = createCashier(1)
    tables = createTable(6) # Masaların tam olarak nasıl tasarlanması ve tanımlanması gerektiğini çözemedim.

    customers = createCustomer()
    for customer in customers:
        print(f"Customer ID: {customer.id} and Customer Priority: {customer.priority}")

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
