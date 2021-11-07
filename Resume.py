import PySimpleGUI as sg

def InitResumeForm(cursor,resume):


    sg.theme('LightGrey2')
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
            data[i][2] = spec[tmp[i][2]-1][1]


    else:
        data = [[' ', ' ',' ']]

    pereizd = bool(resume[5])
    ResumeFormLayout = [
        [sg.Text('Назва резюме:', size=(20, 1)), sg.InputText(key='-Назва-',default_text=resume[2])],
        [sg.Text('Сфера діяльності(номер):', size=(20, 1)), sg.InputText(key='-СфераДіяльності-',default_text=resume[3])],
        [sg.Listbox(sphere[:][:], size=(70, 4), key='-dyalnlist-')],
        [sg.Text('Навики:', size=(20, 1)), sg.InputText(key='-Навики-',default_text=resume[4])],
        [sg.Checkbox('Згоден на переїзд', key = '-check-', default=pereizd)],
        [sg.Text('Бажана зарплата(грн):', size=(20, 1)), sg.InputText(key='-Зарплата-', default_text=str(resume[6]))],
        [sg.Text('Бажаний графік:', size=(20, 1)), sg.InputText(key='-Графік-',default_text=resume[7])],
        [sg.Text('Додаткова інформація:', size=(20, 1)), sg.InputText(key='-Інфо-',default_text=resume[9])],
        [sg.Text('Дата написання резюме:', size=(20, 1)), sg.InputText(key='-Дата-',default_text=str(resume[8]))],

        [sg.Table(values=data[:][:],
                  headings=["    Освіта    ", "  Навчальний заклад  ", "  Спеціальність  "],
                  size=(30, 3), key='-table-')],
        [sg.Text('Освіта(номер):', size=(20, 1)), sg.InputText(key='-Освіта-')],
        [sg.Listbox(osvita[:][:], size=(70, 4), key='-osvlist-')],
        [sg.Text('Навчальний заклад:', size=(20, 1)), sg.InputText(key='-Заклад-')],
        [sg.Text('Спеціальність(номер):', size=(20, 1)), sg.InputText(key='-Спеціальність-')],
        [sg.Listbox(spec[:][:], size=(70, 4), key='-speclist-')],
        [sg.Text('       '),sg.Button('Додати', size=(6, 1))],

        [sg.Button('Зберегти'),sg.Button('Вихід')],
        [sg.Text(' ', size=(50, 2), key='-warning-')]
    ]
    ResumeFormWindow = sg.Window('Резюме працівника. \"Work Finder\"', ResumeFormLayout)
    while True:
        try:
            event, values = ResumeFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel
                ResumeFormWindow.close()
                return
            if event == 'Зберегти':
                command = f'''  UPDATE  "Резюме" 
                                                SET "Назва_резюме" ='{str(values['-Назва-'])}',
                                                "Сфера_Діяльності_ід" = {int(values['-СфераДіяльності-'])},
                                                "Навики" = '{str(values['-Навики-'])}',
                                                "Згоден_на_переїзд" = {values['-check-']},
                                                "Бажана зарплата" = {int(values['-Зарплата-'])},
                                                "Бажаний_Графік" = '{str(values['-Графік-'])}',
                                                "Дата_написання_резюме" = '{str(values['-Дата-'])}',
                                                "Додаткова_інформація" = '{str(values['-Інфо-'])}'
                                                WHERE "Резюме".id  = {resume[0]}
                                                ;
                                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                ResumeFormWindow.FindElement('-warning-').Update('Успішно збережено!', text_color='Green')
            if event == 'Додати':
                command = f'''  INSERT INTO "Освіта_Працівника" ( "Резюме_ід", "Освіта_ід","Навчальний_заклад", "Спеціальність" )
                                                       VALUES (
                                                                {resume[0]},
                                                                  {int(values['-Освіта-'])},
                                                                  '{str(values['-Заклад-'])}',
                                                                  {int(values['-Спеціальність-'])}
                                                                  );
        
                                                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                ResumeFormWindow.FindElement('-warning-').Update('Успішно додано', text_color='Green')
        except Exception as ex:
            print("error in resume")
            ResumeFormWindow.FindElement('-warning-').Update('При збереженні виникла помилка. Поля Сфера діяльності та Бажана зарплата повинні бути заповнені.', text_color='Pink')
            print(ex.args)
