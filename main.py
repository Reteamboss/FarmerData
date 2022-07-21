from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtSql import QSqlTableModel
from designmc3 import Ui_MainWindow
from interlogindesign import Ui_LoginWindow
from rfdesign import Ui_RegFormWindow
from fildesign import Ui_Dialog
import sys
import sqlite3 as sq
import pandas as pd
# import zip_app
import csv
import time
from random import randint


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_11.clicked.connect(QtWidgets.qApp.quit)
        self.ui.pushButton_2.clicked.connect(self.show_by_category)
        self.find_result = self.ui.pushButton_2.clicked.connect(self.show_by_category)
        self.ui.pushButton_4.clicked.connect(self.show_all)
        self.ui.action_CSV.triggered.connect(self.import_from_csv)
        self.ui.tableView.setMouseTracking(True)
        self.ui.tableView.clicked.connect(self.on_click_left_button)
        self.ui.tableView.clicked.connect(self.index_farm)
        self.ui.toolButton.clicked.connect(filter_window.show)
        self.ui.tableView.setSelectionBehavior(True)
        self.ui.comboBox.currentIndexChanged.connect(self.button_activate)
        self.ui.pushButton.clicked.connect(self.add_feedback)

    def contextMenuEvent(self, e):

        self.ui.tableView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        addgrup_action = QAction(u"Delete", self)
        addgrup_action2 = QAction(u"Add", self)
        addgrup_action.triggered.connect(self.delrecord)
        addgrup_action2.triggered.connect(self.addrecord)
        self.ui.tableView.addAction(addgrup_action)
        self.ui.tableView.addAction(addgrup_action2)

        # # self.contextMenu = QMenu(self)
        # # self.contextMenu.addAction(QAction("Change", self))
        # # self.contextMenu.addAction(QAction("Delete", self))
        # # action = self.contextMenu.exec(e.globalPos())
        # try:
        #     if action.text() == "Change":
        #         print("Change action was executed")
        #     elif action.text() == "Delete":
        #         stm.removeRow()
        #
        # except:
        #     "NoneType' object has no attribute 'text'"

    def button_activate(self):
        self.ui.pushButton.setEnabled(True)

    def index_row(self):
        index_row = self.ui.tableView.currentIndex().row()
        return index_row

    def index_farm(self):
        index_farm = self.ui.tableView.model().index(MainWindow.index_row(self), 6).data()
        return index_farm

    def show_all(self):
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('maininfo')
        stm.select()
        MainWindow.set_column_tableview_width(self)
        cur.execute("SELECT * FROM maininfo")
        count = len(cur.fetchall())
        self.ui.label.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))


    def rating_calculate(self, farm_id):
        con1.open()
        cur.execute(f"SELECT rating FROM feedbacks WHERE farm_id = '{farm_id}'")
        rating_result = cur.fetchall()
        result_list = []
        for x in rating_result:
            result = x[0]
            result_list.append(result)
        rating_result_2 = float(sum(result_list) / len(result_list))
        format_rating_result = "{0:1.1f}".format(rating_result_2)

        return format_rating_result

    def rating_insert(self,farm_id):
        con1.open()
        rating = window.rating_calculate(farm_id)
        self.ui.label.setText("{}".format(rating))
        sql_update_query = """UPDATE maininfo SET rating = '{}' WHERE moreinfo_id = '{}'""".format(rating,farm_id)
        cur.execute(sql_update_query)
        con1.commit()

    def add_feedback(self):
        try:
            con1.open()
            username = login_window.sign_in()
            farm_id = window.index_farm()
            text = self.ui.textEdit.toPlainText()
            rating = int(self.ui.comboBox.currentText())
            cur.execute(f"SELECT firstname, lastname FROM users WHERE username = '{username}'")
            name = cur.fetchone()
            firstname = name[0]
            lastname = name[1]
            cur.execute("INSERT INTO feedbacks VALUES (?,?,?,?,?,?);" ,(farm_id, username, firstname, lastname, text, rating))
            window.rating_insert(farm_id)
            con1.commit()
        except:
            "NoneType' object has no attribute 'text'"




    def delrecord(self):
        con1.open()
        stm.setTable('maininfo')
        stm.select()
        stm.setEditStrategy(QSqlTableModel.OnManualSubmit)
        id = window.index_row()
        stm.removeRow(id + 1)
        stm.select()
        stm.submitAll()
        cur.execute("DELETE FROM maininfo WHERE moreinfo_id = '{}'".format(id))
        con1.commit()
        window.set_column_tableview_width()
        self.ui.label.setText('<font color=green>Запись успешно удалена!</font>')

    def addrecord(self):
        stm.insertRow(stm.rowCount())

    # def mouseMoveEvent(self, e):
    #     self.ui.label.setText("mouseMoveEvent")

    # def mouseClickEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         # handle the left-button press in here
    #         self.ui.label.setText("mousePressEvent LEFT")
    #
    #     elif e.button() == Qt.MiddleButton:
    #         # handle the middle-button press in here.
    #         self.ui.label.setText("mousePressEvent MIDDLE")
    #
    #     elif e.button() == Qt.RightButton:
    #         # handle the right-button press in here.
    #         self.ui.label.setText("mousePressEvent RIGHT")
    # def mouseReleaseEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.label.setText("mouseReleaseEvent LEFT")
    #
    #     elif e.button() == Qt.MiddleButton:
    #         self.label.setText("mouseReleaseEvent MIDDLE")
    #
    #     elif e.button() == Qt.RightButton:
    #         self.label.setText("mouseReleaseEvent RIGHT")

    def on_click_left_button(self, index):
        con1.open()
        result = self.ui.tableView.model().index(index.row(), 6).data()
        cur.execute("SELECT * FROM moreinfo WHERE moreinfo_id = '{}'".format(result))
        sql_result = list(cur.fetchone())
        cur.execute("SELECT MarketName FROM maininfo WHERE moreinfo_id = '{}'".format(result))
        market_name = list(cur.fetchone())
        MainWindow.show_more_information(self, sql_result, market_name)
        MainWindow.show_feedback(self)
        return result


    def show_feedback(self):
        try:
            tv = self.ui.tableView_2
            tv.setModel(stm2)
            con1.open()
            stm2.setTable('feedbacks')
            stm2.select()
            farm_id = window.index_farm()
            filter = f"farm_id = '{farm_id}'"
            stm2.setFilter(filter)
            tv.setColumnWidth(2, 130)
            tv.setColumnWidth(3, 130)
            tv.setColumnWidth(4, 345)
            tv.setColumnWidth(5, 40)
            tv.hideColumn(0)
            tv.hideColumn(1)

            stm2.setHeaderData(2, QtCore.Qt.Horizontal, 'FirstName')
            stm2.setHeaderData(3, QtCore.Qt.Horizontal, 'LastName')
            stm2.setHeaderData(4, QtCore.Qt.Horizontal, 'FeedBack')
            stm2.setHeaderData(5, QtCore.Qt.Horizontal, 'Rating')

        except:
            self.ui.label.setText('<font color=red>Вы ничего не выбрали!</font>')







    def show_more_information(self, sql_result, market_name):
        self.ui.label_3.setText(market_name[0])
        self.ui.label_21.setText(f'<a href="{str(sql_result[1])}">{sql_result[1]}</a>')
        self.ui.label_22.setText(sql_result[2])
        self.ui.label_23.setText(sql_result[3])
        self.ui.label_24.setText(f'<a href="{str(sql_result[4])}">{sql_result[4]}</a>')
        self.ui.label_25.setText(f'<a href="{str(sql_result[5])}">{sql_result[5]}</a>')
        self.ui.label_26.setText(f'<a href="{str(sql_result[6])}">{sql_result[6]}</a>')
        self.ui.label_27.setText(f'<a href="{str(sql_result[7])}">{sql_result[7]}</a>')
        self.ui.label_28.setText(sql_result[8])
        self.ui.label_29.setText(sql_result[9])
        self.ui.label_30.setText(sql_result[10])
        self.ui.label_31.setText(sql_result[11])
        self.ui.label_32.setText(sql_result[12])
        self.ui.label_33.setText(sql_result[13])
        self.ui.label_34.setText(sql_result[14])
        self.ui.label_35.setText(sql_result[15])
        self.ui.label_36.setText(sql_result[16])
        self.ui.label_37.setText(sql_result[17])
        self.ui.label_52.setText(sql_result[18])
        self.ui.label_67.setText(sql_result[19])
        self.ui.label_46.setText(sql_result[20])
        self.ui.label_45.setText(sql_result[21])
        self.ui.label_43.setText(sql_result[22])
        self.ui.label_54.setText(sql_result[23])
        self.ui.label_58.setText(sql_result[24])
        self.ui.label_42.setText(sql_result[25])
        self.ui.label_40.setText(sql_result[26])
        self.ui.label_44.setText(sql_result[27])
        self.ui.label_68.setText(sql_result[28])
        self.ui.label_61.setText(sql_result[29])
        self.ui.label_63.setText(sql_result[30])
        self.ui.label_55.setText(sql_result[31])
        self.ui.label_72.setText(sql_result[32])
        self.ui.label_66.setText(sql_result[33])
        self.ui.label_39.setText(sql_result[34])
        self.ui.label_73.setText(sql_result[35])
        self.ui.label_93.setText(sql_result[36])
        self.ui.label_102.setText(sql_result[37])
        self.ui.label_101.setText(sql_result[38])
        self.ui.label_91.setText(sql_result[39])
        self.ui.label_79.setText(sql_result[40])
        self.ui.label_96.setText(sql_result[41])
        self.ui.label_103.setText(sql_result[42])
        self.ui.label_90.setText(sql_result[43])
        self.ui.label_84.setText(sql_result[44])
        self.ui.label_77.setText(sql_result[45])
        self.ui.label_82.setText(sql_result[46])
        self.ui.label_100.setText(sql_result[47])
        self.ui.label_105.setText(sql_result[48])
        self.ui.label_99.setText(sql_result[49])
        self.ui.label_92.setText(sql_result[50])
        self.ui.label_98.setText(sql_result[51])
        self.ui.label_110.setText(sql_result[52])
        self.ui.label_112.setText(sql_result[53])

    def show_by_category(self):
        category = self.ui.lineEdit_2.text()
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('maininfo')

        if category != "":
            categoryfilter = f"city = '{category}' or State = '{category}' or zip = '{category}' "
            stm.setFilter(categoryfilter)
            stm.select()
            MainWindow.set_column_tableview_width(self)
            count = stm.rowCount()
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
        tv = self.ui.tableView
        tv.setModel(stm)
        tv.setSortingEnabled(True)
        tv.setColumnWidth(0, 70)
        tv.setColumnWidth(1, 230)
        tv.setColumnWidth(2, 120)
        tv.setColumnWidth(3, 120)
        tv.setColumnWidth(4, 60)
        tv.setColumnWidth(5, 50)
        tv.hideColumn(6)

        stm.setHeaderData(0, QtCore.Qt.Horizontal, 'FMID')
        stm.setHeaderData(1, QtCore.Qt.Horizontal, 'MarketName')
        stm.setHeaderData(2, QtCore.Qt.Horizontal, 'City')
        stm.setHeaderData(3, QtCore.Qt.Horizontal, 'State')
        stm.setHeaderData(4, QtCore.Qt.Horizontal, 'ZIP')
        stm.setHeaderData(5, QtCore.Qt.Horizontal, 'Rating')



