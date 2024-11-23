import datetime
import os
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as Pyplot
import prompt.main as Main
import prompt.modules.location as ModuleLocation
from custom.helper import Helper
from models.f4_gs_consumed_energy import F4GsConsumedEnergy

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Consumo de Energia =-')
    print('')


"""
Método responsável por verificar se existem consumos cadastrados
"""
def validate_exists_data():

    object_f4gs_consumed_energy = F4GsConsumedEnergy()
    bool_exists_data = object_f4gs_consumed_energy.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem consumos cadastrados.')


"""
Método responsável por recarregar o módulo "Consumo"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Consumo"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Consumo"

Return: list
"""
def get_menu_options() -> list:

    """{
        'code': ,
        'title': 'Editar consumo de energia',
        'action': action_update
    },{
        'code': ,
        'title': 'Excluir consumo de energia',
        'action': action_delete
    }"""

    return [
        {
            'code': 1,
            'title': 'Visualizar consumo de energia',
            'action': action_list
        },{
            'code': 2,
            'title': 'Visualizar consumo de energia por mês e ano',
            'action': action_list_month_year
        },{
            'code': 3,
            'title': 'Visualizar gráfico com consumo de energia por mês e ano',
            'action': action_graphic_month_year
        },{
            'code': 4,
            'title': 'Cadastrar consumo de energia',
            'action': action_insert
        },{
            'code': 5,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Consumo"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Consumo"

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
Método responsável pela formatação de visualização do ID do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['CNE_ID']}' if 'CNE_ID' in dict_data and type(dict_data['CNE_ID']) != None and Helper.is_int(dict_data['CNE_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID do consumo: ')

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
Método responsável pela validação do parâmetro "Localização"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_location_id(dict_data: dict = {}) -> int:

    bool_is_update = ('CNE_ID' in dict_data and type(dict_data['CNE_ID']) == int)

    str_label = f'Importante: Caso deseje manter a localização atual ( abaixo ), basta ignorar o preenchimento.\n{ModuleLocation.format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe a localização: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informada uma localização válida.')

            if int_return.strip() != '' and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if Helper.is_int(int_return) == True:

                get_data_location_by_id(int_return)

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return int(int_return) if int_return.strip() != '' else None


"""
Método responsável pela formatação de visualização do valor do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_value(dict_data: dict = {}) -> str:

    str_return = 'Valor do consumo: '
    str_return += f'{dict_data['CNE_VALUE']} kWh' if 'CNE_VALUE' in dict_data and type(dict_data['CNE_VALUE']) != None and Helper.is_float(dict_data['CNE_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Valor do consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_value(dict_data: dict = {}) -> float:

    bool_is_update = ('CNE_ID' in dict_data and type(dict_data['CNE_ID']) == int)

    str_label = f'O valor de consumo será exibido no formato [valor] kWh ( ex.: 12 kWh, 21 kWh, etc. )\n\n'
    str_label += f'Importante: Caso deseje manter o valor do consumo atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_value(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o valor do consumo em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and float_return.strip() == '':
                raise Exception('Deve ser informado um valor válido.')

            if ',' in float_return:
                float_return = float_return.replace(',', '.')

            if bool_is_update == False and Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    return float(float_return) if float_return.strip() != '' else None


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['CNE_INSERT_DATE'])}' if 'CNE_INSERT_DATE' in dict_data and type(dict_data['CNE_INSERT_DATE']) != None and type(dict_data['CNE_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['CNE_UPDATE_DATE'])}' if 'CNE_UPDATE_DATE' in dict_data and type(dict_data['CNE_UPDATE_DATE']) != None and type(dict_data['CNE_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do valor total do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_total_value(dict_data: dict = {}) -> str:

    str_return = 'Valor total de energia consumida: '
    str_return += f'{dict_data['CNE_TOTAL_VALUE']} kWh' if 'CNE_TOTAL_VALUE' in dict_data and type(dict_data['CNE_TOTAL_VALUE']) != None and Helper.is_float(dict_data['CNE_TOTAL_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do mês e ano do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date_month_year(dict_data: dict = {}) -> str:

    str_return = 'Mês e ano: '
    str_return += f'{dict_data['CNE_INSERT_DATE_MONTH_YEAR']}' if 'CNE_INSERT_DATE_MONTH_YEAR' in dict_data and type(dict_data['CNE_INSERT_DATE_MONTH_YEAR']) != None else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Consumo"

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
        str_return += f'- {ModuleLocation.format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela formatação de visualização de dados agrupados por mês e ano do módulo "Consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_month_year(dict_data: dict = {}) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_total_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date_month_year(dict_data)} \n'

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Consumo"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com a localização informada.')
    print('')

    int_cne_loc_id = validate_location_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_consumed_energy = F4GsConsumedEnergy()

    object_f4gs_consumed_energy.set_select(['CNE.*', 'LOC.LOC_NAME'])
    object_f4gs_consumed_energy.set_table('F4_GS_CONSUMED_ENERGY CNE')
    object_f4gs_consumed_energy.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_GS_LOCATION LOC', 'str_where': 'LOC.LOC_ID = CNE.CNE_LOC_ID'}
    ])
    object_f4gs_consumed_energy.set_where([
        F4GsConsumedEnergy.get_params_to_active_data(),
        F4GsConsumedEnergy.get_params_to_location(int_cne_loc_id)
    ])
    object_f4gs_consumed_energy.set_order([{'str_column': 'CNE_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4gs_consumed_energy.get_data().get_list()

    if list_data == None:
        raise Exception('Não existem consumos cadastrados para essa localização.')

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável pela exibição de cadastros do módulo "Consumo"
"""
def action_list_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com a localização informada.')
    print('')

    int_cne_loc_id = validate_location_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_consumed_energy = F4GsConsumedEnergy()

    dict_data_by_month_year = object_f4gs_consumed_energy.get_data_by_month_year(int_cne_loc_id = int_cne_loc_id)
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    if dict_data_by_month_year['list_data'] == None:
        raise Exception('Não existem consumos cadastrados para essa localização.')

    for dict_data in dict_data_by_month_year['list_data']:

        print(format_data_view_month_year(dict_data))

    require_reload()


