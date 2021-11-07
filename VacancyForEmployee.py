import PySimpleGUI as sg
from RLForVacancy import  InitRLForVacancyForm
import datetime

def InitVacancyFEForm(cursor, vacancy):
    sg.theme('LightGrey2')
    try:
        command = f'''SELECT Рівень_освіти FROM "Освіта" WHERE id = {vacancy[10]};        '''

        cursor.execute(command)
        osvita = list(cursor.fetchone())
        command = f'''SELECT Назва_Спеціальність FROM "Спеціальності" WHERE id = {vacancy[11]};        '''

        cursor.execute(command)
        spec = list(cursor.fetchone())
        command = f'''SELECT Назва_Діяльності FROM "Сфера_Діяльності" WHERE id = {vacancy[3]};        '''

        cursor.execute(command)
        Dyalnyst = list(cursor.fetchone())
    except Exception as ex:
        osvita=[' ']
        spec = [' ']
        Dyalnyst = [' ']

    command = f'''
    SELECT * FROM Працедавець
    WHERE id = {vacancy[1]};
    '''
    cursor.execute(command)
    employer = cursor.fetchone()

    VacancyFEFormLayout = [
        [sg.Text('Назва компанії:', size=(20, 1)), sg.Text(key='-компанії-', text=employer[1])],
        [sg.Text('Назва відділення:', size=(20, 1)), sg.Text(key='-відділення-', text=employer[2])],
        [sg.Text('Телефон:', size=(20, 1)), sg.Text(key='-Телефон-', text=str(employer[3]))],
        [sg.Text('Електронна пошта:', size=(20, 1)), sg.Text(key='-Електронна пошта-', text=employer[4])],
        [sg.Text('Країна:', size=(20, 1)), sg.Text(key='-Країна-', text=employer[7])],
        [sg.Text('Місто:', size=(20, 1)), sg.Text(key='-Місто-', text=employer[8])],
        [sg.Text('Назва вакансії:', size=(20, 1)), sg.Text(key='-Назва_Вакансії-', text=vacancy[2])],
            [sg.Text('Сфера діяльності:', size=(20, 1)),
             sg.Text(key='-СфераДіяльності-', text=Dyalnyst[0])],
            [sg.Text('Необхідні навики:', size=(20, 1)), sg.Text(key='-Навики-', text=vacancy[4])],
            [sg.Checkbox('Віддалена?', key='-check-',disabled= True, default=bool(vacancy[5]))],
            [sg.Text('Заробітна плата(грн):', size=(20, 1)), sg.Text(key='-Зарплата-', text=vacancy[6])],
            [sg.Text('Графік роботи:', size=(20, 1)), sg.Text(key='-Графік-', text=vacancy[7])],
            [sg.Text('Посада:', size=(20, 1)), sg.Text(key='-Посада-', text=vacancy[8])],
            [sg.Text('Необхідний досвід роботи:', size=(20, 1)), sg.Text(key='-досвід-', text=vacancy[9])],
            [sg.Text('Необхідна освіта:', size=(20, 1)), sg.Text(key='-освіта-', text=osvita[0])],
            [sg.Text('Необхідна спеціальність:', size=(20, 1)),
            sg.Text(key='-Спеціальність-', text=spec[0])],
            [sg.Text('Детальний опис:', size=(20, 1)), sg.Text(key='-Інфо-', text=vacancy[12])],

            [sg.Text('Дата написання:', size=(20, 1)), sg.Text(key='-Дата-', text=str(vacancy[13]))],

            [sg.Button('Подати заявку'),sg.Button('Наступна'), sg.Button('Назад')],
            [sg.Text(' ', size=(50, 2), key='-warning-')]
        ]

    # Create the Window
    VacancyFEFormWindow = sg.Window('Вакансія. \"Work Finder\"', VacancyFEFormLayout)

    while True:
        try:
            event, values = VacancyFEFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                VacancyFEFormWindow.close()
                return False
            if event == 'Наступна':
                VacancyFEFormWindow.close()
                return True
            if event == 'Подати заявку':
                rez = InitRLForVacancyForm(cursor, vacancy[1])
                if rez != 0:
                    command = f'''
                                INSERT INTO "Заявка_на_роботу" ("Код_резюме","Код_вакансія","Дата_складання")
                                            VALUES ({rez},{vacancy[0]},'{str(datetime.datetime.now().date())}');
                                '''
                    cursor.execute(command)
                    cursor.execute('COMMIT')





        except Exception as ex:
            print("Error in VacancyForEmployee")
            print(ex.args)
