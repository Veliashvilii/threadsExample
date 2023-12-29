import tkinter as tk
from tkinter import ttk
import random
class TableLayout(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Masalar ve Hesaplama')
        self.geometry('800x600')

        self.create_widgets()

    def create_widgets(self):
        # Customers başlığı
        customers_label = tk.Label(self, text='Customers', font=('Helvetica', 12, 'underline'))
        customers_label.pack(pady=10)

        # Masa kareleri
        customers_frame = ttk.Frame(self)
        for i in range(6):
            table_number = i + 1
            table_label = ttk.Label(customers_frame, text=f'Table {table_number}', borderwidth=1, relief="solid", background='green')
            table_label.grid(row=0, column=i, padx=5, pady=5)
        customers_frame.pack(pady=10)

        # Waiters başlığı
        waiters_label = tk.Label(self, text='Waiters', font=('Helvetica', 12, 'underline'))
        waiters_label.pack(pady=10)

        # Masa kareleri
        waiters_frame = ttk.Frame(self)
        for i in range(6):
            table_number = i + 1
            table_label = ttk.Label(waiters_frame, text=f'Table {table_number}', borderwidth=1, relief="solid", background='green')
            table_label.grid(row=0, column=i, padx=5, pady=5)
        waiters_frame.pack(pady=10)

        # Chefs başlığı
        chefs_label = tk.Label(self, text='Chefs', font=('Helvetica', 12, 'underline'))
        chefs_label.pack(pady=10)

        # Masa kareleri
        chefs_frame = ttk.Frame(self)
        for i in range(6):
            table_number = i + 1
            table_label = ttk.Label(chefs_frame, text=f'Table {table_number}', borderwidth=1, relief="solid", background='green')
            table_label.grid(row=0, column=i, padx=5, pady=5)
        chefs_frame.pack(pady=10)

        # Cashier başlığı
        cashier_label = tk.Label(self, text='Cashier', font=('Helvetica', 12, 'underline'))
        cashier_label.pack(pady=10)

        # Masa kareleri
        cashier_frame = ttk.Frame(self)
        for i in range(6):
            table_number = i + 1
            table_label = ttk.Label(cashier_frame, text=f'Table {table_number}', borderwidth=1, relief="solid", background='green')
            table_label.grid(row=0, column=i, padx=5, pady=5)
        cashier_frame.pack(pady=10)

        # Başlat ve Durdur butonları
        control_frame = ttk.Frame(self)
        start_button = ttk.Button(control_frame, text='Start')
        stop_button = ttk.Button(control_frame, text='Stop')
        start_button.grid(row=0, column=0, padx=5, pady=5)
        stop_button.grid(row=0, column=1, padx=5, pady=5)
        control_frame.pack(pady=10)

        # Input alanları ve Hesapla butonu
        input_frame = ttk.Frame(self)
        input_entries = []
        for i, title in enumerate(['Saniye', 'Müşteri Sayısı', 'Öncelikli Sayısı', 'Toplam simülasyon süresi']):
            input_label = ttk.Label(input_frame, text=f'{title}:')
            input_entry = ttk.Entry(input_frame)
            input_label.grid(row=i, column=0, padx=5, pady=5)
            input_entry.grid(row=i, column=1, padx=5, pady=5)
            input_entries.append(input_entry)

        calculate_button = ttk.Button(self, text='Calculate', command=lambda: self.calculate_result(input_entries))
        input_frame.pack(pady=10)
        calculate_button.pack(pady=10)

        # Sonuç label'ı
        self.result_label = ttk.Label(self, text='Sonuç:')
        self.result_label.pack(pady=10)

    def calculate_result(self, input_entries):
        try:
            input_values = [float(entry.get()) for entry in input_entries]

            saniye=input_values[0]
            müşteri_sayisi=input_values[1]

            öncelikli_sayisi=input_values[2]


            toplam_süre=input_values[3]*60


            total=(toplam_süre/saniye)*müşteri_sayisi
            list=[int(total/9)+1,int(total/9),int(total/9)-1]
            total_table=random.choice(list)
            waiters=int(total/9)-2
            chefs=int((total/9)/2)+1
            kar=total-total_table-waiters-chefs
            # result_value = str(input_values[0])
            # for i in range(1, len(input_values)):
            #     result_value = str(float(result_value) * input_values[i])
            self.result_label.config(text=f'Optimum masa sayısı: {total_table}, Optimum garson sayısı {waiters}, Optimum şef sayısı {chefs}. KAR={kar}')
        except ValueError:
            self.result_label.config(text='Hatalı Giriş')

if __name__ == '__main__':
    app = TableLayout()
    app.mainloop()
