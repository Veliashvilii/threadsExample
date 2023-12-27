import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt

class TableLayout(QWidget):
    def __init__(self):
        super(TableLayout, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Masaların olduğu ana pencere
        main_layout = QVBoxLayout()

        # Customers başlığı
        customers_label = QLabel('Customers')
        customers_label.setAlignment(Qt.AlignCenter)  # Başlığı ortala
        customers_label.setStyleSheet('QLabel { text-decoration: underline; }')  # Altını çiz
        main_layout.addWidget(customers_label)

        # Masa kareleri
        customers_layout = QHBoxLayout()
        for i in range(6):
            table_number = i + 1
            table_label = QLabel(f'Table {table_number}')
            # Set style sheet for table label with border radius and center alignment
            table_label.setStyleSheet('QLabel { border: 1px solid black; background-color: green; text-align: center; border-radius: 10px; }')
            table_label.setAlignment(Qt.AlignCenter)  # Align text to the center
            customers_layout.addWidget(table_label)
        main_layout.addLayout(customers_layout)

        # Waiters başlığı
        waiters_label = QLabel('Waiters')
        waiters_label.setAlignment(Qt.AlignCenter)  # Başlığı ortala
        waiters_label.setStyleSheet('QLabel { text-decoration: underline; }')  # Altını çiz
        main_layout.addWidget(waiters_label)

        # Masa kareleri
        waiters_layout = QHBoxLayout()
        for i in range(6):
            table_number = i + 1
            table_label = QLabel(f'Table {table_number}')
            # Set style sheet for table label with border radius and center alignment
            table_label.setStyleSheet('QLabel { border: 1px solid black; background-color: green; text-align: center; border-radius: 10px; }')
            table_label.setAlignment(Qt.AlignCenter)  # Align text to the center
            waiters_layout.addWidget(table_label)
        main_layout.addLayout(waiters_layout)

        # Chefs başlığı
        chefs_label = QLabel('Chefs')
        chefs_label.setAlignment(Qt.AlignCenter)  # Başlığı ortala
        chefs_label.setStyleSheet('QLabel { text-decoration: underline; }')  # Altını çiz
        main_layout.addWidget(chefs_label)

        # Masa kareleri
        chefs_layout = QHBoxLayout()
        for i in range(6):
            table_number = i + 1
            table_label = QLabel(f'Table {table_number}')
            # Set style sheet for table label with border radius and center alignment
            table_label.setStyleSheet('QLabel { border: 1px solid black; background-color: green; text-align: center; border-radius: 10px; }')
            table_label.setAlignment(Qt.AlignCenter)  # Align text to the center
            chefs_layout.addWidget(table_label)
        main_layout.addLayout(chefs_layout)

        # Cashier başlığı
        cashier_label = QLabel('Cashier')
        cashier_label.setAlignment(Qt.AlignCenter)  # Başlığı ortala
        cashier_label.setStyleSheet('QLabel { text-decoration: underline; }')  # Altını çiz
        main_layout.addWidget(cashier_label)

        # Masa kareleri
        cashier_layout = QHBoxLayout()
        for i in range(6):
            table_number = i + 1
            table_label = QLabel(f'Table {table_number}')
            # Set style sheet for table label with border radius and center alignment
            table_label.setStyleSheet('QLabel { border: 1px solid black; background-color: green; text-align: center; border-radius: 10px; }')
            table_label.setAlignment(Qt.AlignCenter)  # Align text to the center
            cashier_layout.addWidget(table_label)
        main_layout.addLayout(cashier_layout)

        # Başlat ve Durdur butonları
        control_layout = QHBoxLayout()
        start_button = QPushButton('Start')
        stop_button = QPushButton('Stop')
        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)

        # Input alanları ve Hesapla butonu
        input_layout = QGridLayout()
        for i, title in enumerate(['Input 1', 'Input 2', 'Input 3', 'Input 4']):
            input_label = QLabel(f'{title}:')
            input_field = QLineEdit()
            input_layout.addWidget(input_label, i, 0)
            input_layout.addWidget(input_field, i, 1)

        calculate_button = QPushButton('Calculate')

        # Sonuç label'ları
        result_layout = QGridLayout()
        for i, title in enumerate(['Sonuç 1', 'Sonuç 2', 'Sonuç 3', 'Sonuç 4']):
            label1 = QLabel(f'{title}:')
            label2 = QLabel(f'{title}:')
            result_layout.addWidget(label1, i, 0)
            result_layout.addWidget(label2, i, 1)

        # Ana layout'u oluştur
        main_layout.addLayout(self.create_control_layout())
        main_layout.addLayout(self.create_input_layout())
        main_layout.addWidget(self.create_calculate_button())
        main_layout.addLayout(self.create_result_layout())

        self.setLayout(main_layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Masalar ve Hesaplama')
        self.show()

    def create_control_layout(self):
        control_layout = QHBoxLayout()
        start_button = QPushButton('Start')
        stop_button = QPushButton('Stop')
        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)
        return control_layout

    def create_input_layout(self):
        input_layout = QGridLayout()
        for i, title in enumerate(['Input 1', 'Input 2', 'Input 3', 'Input 4']):
            input_label = QLabel(f'{title}:')
            input_field = QLineEdit()
            input_layout.addWidget(input_label, i, 0)
            input_layout.addWidget(input_field, i, 1)
        return input_layout

    def create_calculate_button(self):
        calculate_button = QPushButton('Calculate')
        return calculate_button

    def create_result_layout(self):
        result_layout = QGridLayout()
        for i, title in enumerate(['Sonuç 1', 'Sonuç 2', 'Sonuç 3', 'Sonuç 4']):
            label1 = QLabel(f'{title}:')
            label2 = QLabel(f'{title}:')
            result_layout.addWidget(label1, i, 0)
            result_layout.addWidget(label2, i, 1)
        return result_layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableLayout()
    sys.exit(app.exec_())