import os
import sys
import time

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from custom.helper import Helper
from models.database.database import Database

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes à estrutura do sistema
# ---------------------------------------------------------------------------------------------------------------

"""
Método responsável por executar teste de conexão com o banco de dados
"""
def test_connection_by_database():

    object_database = Database()
    object_database.test_connection_by_database()


"""
Método responsável por retornar o diretório de execução do sistema
"""
def get_current_path_dir() -> str:

    return os.path.dirname(os.path.dirname(__file__))


"""
Método responsável por retornar o diretório de execução de scripts do sistema
"""
def get_current_path_dir_scripts() -> str:

    str_current_path_dir = get_current_path_dir()

    return f'{os.path.dirname(str_current_path_dir)}{os.sep}scripts'


"""
Método responsável por executar o "reset" do bloco de comandos
"""
def reset_commands():

    os.system('cls')
    os.system('clear')


"""
Método responsável por recarregar o sistema
"""
def require_reload_system():

    input(f'\nPressione <enter> para voltar ao menu principal...')
    init_system()


"""
Método responsável por exibir uma mensagem para execução de uma determinada ação
"""
def loading(str_message: str = 'Processando, por favor aguarde...', int_seconds: int = 5, bool_reset: bool = True):

    if bool_reset == True:
        show_head_system()

    print(f'\n{str_message}', end='')
    time.sleep(int_seconds)


"""
Método responsável pela exibição do cabeçalho do sistema
"""
def show_head_system():

    reset_commands()
    
    print(f'███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████')
    print(f'█░░░░░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█░░░░░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░██░░░░░░░░████████████████░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█')
    print(f'█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀░░██░░▄▀▄▀░░████████████████░░▄▀▄▀▄▀▄▀░░░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█')
    print(f'█░░▄▀░░░░░░░░░░█░░▄▀▄▀▄▀▄▀▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░░░░░░░░░█░░░░▄▀░░██░░▄▀░░░░████████████████░░▄▀░░░░▄▀▄▀░░█░░▄▀░░░░░░▄▀░░█░░▄▀░░░░░░░░░░█')
    print(f'█░░▄▀░░█████████░░▄▀░░░░░░▄▀░░██░░▄▀░░█░░▄▀░░█████████░░▄▀░░████░░▄▀░░███░░▄▀░░███████████░░▄▀▄▀░░▄▀▄▀░░██████████████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░█████████')
    print(f'█░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░░░▄▀░░███░░▄▀░░███████████░░░░▄▀▄▀▄▀░░░░███░░░░░░░░░░░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█')
    print(f'█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀▄▀░░███░░▄▀░░██░░░░░░█████░░░░▄▀░░░░█████░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█')
    print(f'█░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀░░██░░▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░░░░░▄▀░░░░███░░▄▀░░██░░▄▀░░███████░░▄▀░░███████░░░░░░░░░░░░░░█░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█░░░░░░░░░░▄▀░░█')
    print(f'█░░▄▀░░█████████░░▄▀░░██░░▄▀░░░░░░▄▀░░█░░▄▀░░█████████░░▄▀░░██░░▄▀░░█████░░▄▀░░██░░▄▀░░███████░░▄▀░░██████████████████████░░▄▀░░██░░▄▀░░█░░▄▀░░██░░▄▀░░█████████░░▄▀░░█')
    print(f'█░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░░░░░░░░░█░░▄▀░░██░░▄▀░░░░░░█░░▄▀░░░░░░▄▀░░███████░░▄▀░░██████████████████████░░▄▀░░░░▄▀▄▀░░█░░▄▀░░░░░░▄▀░░█░░░░░░░░░░▄▀░░█')
    print(f'█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░░░░░░░░░▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀░░██░░▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░███████░░▄▀░░██████████████████████░░▄▀▄▀▄▀▄▀░░░░█░░▄▀▄▀▄▀▄▀▄▀░░█░░▄▀▄▀▄▀▄▀▄▀░░█')
    print(f'█░░░░░░░░░░░░░░█░░░░░░██████████░░░░░░█░░░░░░░░░░░░░░█░░░░░░██░░░░░░░░░░█░░░░░░░░░░░░░░███████░░░░░░██████████████████████░░░░░░░░░░░░███░░░░░░░░░░░░░░█░░░░░░░░░░░░░░█')
    print(f'███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████')


"""
Método responsável por parametrizar a visualização para uma nova estapa de módulo
"""
def init_step():

    show_head_system()

    print('')


"""
Método responsável por retornar as opções de menu do sistema

Return: list
"""
def get_system_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Localização',
            'action': ModuleLocation.action_main
        },{
            'code': 2,
            'title': 'Energia Limpa',
            'action': ModuleGeneratedEnergy.action_main
        },{
            'code': 3,
            'title': 'Consumo de Energia',
            'action': ModuleConsumedEnergy.action_main
        },{
            'code': 4,
            'title': 'Estatísticas de Consumo de Energia',
            'action': ModuleEnergyStatistics.action_main
        },{
            'code': 5,
            'title': 'Sair',
            'action': action_exit
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do sistema

Return: list
"""
def get_system_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_system_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu"

Return: str
"""
def validate_system_menu_option() -> str:

    str_return = input(f'Digite uma opção: ')

    while True:

        try:

            if str_return.strip() == '':
                raise Exception('Deve ser definida uma opção válida.')

            if Helper.is_int(str_return) == False: 
                raise Exception('A opção informada deve ser numérica.')

            if int(str_return) not in get_system_menu_options_codes(): 
                raise Exception('A opção informada deve representar um dos menus disponíveis.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str_return


"""
Método responsável por solicitar a opção do sistema que deverá ser executada
"""
def require_system_menu_option():

    str_option = validate_system_menu_option()

    list_menu_options = get_system_menu_options()

    for dict_menu_option in list_menu_options:
        if dict_menu_option['code'] == int(str_option):
            dict_menu_option['action']()


"""
Método responsável por executar a inicialização do sistema
"""
def init_system():

    try:

        init_step()

        test_connection_by_database()

        list_menu_options = get_system_menu_options()

        for dict_menu_option in list_menu_options:
            print(f'{dict_menu_option['code']}. {dict_menu_option['title']}')

        print('')

        require_system_menu_option()

    except Exception as error:

        print(f'> Ocorreu o seguinte erro: {error}')
        require_reload_system()


# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes a opção "Localização"
# ---------------------------------------------------------------------------------------------------------------

import prompt.modules.location as ModuleLocation

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes a opção "Energia Limpa"
# ---------------------------------------------------------------------------------------------------------------

import prompt.modules.generated_energy as ModuleGeneratedEnergy

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes a opção "Consumo de Energia"
# ---------------------------------------------------------------------------------------------------------------

import prompt.modules.consumed_energy as ModuleConsumedEnergy

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes a opção "Estatísticas de Consumo de Energia"
# ---------------------------------------------------------------------------------------------------------------

import prompt.modules.energy_statistics as ModuleEnergyStatistics

# ... Demais módulos...

# ---------------------------------------------------------------------------------------------------------------
# Métodos referentes a opção "Sair"
# ---------------------------------------------------------------------------------------------------------------

"""
Método responsável pela saída do sistema
"""
def action_exit():

    init_step()

    print(f'Obrigado por utilizar o sistema.\n')


# ---------------------------------------------------------------------------------------------------------------

"""
Ação responsável por executar a inicialização do sistema
"""
if(__name__ == '__main__'):

    init_system()

