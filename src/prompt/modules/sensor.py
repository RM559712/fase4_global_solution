import datetime
import os
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import prompt.main as Main
from custom.helper import Helper
from models.f4_gs_sensor import F4GsSensor

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Sensores =-')
    print('')

"""
Método responsável por verificar se existem sensores cadastrados
"""
def validate_exists_data():

    object_f4gs_sensor = F4GsSensor()
    bool_exists_data = object_f4gs_sensor.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem sensores cadastrados.')


"""
Método responsável por recarregar o módulo "Sensores"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Sensores"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Sensores"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar cadastros',
            'action': action_list
        },{
            'code': 2,
            'title': 'Cadastrar',
            'action': action_insert
        },{
            'code': 3,
            'title': 'Editar',
            'action': action_update
        },{
            'code': 4,
            'title': 'Excluir',
            'action': action_delete
        },{
            'code': 5,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Sensores"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Sensores"

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
Método responsável pela formatação de visualização do ID do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['SNS_ID']}' if 'SNS_ID' in dict_data and type(dict_data['SNS_ID']) != None and Helper.is_int(dict_data['SNS_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID do sensor: ')

    while True:

        try:

            if int_return.strip() == '':
                raise Exception('Deve ser informado um ID válido.')

            if Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return)


"""
Método responsável pela formatação de visualização do nome do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_name(dict_data: dict = {}) -> str:

    str_return = 'Nome do sensor: '
    str_return += f'{dict_data['SNS_NAME'].strip()}' if 'SNS_NAME' in dict_data and type(dict_data['SNS_NAME']) != None and type(dict_data['SNS_NAME']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Nome"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_name(dict_data: dict = {}) -> str:

    bool_is_update = ('SNS_ID' in dict_data and type(dict_data['SNS_ID']) == int)

    str_label = f'Importante: Caso deseje manter o nome atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o nome do sensor: '
    str_return = input(f'{str_label}')

    object_f4gs_sensor = F4GsSensor()

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um nome válido.')

            if bool_is_update == False and type(str_return) != str: 
                raise Exception('O conteúdo informado deve ser texto.')

            if str_return.strip() != '':

                list_params_validate = [

                    {'str_column': 'LOWER(SNS_NAME)', 'str_type_where': '=', 'value': str_return.lower().strip()},
                    F4GsSensor.get_params_to_active_data()

                ]

                if bool_is_update == True:

                    list_params_validate.append({'str_column': 'SNS_ID', 'str_type_where': '!=', 'value': dict_data['SNS_ID']})

                dict_sensor = object_f4gs_sensor.set_where(list_params_validate).get_one()

                if type(dict_sensor) == dict:
                    raise Exception(f'Já existe um registro cadastrado com o nome "{str_return.strip()}".')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela formatação de visualização do código de série do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_serie_code(dict_data: dict = {}) -> str:

    str_return = 'Código de série do sensor: '
    str_return += f'{dict_data['SNS_SERIE_CODE'].strip()}' if 'SNS_SERIE_CODE' in dict_data and type(dict_data['SNS_SERIE_CODE']) != None and type(dict_data['SNS_SERIE_CODE']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Código de série"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_serie_code(dict_data: dict = {}) -> str:

    bool_is_update = ('SNS_ID' in dict_data and type(dict_data['SNS_ID']) == int)

    str_label = f'Importante: Caso deseje manter o código de série atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_serie_code(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o código de série do sensor: '
    str_return = input(f'{str_label}')

    object_f4gs_sensor = F4GsSensor()

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um código de série válido.')

            if bool_is_update == False and (type(str_return) != str and Helper.is_int(str_return) == False): 
                raise Exception('O conteúdo informado deve ser texto ou numérico.')

            if str_return.strip() != '':

                list_params_validate = [

                    {'str_column': 'SNS_SERIE_CODE', 'str_type_where': '=', 'value': str_return.lower().strip()},
                    F4GsSensor.get_params_to_active_data()

                ]

                if bool_is_update == True:

                    list_params_validate.append({'str_column': 'SNS_ID', 'str_type_where': '!=', 'value': dict_data['SNS_ID']})

                dict_sensor = object_f4gs_sensor.set_where(list_params_validate).get_one()

                if type(dict_sensor) == dict:
                    raise Exception(f'Já existe um registro cadastrado com o código de série "{str_return.strip()}".')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela formatação de visualização do tipo de sensor do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_type(dict_data: dict = {}) -> str:

    str_return = 'Tipo de sensor: '
    str_return += f'{F4GsSensor.get_type_options(dict_data['SNS_TYPE'])['title']}' if 'SNS_TYPE' in dict_data and type(dict_data['SNS_TYPE']) != None and Helper.is_int(dict_data['SNS_TYPE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Código de série"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_type(dict_data: dict = {}) -> int:

    bool_is_update = ('SNS_ID' in dict_data and type(dict_data['SNS_ID']) == int)

    str_label = f'Importante: Caso deseje manter o tipo de sensor atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_type(dict_data)}\n' if bool_is_update == True else ''

    str_label += f'Os tipos de sensores são: '
    list_type_options = F4GsSensor.get_type_options()
    for list_type_option in list_type_options:
        str_label += f'{list_type_option['title']} [{list_type_option['code']}]; '

    str_label += f'\nInforme o código do tipo de sensor: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informado um tipo de sensor válido.')

            if bool_is_update == False and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if int_return.strip() != '':

                if int(int_return) not in F4GsSensor.get_type_options_codes(): 
                    raise Exception('A opção informada deve representar um dos tipos disponíveis.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return) if int_return.strip() != '' else 0


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['SNS_INSERT_DATE'])}' if 'SNS_INSERT_DATE' in dict_data and type(dict_data['SNS_INSERT_DATE']) != None and type(dict_data['SNS_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['SNS_UPDATE_DATE'])}' if 'SNS_UPDATE_DATE' in dict_data and type(dict_data['SNS_UPDATE_DATE']) != None and type(dict_data['SNS_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )
- bool_show_id: Status informando se o parâmetro "ID" deverá ser exibido ( bool )
- bool_show_insert_date: Status informando se o parâmetro "Data de cadastro" deverá ser exibido ( bool )
- bool_show_update_date Status informando se o parâmetro "Data de atualização" deverá ser exibido ( bool )

