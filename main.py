import sys

print(sys.prefix)
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from GUI.ui_main_window import Ui_MainWindow  # импортируем сгенерированный класс
from db_work import select_db_info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключаем сигнал кнопки к слоту
        self.ui.pushButton.clicked.connect(self.on_button_click)
        self.table_search_main = self.ui.tableWidget_search_main
        self.init_main_search_table()

    def init_main_search_table(self):
        self.table_search_main.setColumnCount(9)
        # функция для вычисления количества строк в таблице
        rows_amount = 6
        self.table_search_main.setRowCount(rows_amount)
        self.table_search_main.setHorizontalHeaderLabels(
            ["Код\nгруппы", "Код\nкласса", "Код\nСФО", "Код\nНОПС","ФНН", "Переход", "Похожий", "Обозначение", "Наименование"])
        all_unit = select_db_info(f"SELECT nops_vvst_id, predmet_inn, predmet_oboznachenie, predmet_name from catapp_predmetsnabzeniavvst")
        self.refresh_table_data(all_unit)
        # header = self.table_search_main.horizontalHeader()
        # header.setSectionResizeMode(0)
        # header.setSectionResizeMode(1)
        # header.setSectionResizeMode(2)
        # header.setSectionResizeMode(3)
        # header.setSectionResizeMode(4)
        # header.setSectionResizeMode(5)
        # header.setSectionResizeMode(6)
        # header.setSectionResizeMode(7)
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def refresh_table_data(self, unit_list):
        self.table_search_main.setRowCount(10)
        # self.table_search_main.setRowCount(len(unit_list))
        for row_index in range(len(unit_list)):
            if row_index == 6:
                break
            self.table_search_main.setItem(row_index, 4, QTableWidgetItem(unit_list[row_index][1]))
            self.table_search_main.setItem(row_index, 7, QTableWidgetItem(unit_list[row_index][2]))
            self.table_search_main.setItem(row_index, 8, QTableWidgetItem(unit_list[row_index][3]))
            nops_id = unit_list[row_index][0]
            nops_info = select_db_info(f"SELECT nops_number, sfo_vvst_id from catapp_nopsvvst WHERE id = {nops_id}")
            self.table_search_main.setItem(row_index, 3, QTableWidgetItem(nops_info[0][0]))
            sfo_id = nops_info[0][1]
            sfo_info = select_db_info(f"SELECT sfo_number, class_vvst_id from catapp_sfovvst WHERE id = {sfo_id}")
            self.table_search_main.setItem(row_index, 2, QTableWidgetItem(sfo_info[0][0]))
            class_id = sfo_info[0][1]
            class_info = select_db_info(f"SELECT class_number, group_vvst_id from catapp_classvvst WHERE id = {class_id}")
            self.table_search_main.setItem(row_index, 1, QTableWidgetItem(class_info[0][0]))
            group_id = class_info[0][1]
            group_info = select_db_info(
                f"SELECT group_number from catapp_groupvvst WHERE id = {group_id}")
            self.table_search_main.setItem(row_index, 0, QTableWidgetItem(group_info[0][0]))
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def on_button_click(self):
        print("Кнопка была нажата!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
