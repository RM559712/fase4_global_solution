import datetime
import os
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

    print('-= Localização =-')
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
Método responsável pela formatação de visualização do ID do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['LOC_ID']}' if 'LOC_ID' in dict_data and type(dict_data['LOC_ID']) != None and Helper.is_int(dict_data['LOC_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da localização: ')

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
Método responsável pela formatação de visualização do nome do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_name(dict_data: dict = {}) -> str:

    str_return = 'Nome da localização: '
    str_return += f'{dict_data['LOC_NAME'].strip()}' if 'LOC_NAME' in dict_data and type(dict_data['LOC_NAME']) != None and type(dict_data['LOC_NAME']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Nome"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_name(dict_data: dict = {}) -> str:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter o nome atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o nome da localização: '
    str_return = input(f'{str_label}')

    object_f4gs_location = F4GsLocation()

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um nome válido.')

            if bool_is_update == False and type(str_return) != str: 
                raise Exception('O conteúdo informado deve ser texto.')

            if str_return.strip() != '':

                list_params_validate = [

                    {'str_column': 'LOWER(LOC_NAME)', 'str_type_where': '=', 'value': str_return.lower().strip()},
                    F4GsLocation.get_params_to_active_data()

                ]

                if bool_is_update == True:

                    list_params_validate.append({'str_column': 'LOC_ID', 'str_type_where': '!=', 'value': dict_data['LOC_ID']})

                dict_location = object_f4gs_location.set_where(list_params_validate).get_one()

                if type(dict_location) == dict:
                    raise Exception(f'Já existe um registro cadastrado com o nome "{str_return.strip()}".')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela formatação de visualização do CEP do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_cep(dict_data: dict = {}) -> str:

    str_return = 'CEP: '
    str_return += f'{str(dict_data['LAD_CEP']).rjust(8, '0')}' if 'LAD_CEP' in dict_data and type(dict_data['LAD_CEP']) != None and Helper.is_int(dict_data['LAD_CEP']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "CEP"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_cep(dict_data: dict = {}) -> int:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter o CEP atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_cep(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o CEP em formato numérico ( ex.: 12345678 ): '
    int_return = input(f'{str_label}')

    object_correios = Correios()

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informado um CEP válido.')

            if bool_is_update == False and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico ( ex.: 12345678 ).')

            if int_return.strip() != '':

                dict_address_data = object_correios.get_address_data_by_cep(int_cep = int(int_return.strip()))
                if dict_address_data['status'] == False:
                    raise Exception(dict_address_data['message'])

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return) if int_return.strip() != '' else None


"""
Método responsável pela formatação de visualização da rua do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_street(dict_data: dict = {}) -> str:

    str_return = 'Rua: '
    str_return += f'{dict_data['LAD_STREET'].strip()}' if 'LAD_STREET' in dict_data and type(dict_data['LAD_STREET']) != None and type(dict_data['LAD_STREET']) == str else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do número do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_number(dict_data: dict = {}) -> str:

    str_return = 'Número: '
    str_return += f'{dict_data['LAD_NUMBER'].strip()}' if 'LAD_NUMBER' in dict_data and type(dict_data['LAD_NUMBER']) != None and (type(dict_data['LAD_NUMBER']) == str or Helper.is_int(dict_data['LAD_NUMBER']) == True) else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Número"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_address_number(dict_data: dict = {}) -> str:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter o número atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_address_number(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o número: '
    str_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and str_return.strip() == '':
                raise Exception('Deve ser informado um número válido.')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    return str(str_return.strip())


"""
Método responsável pela formatação de visualização do complemento do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_complement(dict_data: dict = {}) -> str:

    str_return = 'Complemento: '
    str_return += f'{dict_data['LAD_COMPLEMENT'].strip()}' if 'LAD_COMPLEMENT' in dict_data and type(dict_data['LAD_COMPLEMENT']) != None and type(dict_data['LAD_COMPLEMENT']) == str else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Complemento"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_address_complement(dict_data: dict = {}) -> str:

    bool_is_update = ('LOC_ID' in dict_data and type(dict_data['LOC_ID']) == int)

    str_label = f'Importante: Caso deseje manter o complemento atual ( abaixo ), basta ignorar o preenchimento. Caso queira apagar o valor, digite "none".\n{format_data_view_address_complement(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o complemento: '
    str_return = input(f'{str_label}')

    while True:

        try:

            

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            str_return = input()

    if str_return.strip() == 'none': return ''
    elif str_return.strip() == '': return None
    else: return str_return.strip()


"""
Método responsável pela formatação de visualização do bairro do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_neighborhood(dict_data: dict = {}) -> str:

    str_return = 'Bairro: '
    str_return += f'{dict_data['LAD_NEIGHBORHOOD'].strip()}' if 'LAD_NEIGHBORHOOD' in dict_data and type(dict_data['LAD_NEIGHBORHOOD']) != None and type(dict_data['LAD_NEIGHBORHOOD']) == str else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da cidade do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_city(dict_data: dict = {}) -> str:

    str_return = 'Cidade: '
    str_return += f'{dict_data['LAD_CITY'].strip()}' if 'LAD_CITY' in dict_data and type(dict_data['LAD_CITY']) != None and type(dict_data['LAD_CITY']) == str else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do estado do endereço do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_address_state(dict_data: dict = {}) -> str:

    str_return = 'Estado: '
    str_return += f'{dict_data['LAD_STATE'].strip()}' if 'LAD_STATE' in dict_data and type(dict_data['LAD_STATE']) != None and type(dict_data['LAD_STATE']) == str else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do endereço completo do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_full_address(dict_data: dict = {}) -> str:

    str_return = 'Endereço: '

    str_return += f'{dict_data['LAD_STREET'].strip()}, nº {dict_data['LAD_NUMBER'].strip()}'

    if 'LAD_COMPLEMENT' in dict_data and type(dict_data['LAD_COMPLEMENT']) != None and type(dict_data['LAD_COMPLEMENT']) == str:
        str_return += f', {dict_data['LAD_COMPLEMENT'].strip()}'

    str_return += f', {dict_data['LAD_NEIGHBORHOOD'].strip()}, {dict_data['LAD_CITY'].strip()}, {dict_data['LAD_STATE'].strip()}, CEP {str(dict_data['LAD_CEP']).rjust(8, '0')}'

    return str_return


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['LOC_INSERT_DATE'])}' if 'LOC_INSERT_DATE' in dict_data and type(dict_data['LOC_INSERT_DATE']) != None and type(dict_data['LOC_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['LOC_UPDATE_DATE'])}' if 'LOC_UPDATE_DATE' in dict_data and type(dict_data['LOC_UPDATE_DATE']) != None and type(dict_data['LOC_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Localização"

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
        str_return += f'- {format_data_view_full_address(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Localização"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4gs_location = F4GsLocation()

    object_f4gs_location.set_select(['LOC.*', 'LAD.*'])
    object_f4gs_location.set_table('F4_GS_LOCATION LOC')
    object_f4gs_location.set_join([
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F4_GS_LOCATION_ADDRESS LAD', 'str_where': 'LAD.LAD_LOC_ID = LOC.LOC_ID'},
    ])
    object_f4gs_location.set_where([F4GsLocation.get_params_to_active_data()])
    object_f4gs_location.set_order([{'str_column': 'LOC_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4gs_location.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada localização
"""
def get_data_by_id(int_loc_id: int = 0) -> dict:

    object_f4gs_location = F4GsLocation()

    object_f4gs_location.set_select(['LOC.*', 'LAD.*'])
    object_f4gs_location.set_table('F4_GS_LOCATION LOC')
    object_f4gs_location.set_join([
        {'str_type_join': 'LEFT JOIN', 'str_table': 'F4_GS_LOCATION_ADDRESS LAD', 'str_where': 'LAD.LAD_LOC_ID = LOC.LOC_ID'},
    ])
    object_f4gs_location.set_where([

        {'str_column': 'LOC_ID', 'str_type_where': '=', 'value': int_loc_id},
        F4GsLocation.get_params_to_active_data()

    ])

    dict_data = object_f4gs_location.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_loc_id}.')

    return object_f4gs_location


"""
Método responsável por executar a ação de retorno de dados de endereço de uma determinada localização
"""
def get_data_address_by_id(int_loc_id: int = 0) -> dict:

    object_f4gs_location_address = F4GsLocationAddress()

    object_f4gs_location_address.set_where([

        {'str_column': 'LAD_LOC_ID', 'str_type_where': '=', 'value': int_loc_id},
        F4GsLocationAddress.get_params_to_active_data()

    ])

    dict_data = object_f4gs_location_address.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro de endereço foi localizado com o ID {int_loc_id}.')

    return object_f4gs_location_address


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Localização"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da localização.')
    print('')

    str_loc_name = validate_name()

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte do endereço da localização. O preenchimento é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    int_lad_cep = validate_cep()

    object_correios = Correios()

    dict_address_data = object_correios.get_address_data_by_cep(int_cep = int_lad_cep)
    if dict_address_data['status'] == False:
        raise Exception(dict_address_data['message'])

    print('')
    print(Correios.format_data_view(dict_params = dict_address_data['dict_data']))

    print('')

    str_lad_number = validate_address_number()

    print('')

    str_lad_complement = validate_address_complement()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['LOC_NAME'] = str_loc_name

    object_f4gs_location = F4GsLocation()
    object_f4gs_location.insert(dict_data)

    int_loc_id = object_f4gs_location.get_last_id()

    # ------------------------------------------
    # Processo de cadastro dos dados de endereço
    # ------------------------------------------

    dict_data_location_address = {}

    dict_data_location_address['LAD_LOC_ID'] = int_loc_id

    dict_data_location_address['LAD_CEP'] = int_lad_cep

    dict_data_location_address['LAD_STREET'] = dict_address_data['dict_data']['logradouro']
    dict_data_location_address['LAD_NUMBER'] = str_lad_number

    if type(str_lad_complement) != type(None):
        dict_data_location_address['LAD_COMPLEMENT'] = str_lad_complement

    dict_data_location_address['LAD_NEIGHBORHOOD'] = dict_address_data['dict_data']['bairro']
    dict_data_location_address['LAD_CITY'] = dict_address_data['dict_data']['localidade']
    dict_data_location_address['LAD_STATE'] = dict_address_data['dict_data']['estado']

    object_f4gs_location_address = F4GsLocationAddress()
    object_f4gs_location_address.insert(dict_data_location_address)

    # Retorno de dados após o cadastro
    object_f4gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f4gs_location.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Localização"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_loc_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f4gs_location.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da localização.')
    print('')

    str_loc_name = validate_name(dict_data)

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    print('Os próximos parâmetros fazem parte do endereço da localização. O preenchimento é obrigatório.')
    input(f'\nPressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    int_lad_cep = validate_cep(dict_data)

    if Helper.is_int(int_lad_cep) == True:

        object_correios = Correios()

        dict_address_data = object_correios.get_address_data_by_cep(int_cep = int_lad_cep)
        if dict_address_data['status'] == False:
            raise Exception(dict_address_data['message'])

        print('')
        print(Correios.format_data_view(dict_params = dict_address_data['dict_data']))

    print('')

    str_lad_number = validate_address_number(dict_data)

    print('')

    str_lad_complement = validate_address_complement(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    if str_loc_name.strip() != '':
        dict_data['LOC_NAME'] = str_loc_name

    object_f4gs_location.update(dict_data)

    # ---------------------------------------------
    # Processo de atualização dos dados de endereço
    # ---------------------------------------------

    object_f4gs_location_address = get_data_address_by_id(int_loc_id)
    dict_data_location_address = object_f4gs_location_address.get_one()

    if Helper.is_int(int_lad_cep) == True:

        dict_data_location_address['LAD_CEP'] = int_lad_cep
        dict_data_location_address['LAD_STREET'] = dict_address_data['dict_data']['logradouro']
        dict_data_location_address['LAD_NEIGHBORHOOD'] = dict_address_data['dict_data']['bairro']
        dict_data_location_address['LAD_CITY'] = dict_address_data['dict_data']['localidade']
        dict_data_location_address['LAD_STATE'] = dict_address_data['dict_data']['estado']

    if str_lad_number.strip() != '':
        dict_data_location_address['LAD_NUMBER'] = str_lad_number

    if type(str_lad_complement) != type(None):
        dict_data_location_address['LAD_COMPLEMENT'] = str_lad_complement

    object_f4gs_location_address.update(dict_data_location_address)

    # Retorno de dados após as atualizações
    object_f4gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f4gs_location.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Localização"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_loc_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_location = get_data_by_id(int_loc_id)
    dict_data = object_f4gs_location.get_one()

    dict_data['LOC_STATUS'] = F4GsLocation.STATUS_DELETED

    object_f4gs_location.update(dict_data)

    print('Registro excluído com sucesso.')

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