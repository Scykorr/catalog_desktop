import sys

print(sys.prefix)
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from GUI.ui_main_window import Ui_MainWindow  # импортируем сгенерированный класс
from db_work import select_db_info
from time import perf_counter
from math import ceil


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.result_info_list = list()
        self.counter_search_table = 1
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Каталог десктоп версия")

        # Подключаем сигнал кнопки к слоту
        self.table_search_main = self.ui.tableWidget_search_main
        # start_time = perf_counter()
        self.init_main_search_table()
        self.get_all_ps_list()
        # end_time = perf_counter()
        # print(start_time - end_time)
        self.ui.pushButton_next_search_table.clicked.connect(self.get_next_page_search_table)
        self.ui.pushButton_previous_search_table.clicked.connect(self.get_previous_page_search_table)
        self.ui.lineEdit.setText(str(self.counter_search_table))
        self.ui.pushButton_get_choosen_page.clicked.connect(self.get_chosen_page)
        self.table_search_main.verticalHeader().setVisible(False)
        self.ui.pushButton_search.clicked.connect(self.check_input_values)

    def init_main_search_table(self):
        self.table_search_main.setColumnCount(10)
        # функция для вычисления количества строк в таблице
        rows_amount = 7
        self.table_search_main.setRowCount(rows_amount)
        self.table_search_main.setHorizontalHeaderLabels(
            ["№\nп/п", "Код\nгруппы", "Код\nкласса", "Код\nСФО", "Код\nНОПС", "ФНН", "Переход", "Похожий",
             "Обозначение",
             "Наименование"])

    def get_all_ps_list(self):
        self.result_info_list.clear()
        unit_list = select_db_info(
            f"SELECT group_number, class_number, sfo_number, nops_number, predmet_inn, predmet_oboznachenie, predmet_name from all_ps")
        for row_index in range(len(unit_list)):
            self.result_info_list.append(
                [unit_list[row_index][0], unit_list[row_index][1], unit_list[row_index][2], unit_list[row_index][3],
                 unit_list[row_index][4], unit_list[row_index][5], unit_list[row_index][6]]
            )
        self.refresh_table_data(self.result_info_list)
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()


    def refresh_table_data(self, unit_list):
        pages_amount = int(len(unit_list) / 20)
        self.ui.label_2.setText(f"Всего: {pages_amount}")
        self.table_search_main.setRowCount(20)
        if self.counter_search_table == 0:
            range_start = len(self.result_info_list) - 20
            range_end = len(self.result_info_list) - 1
        elif len(unit_list) < 20:
            range_start = 0
            range_end = len(self.result_info_list) - 1
        else:
            range_start = (self.counter_search_table - 1) * 20
            range_end = self.counter_search_table * 20 - 1
        for row_index in range(range_start, range_end):
            self.table_search_main.setItem(row_index % 20 + 1, 0, QTableWidgetItem(str(row_index)))
            self.table_search_main.setItem(row_index % 20 + 1, 1, QTableWidgetItem(unit_list[row_index][0]))
            self.table_search_main.setItem(row_index % 20 + 1, 2, QTableWidgetItem(unit_list[row_index][1]))
            self.table_search_main.setItem(row_index % 20 + 1, 3, QTableWidgetItem(unit_list[row_index][2]))
            self.table_search_main.setItem(row_index % 20 + 1, 4, QTableWidgetItem(unit_list[row_index][3]))
            self.table_search_main.setItem(row_index % 20 + 1, 5, QTableWidgetItem(unit_list[row_index][4]))
            self.table_search_main.setItem(row_index % 20 + 1, 8, QTableWidgetItem(unit_list[row_index][5]))
            self.table_search_main.setItem(row_index % 20 + 1, 9, QTableWidgetItem(unit_list[row_index][6]))

        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def get_next_page_search_table(self):
        self.counter_search_table += 1
        if self.counter_search_table == int(len(self.result_info_list) / 20) + 1:
            self.counter_search_table = 0
        self.refresh_table_data(self.result_info_list)
        self.ui.lineEdit.setText(str(self.counter_search_table))
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def get_previous_page_search_table(self):
        self.counter_search_table -= 1
        if self.counter_search_table == -1:
            self.counter_search_table = int(len(self.result_info_list) / 20)
        self.ui.lineEdit.setText(str(self.counter_search_table))
        self.refresh_table_data(self.result_info_list)
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def get_chosen_page(self):
        self.counter_search_table = int(self.ui.lineEdit.text())
        self.refresh_table_data(self.result_info_list)
        self.table_search_main.resizeRowsToContents()
        self.table_search_main.resizeColumnsToContents()

    def check_input_values(self):
        check_values_list = list()
        res_value_after_check_list = list()
        self.get_all_ps_list()
        for el in range(1, 10):
            if self.table_search_main.item(0, el) == None:
                check_values_list.append('')
            else:
                check_values_list.append(self.table_search_main.item(0, el).text())
        if check_values_list[0] == '' and check_values_list[1] == '' and check_values_list[2] == '' and \
                check_values_list[3] == '' and check_values_list[4] == '' and check_values_list[5] == '' and \
                check_values_list[6] == '' and check_values_list[7] == '' and check_values_list[8] == '':
            self.get_all_ps_list()
        else:
            for num, val in enumerate(check_values_list):
                if num == 0 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[0].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 1 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[1].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 2 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[2].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 3 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[3].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 4 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[4].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 7 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[5].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
                if num == 8 and val != '':
                    buffer_list = list()
                    for el in self.result_info_list:
                        if val.lower() in el[6].lower():
                            buffer_list.append(el)
                        self.result_info_list = buffer_list.copy()
            self.table_search_main.clear()
            for num, el in enumerate(check_values_list):
                self.table_search_main.setItem(0, num + 1, QTableWidgetItem(el))
            self.refresh_table_data(self.result_info_list)
            self.table_search_main.resizeRowsToContents()
            self.table_search_main.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
