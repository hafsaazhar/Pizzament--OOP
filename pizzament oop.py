import webbrowser
from abc import ABC, abstractmethod
from sqlite3.dbapi2 import OperationalError
import time
import sqlite3
import smtplib
from email.message import EmailMessage
import random
from datetime import date

# global variables
newProd = []
quantity = []
order = 0


class SDisplay(ABC):
    """ Standard Display, abstract class for class Display.
            Provides 3 methods to the user for implementation """

    @staticmethod
    def show_pizzas():
        """Displays all the products from the database to the user"""
        print()
        x = 0
        # connects to the database created for handling the products
        conn = sqlite3.connect('ProductsInfo.db')
        # creates a cursor to execute commands
        c = conn.cursor()
        c.execute('SELECT * FROM Pizzas')
        # selects everything from the table Pizzas
        f = c.fetchall()
        print("=" * 53)
        print(f'| S.No \t {"Qt.":10}{"Pizza":26} {"price"} |  ')
        print("=" * 53)
        print()
        # prints all the data with proper formatting
        for i in f:
            x += 1
            # x is the serial number and i is the tuple inside the list f
            print(f' {x})\t{i[0]:3}\t {i[1]:30}{i[2]}')
        print()

    @staticmethod
    @abstractmethod
    def show_order():
        """ Method for showing the Orders, to be implemented in
                    the concrete method of the sub class """
        pass

    @abstractmethod
    def show_users(self):
        """ Method for showing the Users, to be implemented in
                 the concrete method of the sub class """
        pass


class SUsers(ABC):
    """ Standard Users, abstract class for Users.
            Provides 2 methods to the user for implementation """

    @abstractmethod
    def user_login(self):
        """ Abstract method for logging user in,to be implemented in
                the concrete method of the sub class"""
        pass

    @abstractmethod
    def delete(self):
        """ Abstract method for deleting user,to be implemented in
                the concrete method of the sub class"""
        pass


class Store(ABC):
    """ Store, abstract class for class PizzaStore.
            Provides 2 methods to the user for implementation """

    @abstractmethod
    def order_items(self):
        """ Abstract method for taking the inputs from the user,to be implemented in
                the concrete method of the sub class"""
        pass

    @abstractmethod
    def review_order(self):
        """ Abstract method for reviewing the Order,to be implemented in
                    the concrete method of the sub class"""
        pass


class SHistory(ABC):
    """ Standard History, abstract class for class PizzaStore.
            Provides 2 methods to the user for implementation """

    @abstractmethod
    def add_to_history(self, x):
        """ Abstract method for adding to history,to be implemented in
                the concrete method of the sub class"""
        pass

    @abstractmethod
    def delete_history(self):
        """ Abstract method for deleting history,to be implemented in
                the concrete method of the sub class"""
        pass


class Display(SDisplay):
    """ Display inherits from SDisplay(abstract) contains 3 methods and uses a concrete (showPizzas)
        method from its abstract class. showUsers and showOrder method OVERRIDE the ones created in
        abstract class the showHistory() is unique to this class alone."""

    def show_users(self):
        """ Shows the username and passwords of all the users to the admin"""
        print()
        x = 0
        conn = sqlite3.connect('UserInfo.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Users')
        f = c.fetchall()
        print("=" * 53)
        print(f'S.No\t{"Username":20}Password\t\tEmail  ')
        print("=" * 53)
        print()
        for i in f:
            x += 1
            print(f'{x})\t{i[0]:20}{i[1]:}\t\t{i[2]}')
        print()

    def __neg__(self):
        """ Overloads the negative operator to display orders"""
        return Display.show_order()

    def __pos__(self):
        """ Overloads the positive operator to display the history"""
        return Display.show_history

    def __invert__(self):
        """ Overloads the invert operator to display all Pizzas"""
        return self.show_pizzas()

    @staticmethod
    def show_order():
        """ a static method displays the most recent order to the user
         that has logged in"""

        # accesses the global qt that has  quantities of the pizzas stored
        global quantity
        print()
        temp = []  # a temporary list
        conn = sqlite3.connect('OrdersInfo.db')
        c = conn.cursor()

        # selects everything along with rowid, Placed at the 0th index
        c.execute(f'SELECT rowid, * FROM Orders')
        all_orders = c.fetchall()

        for _ in all_orders:  # assigns _ to every value in all_orders iteration by iteration
            # at 0 index there's rowid column, so every id gets appended in to temp
            temp.append(_[0])

        # since temp is a list mk is the max value in it i.e the latest row
        mk = max(temp)

        # selects everything form the last row
        c.execute(f'SELECT * FROM Orders WHERE rowid = {mk}')

        # fetches a tuple
        f = c.fetchone()
        # Converts the str data of name of pizzas into a list

        y = eval(f[1])
        for i in range(len(f)-2):
            if i == 0:
                # prints the username present at the first index
                print("Username : " + f[i])
                print("Dated : "+f[3])
                print("Time : " + f[4])

            elif i == 1:
                print('Order : ', end='')
                _ = 0
                for x in y:
                    # increments the value, acts as the serial number
                    _ += 1

                    # qt[_-1] shows the quantity of the pizza
                    print(str(_) + ")", x, end=f' x{quantity[_ - 1]}   ')
            else:
                print()
                # prints the total which is at the last index(2) of the tuple
                print('Total bill : ' + str(f[2]))
        print()

    @staticmethod
    def show_history():
        """ a static method displays the history of the user
             that has logged in"""

        # uses the username of the user class
        un = Users.Loger_Username
        conn = sqlite3.connect('History.db')
        c = conn.cursor()
        # selects the row of the currently logged in user
        c.execute(f"SELECT * FROM History WHERE Username ='{un}'")
        f = c.fetchone()

        # The row must have atleast some value
        if f is not None:

            # converts all the 5 str assigned at diff indices to list
            x = eval(f[1])
            y = eval(f[2])
            z = eval(f[3])
            a = eval(f[5])
            b = eval(f[6])
            for _ in range(len(f)):
                if _ == 0:
                    # prints the username present at the first index
                    print(f'\nUSERNAME : {f[_]}')
                    print(f'{"="*12}{"="*len(f[_])}')
                    print()
                elif _ == 1:
                    s = 0
                    print('ALL ORDERS UPTIL NOW : ')
                    print("**********************")
                    # x is a nested list of orders
                    for i in x:
                        print()
                        # increments s which serves as the serial number
                        s += 1
                        print(str(s) + ")", end=' ')
                        print("Dated : " + a[s-1])
                        print("Time : " + b[s-1])
                        count = -1
                        for j in i:
                            count += 1

                            # prints all the orders which were bought it a single session
                            print(j, end=" ")

                            # prints each pizza's count in front of it
                            print('x' + str(y[s - 1][count]), end='  ')

                        # the total at the end
                        print(':' + str(z[s - 1]))

                # prints the total of all the bills
                elif _ == 4:
                    print()
                    print('Total Expenditure : ' + str(f[_]))
        else:
            print('There is no history to display!')


