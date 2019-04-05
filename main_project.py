import csv
import sqlite3
import time
import pandas


"""
By Tomas Lozano - 040869662
CST8333 Programming Language Research Project
Last modified: 2018-12-01

This project loads a database with a csv file information and gives you the options to
read, write and delete from the file. Also you have more options in the menu like
asking for help with the commands, the authors information or closing the file and 
database connection
"""
#Generic class that gives the parameters for the Authors information
#Author Tomas Lozano
#Last modified: 2018-12-01
class info:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    def myInfo(self):
        return "By " + self.first + " " + self.last

#Class that inherits the information from info Class and adds the authors ID
#Author Tomas Lozano
#Last modified: 2018-12-01
class myInfo(info):
    def __init__(self, first, last, ID):
        info.__init__(self, first, last)
        self.ID = ID

    def allTheInfo(self):
        return self.myInfo() + " - " + self.ID

#Class that loads the csv file into a database and works with the database.
#Author Tomas Lozano
#Last modified: 2018-12-01
class Assign (myInfo):

    #Class constructor
    def __init__(self, first, last, ID):
         myInfo.__init__(self, first, last, ID)

    #Main method that starts the project
    def main(self):
        self.db_filename = 'csv.db'
        
        print("By Tomas Lozano - 040869662")
        print("CST8333 Programming Language Research Project")
        print("Last modified: 2018-12-01\n")
        
        #Welcome and ask the user if they want to load the file.
        print ("Welcome to the automated sorting system")

        #Takes the input from the user
        openFile = input("Do you want to load the file? Y/N: ")
        
        #If the input from the user is Y, then the file is opened
        #In case you want to exit the program without loading, you just input N
        if (openFile == "Y" or openFile == "yes" or openFile == "Yes" or openFile == "y"):

            self.dr = pandas.read_csv('32100054.csv')

            
            #print("col names", list(self.dr)) # column names
            #print("col count", len(list(self.dr))) # column count
            #print("row count", len(self.dr)) # row count

            #Connection to the database
            self.conn = sqlite3.connect(self.db_filename)
                
            self.cursor = self.conn.cursor()
            #Creation of the table
            self.cursor.execute("DROP TABLE IF EXISTS food")
            self.cursor.execute("""
                CREATE TABLE food
                (REF_DATE TEXT, GEO TEXT, DGUID TEXT, FoodCategories TEXT, Commodity TEXT, UOM TEXT, UOM_ID TEXT,
                SCALAR_FACTOR TEXT, SCALAR_ID TEXT, VECTOR TEXT, COORDINATE TEXT, VALUE TEXT, STATUS TEXT,
                SYMBOL TEXT, TERMINATED TEXT, DECIMALS TEXT)
                """)
            SQL = "insert into food values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

            #Takes the values of the csv file and turns it into a list to be inserted in the table
            # https://stackoverflow.com/questions/23748995/pandas-dataframe-to-list
            for data in self.dr.values.tolist():
                self.cursor.execute(SQL, data)
                
            self.conn.commit()
            
            print ("\nFile has been loaded")
            print("Database connection has been established\n")

            #Declaring a boolean variable to be true, to know when to exit the while loop
            flag = True

            #The programm ask what action you want to take until the flag is false
            while flag:
                print("Please input a command")
                print("input: count, first, last, add, update, delete, info, help, exit")
                F_comm = input()
                
                #Calls the count rows method
                if(F_comm == "count"):
                    self.count_rows()

                #Calls the first row method
                elif(F_comm == "first"):
                    self.first_row()

                #calls the last row method
                elif(F_comm == "last"):
                    self.last_row()

                #Calls the add method
                elif(F_comm == "add"):
                    self.add_row()

                #Calls the update method
                elif(F_comm == "update"):
                    self.update_row()

                #Calls the delete method
                elif(F_comm == "delete"):
                    self.delete_row()

                #Calls the method info, givin the authors information
                elif(F_comm == "info"):
                    self.myName()
                
                elif(F_comm == "help"):
                    self.help()

                #command to close the file and exit the program
                elif(F_comm == "exit"):
                    print("closing file ... ")
                    time.sleep(3)
                    print("Thank you and Goodbye")
                    self.conn.close()
                    
                    flag = None

                #prints out the student name
                elif(F_comm == "name"):
                    print("\nBy Tomas Lozano - 040869662")
                    print("CST8333 Programming Language Research Project")
                    print("Last modified: 2018-12-01\n")

                #Error handler in case the user inputs the wrong command
                else:
                    print("Please input the correct command\n")
                    
        #Closes the file in case the user doesn't want to run the program
        elif (openFile == "N" or openFile == "n" or openFile == "No" or openFile == "no"):

            print("Thank you and Goodbye")

        

    #Counts the amount of rows in the file
    def count_rows(self):
        print("The file has " + str(len(self.dr)) + " records \n")
        #return len(self.dr)

    #Print the first row of the database
    def first_row(self):
        print("\nThe first row of data has the next values:")
        first_row = self.cursor.execute("SELECT * FROM food LIMIT 1")
        print(list(first_row))
        print("")

    #Prints the last row of the data base
    def last_row(self):

        #l_row_display = input("\nHow many rows do you want to display? ")
        print("\nThe last row of data has the next values:")
        #last_row = self.cursor.execute("SELECT * FROM food ORDER BY rowid DESC LIMIT ?", (l_row_display,))
        last_row = self.cursor.execute("SELECT * FROM food ORDER BY rowid DESC LIMIT 1")
        print(list(last_row))
        print("")        

    #Add a new row to the end of the database. The user has to input certain parameters and the rest are standard
    #https://www.w3schools.com/sql/sql_insert.asp
    def add_row(self):
        print("\nWhat values do you want to insert?")
        food_categories = input("Food Categories: ")
        commodity = input("Commodity: ")
        vector = input("Vector: ")
        value = input("Value: ")

        self.cursor.execute("INSERT INTO food VALUES ('2018', 'Canada', '2016A000011124', ?, ?, 'Kilograms', '194', 'units', '0', ?, 'v41356795', ?, '0', '0', '0', '2')", (food_categories, commodity, vector, value))
        print("\nValues have been inserted into the Database\n")
        self.conn.commit()

    #Updates the last row of the data base on certain parameters that are input by the user 
    #https://www.w3schools.com/sql/sql_update.asp
    #https://www.w3schools.com/sql/sql_min_max.asp
    def update_row(self):
        print("\nUpdate the data of the last row")
        food_categories = input("Food Categories: ")
        commodity = input("Commodity: ")
        vector = input("Vector: ")
        value = input("Value: ")

        self.cursor.execute("UPDATE food SET FoodCategories = ?, Commodity = ?, VECTOR = ?, VALUE = ? WHERE rowid = (SELECT max(rowid) from food)", (food_categories, commodity, vector, value))
        print("\nDatabase has been updated\n")
        self.conn.commit()     

    #Delete the last row of the database
    #https://www.w3schools.com/sql/sql_delete.asp
    #https://www.w3schools.com/sql/sql_min_max.asp
    def delete_row(self):
        
        self.cursor.execute("DELETE FROM food WHERE rowid = (SELECT max(rowid) from food)")
        self.conn.commit()
        print("\nThe data has been deleted from the database\n")       

    #Returns first name, last name and Id of the Author. Also the course information
    #https://www.python-course.eu/python3_inheritance.php
    def myName(self):
        print("")
        x = myInfo("Tomas", "Lozano", "040869662")
        print(x.allTheInfo() + "\nfor CST8333 Programming Language Research Project\n")
    
    #Method that helps you understand the commands from the main menu
    #https://www.programiz.com/python-programming/iterator
    def help(self):
        my_commands = ["count", "first", "last", "add", "update", "delete", "info", "exit"]
        print("\nYou have " + str(len(list(my_commands))) + " options for help")
        my_iter = iter(my_commands)
        i = 1
        noMoreHelp = True

        while(noMoreHelp):
                print(str(i) + ": " + next(my_iter))
                i += 1
                if(i == 9):
                    break

        while (noMoreHelp):
            print("Which command do you want help with? (Please input the number)")  
            myHelp = input("Command: ")
            print("")

            if (myHelp == "1"):
                print("The count command counts the amount of rows with data in the loaded file\n")
            elif (myHelp == "2"):
                print("The first command shows the information of the first row on the database\n")
            elif (myHelp == "3"):
                print("The last command shows the information of the last row on the database\n")
            elif (myHelp == "4"):
                print("The add command adds a new row to the end of the database\n")
            elif (myHelp == "5"):
                print("The update command changes the information of the last row of the database\n")
            elif (myHelp == "6"):
                print("The delete command deletes the last row of the database\n")
            elif (myHelp == "7"):
                print("The info command shows the information of the author of the program\n")
            elif (myHelp == "8"):
                print("The exit command leaves the program\n")
            else:
                print("Please input the correct command\n")
            moreHelp = input("Do you need more help? Y/N ")
            if (moreHelp == "n" or moreHelp == "N"):
                print("")
                noMoreHelp = None


if __name__ == "__main__":
    t = Assign("firstName", "lastName", "ID")
    t.main()

