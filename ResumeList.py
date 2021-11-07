import PySimpleGUI as sg
from Resume import InitResumeForm
import datetime

sg.theme('LightGrey2')


def InitResumeListForm(cursor,employee):


    command = f'''SELECT * FROM "Резюме" WHERE "Код_Працівник" = {employee[0]}


    '''

    cursor.execute(command)

    tmp = list(cursor.fetchall())
    if len(tmp) > 0:
        data = list()
        for i in range(len(tmp)):
            data.append(tmp[i][2])


    else:
        command = f'''
                        INSERT INTO Резюме (Код_Працівник,Назва_резюме, Сфера_Діяльності_ід, "Бажана зарплата","Дата_написання_резюме")
                                    VALUES ({employee[0]},'Нове резюме',1,0,'{datetime.datetime.now().date()}');
                        '''
        cursor.execute(command)
        cursor.execute('COMMIT')
        command = f'''SELECT * FROM "Резюме" WHERE "Код_Працівник" = {employee[0]}


        '''
        cursor.execute(command)
        tmp = list(cursor.fetchall())
        data = list()
        for i in range(len(tmp)):
            data.append(tmp[i][2])




    EmployeeResumeListFormLayout =[
        [sg.Text('Список ваших резюме:', size=(20, 1))],
        [sg.Listbox(data, size=(20, 4), enable_events=True, key='-LIST-')],
        [sg.Button('Додати', size=(6, 1)), sg.Button('Назад', size=(6, 1))]
    ]

    EmployeeRLFormWindow = sg.Window('Резюме. \"Work Finder\"', EmployeeResumeListFormLayout)

    while True:
        try:
            event, values = EmployeeRLFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                EmployeeRLFormWindow.close()
                return employee
            if event == '-LIST-' and len(values['-LIST-']):
                for i in range(len(data)):
                    if values['-LIST-'][0] == data[i]:
                        EmployeeRLFormWindow.close()
                        InitResumeForm(cursor,tmp[i])
                        InitResumeListForm(cursor, employee)
            if event == 'Додати':
                command = f'''
                        INSERT INTO Резюме (Код_Працівник,Назва_резюме, Сфера_Діяльності_ід, "Бажана зарплата",Дата_написання_резюме)
                                    VALUES ({employee[0]},'Нове резюме',1,0,{str(datetime.datetime.now().date())});
                        '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                EmployeeRLFormWindow.close()
                InitResumeListForm(cursor,employee)



        except Exception as ex:
            print("Error in ResumeListForm")
            print(ex.args)
