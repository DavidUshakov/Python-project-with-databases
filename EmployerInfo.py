import PySimpleGUI as sg

sg.theme('LightGrey2')


def InitEmployerInfoForm(cursor, employer):
    EmployerInfoFormLayout = [
[
            [sg.Text('Назва компанії:', size=(20, 1)), sg.InputText(key='-компанії-', default_text=employer[1])],
            [sg.Text('Назва відділення:', size=(20, 1)), sg.InputText(key='-відділення-', default_text=employer[2])],
            [sg.Text('Телефон:', size=(20, 1)), sg.InputText(key='-Телефон-', default_text=   str(employer[3]))],
            [sg.Text('Електронна пошта:', size=(20, 1)), sg.InputText(key='-Електронна пошта-', default_text=employer[4])],
            [sg.Text('Країна:', size=(20, 1)), sg.InputText(key='-Країна-', default_text=employer[7])],
            [sg.Text('Місто:', size=(20, 1)), sg.InputText(key='-Місто-', default_text=employer[8])],
            [sg.Text('Логін:', size=(20, 1)), sg.InputText(key='-Логін-', default_text=employer[5])],
            [sg.Text('Пароль:', size=(20, 1)), sg.InputText(key='-Пароль-', default_text=employer[6])],
            [sg.Button('Зберегти', size=(25, 1)),sg.Button('Вихід', size=(25, 1))],
            [sg.Text('', size=(50, 2), key='-warning-')]
        ]
    ]
    EmployerInfoFormWindow = sg.Window('Інформація о працедавцеві. \"Work Finder\"', EmployerInfoFormLayout)

    while True:
        try:
            event, values = EmployerInfoFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel
                EmployerInfoFormWindow.close()
                return employer
            if event == 'Зберегти':
                command = f'''  UPDATE  "Працедавець" 
                                SET "Назва компанії" ='{str(values['-компанії-'])}',
                                "Назва відділення" = '{str(values['-відділення-'])}',
                                "Номер телефону" = '{int(values['-Телефон-'])}',
                                "Електронна пошта" = '{str(values['-Електронна пошта-'])}',
                                "Країна" = '{str(values['-Країна-'])}',
                                "Місто" = '{str(values['-Місто-'])}',
                                "Логін" = '{str(values['-Логін-'])}',
                                "Пароль" = '{str(values['-Пароль-'])}'
                                WHERE "Працедавець".id  = {employer[0]}
                                ;
                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                cursor.execute(f"Select * From Працедавець Where id = {employer[0]};")
                employer = cursor.fetchone()
                EmployerInfoFormWindow.FindElement('-warning-').Update('Успішно збережено!',text_color='Green')
        except Exception as ex:
            EmployerInfoFormWindow.FindElement('-warning-').Update('При збереженні даних виникла помилка. Перевірте правильність введення в полях',text_color='Pink')

            print("Error in EmployerInfo ")