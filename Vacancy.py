import PySimpleGUI as sg


def InitVacancyForm(cursor, vacancy):
    sg.theme('LightGrey2')
    command = f'''SELECT * FROM "Сфера_Діяльності";        '''

    cursor.execute(command)
    names = list(cursor.fetchall())
    command = f'''SELECT * FROM "Освіта";        '''

    cursor.execute(command)
    osvita = list(cursor.fetchall())
    command = f'''SELECT * FROM "Спеціальності";        '''

    cursor.execute(command)
    spec = list(cursor.fetchall())


    pereizd = bool(vacancy[5])
    VacancyFormLayout = [
        [sg.Text('Назва вакансії:', size=(20, 1)), sg.InputText(key='-Назва_Вакансії-', default_text=vacancy[2])],
        [sg.Text('Сфера діяльності(номер):', size=(20, 1)),
         sg.InputText(key='-СфераДіяльності-', default_text=vacancy[3])],
        [sg.Listbox(names[:][:], size=(70, 4), key='-LIST-')],
        [sg.Text('Необхідні навики:', size=(20, 1)), sg.InputText(key='-Навики-', default_text=vacancy[4])],
        [sg.Checkbox('Віддалена?', key='-check-', default=pereizd)],
        [sg.Text('Заробітна плата(грн):', size=(20, 1)), sg.InputText(key='-Зарплата-', default_text=vacancy[6])],
        [sg.Text('Графік роботи:', size=(20, 1)), sg.InputText(key='-Графік-', default_text=vacancy[7])],
        [sg.Text('Посада:', size=(20, 1)), sg.InputText(key='-Посада-', default_text=vacancy[8])],
        [sg.Text('Необхідний досвід роботи:', size=(20, 1)), sg.InputText(key='-досвід-', default_text=vacancy[9])],
        [sg.Text('Необхідна освіта(номер):', size=(20, 1)), sg.InputText(key='-освіта-', default_text=vacancy[10])],
        [sg.Listbox(osvita[:][:], size=(70, 4), key='-osvlist-')],
        [sg.Text('Необхідна спеціальність(номер):', size=(20, 1)),
        sg.InputText(key='-Спеціальність-', default_text=vacancy[11])],
        [sg.Listbox(spec[:][:], size=(70, 4), key='-speclist-')],
        [sg.Text('Детальний опис:', size=(20, 1)), sg.InputText(key='-Інфо-', default_text=vacancy[12])],

        [sg.Text('Дата написання:', size=(20, 1)), sg.InputText(key='-Дата-', default_text=str(vacancy[13]))],

        [sg.Button('Зберегти'), sg.Button('Назад')],
        [sg.Text(' ', size=(50, 2), key='-warning-')]
    ]

    # Create the Window
    VacancyFormWindow = sg.Window('Вакансія. \"Work Finder\"', VacancyFormLayout)

    while True:
        try:
            event, values = VacancyFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                VacancyFormWindow.close()
                return
            if event == 'Зберегти':
                command = f'''  UPDATE  "Вакансія" 
                                                SET "Назва_Вакансії" ='{str(values['-Назва_Вакансії-'])}',
                                                "Діяльність" = {values['-СфераДіяльності-']},
                                                "Необхідні навики" = '{str(values['-Навики-'])}',
                                                "Віддалена?" = {int(values['-check-'])},
                                                "Заробітна_плата" = {values['-Зарплата-']},
                                                "Графік_роботи" = '{str(values['-Графік-'])}',
                                                "Посада" = '{str(values['-Посада-'])}',
                                                "Необхідний_досвід_роботи" = {values['-досвід-']},
                                                "Необхідна_освіта" = {values['-освіта-']},
                                                "Необхідна_спеціальність" = {values['-Спеціальність-']},
                                                "Детальний_опис" = '{str(values['-Інфо-'])}',
                                                "Дата_Написання" = '{str(values['-Дата-'])}'
                                                WHERE "Вакансія".id  = {vacancy[0]}
                                                ;
                                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                VacancyFormWindow.FindElement('-warning-').Update('Успішно збережено!', text_color='Green')
        except Exception as ex:
            print("error in resume")
            VacancyFormWindow.FindElement('-warning-').Update(
                'При збереженні виникла помилка. Поля Сфера діяльності та  зарплата повинні бути заповнені.',
                text_color='Pink')
            print(ex.args)
