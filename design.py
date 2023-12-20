import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout, QSpacerItem, QSizePolicy

class TableLayout(QWidget):
    def __init__(self):
        super(TableLayout, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Masaların olduğu ana pencere
        main_layout = QVBoxLayout()

        # Masa kareleri
        table_layouts = []  # List to store table layouts
        for j in range(4):  # Create 4 rows of table layouts
            table_layout = QHBoxLayout()
            for i in range(6):
                table_number = i + 1
                if table_number > 24:
                    break
                table_label = QLabel(f'Masa {table_number}')
                # Set style sheet for table label
                table_label.setStyleSheet('QLabel { border: 1px solid black; background-color: green; text-align: center; }')
                table_layout.addWidget(table_label)
            table_layouts.append(table_layout)

        # Başlat ve Durdur butonları
        control_layout = QHBoxLayout()
        start_button = QPushButton('Başlat')
        stop_button = QPushButton('Durdur')
        control_layout.addWidget(start_button)
        control_layout.addWidget(stop_button)

        # Input alanları ve Hesapla butonu
        input_layout = QGridLayout()
        for i in range(4):
            input_label = QLabel(f'Input {i + 1}:')
            input_field = QLineEdit()
            input_layout.addWidget(input_label, i, 0)
            input_layout.addWidget(input_field, i, 1)

        calculate_button = QPushButton('Hesapla')

        # Sonuç label'ları
        result_layout = QGridLayout()
        for i in range(4):
            label1 = QLabel(f'Sonuç {i + 1}:')
            label2 = QLabel(f'Sonuç {i + 5}:')
            result_layout.addWidget(label1, i, 0)
            result_layout.addWidget(label2, i, 1)

        # Ana layout'u oluştur
        for idx, layout in enumerate(table_layouts):
            main_layout.addLayout(layout)
            if idx < len(table_layouts) - 1:
                spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
                main_layout.addItem(spacer)

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
