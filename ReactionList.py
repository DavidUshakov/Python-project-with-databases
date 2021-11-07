import PySimpleGUI as sg
from VacancyForEmployee import  InitVacancyFEForm
def InitReactionListForm(cursor, employee):
    sg.theme('LightGrey2')
    try:
        command = f'''SELECT id FROM "Резюме" WHERE "Код_Працівник" = {employee[0]};
    
    
                    '''
        cursor.execute(command)
        resumes = list(cursor.fetchall())
        data= list()
        resume = list()
        vacancyName = list()
        vacancyId = list()
        counter = 0
        for j in range(len(resumes)):
            command = f'''SELECT Код_резюме, Код_вакансія,Дата_складання,Дата_перегляду,Рішення FROM "Заявка_на_роботу" WHERE "Код_резюме" = {resumes[j][0]};
        
        
                    '''
            cursor.execute(command)
            react = cursor.fetchall()

            for i in range(len(react)):
                command = f'''SELECT Назва_резюме FROM "Резюме" WHERE id =  {react[i][0]};        '''

                cursor.execute(command)
                resume.append(cursor.fetchone())

                command = f'''SELECT id, Назва_Вакансії FROM "Вакансія" WHERE id = {react[i][1]};        '''
                cursor.execute(command)
                r = list(cursor.fetchone())
                vacancyName.append(r[1])
                vacancyId.append(r[0])
                a= react[i][4]
                data.append(resume[counter][0].center(40-len(resume[counter][0]))+
                            vacancyName[counter].center(40-len(vacancyName[counter][0]))+
                            str(react[i][2]).center(40-len(str(react[i][2])))+
                            str(react[i][3]).center(40-len(str(react[i][3])))+
                            str(react[i][4]).center(40-len(str(react[i][4]))))
                counter+=1

        ReactionListFormLayout = [
            [sg.Text('Список ваших поданих заявок:', size=(30, 1))],
            [sg.Listbox(data, size=(120, 10), enable_events=True, key='-LIST-')],
            [sg.Button('Назад', size=(6, 1))]
        ]

        ReactionListFormWindow = sg.Window('Подані заявки. \"Work Finder\"', ReactionListFormLayout)

        while True:

            event, values = ReactionListFormWindow.read()
            if event == sg.WIN_CLOSED or event == 'Назад':  # if user closes window or clicks cancel
                ReactionListFormWindow.close()
                return
            if event == '-LIST-' and len(values['-LIST-']):

                for i in range(len(vacancyId)):
                    if  values['-LIST-'][0].find(vacancyName[i]):
                        ReactionListFormWindow.close()
                        command = f'''SELECT * FROM "Вакансія" WHERE id = {vacancyId[i]};        '''
                        cursor.execute(command)
                        InitVacancyFEForm(cursor,list(cursor.fetchone()))
                        return
                      #  InitResumeListForm(cursor, employee)


    except Exception as ex:
        print("we have an error in ReactionList")
        print(ex.args)

