import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout

class TableLayout(QWidget):
    def __init__(self):
        super(TableLayout, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Masaların olduğu ana pencere
        main_layout = QVBoxLayout()

        # Masa kareleri
        table_layout = QHBoxLayout()
        for i in range(6):
            table_label = QLabel(f'Masa {i + 1}')
            table_layout.addWidget(table_label)

        # Başlat ve Durdur butonları
        control_layout = QHBoxLayout()
        start_button = QPushButton('Başlat')
        stop_button = QPushButton('Durdur')
        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)

        # Input alanları ve Hesapla butonu
        input_layout = QVBoxLayout()
        for i in range(4):
            input_label = QLabel(f'Input {i + 1}:')
            input_field = QLineEdit()
            input_layout.addWidget(input_label)
            input_layout.addWidget(input_field)

        calculate_button = QPushButton('Hesapla')

        # Sonuç label'ları
        result_layout = QGridLayout()
        for i in range(4):
            label1 = QLabel(f'Sonuç {i + 1}:')
            label2 = QLabel(f'Sonuç {i + 5}:')
            result_layout.addWidget(label1, i, 0)
            result_layout.addWidget(label2, i, 1)

        # Ana layout'u oluştur
        main_layout.addLayout(table_layout)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(calculate_button)
        main_layout.addLayout(result_layout)

        self.setLayout(main_layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Masalar ve Hesaplama')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableLayout()
    sys.exit(app.exec_())
