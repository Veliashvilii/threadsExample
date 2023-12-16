from roles import Waiter, Cashier, Chef, Customer
import threading, time, random


def main():
    #When starts program we have 6 table, 3 waiter, 2 chef and 1 cashier
    #Cashier
    cashier = Cashier(id=1)
    cashier_thread = threading.Thread(target=cashier.run)
    # cashier_thread.start()
    #Chefs
    chef1 = Chef(id=1)
    chef1_thread = threading.Thread(target=chef1.run)
    chef2 = Chef(id=2)
    chef2_thread = threading.Thread(target=chef2.run)
    #Waiters
    waiter1 = Waiter(id=1)
    waiter1_thread = threading.Thread(target=waiter1.run)
    waiter2 = Waiter(id=2)
    waiter2_thread = threading.Thread(target=waiter2.run)
    waiter3 = Waiter(id=3)
    waiter3_thread = threading.Thread(target=waiter3.run)

    #Start Threads
    cashier_thread.start()
    chef1_thread.start()
    chef2_thread.start()
    waiter1_thread.start()
    waiter2_thread.start()
    waiter3_thread.start()

    #Define Customers
    
    customer_num = random.randint(1,10)
    customers = []
    i = 0
    for i in range(customer_num):
        customer = Customer(id=i+1, priority=random.randint(0,1))
        customers.append(customer)

    for customer in customers:
        print(f"Customer ID: {customer.id} and Customer Priority: {customer.priority}")


if __name__ == "__main__":
    main()
