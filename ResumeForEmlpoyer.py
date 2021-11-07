import PySimpleGUI as sg
from EmployeeJobsForm import InitEmployeeJobsForm

def InitResumeFEForm(cursor, resume):
    try:
        sg.theme('LightGrey2')
        command = f'''
            SELECT * FROM Працівник
            WHERE id = {resume[1]};
            '''
        cursor.execute(command)
        employee = cursor.fetchone()
        command = f'''SELECT * FROM "Освіта";        '''

        cursor.execute(command)
        osvita = list(cursor.fetchall())
        command = f'''SELECT * FROM "Сфера_Діяльності";        '''

        cursor.execute(command)
        sphere = list(cursor.fetchall())
        command = f'''SELECT * FROM "Спеціальності";        '''

        cursor.execute(command)
        spec = list(cursor.fetchall())

        command = f'''SELECT Освіта_ід, Навчальний_заклад, Спеціальність FROM "Освіта_Працівника" WHERE "Резюме_ід" = {resume[0]}
    
    
            '''

        cursor.execute(command)

        tmp = list(cursor.fetchall())
        if len(tmp) > 0:
            data = list(list())

            for i in range(len(tmp)):
                data.append(list(tmp[i]))
                data[i][0] = osvita[tmp[i][0] - 1][1]
                data[i][2] = spec[tmp[i][2] - 1][1]


        else:
            data = [[' ', ' ', ' ']]

        VacancyFEFormLayout = [
            [
                [sg.Text('Прізвище:', size=(20, 1)), sg.Text(key='-Прізвище-', text=employee[1])],
                [sg.Text('Ім\'я:', size=(20, 1)), sg.Text(key='-Імя-', text=employee[2])],
                [sg.Text('По-батькові:', size=(20, 1)), sg.Text(key='-По-батькові-', text=employee[3])],
                [sg.Text('Телефон:', size=(20, 1)), sg.Text(key='-Телефон-', text=str(employee[4]))],
                [sg.Text('Електронна пошта:', size=(20, 1)),
                 sg.Text(key='-Електронна пошта-', text=employee[5])],
                [sg.Text('Рік народження:', size=(20, 1)),
                 sg.Text(key='-Рік народження-', text=str(employee[6]))],
                [sg.Text('Країна:', size=(20, 1)), sg.Text(key='-Країна-', text=employee[7])],
                [sg.Text('Місто:', size=(20, 1)), sg.Text(key='-Місто-', text=employee[8])],
                [sg.Button('Список попередніх робіт', key='jobs')],

                [sg.Text('Назва резюме:', size=(20, 1)), sg.Text(key='-Назва-', text=resume[2])],
                [sg.Text('Сфера діяльності:', size=(20, 1)),
                 sg.Text(key='-СфераДіяльності-', text=sphere[0])],
                [sg.Text('Навики:', size=(20, 1)), sg.Text(key='-Навики-', text=resume[4])],
                [sg.Checkbox('Згоден на переїзд', key='-check-', default=bool(resume[5]), disabled= True)],
                [sg.Text('Бажана зарплата(грн):', size=(20, 1)),
                 sg.Text(key='-Зарплата-', text=str(resume[6]))],
                [sg.Text('Бажаний графік:', size=(20, 1)), sg.Text(key='-Графік-', text=resume[7])],
                [sg.Text('Додаткова інформація:', size=(20, 1)), sg.Text(key='-Інфо-', text=resume[9])],
                [sg.Text('Дата написання резюме:', size=(20, 1)), sg.Text(key='-Дата-', text=str(resume[8]))],
                [sg.Table(values=data[:][:],
                          headings=["    Освіта    ", "  Навчальний заклад  ", "  Спеціальність  "],
                          size=(30, 3), key='-table-')],
                [sg.Button('Прийняти', size=(25, 1)), sg.Button('Відхилити', size=(25, 1))],
                [sg.Text('Інше повідомлення:', size=(20, 1)), sg.InputText(key='-message-')],
                [sg.Button('Надіслати', size=(25, 1)), sg.Button('Вихід', size=(25, 1))],
                [sg.Text('', size=(50, 2), key='-warning-')]
            ]
        ]
        VacancyFEFormWindow = sg.Window('Резюме. \"Work Finder\"', VacancyFEFormLayout)

        while True:

            event, values = VacancyFEFormWindow.read()
            VacancyFEFormWindow.close()
            if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel

                return 'cancel'

            if event == 'jobs':
                InitEmployeeJobsForm(cursor,employee, False)
            if event == 'Прийняти':
                return  'Прийнято'
            if event == 'Відхилити':
                return 'Відхилено'
            if event == 'Надіслати':
                return str(values['-message-'])

    except Exception as ex:
        print("Error in ResumeForEmployer")

        print(ex.args)

