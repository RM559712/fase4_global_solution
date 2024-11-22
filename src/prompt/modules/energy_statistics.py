import datetime
import os
import subprocess
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
import pprint
from custom.correios import Correios
from custom.helper import Helper
from models.f4_gs_location import F4GsLocation
from models.f4_gs_location_address import F4GsLocationAddress

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Estatísticas de Consumo de Energia =-')
    print('')

"""
Método responsável por verificar se existem localizações cadastradas
"""
def validate_exists_data():

    object_f4gs_location = F4GsLocation()
    bool_exists_data = object_f4gs_location.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem localizações cadastradas.')


"""
Método responsável por recarregar o módulo "Localização"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Localização"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Localização"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar estatísticas geradas em R',
            'action': action_list_statistics_r
        },{
            'code': 2,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Localização"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Localização"

Return: str
"""
def validate_menu_option() -> str:

    str_return = input(f'Digite uma opção: ')

    while True:

        try:

            if str_return.strip() == '':
                raise Exception('Deve ser definida uma opção válida.')

            if Helper.is_int(str_return) == False: 
                raise Exception('A opção informada deve ser numérica.')

            if int(str_return) not in get_menu_options_codes(): 
                raise Exception('A opção informada deve representar um dos menus disponíveis.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str_return


"""
Método responsável por solicitar a opção do sistema que deverá ser executada
"""
def require_menu_option():

    str_option = validate_menu_option()

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        if dict_menu_option['code'] == int(str_option):
            dict_menu_option['action']()


"""
Método responsável pela exibição de estatísticas geradas em R do módulo "Estatísticas de Consumo de Energia"
"""
def action_list_statistics_r():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    str_current_dir_path_scripts = Main.get_current_path_dir_scripts()

    str_file_name = 'report_energy_statistics.R'
    str_full_path = f'{str_current_dir_path_scripts}{os.sep}SCR{os.sep}{str_file_name}'

    if os.path.exists(str_full_path) == False:
        raise Exception('Não foi possível concluir o processo pois o arquivo informado para execução do relatório meteorológico em R não existe.')

    subprocess.run(['cmd', '/c', 'Rscript', str_full_path])
    
    require_reload()


"""
Método responsável pela exibição padrão do módulo "Localização"
"""
def action_main():

    try:

        Main.init_step()

        Main.test_connection_by_database()

        show_head_module()

        list_menu_options = get_menu_options()

        for dict_menu_option in list_menu_options:
            print(f'{dict_menu_option['code']}. {dict_menu_option['title']}')

        print('')

        require_menu_option()

    except Exception as error:

        print(f'> Ocorreu o seguinte erro: {error}')
        require_reload()