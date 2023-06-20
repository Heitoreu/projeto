import PySimpleGUI as sg
import datetime as dt
import json

sg.theme('DarkAmber')

def login():
        layout = [[sg.Text('Usuario: '), sg.InputText()],
                [sg.Text('Senha: '), sg.InputText()],
                [sg.Button('Entrar'), sg.Button('Cancel')] ]

        window = sg.Window('Login', layout)

        val = False
        Registro = list()

        while True:
                event, values = window.read()
                if event in (sg.WIN_CLOSED,'Cancel'):
                        break
                elif event in ('Entrar'):
                        if(values[0] == 'adm') and (values[1] == '123'):
                                with open('registro.json', 'r') as trans:
                                        Registro = json.load(trans)
                                data = dt.datetime.now().strftime('%d/%m/%y - %H:%M')
                                nome = values[0]

                                Registro.append(dict(horario_do_login = data, usuario = nome))

                                with open('registro.json', 'w') as trans:
                                        json.dump(Registro, trans, indent='\t')
                                sg.popup('Entrada confirmada', auto_close=True, auto_close_duration= 1.5)
                                window.close()
                                val = True
                                if val == False:
                                        sg.popup('login ou senha incorreta tente novamente', auto_close=True, auto_close_duration= 1.5)

        window.close()
        return True if val else False