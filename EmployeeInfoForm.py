import PySimpleGUI as sg
from EmployeeJobsForm import  InitEmployeeJobsForm

sg.theme('LightGrey2')


def InitEmployeeInfoForm(cursor,employee):
    EmployeeInfoFormLayout = [
        [
            [sg.Text('Прізвище:', size=(20, 1)), sg.InputText(key='-Прізвище-',default_text=employee[1])],
            [sg.Text('Ім\'я:', size=(20, 1)), sg.InputText(key='-Імя-',default_text=employee[2])],
            [sg.Text('По-батькові:', size=(20, 1)), sg.InputText(key='-По-батькові-',default_text=employee[3])],
            [sg.Text('Телефон:', size=(20, 1)), sg.InputText(key='-Телефон-',default_text=   str(employee[4]))],
            [sg.Text('Електронна пошта:', size=(20, 1)), sg.InputText(key='-Електронна пошта-',default_text=employee[5])],
            [sg.Text('Рік народження:', size=(20, 1)), sg.InputText(key='-Рік народження-',default_text=str(employee[6]))],
            [sg.Text('Країна:', size=(20, 1)), sg.InputText(key='-Країна-',default_text=employee[7])],
            [sg.Text('Місто:', size=(20, 1)), sg.InputText(key='-Місто-',default_text=employee[8])],
            [sg.Text('Логін:', size=(20, 1)), sg.InputText(key='-Логін-',default_text=employee[9])],
            [sg.Text('Пароль:', size=(20, 1)), sg.InputText(key='-Пароль-',default_text=employee[10])],
            [sg.Button('Список попередніх робіт', key = 'jobs')],
            [sg.Button('Зберегти', size=(25, 1)),sg.Button('Вихід', size=(25, 1))],

            [sg.Text('', size=(50, 2), key='-warning-')]
        ]
    ]

    # Create the Window
    EmployeeInfoFormWindow = sg.Window('Інформація о працівникові. \"Work Finder\"', EmployeeInfoFormLayout)

    while True:
        try:
            event, values = EmployeeInfoFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel
                EmployeeInfoFormWindow.close()
                return employee

            if event == 'jobs':
                InitEmployeeJobsForm(cursor,employee, True)

            if event == 'Зберегти':
                command = f'''  UPDATE  "Працівник" 
                                SET "Прізвище" ='{str(values['-Прізвище-'])}',
                                "Імя" = '{str(values['-Імя-'])}',
                                "По-батькові" = '{str(values['-По-батькові-'])}',
                                "телефон" = '{int(values['-Телефон-'])}',
                                "Електронна пошта" = '{str(values['-Електронна пошта-'])}',
                                "Рік народження" = '{int(values['-Рік народження-'])}',
                                "Країна" = '{str(values['-Країна-'])}',
                                "Місто" = '{str(values['-Місто-'])}',
                                "Логін" = '{str(values['-Логін-'])}',
                                "Пароль" = '{str(values['-Пароль-'])}'
                                WHERE "Працівник".id  = {employee[0]}
                                ;
                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')

                cursor.execute(f"Select * From Працівник Where id = {employee[0]};")
                employee = cursor.fetchone()
                EmployeeInfoFormWindow.FindElement('-warning-').Update('Успішно збережено!',text_color='Green')
        except Exception as ex:
            EmployeeInfoFormWindow.FindElement('-warning-').Update('При збереженні даних виникла помилка. Перевірте правильність введення в полях',text_color='Pink')

            print("Error in EmployeeInfoForm ")
            print(ex.args)
