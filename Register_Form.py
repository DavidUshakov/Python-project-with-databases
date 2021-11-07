import PySimpleGUI as sg
# All the stuff inside your window.

# def IsTableNotEmpty(table):
#     for row in table:
#         return True
#     return False

def init(db, cursor):
    sg.theme('LightGrey2')

    RegisterFormLayout = [[sg.Text('Login:', size=(8, 1)), sg.InputText(key='-login-')],
                          [sg.Text('Password:', size=(8, 1)), sg.InputText(key='-password-')],

                          [sg.Button('Вхід', size=(4, 1)), sg.Button('Зареєструвати працівника'),sg.Button('Зареєструвати працедавця'), sg.Button('Відміна')],
                          [sg.Text('', size = (50,2), key= '-warning-', text_color= 'Pink')]
                          ]

    RegisterFormWindow = sg.Window('Вхід до додатку \"Work Finder\"', RegisterFormLayout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:

        event, values = RegisterFormWindow.read()

        if event == sg.WIN_CLOSED or event == 'Відміна': # if user closes window or clicks cancel
            RegisterFormWindow.close()
            return (0, None)


        if event =='Вхід':
            try:
                logPass = f'''SELECT * FROM Працівник where 
                Логін = "{values['-login-']}" and Пароль = "{values['-password-']}" '''
                cursor.execute(logPass)
                login = cursor.fetchone()

                if login:

                    RegisterFormWindow.close()
                    return (1, login)

                else:
                    logPass = f'''SELECT * FROM  Працедавець where 
                                     Логін = "{values['-login-']}" and Пароль = "{values['-password-']}"'''
                    cursor.execute(logPass)
                    login = cursor.fetchone()
                    if login:
                        RegisterFormWindow.close()
                        return (2, login)

                    else:
                        RegisterFormWindow.FindElement('-warning-').Update('Невірні логін або пароль. Якщо забули свій пароль, створіть новий обліковий запис, або зверніться до адміністратора.',text_color='Pink')

            except Exception as ex:
                print("We have enter error")


        if event == 'Зареєструвати працівника':
            try:
                logPass = f'''SELECT id, Логін, Пароль FROM Працівник where Логін = "{values['-login-']}" '''
                cursor.execute(logPass)
                password = cursor.fetchone()
                if password:
                    RegisterFormWindow.FindElement('-warning-').Update('Користувач з таким логіном вже існує.\nПридумайе інший, або зверніться до адміністратора, якщо забули пароль.',text_color='Pink')
                else:
                    command = f'''  INSERT INTO "Працівник" ( "Логін", "Пароль")
                                       VALUES ('{values['-login-']}','{values['-password-']}');
                                            '''
                    cursor.execute(command)
                    cursor.execute('COMMIT')
                    RegisterFormWindow.FindElement('-warning-').Update('Успішно створено обліковий запис працівника',text_color='Green')

            except Exception as ex:
                print("error in employee Register ")


        if event == 'Зареєструвати працедавця':
            try:
                logPass = f'''SELECT id, Логін, Пароль FROM Працедавець where Логін = "{values['-login-']}" '''
                cursor.execute(logPass)
                password = cursor.fetchone()
                if password:
                    RegisterFormWindow.FindElement('-warning-').Update(str = "Користувач з таким логіном вже існує.\nПридумайе інший, або зверніться до адміністратора, якщо забули пароль.",text_color='Pink')
                else:
                    command = f'''  INSERT INTO "Працедавець" ( "Логін", "Пароль")
                                       VALUES ('{values['-login-']}','{values['-password-']}');
                                            '''
                    cursor.execute(command)
                    cursor.execute('COMMIT')
                    RegisterFormWindow.FindElement('-warning-').Update('Успішно створено обліковий запис працедавця',text_color='Green')

            except Exception as ex:
                print("error in employer Register ")
                print(ex.args)