class History:
    """ History inherits from SHistory(abstract) contains 4 methods.
        AddToHistory  and deleteHistory method OVERRIDE the ones created in
        abstract class the __init__ and checkHistory are unique to this class alone."""
    confirmation = 0

    def __init__(self):
        """Creates a History.db database and a table named History
        with 5 columns in it, every time it is called. But if the table
         already exists it simply passes"""

        try:
            conn = sqlite3.connect('History.db')
            c = conn.cursor()

            # creates a table in the database(History) with 5 columns (Username,
            # AllOrders, AllQuantities, Bills, AllPayments)

            c.execute("CREATE TABLE History (Username TEXT, AllOrders TEXT,"
                      " AllQuantities TEXT, Bills TEXT , AllPayments INTEGER, Dates TEXT, Times TEXT)")
            conn.commit()
        except OperationalError:
            # passes if the table History already exists
            pass

    @staticmethod
    def add_to_history(un):
        """Adds a row in the database with the username passed as argument"""

        conn = sqlite3.connect('History.db')
        c = conn.cursor()
        # adds username(un) to the first column and empty list in the next 3
        # and 0 in the last one
        c.execute('INSERT INTO History VALUES(?,?,?,?,?,?,?)', (un, '[]', '[]', '[]', 0, '[]', '[]'))
        # commits the program
        conn.commit()
        # closes the connection
        conn.close()

    @staticmethod
    def check_history(un):
        """Checks if the username is already in the database or not.
        Returns True if the argument is not present in the History database
        or vice versa"""

        temp = []  # a temporary list
        conn = sqlite3.connect('History.db')
        c = conn.cursor()
        c.execute('SELECT * FROM History')
        f = c.fetchall()
        for _ in f:
            # appends all the username in temp
            temp.append(_[0])
        # checks ths username is in the list or not
        return un not in temp

    @staticmethod
    def delete_history():
        """Deletes the history of the user"""

        print('Are you sure you want to delete your order history? (y/n)')
        ques = input().capitalize()  # capitalizes the input to only Y/N
        if ques == 'Y':
            conn = sqlite3.connect('History.db')
            c = conn.cursor()
            # deletes the row starting with th given username
            c.execute(f"DELETE FROM History WHERE Username = '{Users.Loger_Username}'", )
            conn.commit()
            conn.close()
        elif ques == 'N':
            print('Nice choice, maintaining history is a good thing :) ')
        else:
            print("Select a valid option!")

    @staticmethod
    def confirm():
        """Confirms the payment and adds the confirmed
         order into the history"""

        # calls global variable
        global quantity

        if History.confirmation == 0:
            # checks whether user has ordered or not
            if order == 1:

                print()
                temp = []  # a temporary list

                # connects to orders database
                conn = sqlite3.connect('OrdersInfo.db')
                c = conn.cursor()
                # Selects everything from the database
                c.execute(f'SELECT rowid, * FROM Orders')
                all_orders = c.fetchall()
                # iterates through each tuple in the list
                for _ in all_orders:
                    # appends the rowid in the temporary list
                    temp.append(_[0])
                # gets the latest rowid
                max_row_id = max(temp)
                # Selects the latest order from orders database
                c.execute(f'SELECT * FROM Orders WHERE rowid = {max_row_id}')
                f = c.fetchone()

                # converts str into list
                y = eval(f[1])
                conn.close()
                # connects to history database
                conn1 = sqlite3.connect('History.db')
                c1 = conn1.cursor()
                # selects everything from the row of the currently logged in user
                c1.execute(f"SELECT * FROM History WHERE Username ='{Users.Loger_Username}' ")
                user_history = c1.fetchone()

                # converts the str in list and and appends flavours into the list
                lst = eval(user_history[1])
                lst.append(y)
                # converts the str in list and and appends quantities into the list
                lst2 = eval(user_history[2])
                lst2.append(quantity)
                # converts the str in list and and appends bills into the list
                lst3 = eval(user_history[3])
                lst3.append(f[2])
                # adds the newest bill into the old ones
                temp = list(user_history)
                temp[4] += f[2]
                # adds the current date into the list of previous ones
                lst4 = eval(user_history[5])
                lst4.append(PizzaStore.today)
                # adds the current into into the list of previous ones
                lst5 = eval(user_history[6])
                lst5.append(PizzaStore.Time)

                # Updates the history table (Username, AllQuantities, Bills, AllPayments)
                c1.execute("UPDATE History SET AllOrders = ? WHERE Username = ? ", (str(lst), Users.Loger_Username))
                conn1.commit()
                c1.execute("UPDATE History SET AllQuantities = ? WHERE Username = ? ",
                           (str(lst2), Users.Loger_Username))
                conn1.commit()
                c1.execute("UPDATE History SET Bills = ? WHERE Username = ? ", (str(lst3), Users.Loger_Username))
                conn1.commit()
                c1.execute("UPDATE History SET AllPayments = ? WHERE Username = ? ",
                           (temp[4], Users.Loger_Username))
                conn1.commit()
                c1.execute("UPDATE History SET Dates = ? WHERE Username = ? ", (str(lst4), Users.Loger_Username))
                conn1.commit()
                c1.execute("UPDATE History SET Times = ? WHERE Username = ? ", (str(lst5), Users.Loger_Username))
                conn1.commit()
                conn1.close()

                while True:
                    x = input('''Select method of payment
1) Credit card
2) Cash\n        
Your option : ''')
                    if x == "1":
                        print('Enter your Card no. and Bank name : ')
                        input()
                        time.sleep(0.5)
                        print('Payment received. ')
                        # changes the global variable, allows the user to use the exit option
                        History.confirmation = 1
                        break
                    elif x == '2':
                        print()
                        print('Please leave the cash inside the Bill holder :)')
                        # changes the global variable, allows the user to use the exit option
                        History.confirmation = 1
                        break
                    else:
                        print()
                        print("Please select a valid option!")
                        continue
            else:
                print('Please order before selecting this option!')

        else:
            print("You have already paid")


