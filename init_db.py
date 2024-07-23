import sqlite3

connection = sqlite3.connect('cuestionarioBD.db')
cur = connection.cursor()


connection.commit()
connection.close()