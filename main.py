from Register_Form import init
from EmployeeForm import InitEmplyeeForm
from EmployerForm import  InitEmplyerForm

import sqlite3

try:
    db = sqlite3.connect('somedatabase.db')
    cursor = db.cursor()


    Emplo,nextform  =  init(db,cursor)
    if Emplo == 1:
        InitEmplyeeForm(db,cursor,nextform)
    if Emplo == 2:
        InitEmplyerForm(db,cursor,nextform)
    print("Connection succeded")
except Exception as ex:
    print("We have connection error")
cursor.close()

db.close()
