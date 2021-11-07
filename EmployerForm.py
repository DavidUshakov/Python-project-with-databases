import PySimpleGUI as sg
from EmployerInfo import  InitEmployerInfoForm
from VacancyList import  InitVacancyListForm
from ResumeForEmlpoyer import InitResumeFEForm
import datetime
def checkResumes(cursor, employer):
    command = f''' SELECT * FROM Вакансія WHERE Код_Працедавець = {employer[0]}

                            '''
    cursor.execute(command)
    vacancies = cursor.fetchall()

    for i in range(len(vacancies)):
        command = f''' SELECT * FROM Заявка_на_роботу WHERE Код_вакансія = {vacancies[i][0]} AND Рішення IS NULL;

                    '''
        cursor.execute(command)
        zayavki = cursor.fetchall()
        for j in range(len(zayavki)):
            command = f''' SELECT * FROM Резюме WHERE id = {zayavki[j][1]};
                                        '''
            cursor.execute(command)
            resume = cursor.fetchone()
            ansv =InitResumeFEForm(cursor, resume)
            if ansv == 'cancel':
                return
            else:
                command =f'''
                UPDATE Заявка_на_роботу SET "Рішення" = '{ansv}',
                "Дата_перегляду" = '{str(datetime.datetime.now().date())}'
                WHERE id = {zayavki[j][0]};

                                '''

                cursor.execute(command)
                cursor.execute('COMMIT')



def InitEmplyerForm(db, cursor, employer):
    sg.theme('LightGrey2')

    EmployerFormLayout = [
         [sg.Button('Переглянути особисту інформацію', size=(50, 1))],
        [sg.Button('Мої вакансії', size=(50, 1))],
         [sg.Button('Подані заявки на вакансії', size=(50, 1))],
         [sg.Button('Вихід', size=(50, 1))]]

    EmployerFormWindow = sg.Window('Форма працедаця. \"Work Finder\"', EmployerFormLayout)
    while True:
        try:
            event, values = EmployerFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel
                EmployerFormWindow.close()
                return
            if event == 'Переглянути особисту інформацію':
                employer = InitEmployerInfoForm(cursor, employer)
            if event == 'Мої вакансії':
                InitVacancyListForm(cursor, employer)
            if event =='Подані заявки на вакансії':
                checkResumes(cursor,employer)
        except Exception as ex:
            print("Error in EmployerForm")
            print(ex.args)






