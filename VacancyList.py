import PySimpleGUI as sg
from Vacancy import InitVacancyForm
import datetime

sg.theme('LightGrey2')


def InitVacancyListForm(cursor, employer):


    command = f'''SELECT * FROM "Вакансія" WHERE "Код_Працедавець" = {employer[0]}


    '''

    cursor.execute(command)

    tmp = list(cursor.fetchall())
    if len(tmp) > 0:
        data = list()
        for i in range(len(tmp)):
            data.append(tmp[i][2])


    else:
        command = f'''
                        INSERT INTO Вакансія (Код_Працедавець,Назва_Вакансії,Діяльність,"Віддалена?",
                        Заробітна_плата,Необхідний_досвід_роботи,Необхідна_освіта,Необхідна_спеціальність, Дата_Написання)
                                    VALUES ({employer[0]},'Новa вакансія',1,1,1,1,1,1,{str(datetime.datetime.now().date())});
                        '''
        cursor.execute(command)
        cursor.execute('COMMIT')
        command = f'''SELECT * FROM "Вакансія" WHERE "Код_Працедавець" = {employer[0]}


        '''
        cursor.execute(command)
        tmp = list(cursor.fetchall())
        data = list()
        for i in range(len(tmp)):
            data.append(tmp[i][2])




    EmployeeResumeListFormLayout =[
        [sg.Text('Список ваших вакансій:', size=(20, 1))],
        [sg.Listbox(data, size=(20, 4), enable_events=True, key='-LIST-')],
        [sg.Button('Додати', size=(6, 1)), sg.Button('Назад', size=(6, 1))]
    ]

    EmployerVLFormWindow = sg.Window('Мої Вакансії. \"Work Finder\"', EmployeeResumeListFormLayout)

    while True:
        try:
            event, values = EmployerVLFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                EmployerVLFormWindow.close()
                return employer
            if event == '-LIST-' and len(values['-LIST-']):
                for i in range(len(data)):
                    if values['-LIST-'][0] == data[i]:
                        EmployerVLFormWindow.close()
                        InitVacancyForm(cursor,tmp[i])
                        InitVacancyListForm(cursor, employer)
            if event == 'Додати':
                command = f'''
                                        INSERT INTO Вакансія (Код_Працедавець,Назва_Вакансії)
                                                    VALUES ({employer[0]},'Новa вакансія');
                                        '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                EmployerVLFormWindow.close()
                InitVacancyListForm(cursor, employer)



        except Exception as ex:
            print("Error in VacancyListForm")