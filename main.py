import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.fill_table()

    def fill_table(self):
        coffee_info = self.get_coffee_info()

        coffee_info = self.insert_names_of_properties(coffee_info)

        self.coffee_table.setColumnCount(len(coffee_info[0]) - 1)
        self.coffee_table.setRowCount(len(coffee_info))

        for i, row in enumerate(coffee_info):
            for j, elem in enumerate(row[1:]):
                self.coffee_table.setItem(i, j, QTableWidgetItem(str(row[j + 1])))
                self.coffee_table.item(i, j).setFlags(Qt.ItemIsEditable)

        self.make_header_of_table()

    def get_coffee_info(self):
        cur = self.con.cursor()
        return cur.execute("""SELECT * FROM Coffee""").fetchall()

    def insert_names_of_properties(self, coffee_info):
        cur = self.con.cursor()
        roasting_degree, ground_or_in_grains = cur.execute("""SELECT name FROM Roasting_degrees""").fetchall(), \
                                               cur.execute("""SELECT name FROM Ground_and_in_grains""").fetchall()

        for i, coffee in enumerate(coffee_info):
            new_coffee = list(coffee)
            new_coffee[2] = roasting_degree[new_coffee[2]][0]
            new_coffee[3] = ground_or_in_grains[new_coffee[3]][0]

            coffee_info[i] = new_coffee

        return coffee_info

    def make_header_of_table(self):
        self.coffee_table.setHorizontalHeaderLabels(('Название кофе', 'Степень обжарки', 'Молотый/в зёрнах',
                                                     'Описание вкуса', 'Цена', 'Объём упаковки'))

        header = self.coffee_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

    def closeEvent(self, event):
        self.con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    espresso = Espresso()
    espresso.show()
    sys.exit(app.exec())