Return: str
"""
def format_data_view(dict_data: dict = {}, bool_show_id: bool = True, bool_show_insert_date: bool = True, bool_show_update_date: bool = True) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_id(dict_data)} \n' if bool_show_id == True else ''
        str_return += f'- {format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_serie_code(dict_data)} \n'
        str_return += f'- {format_data_view_type(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Sensores"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4gs_sensor = F4GsSensor()

    object_f4gs_sensor.set_where([F4GsSensor.get_params_to_active_data()])
    object_f4gs_sensor.set_order([{'str_column': 'SNS_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4gs_sensor.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de um determinado sensor
"""
def get_data_by_id(int_sns_id: int = 0) -> dict:

    object_f4gs_sensor = F4GsSensor()

    object_f4gs_sensor.set_where([

        {'str_column': 'SNS_ID', 'str_type_where': '=', 'value': int_sns_id},
        F4GsSensor.get_params_to_active_data()

    ])

    dict_data = object_f4gs_sensor.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_sns_id}.')

    return object_f4gs_sensor


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Sensores"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do sensor.')
    print('')

    str_sns_name = validate_name()

    print('')

    str_sns_serie_code = validate_serie_code()

    print('')

    int_sns_type = validate_type()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['SNS_NAME'] = str_sns_name
    dict_data['SNS_SERIE_CODE'] = str_sns_serie_code
    dict_data['SNS_TYPE'] = int_sns_type

    object_f4gs_sensor = F4GsSensor()
    object_f4gs_sensor.insert(dict_data)

    int_sns_id = object_f4gs_sensor.get_last_id()

    # Retorno de dados após o cadastro
    object_f4gs_sensor = get_data_by_id(int_sns_id)
    dict_data = object_f4gs_sensor.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Sensores"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_sns_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor = get_data_by_id(int_sns_id)
    dict_data = object_f4gs_sensor.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do sensor.')
    print('')

    str_sns_name = validate_name(dict_data)

    print('')

    str_sns_serie_code = validate_serie_code(dict_data)

    print('')

    str_sns_type = validate_type(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    if str_sns_name.strip() != '':
        dict_data['SNS_NAME'] = str_sns_name

    if str_sns_serie_code.strip() != '':
        dict_data['SNS_SERIE_CODE'] = str_sns_serie_code
    
    if str_sns_type > 0:
        dict_data['SNS_TYPE'] = str_sns_type

    object_f4gs_sensor.update(dict_data)

    # Retorno de dados após as atualizações
    object_f4gs_sensor = get_data_by_id(int_sns_id)
    dict_data = object_f4gs_sensor.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Sensores"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_sns_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor = get_data_by_id(int_sns_id)
    dict_data = object_f4gs_sensor.get_one()

    dict_data['SNS_STATUS'] = F4GsSensor.STATUS_DELETED

    object_f4gs_sensor.update(dict_data)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Sensores"
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