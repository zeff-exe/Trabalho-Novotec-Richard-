import PySimpleGUI as sg
import re

sg.theme('DarkGrey15')

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    
    soma = sum(int(digit) * (10 - i) for i, digit in enumerate(cpf[:9]))
    dv = (soma * 10) % 11
    dv = 0 if dv == 10 else dv

    if int(cpf[9]) != dv:
        return False

    soma = sum(int(digit) * (11 - i) for i, digit in enumerate(cpf[:10]))
    dv = (soma * 10) % 11
    dv = 0 if dv == 10 else dv

    return int(cpf[10]) == dv

def Validar(cpf, senha):
    with open('usuarios.txt', 'r') as file:
        for line in file:
            campos = line.strip().split(':')
            if len(campos) == 2:
                cpf_file, senha_file = campos
                if cpf == cpf_file and senha == senha_file:
                    return True
    return False

def register():
    layout = [
        [sg.Text("Registro de Usuário")],
        [sg.Text("Nome:"), sg.Input(key="user")],
        [sg.Text("E-mail:"), sg.Input(key="email")],
        [sg.Text("Senha:"), sg.Input(key="password", password_char="*")],
        [sg.Text("CPF:"), sg.Input(key="cpf")],
        [sg.Text("Confirmar Senha:"), sg.Input(key="confirm", password_char="*")],
        [sg.Button("Registrar"), sg.Button("Cancelar")]
    ]

    window = sg.Window("Registrar", layout)

    while True:
        event, values = window.read()

        if event == "Registrar":
            nome = values["user"]
            email = values["email"]
            senha = values["password"]
            confirmar_senha = values["confirm"]
            cpf = values["cpf"]

            if senha != confirmar_senha:
                sg.popup("Senhas não conferem")
            elif validar_cpf(cpf):
                sg.popup("Usuário registrado com sucesso!")
                with open("usuarios.txt", "a") as arquivo:
                    arquivo.write(f"{cpf}:{senha}\n")
                window.close()
                break
            else:
                sg.popup('CPF inválido')
        elif event == "Cancelar" or event == sg.WIN_CLOSED:
            break

    window.close()

def login():
    layout = [
        [sg.Text('CPF'), sg.Input(key='cpf')],
        [sg.Text('Senha'), sg.Input(key='password', password_char='*')],
        [sg.Button('Login')],
        [sg.Text('Caso não tenha conta, clique para criar uma conta.'), sg.Button('Criar Conta')]
    ]

    window = sg.Window('Login', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Login':
            if Validar(values['cpf'], values['password']):
                sg.popup('Login efetuado com sucesso!')
                window.close()
                media()
            else:
                sg.popup('Login não autorizado.')
        elif event == 'Criar Conta':
            register()
            pass

    window.close()

def media():
    alunos = []
    melhor_aluno = {}

    layout = [
        [sg.Text("Digite o nome do aluno:")],
        [sg.InputText(key="nome")],
        [sg.Text("Digite a primeira nota do aluno:")],
        [sg.InputText(key="nota1")],
        [sg.Text("Digite a segunda nota do aluno:")],
        [sg.InputText(key="nota2")],
        [sg.Button("Cadastrar"), sg.Button("Sair")],
        [sg.Text("", key="mensagem")]
    ]

    window = sg.Window("Cadastrar Alunos", layout)

    while True:
        event, values = window.read()
        if event == "Sair" or event == sg.WIN_CLOSED:
            break
        elif event == "Cadastrar":
            nome = values["nome"]
            nota1 = values["nota1"]
            nota2 = values["nota2"]

            if not nome.isalpha():
                window["mensagem"].update("Digite um nome válido.")
                continue
            if not nota1.isdigit() or not nota2.isdigit():
                window["mensagem"].update("Ambas as notas devem ser numéricas e positivas.")
                continue
            nota1, nota2 = int(nota1), int(nota2)
            if nota1 < 0 or nota2 < 0 or nota1 > 10 or nota2 > 10:
                window["mensagem"].update("Notas devem ser entre 0 e 10.")
                continue

            media = (nota1 + nota2) / 2
            classificacao = "A" if media >= 9 else "B" if media >= 8 else "C" if media >= 7 else "D" if media >= 6 else "E" if media >= 5 else "F"
            aluno = {"nome": nome, "media": media, "classificacao": classificacao}
            alunos.append(aluno)

            if not melhor_aluno or media > melhor_aluno.get("media", 0):
                melhor_aluno = aluno

            window["mensagem"].update("Aluno cadastrado com sucesso!")

    window.close()

    # Exibição dos resultados
    texto_resultados = "\n".join(f"Aluno: {aluno['nome']}: média: {aluno['media']}: Aproveitamento: {aluno['classificacao']} ({'APROVADO' if aluno['media'] >= 7 else 'REPROVADO'})" for aluno in alunos)
    if melhor_aluno:
        texto_resultados += f"\n\nMelhor Aluno:\n{melhor_aluno['nome']}: Aproveitamento: {melhor_aluno['classificacao']}"

    layout_resultados = [
        [sg.Text("Resultados Finais:")],
        [sg.Multiline(texto_resultados, size=(40, 10), key="resultados", disabled=True)],
        [sg.Button("Fechar")]
    ]

    window_resultados = sg.Window("Resultados", layout_resultados)

    while True:
        event, values = window_resultados.read()
        if event == "Fechar" or event == sg.WIN_CLOSED:
            break

    window_resultados.close()

def main():
    while True:
        layout = [
            [sg.Text('Escolha uma opção:')],
            [sg.Button('Login'), sg.Button('Registrar')]
        ]
        window = sg.Window('Menu Principal', layout)

        event, values = window.read()
        window.close()

        if event == 'Login':
            login()
        elif event == 'Registrar':
            register()
        else:
            break

main()