class PizzaStore(Store):
    """ PizzaStore inherits from Store(abstract) contains 6 methods.
    Order and reviewOrder method OVERRIDE the ones created in
    abstract class the __init__ and setDefault Items are unique to this class alone
    checkProducts and setNewProd are static methods.
    Association(composition) is used in connecting PizzaStore to Display  """

    today = ''
    Time = " "
    total = 0

    def __init__(self):
        """Creates the attributes of PizzaStore upon instantiation"""

        self.pizza1 = 'Cheese Pizza'
        self.pizza2 = 'Veggie Pizza'
        self.pizza4 = 'Meat Pizza'
        self.pizza5 = 'Margherita Pizza'
        self.pizza3 = 'Pepperoni Pizza'
        self.pizza6 = 'BBQ Chicken Pizza'
        self.pizza7 = 'Hawaiian Pizza'
        self.pizza8 = 'Diet Pizza'
        self.pizza9 = 'Mushroom Pizza'
        self.pizza10 = 'Pineapple Pizza'
        self.quantity1 = 50
        self.quantity2 = 40
        self.quantity3 = 30
        self.quantity4 = 20
        self.quantity5 = 10
        self.quantity6 = 60
        self.quantity7 = 5
        self.quantity8 = 0
        self.quantity9 = 15
        self.quantity10 = 0
        self.price1 = 1350
        self.price2 = 1200
        self.price3 = 1600
        self.price4 = 1450
        self.price5 = 1150
        self.price6 = 1550
        self.price7 = 1400
        self.price8 = 850
        self.price9 = 950
        self.price10 = 1300
        self.x = [(self.quantity1, self.pizza1, self.price1), (self.quantity2, self.pizza2, self.price2),
                  (self.quantity3, self.pizza5, self.price5), (self.quantity4, self.pizza6, self.price6),
                  (self.quantity5, self.pizza7, self.price7), (self.quantity6, self.pizza8, self.price8),
                  (self.quantity7, self.pizza3, self.price3), (self.quantity8, self.pizza4, self.price4),
                  (self.quantity9, self.pizza9, self.price9), (self.quantity10, self.pizza10, self.price10)]
        self.display = Display()  # an object is created of Display class. (composition)
        self.ordering_quantity = []

    @staticmethod
    def check_products(x):
        """ Checks where the argument is present in the
        list of those who are sold out"""
        temp = []
        conn = sqlite3.connect('ProductsInfo.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Pizzas')
        y = c.fetchall()
        for i in range(len(y)):
            if y[i][0] == 0:
                # appends the flavours of Pizza that are sold out in a list
                temp.append(y[i][1])
        # checks where the argument is present in that list
        return x not in temp

    def set_default_items(self):
        """ Sets the default values in the table Pizzas"""

        conn = sqlite3.connect('ProductsInfo.db')
        c = conn.cursor()
        # If the table is not created, create it
        try:
            c.execute('CREATE TABLE Pizzas(Quantity INTEGER, Flavours TEXT, Price INTEGER)')
            c.executemany('INSERT INTO Pizzas VALUES (?, ?, ?)', self.x)
            conn.commit()
        # Otherwise Pass
        except sqlite3.OperationalError:
            pass

    @staticmethod
    def set_new_prod():
        """Assigns all of info from the Pizzas(table) to a global variable"""
        global newProd
        conn = sqlite3.connect("ProductsInfo.db")
        c = conn.cursor()
        c.execute('SELECT * FROM Pizzas')
        newProd = c.fetchall()

    def order_items(self):
        """Displays all the products from the Pizzas table, takes the input of
        Pizza's Serial and quantity. Subtracts the quantity
        that you have bought from the data base. and calculates the total bill.
        then saves all of it in the Order's database"""

        # saves the present day's date into a class variable
        Today = date.today()
        PizzaStore.today = Today.strftime('%d-%m-%y')
        # saves the current time into a class variable
        PizzaStore.Time = time.strftime("%I:%M:%S %p")

        print()
        print('YOU CAN ONLY ORDER ONCE, PLEASE PROCEED CAUTIOUSLY !')
        print('Tip: choose more, you can edit the order by Review Order option!')

        # calls the global variable
        global quantity
        History.confirmation = 0

        # sets the default value in a separate list
        PizzaStore.set_new_prod()
        conn = sqlite3.connect('OrdersInfo.db')
        c = conn.cursor()
        # creates a table, if not present already
        try:
            c.execute('CREATE TABLE Orders(Username TEXT, Pizzas TEXT, Total INTEGER, Date TEXT, Time TEXT)')
            conn.commit()
        # otherwise passes
        except sqlite3.OperationalError:
            pass

        self.order = []  # a temporary list
        # a temporary list to store all quantities selected
        self.totalOrder = []
        temp = []  # a temporary list
        count1 = 0  # a variable that is to be incremented
        flag = 1
        while flag:
            try:
                conn2 = sqlite3.connect('ProductsInfo.db')
                c2 = conn2.cursor()
                # displays all pizzas from the data base
                # self.d.showPizzas()
                ~self.display
                p = int(input('Enter the serial number of the pizza you want to buy : '))
                q = int(input('Enter the quantity : '))
                # appends the entered quantity into a list
                self.ordering_quantity.append(q)
                # a variable to use the list ordering quantity outside this scope
                quantity = self.ordering_quantity

                c2.execute('SELECT * FROM Pizzas')
                total_no_of_items = c2.fetchall()

                # checks whether the input is positive and S.no is correct
                if 1 <= p <= len(total_no_of_items) and 0 <= q:
                    self.order.append([p - 1, q])

                    # checks whether the entered serial number is sold out or not
                    if PizzaStore.check_products(newProd[self.order[0][0]][1]):
                        # selects the whole row of the pizza associated with the selected serial number
                        c2.execute(f'SELECT * FROM Pizzas WHERE Flavours ="{newProd[self.order[0][0]][1]}"')
                        y = c2.fetchone()
                        # appends all the contents in a list after type casting the tuple into the list
                        self.totalOrder.append(list(y))

                        # checks whether the quantity of a the selected pizza is possible to provide
                        if self.totalOrder[count1][0] < q:

                            print()
                            print(f'Sorry, We can\'t provide that many '
                                  f'{newProd[self.order[0][0]][1]} at the moment. '
                                  f'Please try a different one :')

                            # if there is an unreasonable input all values are set back to default
                            self.totalOrder.pop()  # the recently added contents are discarded
                            self.order.clear()  # the temporary list is cleared
                            self.order = []  # or this
                            temp = []  # the temporary list is cleared
                            quantity.pop()  # the recently added contents are discarded
                            continue

                        else:
                            # subtracts the quantity ordered of the selected pizza from the database
                            self.totalOrder[count1][0] -= q
                        # Calculates the total by multiplying the quantity to the price
                        PizzaStore.total += q * y[2]

                        # sets the new quantity in the database
                        c2.execute(f'UPDATE Pizzas SET Quantity = {self.totalOrder[count1][0]} WHERE\
                        Flavours ="{newProd[self.order[0][0]][1]}"')

                        conn2.commit()
                        conn2.close()
                        # increases the count so that the next item in the order can get calculated
                        count1 += 1
                        self.order.clear()

                    else:
                        print()
                        print('Sorry, that one is completely sold out.\nPlease, select another one :( ')
                        self.order.clear()
                        continue

                    print()
                    while True:
                        print('Do you want to order other pizzas too ? (y/n)')
                        p = input().capitalize()
                        if p == 'N':

                            # the while loop breaks
                            flag = 0
                            # accesses every order of the total Order

                            for i in self.totalOrder:
                                # all of the Pizzas of each order are appended to a list

                                temp.append(i[1])
                            # all values are inserted into a table in another database

                            c.execute("INSERT INTO Orders VALUES (?,?,?,?,?)",
                                      (Users.Loger_Username, str(temp), PizzaStore.total, PizzaStore.today, PizzaStore.Time))
                            conn.commit()
                            conn.close()
                            temp = []
                            # the overloaded operator displays the latest order
                            # self.d.showOrder()
                            -self.display
                            # a check is maintained so that one can only Order once
                            global order
                            order = 1
                            break
                        elif p == 'Y':
                            break
                        else:
                            print('Enter a valid option!')
                else:
                    print()
                    print('Please select a valid value!')
                    self.ordering_quantity.pop()
            # if the user makes error in inputs
            except ValueError:
                print()
                print('Oops! You made an error in the input.')
            except IndexError:
                print()
                print('Please review the menu and try again.')

    def review_order(self):
        """Allows the user to delete the item, he wishes not to buy
        and updates the the database according to the new values"""

        # checks if the person has ordered
        if order == 0:
            print('Please order first!')

        else:
            # calls the global variable that has all the Values stored in it
            global quantity

            -self.display
            print('Do you want to confirm the order? (y/n) ')
            print('Select (y), if u don\'t want to make any changes. '
                  'Select (n), if u want to edit your order.')
            print('You can only edit a single entry, to change more '
                  'Reuse the Review Order option')

            while True:
                try:
                    option = input("Your selection : ").capitalize()
                    if option == 'Y':
                        break

                    elif option == "N":
                        sno = int(input('Enter the serial number of the Pizza (FROM YOUR ORDER) '
                                        ' you wish to delete : '))
                        quant = int(input('Enter the quantity you want '
                                          'to be removed of the selected Pizza : '))
                        print()
                        temp = []  # a temp list

                        # connects to Order's database
                        conn = sqlite3.connect('OrdersInfo.db')
                        c = conn.cursor()
                        c.execute(f'SELECT rowid, * FROM Orders')
                        # all_orders fetches all the value from the Orders table
                        all_orders = c.fetchall()

                        # iterates through the list all_orders(which has tuples as its items)
                        for _ in all_orders:
                            # stores all of the row ids in a temporary list
                            temp.append(_[0])
                        # max_row_id is assigned as the last row number
                        max_row_id = max(temp)

                        # selects the last order made
                        c.execute(f'SELECT * FROM Orders WHERE rowid = {max_row_id}')
                        f = c.fetchone()
                        # converts the pizzas ordered into a list
                        y = eval(f[1])

                        # checks if the inputs are reasonable
                        if 0 <= sno <= len(y) and 0 <= quant <= quantity[sno - 1]:
                            # selects the pizza flavour from the ordered list
                            s = y[sno - 1]
                            # connects to Products' database
                            conn1 = sqlite3.connect('ProductsInfo.db')
                            c1 = conn1.cursor()
                            # searches the content of the pizza name selected
                            c1.execute(f'SELECT * FROM Pizzas WHERE Flavours = "{s}"')
                            f1 = c1.fetchone()
                            # assigns the f2 the list of all contents of the selected pizza
                            f2 = list(f1)
                            # adds the deleted Pizza's quantity back to the table
                            f2[0] += quant
                            # updates the table's quantity column
                            c1.execute('UPDATE Pizzas SET Quantity =? WHERE Flavours =?', (f2[0], s))
                            conn1.commit()
                            # closes the connection
                            conn1.close()

                            # subtracts the amount from the total payment
                            PizzaStore.total -= f1[2] * quant

                            # subtracts the quantity of a particular pizza from the order
                            quantity[sno - 1] = self.ordering_quantity[sno - 1] - quant

                            # total of the Orders table is updated, if quantity =0 then name of the pizza
                            # gets removed as well and the table updates
                            if quantity[sno - 1] == 0:
                                quantity.pop(sno-1)
                                y.pop(sno - 1)
                                c.execute(f'UPDATE Orders SET Pizzas ="{y}" WHERE rowid ={max_row_id}')
                                conn.commit()
                                c.execute(f'UPDATE Orders SET Total = {PizzaStore.total} WHERE rowid ={max_row_id} ')
                                conn.commit()
                                conn.close()
                                print("The cancelled pizza has been successfully sent back to the store. ")
                                break
                            # if the quantity is not zero the name of the pizza stays
                            else:
                                c.execute(f'UPDATE Orders SET Total = {PizzaStore.total} WHERE rowid ={max_row_id} ')
                                conn.commit()
                                conn.close()
                                print("*The cancelled quantity has been successfully sent back to the store* ")
                                break
                        else:
                            print('PLEASE ENTER VAlID VALUES')
                    else:
                        print("Try again")
                        raise ValueError

                except ValueError:
                    continue

            print('Your Order is :')
            self.display.show_order()


