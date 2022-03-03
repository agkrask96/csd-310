"""Abigail Kraska 
   Whatabook Program
   CYBR 410
   3/2/2022
"""

""" import statements """
import sys
import mysql.connector
from mysql.connector import errorcode

""" database config object """
config ={
"user":"whatabook_user",
"password":"MySQL8IsGreat!",
"host": "127.0.0.1",
"database":"whatabook",
"raise_on_warnings":True
}

def show_menu():
    #displays the main menu and invalid responses terminate the program
    print ("\n  -- Main Menu --")
    print(" 1. View Books \n 2. View Store Locations\n 3. My Account\n 4. Exit Program")

    try: 
        choice=int(input(' Enter one of the options listed above, 1, 2, 3, or 4: '))

        return choice
    except ValueError:
        print ("\n Invalid number, program terminated...\n")

        sys.exit(0)

def show_books(_cursor):
    # displays the books for option 1 of the main menu
    _cursor.execute("SELECT book_id, book_name, author, details from book")

    books=_cursor.fetchall()

    print("\n -- DISPLAYING BOOK LISTING --")

    for book in books:
        print("Book Name: {}\n Author: {} \n Details: {} \n".format(book[0], book[1], book[2]))

def show_locations(_cursor):
    # displays the store locations for option 2 of the main menu
    _cursor.execute("SELECT store_id, locale from store")

    locations= _cursor.fetchall()

    print ("\n  -- DISPLAYING STORE LOCATIONS --")

    for location in locations:
        print (" Locale: {} \n".format(location[1]))

def validate_user():
    # terminates the program if there is an invalid customer id entered
    try:
        user_id=int(input('\n Enter a customer id, 1, 2, or 3: '))

        if user_id <1 or user_id>3:
            print ("\n Invalid customer number, program terminated...\n")
            sys.exit(0)

        return user_id
    except ValueError:
        print ("\n Invalid number, program terminated...\n")

        sys.exit(0)

def show_account_menu(): 
    # displays the account menu and terminates it if an invalid number is entered
    try:
        print("\n -- Customer Menu --")
        print (" 1. Wishlist\n 2. Add Book\n 3. Main Menu")
        account_option=int(input('Enter one of the options listed above, 1, 2, or 3: '))

        return account_option

    except ValueError:
        print ("\n Invalid number, program terminated...\n")
        sys.exit(0)

def show_wishlist(_cursor, _user_id):
    # retrieves and displays the books on the wishlist
    _cursor.execute("SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author " + 
                    "FROM wishlist " +
                    "INNER JOIN user ON wishlist.user_id = user.user_id "+
                    "INNER JOIN book ON wishlist.book_id = book.book_id " +
                    "WHERE user.user_id= {}".format(_user_id))

    wishlist= _cursor.fetchall()

    print (" \n -- DISPLAYING WISHLIST ITEMS --")

    for book in wishlist: 
        print(" Book Name: {}\n Author: {}\n".format(book[4], book [5]))

def show_books_to_add(_cursor, _user_id):
    # shows the books that are available to add to the wishlist
    query= ("SELECT book_id, book_name, author, details "
            "FROM book "
            "WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = {})".format(_user_id))

    print (query)

    _cursor.execute(query)

    books_to_add=_cursor.fetchall()

    print ("\n -- DISPLAYING AVAILABLE BOOKS --")

    for book in books_to_add:
        print (" Book Id: {}\n  Book Name: {}\n".format(book[0], book[1]))            

def add_book_to_wishlist(_cursor, _user_id, _book_id):
    # adds the book to the wishlist and terminates the program if an invalid book id is entered
    if _book_id >0 and _book_id <10:
        _cursor.execute("INSERT INTO wishlist(user_id, book_id) VALUES({}, {})".format(_user_id, _book_id))
    else:
        print("Invalid book id, terminating program!")
        sys.exit(0) 
try:
    # handles database errors and menu setup
    db= mysql.connector.connect(**config) 

    cursor= db.cursor()

    print("\n Welcome to the WhatABook Application!")

    user_selection= show_menu()

    while user_selection != 4:
        # connects the user input numbers with the correct methods to retrieve the data
                
        if user_selection==1:
            show_books(cursor)
            user_selection= show_menu()

        if user_selection ==2: 
            show_locations(cursor)
            user_selection= show_menu()

        if user_selection ==3: 
            my_user_id= validate_user()
            account_option= show_account_menu()

            while account_option != 3:
                if account_option == 1:
                    # displays wishlist
                    show_wishlist(cursor, my_user_id)

                if account_option == 2:
                    # adds book to wishlist
                    show_books_to_add(cursor, my_user_id)

                    book_id=int(input("\n Enter the id of the book you want to add: "))

                    add_book_to_wishlist(cursor, my_user_id, book_id)

                    db.commit()

                    print ("\n Book id: {} was added to your wishlist!".format(book_id))

                    account_option=show_menu()

                if account_option< 1 or account_option>3:
                    # displays errors for invalid input
                    print ("\n Invalid option, please retry...")

                account_option=show_account_menu()

            if user_selection<1 or user_selection>4:
                print ("\n Invalid option, please retry...")
            
            user_selection=show_menu()

    if user_selection == 4:
        print ("Program terminated")
        sys.exit(0)
            
except mysql.connector.Error as err:
    # handles program errors
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print ("The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print (" The specified database does not exist")

    else: 
        print (err)

finally:
    # closes the database connection
    db.close()




                               
                  
