import PySimpleGUI as sg
from EmployeeInfoForm import  InitEmployeeInfoForm
from ResumeList import  InitResumeListForm
from VacancyForEmployee import InitVacancyFEForm
from ReactionList import InitReactionListForm
def InitEmplyeeForm(db,cursor,employee):
    sg.theme('LightGrey2')

    EmployeeFormLayout = [
        [[sg.Button('Переглянути доступні вакансії', size=(50, 1))],
         [sg.Button('Переглянути особисту інформацію', size=(50, 1))],
        [sg.Button('Мої резюме', size=(50, 1))],
         [sg.Button('переглянути результати по поданим заявкам', size=(50, 1))],
         [sg.Button('Вихід', size=(50, 1))]]
    ]

    # Create the Window
    EmployeeFormWindow = sg.Window('Форма працівника. \"Work Finder\"', EmployeeFormLayout)
    while True:
        event, values = EmployeeFormWindow.read()
        if event == sg.WIN_CLOSED or event == 'Вихід':  # if user closes window or clicks cancel
            EmployeeFormWindow.close()
            return
        if event == 'Переглянути особисту інформацію':
            employee = InitEmployeeInfoForm(cursor, employee)
        if event == 'Мої резюме':
            InitResumeListForm(cursor,employee)
        if event == 'Переглянути доступні вакансії':
            command = '''
            SELECT * FROM Вакансія
            ;
            '''
            cursor.execute(command)
            vacancies = cursor.fetchall()
            for i in range(len(vacancies)):
                if InitVacancyFEForm(cursor, vacancies[i]) == False:
                    break
        if event == 'переглянути результати по поданим заявкам':
            InitReactionListForm(cursor, employee)


