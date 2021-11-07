import PySimpleGUI as sg

sg.theme('LightGrey2')


def InitRLForVacancyForm(cursor,employee):

    command = f'''SELECT id, Назва_резюме FROM "Резюме" WHERE "Код_Працівник" = {employee}    '''

    cursor.execute(command)

    tmp = list(cursor.fetchall())
    if len(tmp) > 0:
        data = list()
        for i in range(len(tmp)):
            data.append(tmp[i][1])
    else:   return 0

    RLFVFormLayout =[
        [sg.Text('Список ваших резюме:', size=(20, 1))],
        [sg.Listbox(data, size=(40, 4), enable_events=True, key='-LIST-')],
        [ sg.Button('Назад', size=(6, 1))]
    ]
    RLFVFormWindow = sg.Window('Резюме. \"Work Finder\"', RLFVFormLayout)
    while True:
        try:
            event, values = RLFVFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                RLFVFormWindow.close()
                return 0
            if event == '-LIST-' and len(values['-LIST-']):
                for i in range(len(tmp)):
                    if values['-LIST-'][0] == tmp[i][1]:
                        RLFVFormWindow.close()
                        return tmp[i][0]
        except Exception as ex:
            print("Error in RLForVacancy")
            print(ex.args)