"""
Método responsável pela exibição de gráficos do módulo "Consumo"
"""
def action_graphic_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com a localização informada.')
    print('')

    int_cne_loc_id = validate_location_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_consumed_energy = F4GsConsumedEnergy()

    dict_data_by_month_year = object_f4gs_consumed_energy.get_data_by_month_year(str_order = 'ASC', int_cne_loc_id = int_cne_loc_id)
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    if dict_data_by_month_year['list_data'] == None:
        raise Exception('Não existem consumos cadastrados para essa localização.')

    list_month_year = []
    list_value = []

    for dict_data in dict_data_by_month_year['list_data']:

        list_month_year.append(dict_data['CNE_INSERT_DATE_MONTH_YEAR'])
        list_value.append(dict_data['CNE_TOTAL_VALUE'])

    for xi, yi, str_title in zip(list_month_year, list_value, list_value):
        Pyplot.annotate(f'{str_title} kWh', (xi, yi), color = '#E31414', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')

    Pyplot.plot(list_month_year, list_value, marker = 'o', color = '#E31414')
    Pyplot.title("Energia consumida por mês e ano")
    Pyplot.xlabel("Mês e ano")
    Pyplot.ylabel("Energia consumida em kWh")
    Pyplot.grid(True, linestyle = ':')

    Main.init_step()

    show_head_module()

    print('Visualizando gráfico...')

    Pyplot.show()

    Main.init_step()

    show_head_module()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável por executar a ação de retorno de dados de um determinado consumo
"""
def get_data_by_id(int_cne_id: int = 0) -> dict:

    object_f4gs_consumed_energy = F4GsConsumedEnergy()

    object_f4gs_consumed_energy.set_select(['CNE.*', 'LOC.LOC_NAME'])
    object_f4gs_consumed_energy.set_table('F4_GS_CONSUMED_ENERGY CNE')
    object_f4gs_consumed_energy.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_GS_LOCATION LOC', 'str_where': 'LOC.LOC_ID = CNE.CNE_LOC_ID'}
    ])
    object_f4gs_consumed_energy.set_where([

        {'str_column': 'CNE_ID', 'str_type_where': '=', 'value': int_cne_id},
        F4GsConsumedEnergy.get_params_to_active_data()

    ])

    dict_data = object_f4gs_consumed_energy.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_cne_id}.')

    return object_f4gs_consumed_energy


"""
Método responsável por executar a ação de retorno de dados de uma determinada localização
"""
def get_data_location_by_id(loc_id: int = 0) -> dict:

    object_f4gs_location = ModuleLocation.get_data_by_id(loc_id)
    dict_data = object_f4gs_location.get_one()

    return dict_data


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Consumo"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do consumo.')
    print('')

    int_cne_loc_id = validate_location_id()

    print('')

    float_cne_value = validate_value()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['CNE_LOC_ID'] = int_cne_loc_id
    dict_data['CNE_VALUE'] = float_cne_value

    object_f4gs_consumed_energy = F4GsConsumedEnergy()
    object_f4gs_consumed_energy.insert(dict_data)

    int_cne_id = object_f4gs_consumed_energy.get_last_id()

    # Retorno de dados após o cadastro
    object_f4gs_consumed_energy = get_data_by_id(int_cne_id)
    dict_data = object_f4gs_consumed_energy.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Consumo"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_cne_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_consumed_energy = get_data_by_id(int_cne_id)
    dict_data = object_f4gs_consumed_energy.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do consumo.')
    print('')

    int_cne_loc_id = validate_location_id(dict_data)

    print('')

    float_cne_value = validate_value(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    if Helper.is_int(int_cne_loc_id) == True:
        dict_data['CNE_LOC_ID'] = int_cne_loc_id

    if Helper.is_float(float_cne_value) == True:
        dict_data['CNE_VALUE'] = float_cne_value

    object_f4gs_consumed_energy.update(dict_data)

    # Retorno de dados após as atualizações
    object_f4gs_consumed_energy = get_data_by_id(int_cne_id)
    dict_data = object_f4gs_consumed_energy.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Consumo"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_cne_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_consumed_energy = get_data_by_id(int_cne_id)
    dict_data = object_f4gs_consumed_energy.get_one()

    dict_data['CNE_STATUS'] = F4GsConsumedEnergy.STATUS_DELETED

    object_f4gs_consumed_energy.update(dict_data)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Consumo"
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