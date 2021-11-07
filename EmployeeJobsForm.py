import PySimpleGUI as sg

sg.theme('LightGrey2')


def InitEmployeeJobsForm(cursor, employee, isEmployee):
    command = f'''SELECT * FROM "Сфера_Діяльності";        '''

    cursor.execute(command)
    names = list(cursor.fetchall())

    command = f'''SELECT * FROM "Хроніка_працевлаштуваннь" WHERE "Працівник_ід" = {employee[0]}
        
    
    '''


    cursor.execute(command)


    tmp = list(cursor.fetchall())
    if len(tmp) >0:
        data = list(list(str()))

        for i in range(len(tmp)):
            data.append(list(tmp[i]))

            for j in range(len(tmp[i])-2):
                if j == 1:
                    data[i][1] = names[tmp[i][3]][1]
                else:
                    data[i][j]= str(data[i][j+2])

    else:
        data = [[' ',' ',' ',' ',' ']]
    # names = list(list(str()))
    # for i in range(len(tmpn)):
    #     names.append(list(tmpn[i]))
    #     for j in range(len(tmpn[i]) ):
    #         names[i][j] = str(tmpn[i][j])

    EmployeeJobsFormLayout = [
        [sg.Table(values=data[:][:], headings=["Компанія","Діяльність","Посада","Дата прийому на роботу", "Дата звільнення"],size=(10,10), key ='-table-')],
        [sg.Text('Додати інформацію:', size=(20, 1))],
        [sg.Text('Компанія:', size=(20, 1)), sg.InputText(key='-Company-')],
        [sg.Text('Діяльність(номер):', size=(20, 1)), sg.InputText(key='-Diyalnyst-')],
        [sg.Listbox(names[:][:], size=(70, 4), key='-LIST-')],
        [sg.Text('Посада:', size=(20, 1)), sg.InputText(key='-Posada-')],
        [sg.Text('Дата прийому на роботу:', size=(20, 1)), sg.InputText(key='-Priem-')],
        [sg.Text('Дата звільнення:', size=(20, 1)), sg.InputText(key='-Uval-')],
        [sg.Button('Додати', size=(6, 1), visible= isEmployee), sg.Button('Видалити', size=(6, 1)), sg.Button('Назад', size=(6, 1))],
        [sg.Text('', size=(60, 2), key='-warning-', text_color='Pink')]
    ]
    EmployeeJobsFormWindow = sg.Window('Роботи працівника. \"Work Finder\"', EmployeeJobsFormLayout)



    while True:
        try:
            event, values = EmployeeJobsFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                EmployeeJobsFormWindow.close()
                return employee


            if event == 'Додати':

                command = f'''  INSERT INTO "Хроніка_працевлаштуваннь" ( "Працівник_ід", "Компанія","Діяльність","Посада", "Дата_прийому_на_роботу","Дата_звільнення" )
                                       VALUES (
                                                {employee[0]},
                                                  '{str(values['-Company-'])}',
                                                  {int(values['-Diyalnyst-'])},
                                                  '{str(values['-Posada-'])}',
                                                  '{str(values['-Priem-'])}',
                                                  '{str(values['-Uval-'])}'
                                                  );
                                                
                                                                           '''
                cursor.execute(command)
                cursor.execute('COMMIT')
                EmployeeJobsFormWindow.FindElement('-warning-').Update('Успішно додано',
                                                                       text_color='Green')
                # command = f'''SELECT * FROM "Хроніка_працевлаштуваннь" WHERE "Працівник_ід" = {employee[0]}
                #
                #
                # '''
                #
                # cursor.execute(command)
                #
                # tmp = list(cursor.fetchall())
                # data = list(list(str()))
                # for i in range(len(tmp)):
                #     data.append(list(tmp[i]))
                #     for j in range(len(tmp[i]) - 2):
                #         data[i][j] = str(data[i][j + 2])
                # EmployeeJobsFormWindow.FindElement('-table-').Update(values=data[:][:], headings=["Компанія","Діяльність","Посада","Дата прийому на роботу", "Дата звільнення"],size=(10,10))

            if event == 'Видалити':
                # command = f'''  DELETE FROM "Хроніка_працевлаштуваннь"
                # Where "Працівник_ід" = {employee[0]} AND "Компанія"='{str(values['-Company-'])}' AND
                # "Посада"='{str(values['-Posada-'])}';
                # '''
                command = f'''  DELETE FROM Хроніка_працевлаштуваннь
                 Where Працівник_ід = {employee[0]} AND Компанія="{str(values['-Company-'])}" AND Посада="{str(values['-Posada-'])}";
                '''

                cursor.execute(command)
                cursor.execute('COMMIT')
                EmployeeJobsFormWindow.FindElement('-warning-').Update('Успішно видалено',  text_color='Green')
        except Exception as ex:
            EmployeeJobsFormWindow.FindElement('-warning-').Update('Підчас зміни записів виникла помилка.', text_color='Pink')

            print("Error in EmployeeJobsForm")