class Users(SUsers):
    """Users inherits from the SUsers(abstract). Its interlinked with PizzaStore and
    History through association(composition). Has 6 methods, userLogin and
    delete are Overridden from that of the base class. __init__ and verify
    are its own unique concrete methods. checkUser and generateCode are kept
        static"""

    Loger_Username = ''

    def __init__(self):
        """Creates the attributes of Users upon instantiation"""
        self.Options = PizzaStore()
        self.secCode = ''
        self.username = ''
        self.xcount = 0
        self.history = History()  # Composition between user and history

    # if there isn't, a table it gets created
    try:
        conn = sqlite3.connect('UserInfo.db')  # Creates a Users database
        c = conn.cursor()
        c.execute('CREATE TABLE Users'  # creates the table with 3 columns
                  '(Username TEXT, Password TEXT, Email TEXT)')
        conn.commit()
        conn.close()
    # else it passes
    except OperationalError:
        pass

    @staticmethod
    def check_user(x):
        """Checks whether the Username has been already assigned to
        a user or not. Returns True if not already in database
        and vice versa"""

        temp = []  # a temporary list
        conn = sqlite3.connect('UserInfo.db')
        c = conn.cursor()
        c.execute("SELECT Username FROM Users")  # selects all the usernames
        y = c.fetchall()

        # iterates through every item(tuple) in y(list)
        for i in range(len(y)):
            # in every item the first item is a username, so appending that to the list
            temp.append(y[i][0])
        # checks if the argument is present in the list
        return x not in temp

    @staticmethod
    def generate_code():
        """Creates a random 6-digit code"""

        random_string = ''  # an empty string
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        # adds a random character in an empty string for 6 times
        for _ in range(6):
            random_string += random.choice(string)
        return random_string

    def verify(self):
        """verifies that whether the user is authentic or not by using
        email confirmation"""

        while True:
            try:

                self.user_email = input('Enter your authentic email address : ')
                # connects to the SMTP server
                server = smtplib.SMTP('smtp.gmail.com', 587)
                # makes the connection secure
                server.starttls()
                admin_email = 'cepOOPproject@gmail.com'
                # logs in the server with the provided email address and password
                server.login(admin_email, 'whatismypassword')
            except Exception:

                print()
                print('Please check your internet connection and try again. ')
                continue

            else:
                try:
                    # creates an object of email class
                    email = EmailMessage()
                    # takes sender's email
                    email['From'] = admin_email
                    # takes sender's subject
                    email["Subject"] = 'Your verification Code'
                    # takes the receiver's email
                    email['To'] = self.user_email
                    # sets a code that is to be sent
                    self.secCode = Users.generate_code()
                    # sets the content of the message to the code produced
                    email.set_content(self.secCode)
                    # sends the email
                    server.send_message(email)
                    # closes the server
                    server.close()
                    print()
                    print('email sent successfully!')
                    # delays the code for 1 second
                    time.sleep(1)
                    print('Please check your inbox and spam folder in 5 seconds.')
                    break
                # deals with the error
                except smtplib.SMTPRecipientsRefused:
                    print()
                    print('Such email doesn\'t exist!')
                    continue

    def user_login(self):
        """logs in the user, verifies first if the user is new"""

        # connects to the Users database
        conn = sqlite3.connect('UserInfo.db')
        c = conn.cursor()
        while True:
            try:
                print("Do you already have an account? (y/n)")
                ques = input().capitalize()
                if ques == "N":
                    # runs the verification algorithm
                    Users.verify(self)
                    code = input('Please Enter the code here : ')
                    while True:
                        # checks if the code from the email and input are same
                        if self.secCode == code:
                            self.username = input('Enter your username : ')
                            # sets the value for global username to the name entered
                            Users.Loger_Username = self.username
                            self.password = input('Enter your password : ')

                            # checks if the username and password are strong
                            if len(self.username) >= 8 and len(self.password) >= 7:
                                # checks if the username exists
                                x = Users.check_user(self.username)
                                if x:
                                    # inserts into the table Users the new username, email and password
                                    c.execute('INSERT INTO Users VALUES (?,?,?)',
                                              (self.username, self.password, self.user_email))
                                    conn.commit()
                                    conn.close()
                                    # adds the username to to the History.db
                                    self.history.add_to_history(self.username)
                                    break

                                else:
                                    print()
                                    print('Sorry, this username has already been taken.')
                                    continue
                            else:
                                print()
                                print("Username and Password should be greater than 7 characters.")
                                continue
                        else:
                            print()
                            print('The code is invalid!')
                            code = input('Please enter the code here : ')
                            continue

                elif ques == "Y":
                    while True:
                        self.username = input('Enter your username : ')
                        # sets the value for class username to the name entered
                        Users.Loger_Username = self.username
                        self.password = input('Enter your password : ')
                        # connects to the users database
                        conn = sqlite3.connect('UserInfo.db')
                        c = conn.cursor()
                        # selects the password from database against the username provided
                        c.execute(f"SELECT Password FROM Users WHERE Username = '{self.username}'")
                        x = c.fetchone()
                        # checks if the entered password matches to that saved in the database
                        if x[0] == self.password:
                            # for admin
                            if self.password == 'Hafsa':
                                print('The system has recognized the user as Admin...')
                            print()
                            print('User logged in successfully!')
                            # checks if the username is not present in the history database
                            if self.history.check_history(self.username):
                                # adds the user to the database if not
                                self.history.add_to_history(self.username)
                            else:
                                pass
                            break

                        else:
                            print()
                            print('The password does not match with the given username. ')
                            continue

                else:
                    print()
                    print("Please select a valid option!")
                    continue
            except TypeError:
                print()
                print("Such Account Doesn't Exist!")
                continue

            else:
                break

    def delete(self):
        """Allows the user to delete his/her account"""

        # creates an instance count variable
        self.xcount = 0
        print('Are you sure you want to delete your account? (y/n)')
        ques = input().capitalize()
        if ques == 'Y':
            # connects to the database
            conn = sqlite3.connect('UserInfo.db')
            c = conn.cursor()
            # deletes the row from the database, associated with the entered username
            c.execute(f"DELETE FROM Users WHERE Username ='{self.username}'")
            conn.commit()
            conn.close()

            print()
            print('Account deleted successfully!')
            # increases the count
            self.xcount += 1
        else:
            print()
            print('Please continue to support us.')


