import PySimpleGUI as sg
from funcoes import *
from login import login

menu_def = [['Registros', ['Cadastrar', 'Atualizar Informações', 'Excluir']],
            ['Pesquisas', ['Listar todos os funcionarios']],
            ['Sair', ['Sair']]]
# Define o layout da interface gráfica
def main():
    layout = [[sg.Menu(menu_def, pad=(200,1))]]

    # Cria a janela da interface gráfica
    window = sg.Window('Sistema de Gerenciamento de funcionários',layout, element_justification='c',finalize=True)
    window.maximize()

    # Loop principal do programa
    while True:
        event, values = window.read()

        if event in(sg.WIN_CLOSED,'Sair'):
            break
        elif event == 'Cadastrar':
            cadastrar()
        elif event == 'Atualizar Informações':
            atualizar()
        elif event == 'Excluir':
            excluir()
        elif event == 'Listar todos os funcionarios':
            listar()
        else:
            sg.popup('Opção inválida. Tente novamente.')

    # Fecha a janela da interface gráfica
    window.close()
    exit()

if login():
    main()
else:
    sg.popup('Erro!')