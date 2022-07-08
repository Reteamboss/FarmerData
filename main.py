from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtCore import Qt
from designmc3 import Ui_MainWindow
from interlogindesign import Ui_LoginWindow
from rfdesign import Ui_RegFormWindow
import sys
import sqlite3 as sq
import pandas as pd
import csv
import time
from random import randint


class RegistrationForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.ui = Ui_RegFormWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.registration)
        self.ui.pushButton_2.clicked.connect(self.back_login_window)

    def registration(self):
        # user_id = cur.execute('SELECT COUNT(DISTINCT user_id) FROM users')
        firstname = self.ui.lineEdit_2.text()
        lastname = self.ui.lineEdit_3.text()
        username = self.ui.lineEdit_4.text()
        password = self.ui.lineEdit_5.text()
        email = self.ui.lineEdit_6.text()
        cur.execute(f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")

        if cur.fetchone() is None:
            cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)",
                        (firstname, lastname, username, password, email))
            con.commit()
            self.ui.label_7.setText("<font color=green>Вы успешно зарегестрировались!</font>")
            time.sleep(1)
            RegistrationForm.back_login_window(self)
        else:
            self.ui.label_7.setText("<font color=red>Такой логин уже существует!</font>")

    def back_login_window(serf):
        login_window.show()
        reg_form.close()


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(QtWidgets.qApp.quit)
        self.ui.commandLinkButton_3.clicked.connect(self.registration)
        self.ui.pushButton.clicked.connect(self.sign_in)

    def sign_in(self):
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()
        querry = cur.execute(
            f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")
        # user = cur.execute(f"SELECT user_id FROM users WHERE username = '{username}' AND password = '{password}'")
        con.commit()
        if not cur.fetchone():
            self.ui.label_4.setText("<font color=red>Неверный логин и/или пароль!</font>")
        else:
            window.show()
            login_window.close()
            self.ui.label_4.setText("<font color=green>Успешно!Добро пожаловать!</font>")

    def registration(self):
        login_window.close()
        reg_form.show()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_11.clicked.connect(QtWidgets.qApp.quit)
        self.ui.pushButton_2.clicked.connect(self.show_by_category)
        self.find_result = self.ui.pushButton_2.clicked.connect(self.show_by_category)
        self.ui.pushButton_4.clicked.connect(self.show_all)
        self.ui.pushButton.clicked.connect(self.add_feedback)
        self.ui.action_CSV.triggered.connect(self.import_from_csv)
        self.ui.actionState_2.triggered.connect(self.sorted_state_min_max)
        self.ui.actionState_3.triggered.connect(self.sorted_state_max_min)
        self.ui.actionCity_2.triggered.connect(self.sorted_city_min_max)
        self.ui.actionCity_3.triggered.connect(self.sorted_city_max_min)
        self.ui.tableView.setSelectionBehavior(self.ui.tableView.SelectRows)
        self.ui.tableView.setMouseTracking(True)
        # self.ui.lineEdit_2.activated(self.show_by_category)
        # self.ui.action_2.triggered.connect()
        # self.ui.tableView.setHorizontalHeader()

        # self.ui.tableView.grabMouse()

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("Change", self))
        context.addAction(QAction("Delete", self))
        action = context.exec(e.globalPos())

        try:
            if action.text() == "Change":
                print("Change action was executed")
            elif action.text() == "Delete":
                print("Delete action was executed")
        except:
            "NoneType' object has no attribute 'text'"

    def show_all(self):
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('maininfo')
        stm.select()
        MainWindow.set_column_tableview_width(self)
        cur.execute("SELECT * FROM maininfo")
        count = len(cur.fetchall())
        print(count)
        self.ui.label.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))

    def add_feedback(self):
        tv = self.ui.tableView_2
        tv.setModel(stm2)
        # tv.setItemDelegateForColumn(0, QtSql.QSqlRelationalDelegate(tv))
        con1.open()
        stm2.setTable('feedbacks')
        stm2.select()
        stm2.insertRow(stm.rowCount())
        self.ui.label.setText('<font color=green>Отзыв успешно добавлен!</font>')

    def delrecord(self):
        tv = self.ui.tableView
        tv.setModel(stm)
        tv.setItemDelegateForColumn(0, QtSql.QSqlRelationalDelegate(tv))
        con1.open()
        stm.setTable('expenses')
        stm.setRelation(0, QtSql.QSqlRelation('categoryname', 'id_cat', 'category_name'))
        stm.select()
        stm.setHeaderData(0, QtCore.Qt.Horizontal, 'Категория')
        stm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        stm.setHeaderData(2, QtCore.Qt.Horizontal, 'Стоимость')
        stm.setHeaderData(3, QtCore.Qt.Horizontal, 'Дата\n yyyy-mm-dd')
        self.ui.lineEdit.setValidator(QtGui.QIntValidator(0, 10000, parent=window))
        count = str(stm.rowCount())
        validator = QtGui.QRegExpValidator(QtCore.QRegExp("[0-{}]".format(count)), parent=window)
        self.ui.lineEdit.setValidator(validator)
        id = int(self.ui.lineEdit.text())
        stm.removeRow(id - 1)
        self.ui.label.setText('<font color=green>Запись успешно удалена!</font>')

    def mouseMoveEvent(self, e):
        self.ui.label.setText("mouseMoveEvent")

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # handle the left-button press in here
            self.ui.label.setText("mousePressEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            # handle the middle-button press in here.
            self.ui.label.setText("mousePressEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            # handle the right-button press in here.
            self.ui.label.setText("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            index_row = self.ui.tableView.currentIndex
            self.ui.label.setText(f"{index_row}")

        elif e.button() == Qt.MiddleButton:
            self.ui.label.setText("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.ui.label.setText("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.ui.label.setText("mouseDoubleClickEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            self.ui.label.setText("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            self.ui.label.setText("mouseDoubleClickEvent RIGHT")

    def sorted(self, column, minmax):  # minmax - 1 - по возрастанию, minmax - 2 по убыванию, column - номер колонки
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('maininfo')
        if minmax == 1:
            stm.setSort(column, QtCore.Qt.AscendingOrder)  # min->max
        elif minmax == 2:
            stm.setSort(column, QtCore.Qt.DescendingOrder)  # max->min
        stm.select()
        MainWindow.set_column_tableview_width(self)
        con1.close()

    def sorted_rating_min_max(self):
        MainWindow.sorted(self, 5, 1)

    def sorted_state_min_max(self):
        MainWindow.sorted(self, 3, 1)

    def sorted_city_min_max(self):
        MainWindow.sorted(self, 2, 1)

    # def sorted_location_min_max(self):
    #     MainWindow.sorted(self,5,1)
    def sorted_rating_max_min(self):
        MainWindow.sorted(self, 5, 2)

    def sorted_state_max_min(self):
        MainWindow.sorted(self, 3, 2)

    def sorted_city_max_min(self):
        MainWindow.sorted(self, 2, 2)

    # def sorted_location_max_min(self):
    #     MainWindow.sorted(self,5,2)

    def show_by_date(self):
        dataedit3 = self.ui.dateEdit.date().toString('yyyy-MM-dd')
        tv = self.ui.tableView
        tv.setModel(stm)
        tv.setItemDelegateForColumn(0, QtSql.QSqlRelationalDelegate(tv))
        con1.open()
        stm.setTable('expenses')
        stm.setRelation(0, QtSql.QSqlRelation('categoryname', 'id_cat', 'category_name'))
        datafilter = "data = '{}'".format(dataedit3)
        stm.setFilter(datafilter)
        stm.setHeaderData(0, QtCore.Qt.Horizontal, 'Категория')
        stm.setHeaderData(1, QtCore.Qt.Horizontal, 'Название')
        stm.setHeaderData(2, QtCore.Qt.Horizontal, 'Стоимость')
        stm.setHeaderData(3, QtCore.Qt.Horizontal, 'Дата\n yyyy-mm-dd')
        stm.select()
        count = stm.rowCount()
        con1.close()
        self.ui.label.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))

    def show_by_category(self):
        category = self.ui.lineEdit_2.text()
        tv = self.ui.tableView
        tv.setModel(stm)
        # tv.setItemDelegateForColumn(0, QtSql.QSqlRelationalDelegate(tv))
        con1.open()
        stm.setTable('maininfo')

        if category != "":
            categoryfilter = f"city = '{category}' or State = '{category}' or zip = '{category}' "
            stm.setFilter(categoryfilter)
            print(category)
            # stm.setSort(3, QtCore.Qt.AscendingOrder)
            stm.select()
            MainWindow.set_column_tableview_width(self)
            count = stm.rowCount()
            con1.close()
            self.ui.label.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))
        else:
            self.ui.label.setText('<font color=red>Вы ничего не выбрали!</font>')

    def import_from_csv(self):
        file = QtWidgets.QFileDialog.getOpenFileName(parent=window, caption="Выбор файла", directory="c:\\python36",
                                                     filter="csv format (*.csv)",
                                                     initialFilter="csv format (*.csv)")
        filename = file[0]
        if filename != "":
            with open(filename, 'r') as fin:
                dr = csv.DictReader(fin)
                rating = randint(1, 5)
                to_db = [(i['FMID'], i['MarketName'], i['city'], i['State'], i['zip']) for i in dr]
                cur.executemany(
                    "INSERT OR IGNORE INTO maininfo (FMID,MarketName, city, State,zip) VALUES ( ?, ?, ?, ?, ?);", to_db)
                # cur.execute(
                #     f"INSERT INTO maininfo (rating) VALUES ({randint(1,5)})"
                # )
            with open(filename, 'r') as fin:
                dr2 = csv.DictReader(fin)
                to_db2 = [(i['Website'],
                           i['street'], i['County'], i['OtherMedia'], i['Facebook'],
                           i['Twitter'], i['Youtube'], i['Season1Date'],
                           i['Season1Time'],
                           i['Season2Date'], i['Season2Time'], i['Season3Date'], i['Season3Time'],
                           i['Season4Date'], i['Season4Time'], i['x'], i['y'], i['Location'], i['Credit'], i['WIC'],
                           i['WICcash'],
                           i['SFMNP'], i['SNAP'], i['Organic'], i['Bakedgoods'], i['Cheese'], i['Crafts'], i['Flowers'],
                           i['Eggs'], i['Seafood'], i['Herbs'], i['Vegetables'], i['Honey'], i['Jams'], i['Maple'],
                           i['Meat'],
                           i['Nursery'], i['Nuts'], i['Plants'], i['Poultry'], i['Prepared'], i['Soap'],
                           i['Trees'], i['Wine'], i['Coffee'], i['Beans'], i['Fruits'], i['Grains'], i['Juices'],
                           i['Mushrooms'], i['PetFood'], i['Tofu'], i['WildHarvested']) for i in dr2]

                cur.executemany(
                    "INSERT OR IGNORE INTO moreinfo (Website , street,County, OtherMedia, Facebook,Twitter,Youtube,"
                    "Season1Date,Season1Time,Season2Date,Season2Time,Season3Date,Season3Time,Season4Date,Season4Time,"
                    "x,y,Location,Credit,WIC,WICcash,SFMNP,SNAP,Organic,Bakedgoods,Cheese,Crafts,Flowers,Eggs,Seafood,"
                    "Herbs,Vegetables,Honey,Jams,Maple,Meat,Nursery,Nuts,Plants,Poultry,Prepared,Soap,Trees,Wine,"
                    "Coffee,Beans,Fruits,Grains,Juices,Mushrooms,PetFood,Tofu,WildHarvested) "
                    "VALUES ( ?, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,? ,"
                    "?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db2)

                con.commit()

                self.ui.label.setText('<font color=green>Файл успешно загружен!</font>')
        else:
            self.ui.label.setText('<font color=red>Вы ничего не выбрали!</font>')

    def save_file(self):

        f = QtWidgets.QFileDialog.getSaveFileName(parent=window, caption="Выбор папки",
                                                  directory=QtCore.QDir.currentPath(),
                                                  filter="CSV Format (*.csv)")
        file = f[0]
        if file != "":
            df = pd.read_sql("SELECT * FROM expenses", con)
            df.to_csv(file)
            self.ui.label.setText('<font color=green>Файл успешно выгружен!</font>')
        else:
            self.ui.label.setText('<font color=red>Вы ничего не выбрали!</font>')

    def set_column_tableview_width(self):
        self.ui.tableView.setColumnWidth(0, 70)
        self.ui.tableView.setColumnWidth(1, 230)
        self.ui.tableView.setColumnWidth(2, 120)
        self.ui.tableView.setColumnWidth(3, 120)
        self.ui.tableView.setColumnWidth(4, 60)
        self.ui.tableView.setColumnWidth(5, 50)
        self.ui.tableView.hideColumn(6)


with sq.connect("farms.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS moreinfo (
        moreinfo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Website TEXT,
        street TEXT,
        County TEXT,
        OtherMedia TEXT,
        Facebook TEXT,
        Twitter TEXT,
        Youtube TEXT,
        Season1Date TEXT,
        Season1Time TEXT,
        Season2Date TEXT,
        Season2Time TEXT,
        Season3Date TEXT,
        Season3Time TEXT,
        Season4Date TEXT,
        Season4Time TEXT,
        x TEXT,
        y TEXT,
        Location TEXT,
        Credit TEXT,
        WIC TEXT,
        WICcash TEXT,
        SFMNP TEXT,
        SNAP TEXT,
        Organic TEXT,
        Bakedgoods TEXT,
        Cheese TEXT,
        Crafts TEXT,
        Flowers TEXT,
        Eggs TEXT,
        Seafood TEXT,
        Herbs TEXT,
        Vegetables TEXT,
        Honey TEXT,
        Jams TEXT,
        Maple TEXT,
        Meat TEXT,
        Nursery TEXT,
        Nuts TEXT,
        Plants TEXT,
        Poultry TEXT,
        Prepared TEXT,
        Soap TEXT,
        Trees TEXT,
        Wine TEXT,
        Coffee TEXT,
        Beans TEXT,
        Fruits TEXT,
        Grains TEXT,
        Juices TEXT,
        Mushrooms TEXT,
        PetFood TEXT,
        Tofu TEXT,
        WildHarvested TEXT )
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS maininfo (
        FMID INT , 
        MarketName TEXT,
        city TEXT,
        State TEXT,
        zip TEXT,
        rating INTEGER,
        moreinfo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (moreinfo_id) REFERENCES moreinfo (moreinfo_id))
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        lastname VARCHAR,
        firstname VARCHAR,
        username VARCHAR,
        password VARCHAR,
        email VARCHAR )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS feedbacks (
            farm_id INTEGER,
            user_id INTEGER,
            text VARCHAR,
            FOREIGN KEY (farm_id) REFERENCES maininfo (id),
            FOREIGN KEY (user_id) REFERENCES users (id))""")

    con.commit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    login_window = LoginWindow()
    reg_form = RegistrationForm()
    con1 = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con1.setDatabaseName('farms.db')
    con1.open()
    stm = QtSql.QSqlRelationalTableModel(parent=window)
    stm2 = QtSql.QSqlRelationalTableModel(parent=window)
    # stm.setRelation(0, QtSql.QSqlRelation('categoryname', 'id_cat', 'category_name'))
    con1.close()
    # window.show()
    login_window.show()

    sys.exit(app.exec_())