class Admin(Users, PizzaStore, Display):
    """Admin inherits form Users, PizzaStore, Display"""

    def __init__(self):
        """Loads the admin account in the database"""

        self.history = History()
        # connects to the Users database
        conn = sqlite3.connect('UserInfo.db')
        c = conn.cursor()
        c.execute("SELECT * FROM Users ")
        f = c.fetchone()
        # checks if the database is empty
        if f is None:
            # inserts admin's username and password to the database by default
            c.execute("INSERT INTO Users VALUES('Mudasir', 'Hafsa', 'Rafay')")
            conn.commit()
            conn.close()
        else:
            pass

    @staticmethod
    def add_product():
        """Adds an admin defined product in the Products database"""

        qt = int(input('Enter the quantity of the pizza : '))
        flavour = input('Enter the flavour of th pizza : ')
        price = int(input('Enter the price of the pizza : '))
        # connects to the Products database:
        conn = sqlite3.connect('ProductsInfo.db')
        c = conn.cursor()
        # adds the specified values to a new row in the database
        c.execute('INSERT INTO Pizzas VALUES (?,?,?)', (qt, flavour, price))
        conn.commit()

    def delete(self):
        """ Deletes a user account"""

        username = input('Enter the name of the user you want to delete: ')
        # connects to the users database
        conn = sqlite3.connect('UserInfo.db')
        c = conn.cursor()
        # deletes the specified User from the database
        c.execute(f"DELETE FROM Users WHERE Username ='{username}'")
        conn.commit()
        conn.close()

    @staticmethod
    def delete_history():
        """Deletes a user's history"""

        username = input('Enter the name of the user you want to delete: ')
        # connects to the users database
        conn = sqlite3.connect('History.db')
        c = conn.cursor()
        # deletes the specified history from the database
        c.execute(f"DELETE FROM History WHERE Username = '{username}'")
        conn.commit()
        conn.close()

    def show_history(self):
        """Overrides the showHistory method. Displays
        the history of any specified user"""

        # connects to the history database
        name = input('Enter the name of the user : ')

        if name != 'Mudasir':
            Users.Loger_Username = name

            conn = sqlite3.connect('History.db')
            c = conn.cursor()
            # selects the row of the currently logged in user
            c.execute(f"SELECT * FROM History WHERE Username ='{Users.Loger_Username}'")
            f = c.fetchone()

            # The row must have atleast some value
            if f is not None:
                # Calls the showHistory method of the super class Display
                super().show_history()

            else:
                print('There is no history to display.')

        else:
            print()
            print('You can\'t order as admin, nor your history is maintained.\n'
                  ' Log in as a user if you want to do that')
            print()


