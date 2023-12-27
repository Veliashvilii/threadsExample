from pulp import LpProblem, LpVariable, LpInteger, lpSum, LpMaximize

def optimize_restaurant():
    # Optimizasyon problemi tanımla
    model = LpProblem(name="restaurant_optimization", sense=LpMaximize)

    # Masa ve garson sayıları için değişkenler tanımla (tamsayı değişkenleri olarak)
    tables = LpVariable.dicts("tables", range(1, 101), lowBound=0, upBound=1, cat=LpInteger)
    waiters = LpVariable("waiters", lowBound=1, upBound=100, cat=LpInteger)

    # Toplam karı maksimize etmek için hedef fonksiyonu tanımla
    model += lpSum(tables[i] for i in range(1, 101)) - waiters

    # Müşteri kaybını sınırla (720 saniyede toplam müşteri sayısı)
    model += lpSum(tables[i] * 1.8 for i in range(1, 101)) + waiters * 4 <= 720, "customer_limit"

    # Her masadan sipariş alma süresi 3 saniye olduğu için, her masanın işlem süresini ekleyin
    model += lpSum(tables[i] * 3 for i in range(1, 101)) <= 180, "order_time_constraint"

    # Optimizasyon problemi çöz
    model.solve()

    # Kar hesabını oluştur
    profit = lpSum(tables[i] for i in range(1, 101)).value() - waiters.value()

    # Sonuçları al
    max_capacity = sum(int(tables[i].value()) for i in range(1, 101))
    optimal_waiters = int(waiters.value())

    return max_capacity, optimal_waiters, profit

best_tables, best_waiters, max_profit = optimize_restaurant()
print("Optimum Masa Sayısı:", best_tables)
print("Optimum Garson Sayısı:", best_waiters)
print("Kar:", max_profit)
