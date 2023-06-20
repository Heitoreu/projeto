import json
import PySimpleGUI as sg

caminho = 'dados.json'
funci = json.load(open(caminho))
cargos = ['Atendente', 'Gerente', 'Supervisor', 'Estagiario']

sg.theme('DarkAmber')
menu_def = [['Registros', ['Cadastrar', 'Atualizar Informações', 'Excluir']],
            ['Pesquisas', ['Listar todos os funcionarios']],
            ['Sair', ['Sair']]]


#Funcao para ler os arquivos do Json
def carregar():
    try:
        with open(caminho, 'r') as openfile:
            funci = json.load(openfile)
            if len(funci) == 0:
                sg.popup("Nenhum funcionário  cadastrado!")
                return None
            return funci
    except:
        sg.popup("Erro ao carregar os funcionários.")
        return None


#Funcao para escrever os arquivos do Json        
def salvar(funci):
     with open(caminho, "w") as outfile: 
                json.dump(funci, outfile, indent='\t')


#Funcao para cadastro de 
def cadastrar():
    layout = [[sg.Menu(menu_def, pad=(200,1))],
              [sg.Text('Digite o nome do funcionário: '),sg.InputText(key='nome')],
              [sg.Text('Digite o sobrenome do funcionario: '), sg.InputText(key='sobrenome')],
              [sg.Text('Digite a idade do funcionário: '), sg.InputText(key='idade')],
              [sg.Text('Digite o CPF do funcionário:'),sg.InputText(key='cpf')],
              [sg.Text('Selecione o cargo desejado: '),sg.Combo(values=cargos, key='cargo')],
              [sg.Button('Cadastrar')]]
    window = sg.Window('Cadastro de funcionário', layout)
    
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Cadastrar':
            funci.append({"código": values[len(funci)],"nome": values['nome'], "sobrenome": values['sobrenome'], "idade": values['idade'], "cpf": values['cpf'], "cargo": values['cargos'], })
            salvar(funci)
            sg.popup('funcionário cadastrado com sucesso!')
    
    window.close()


#Funcao para atualizar dados do 
def atualizar():
    layout=[[sg.Menu(menu_def, pad=(200,1))],
            [sg.Text('Digite o nome completo do funcionário a ser atualizado: '), sg.InputText(key='nome_completo')],
            [sg.Button('Buscar e Atualizar', key='bt')]]
    window = sg.Window('Atualizar Cadastro',layout)
    #nome_completo = input("Digite o nome completo do  a ser excluido: ")

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'bt':
            nome, sobrenome = str(values['nome_completo']).split(' ',1)
            subs(nome, sobrenome)
    window.close()
def subs(nome, sobrenome):#interage com atualizar_aluno
    layout = [[sg.Text('Digite a nova idade do funcionário: '),sg.InputText(key='idade')],
              [sg.Text('Digite o novo cpf do funcionário: '),sg.InputText(key='cpf')],
              [sg.Text('Selecione o novo cargo do funcionário:'),sg.OptionMenu(values=cargos, key='cargo')],
              [sg.Button('Atualizar', key = 'atu')]]
    windown = sg.Window('',layout)
    
    while True:
        event,values = windown.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event == 'atu':
            for fun in funci:
                if fun['nome'].lower() == nome.lower() and fun['sobrenome'].lower() == sobrenome.lower():
                    fun['idade'] = values['idade'] if values['idade'] != '' else fun['idade']
                    fun['cpf'] = values['cpf'] if values['cpf'] != '' else fun['cpf']
                    fun['cargo'] = values['cargo'] if values['cargo'] != '' else fun['cargo']
                    salvar(funci)
                    sg.popup(f"Informacoes do funcionário {nome} {sobrenome} atualizadas com sucesso!",auto_close = True, auto_close_duration = 3)
                    windown.close()
                    return
            sg.popup(f"Não foi encontrado nenhum funcionário com o nome {nome} {sobrenome}.")
    windown.close()


#Funcao para excluir 
def excluir():
    layout=[[sg.Menu(menu_def, pad=(200,1))],
            [sg.Text('Digite o nome completo do funcionário a ser excluido: '), sg.InputText(key='nome_completo')],
            [sg.Button('Buscar e Excluir', key='bt')]]
    window = sg.Window('Excluir do cadastro',layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'bt':
            nome, sobrenome = str(values['nome_completo']).split(' ', 1)
            for fun in funci:
                if fun['nome'].lower() == nome.lower() and fun['sobrenome'].lower() == sobrenome.lower():
                    funci.remove(fun)
                    salvar(funci)
                    sg.popup(f"funcionário {values['nome_completo']} excluído com sucesso!")
                    return
                else:
                    sg.popup(f"Não foi encontrado nenhum funcionário com o nome {values['nome_completo']}.")
                    return
    
    
    window.close()


#Funcao para listar apenas os funcionários em determinado 
def listar():


    #busca e cria uma lista formatada para o sg.table
    funci = json.load(open(caminho, 'r'))
    cols = ['nome','sobrenome','idade','cpf','cargo']
    lastvalue = None
    data = list()
    
    layout = [[sg.Menu(menu_def, pad=(200,1))],
              [sg.Text('Listagem de funcionários:'),sg.OptionMenu(values=['Todos']+ [i for i in cargos],default_value='Todos', key='opc')],
              [sg.Table(values = data ,headings = cols,key='tb',expand_x=True,expand_y=True,justification='center')]]
    window = sg.Window('Lista de funcionários', layout, element_justification='r', auto_size_buttons=True,auto_size_text=True, size=(800,600))

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if values['opc'] != lastvalue:
            lastvalue = values['opc']
            data = list()
            window['tb'].update(values = data)
            if lastvalue != 'Todos':
                j = 0
                while j < len(funci):
                    i = 0
                    mid = list()
                    if funci[j]['cargo'] == values['opc']:
                        while i < len(cols):
                            mid.append(funci[j][cols[i]])
                            i += 1
                        data.append(mid)
                    j += 1
                window['tb'].update(values = data)
            else:
                j = 0
                while j < len(funci):
                    i = 0
                    mid = list()
                    while i < len(cols):
                        mid.append(funci[j][cols[i]])
                        i += 1
                    data.append(mid)
                    j += 1
                window['tb'].update(values = data)
    window.close()

#Menu 
'''while True:
    alunos = carregar_alunos()
    print("Selecione uma opcao:")
    print("1 - Cadastrar aluno")
    print("2 - Atualizar informacoes de um aluno")
    print("3 - Excluir aluno")
    print("4 - Listar todos os alunos")
    print("5 - Sair")
    opcao = int(input())

    if opcao == 1:
        cadastrar_aluno()
    elif opcao == 2:
        atualizar_aluno()
    elif opcao == 3:
        excluir_aluno()
    elif opcao == 4:
        listar_alunos()
    elif opcao == 5:
        break
    else:
        print("Opcao invalida. Tente novamente.")'''