class User():
    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email

class RegistrationForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.ui = Ui_RegFormWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.registration)
        self.ui.pushButton_2.clicked.connect(self.back_login_window)


    def registration(self):
        user = User(firstname=self.ui.lineEdit_2.text(),
                      lastname=self.ui.lineEdit_3.text(),
                      username=self.ui.lineEdit_4.text(),
                      password=self.ui.lineEdit_5.text(),
                      email=self.ui.lineEdit_6.text())
        cur.execute(f"SELECT username, password FROM users WHERE username = '{user.username}' AND password = '{user.password}'")

        if cur.fetchone() is None:
            cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)",
                        (user.firstname, user.lastname, user.username, user.password, user.email))
            con.commit()
            self.ui.label_7.setText("<font color=green>Вы успешно зарегестрировались!</font>")
            time.sleep(1)
            RegistrationForm.back_login_window(self)
        else:
            self.ui.label_7.setText("<font color=red>Такой логин уже существует!</font>")

    def back_login_window(serf):
        login_window.show()
        reg_form.close()


class FilterWindow(QtWidgets.QDialog):
    def __init__(self):
        super(FilterWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.currentTextChanged.connect(self.choose_city)
        self.ui.comboBox_2.currentTextChanged.connect(self.choose_zip)
        self.ui.buttonBox.accepted.connect(self.show_by_filter)
        # self.ui.buttonBox.accepted.connect(self.calculate_distance_area)
        self.ui.buttonBox.rejected.connect(self.back_main_window)

        with open("zip_codes_states.csv", 'r') as fin:
            dr2 = csv.DictReader(fin)
            to_db = [(i['zip_code'], i['latitude'], i['longitude'], i['city'], i['state'], i['county']) for i in dr2]

            cur.executemany(
                "INSERT OR IGNORE INTO zip_codes (zip_code, latitude,longitude, city, state, county) VALUES ( ?, ?, ?, ?, ?, ?);",
                to_db)

        def combobox_info():  # функция для добавления информации о городах и почтовых зип в комбобокс
            cur.execute(f"SELECT State FROM maininfo")
            self.sql = cur.fetchall()
            return self.sql

        combobox_info()
        self.state = set()
        for i in self.sql:
            self.state.update(i)
        self.ui.comboBox.addItems(self.state)

    def choose_city(self):
        self.ui.comboBox_2.clear()
        self.ui.comboBox_3.clear()
        self.choose_state = self.ui.comboBox.currentText()
        cur.execute("SELECT city FROM maininfo WHERE state = '{}'".format(self.choose_state))
        self.sql_city = cur.fetchall()
        self.city = set()
        for i in self.sql_city:
            self.city.update(i)
        self.ui.comboBox_2.addItems(self.city)

    def choose_zip(self):
        self.choose_city = self.ui.comboBox_2.currentText()
        cur.execute("SELECT zip FROM maininfo WHERE city = '{}'".format(self.choose_city))
        self.sql_city = cur.fetchall()
        self.zip_cod = set()
        for i in self.sql_city:
            self.zip_cod.update(i)
        self.ui.comboBox_3.addItems(self.zip_cod)

    def show_by_filter(self):
        filter_window.close()
        zip = self.ui.comboBox_3.currentText()
        window.ui.tableView.setModel(stm)
        con1.open()
        stm.setTable('maininfo')
        categoryfilter = f" zip = '{zip}' "
        stm.setFilter(categoryfilter)
        stm.select()
        window.set_column_tableview_width()
        count = stm.rowCount()
        con1.close()
        window.ui.label.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))

    def back_main_window(self):
        filter_window.close()
        window.show()

    # def calculate_distance_area(self):
    #     zip1 = self.ui.comboBox_3.currentText()
    #     distance_area = self.ui.lineEdit.text()
    #     cur.execute("SELECT zip_code FROM zip_codes")
    #     zip_result2 = cur.fetchall()
    #     zip2 = []
    #     true_zip = []
    #     for i in zip_result2:
    #         zip2.append(i)
    #     for x in zip2:
    #         distance = zip_app.process_dist(zip1,zip2)
    #         if distance < distance_area:
    #             true_zip.append(x)
    #     print(true_zip)


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
        cur.execute(f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")
        con.commit()
        if not cur.fetchone():
            self.ui.label_4.setText("<font color=red>Неверный логин и/или пароль!</font>")
        else:
            self.ui.label_4.setText("<font color=green>Успешно!Добро пожаловать!</font>")
            window.show()
            cur.execute(f"SELECT firstname, lastname FROM users WHERE username = '{username}' AND password = '{password}'")
            name = cur.fetchone()
            window.ui.label_113.setText(f"{name[0]} {name[1]}")
            login_window.close()
            return username

    def registration(self):
        login_window.close()
        reg_form.show()


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
        rating REAL,
        moreinfo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        FOREIGN KEY (moreinfo_id) REFERENCES moreinfo (moreinfo_id))
        """)

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        lastname VARCHAR,
        firstname VARCHAR,
        username VARCHAR PRIMARY KEY,
        password VARCHAR,
        email VARCHAR )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS feedbacks (
            farm_id INTEGER,
            user_login VARCHAR,
            firstname VARCHAR, 
            lastname VARCHAR,
            text VARCHAR,
            rating INTEGER,
            FOREIGN KEY (farm_id) REFERENCES maininfo (moreinfo_id))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS zip_codes (
                zip_code VARCHAR,
                latitude VARCHAR,
                longitude VARCHAR,
                city VARCHAR,
                state VARCHAR,
                county VARCHAR )""")

    con.commit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    filter_window = FilterWindow()
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