# since the rest of the code that follows, is in procedural manner.
# Hence keeping it safe. Only the code above this statement will be accessible in another module if imported.


if __name__ == '__main__':

    def exit_():
        """Exits the inner loop of the user/admin options menu"""

        # calls the global variable
        global quantity
        global order
        quantity = []  # clears it

        PizzaStore.total = 0  # sets its default value

        # checks whether user has payed or not
        if History.confirmation == 1:

            global flag  # calls the global flag
            print('Are you sure you want to exit ? (y/n) ')
            ans = input().capitalize()
            if ans == 'Y':
                flag = 0  # breaks the loop
                order = 0  # sets its default value
            else:
                print('')
        else:
            print()
            print("**Please pay before exiting**")

# TODO ----------------------------------------------------------------------------------------------
    print("Kindly configure your IDLE to size: 10 with an indent spacing of 4. Thank you! ")
    print()
    print("\t\t*******     Welcome to  THE PIZZAMENT     ********")
    print("\t\t" + "=" * 50)

    while True:
        print('''\nHow do you want to proceed?
1) Command Line Interface
2) Web view
3) Close''')
        try:

            choice = int(input("\nSelect your option : "))
            if choice == 1:

                # Runs the menu in an infinite loop
                while True:
                    try:
                        print()
                        x = input('''How do you want to login as?
1) User
2) Admin
3) Exit
Your Option : ''')
                        if x == "1":
                            a = Admin()  # object of Admin
                            u = Users()  # object of Users
                            u.user_login()  # calls User's login method

                            flag = 1
                            while flag:
                                # dictionary for accessing the methods
                                user_options = {'1': u.Options.order_items, '2': u.Options.review_order,
                                                '3': u.history.confirm, '4': u.delete,'5': +u.Options.display,
                                                '6': u.history.delete_history, '7': exit_}
                                print()
                                print('''\nWhich of the following options do you want to perform?
1) Order
2) Review Order
3) Proceed to payment
4) Delete account
5) Show History
6) Delete History
7) Exit \n''')
                                user_selection = input('Your option : ')
                                p = PizzaStore()  # object of PizzaStore
                                p.set_default_items()  # sets default items into a list

                                # Maintains a check that user only orders once
                                if order == 1 and user_selection == '1':
                                    print('You can only order once! \nPlease exit and try again.')
                                    continue
                                else:
                                    # checks for invalid input
                                    if '1' <= user_selection <= '6':
                                        # calls the selected function from the dictionary

                                        user_options.get(user_selection)()
                                        # exits the user options menu if account is deleted
                                        if user_selection == '4' and u.xcount == 1:
                                            flag = 0

                                    elif user_selection == '7':
                                        if History.confirmation == 1:
                                            user_options.get('7')()
                                        else:
                                            print("\nPlease pay before exiting!")

                                    else:
                                        print('Please select a valid option!')
                                        continue

                        elif x == "2":
                            print('\nHint: admin username is Mudasir, password is Hafsa and Email is Raffay ')
                            a = Admin()  # object of Admin
                            a.user_login()  # user login algorithm

                            if a.username == 'Mudasir' and a.password == 'Hafsa':
                                flag = 1
                                while flag:
                                    # admin can exit whenever he wants
                                    History.confirmation = 1
                                    admin_options = {'1': a.show_pizzas, '2': a.add_product, '3': a.show_users,
                                                     '4': a.delete, "5": a.show_history,
                                                     '6': a.delete_history, '7': exit_}
                                    print('''\nWhich of the following options do you want to perform ?
1) Show all products
2) Add products
3) Show all users
4) Delete a user
5) Show History
6) Delete History
7) Exit''')
                                    admin_selection = input('Your option : ')
                                    p = PizzaStore()  # object of PizzaStore
                                    p.set_default_items()  # sets default items into a list

                                    # checks for invalid input
                                    if '1' <= admin_selection <= '7':
                                        # calls the selected function from the dictionary
                                        admin_options.get(admin_selection)()
                                    else:
                                        print('Please select a valid option!')
                                        continue
                            else:
                                print('You are not registered as an admin.')
                                print('Logging out')
                                for i in range(4):
                                    print('.')
                                    # delays the code for 0.3 seconds
                                    time.sleep(0.3)
                                print()

                                continue
                        elif x == '3':
                            print()
                            print('Hope you have a great day! :)')
                            break

                        else:
                            print()
                            print('Enter a valid option please!')
                            continue

                    except OperationalError:
                        print('There is no data on the user!')

                    # catches any sort of exception
                    except Exception:
                        print('Oops! something went wrong, please try again.')

            elif choice == 2:
                print()
                # opens the link in browser in a new tab
                webbrowser.open_new_tab("http://raffay2001.pythonanywhere.com/")
                time.sleep(5)

            elif choice == 3:
                print('''Was tha application good enough ?
1) Yes
2) No''')
                views = int(input('Select your option: '))
                if views == 1:
                    print('\nThank you for liking it, hope to serve you again :)')
                    break
                elif views == 2:
                    print('\nWe\'ll try better next time :)')
                    break
                else:
                    print('Please select a valid option 1')
            else:
                print('Please enter a valid option 1')

        except ValueError:
            print("You can only select the above mentioned options.")
