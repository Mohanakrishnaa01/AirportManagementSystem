import getpass
import oracledb

un = 'system'
cs = 'localhost:1521/XE'
pw = getpass.getpass('Enter password: ')

name = "Monish"
email = "monish@gmail.com"
password = "pass"
address = "Chennai"

with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
    with connection.cursor() as cursor:
        # Use bind variables and placeholders
        sql = """INSERT INTO Users (username, email, password, address) 
                 VALUES (:name, :email, :password, :address)"""
        
        # Use execute() method with dictionary binding
        cursor.execute(sql, {'name': name, 'email': email, 'password': password, 'address': address})
        
        # Commit the transaction
        connection.commit()

        # Select and print the inserted data
        sql_select = '''SELECT * FROM Users'''
        cursor.execute(sql_select)
        data = cursor.fetchall()
        