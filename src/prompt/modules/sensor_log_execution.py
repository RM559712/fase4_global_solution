import datetime
import os
import pprint
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as Pyplot
import mplcursors
import prompt.main as Main
import prompt.modules.sensor as ModuleSensor
from custom.helper import Helper
from models.f4_gs_sensor_log_execution import F4GsSensorLogExecution

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Log de Execução de Sensores =-')
    print('')


"""
Método responsável por verificar se existem logs cadastrados
"""
def validate_exists_data():

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()
    bool_exists_data = object_f4gs_sensor_log_execution.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem logs cadastrados.')


"""
Método responsável por recarregar o módulo "Log de Execução de Sensores"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Log de Execução de Sensores"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Log de Execução de Sensores"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar logs',
            'action': action_list
        },{
            'code': 2,
            'title': 'Visualizar logs por dia, mês e ano',
            'action': action_list_day_month_year
        },{
            'code': 3,
            'title': 'Visualizar gráfico de logs por dia, mês e ano',
            'action': action_graphic_day_month_year
        },{
            'code': 4,
            'title': 'Visualizar logs por mês e ano',
            'action': action_list_month_year
        },{
            'code': 5,
            'title': 'Visualizar gráfico de logs por mês e ano',
            'action': action_graphic_month_year
        },{
            'code': 6,
            'title': 'Cadastrar',
            'action': action_insert
        },{
            'code': 7,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Log de Execução de Sensores"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Log de Execução de Sensores"

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
Método responsável pela formatação de visualização do ID do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['SLE_ID']}' if 'SLE_ID' in dict_data and type(dict_data['SLE_ID']) != None and Helper.is_int(dict_data['SLE_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID do log: ')

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
Método responsável pela validação do parâmetro "Sensor"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_sensor_id(dict_data: dict = {}) -> int:

    bool_is_update = ('SLE_ID' in dict_data and type(dict_data['SLE_ID']) == int)

    str_label = f'Importante: Caso deseje manter o sensor atual ( abaixo ), basta ignorar o preenchimento.\n{ModuleSensor.format_data_view_name(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o sensor: '
    int_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and int_return.strip() == '':
                raise Exception('Deve ser informado um sensor válido.')

            if int_return.strip() != '' and Helper.is_int(int_return) == False: 
                raise Exception('O conteúdo informado deve ser numérico.')

            if Helper.is_int(int_return) == True:

                get_data_sensor_by_id(int_return)

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            int_return = input()

    return str(int_return.strip())


"""
Método responsável pela formatação de visualização do valor do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_value(dict_data: dict = {}) -> str:

    str_return = 'Valor do consumo: '
    str_return += f'{dict_data['SLE_VALUE']} kWh' if 'SLE_VALUE' in dict_data and type(dict_data['SLE_VALUE']) != None and Helper.is_float(dict_data['SLE_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Valor do consumo"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_value(dict_data: dict = {}) -> float:

    bool_is_update = ('SLE_ID' in dict_data and type(dict_data['SLE_ID']) == int)

    str_label = f'O valor de consumo será exibido no formato [valor] kWh ( ex.: 12 kWh, 21 kWh, etc. )\n\n'
    str_label = f'Importante: Caso deseje manter o valor do consumo atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_value(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o valor do consumo em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
    float_return = input(f'{str_label}')

    while True:

        try:

            if bool_is_update == False and float_return.strip() == '':
                raise Exception('Deve ser informado um valor válido.')

            if ',' in float_return:
                float_return = float_return.replace(',', '.')

            if Helper.is_float(float_return) == False and Helper.is_int(float_return) == False:
                raise Exception('O conteúdo informado deve ser numérico ( ex.: 123, 123.45 ou 123,45 ).')

            break

        except Exception as error:

            print(f'{error} Tente novamente: ', end = '')
            float_return = input()

    return float(float_return)


"""
Método responsável pela formatação de visualização da data de cadastro do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['SLE_INSERT_DATE'])}' if 'SLE_INSERT_DATE' in dict_data and type(dict_data['SLE_INSERT_DATE']) != None and type(dict_data['SLE_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da quantidade total do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_quantity(dict_data: dict = {}) -> str:

    str_return = 'Total de execuções: '
    str_return += f'{dict_data['SLE_QUANTITY']}' if 'SLE_QUANTITY' in dict_data and type(dict_data['SLE_QUANTITY']) != None and Helper.is_float(dict_data['SLE_QUANTITY']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do valor total do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_total_value(dict_data: dict = {}) -> str:

    str_return = 'Valor total de energia consumida: '
    str_return += f'{dict_data['SLE_TOTAL_VALUE']} kWh' if 'SLE_TOTAL_VALUE' in dict_data and type(dict_data['SLE_TOTAL_VALUE']) != None and Helper.is_float(dict_data['SLE_TOTAL_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )
- bool_show_id: Status informando se o parâmetro "ID" deverá ser exibido ( bool )
- bool_show_insert_date: Status informando se o parâmetro "Data de cadastro" deverá ser exibido ( bool )

Return: str
"""
def format_data_view(dict_data: dict = {}, bool_show_id: bool = True, bool_show_insert_date: bool = True) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_id(dict_data)} \n' if bool_show_id == True else ''
        str_return += f'- {ModuleSensor.format_data_view_name(dict_data)} \n'
        str_return += f'- {format_data_view_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''

    return str_return


"""
Método responsável pela formatação de visualização do dia, mês e ano do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date_day_month_year(dict_data: dict = {}) -> str:

    str_return = 'Dia, mês e ano: '
    str_return += f'{dict_data['SLE_INSERT_DATE_DAY_MONTH_YEAR']}' if 'SLE_INSERT_DATE_DAY_MONTH_YEAR' in dict_data and type(dict_data['SLE_INSERT_DATE_DAY_MONTH_YEAR']) != None else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do mês e ano do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date_month_year(dict_data: dict = {}) -> str:

    str_return = 'Mês e ano: '
    str_return += f'{dict_data['SLE_INSERT_DATE_MONTH_YEAR']}' if 'SLE_INSERT_DATE_MONTH_YEAR' in dict_data and type(dict_data['SLE_INSERT_DATE_MONTH_YEAR']) != None else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados agrupados por dia, mês e ano do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_day_month_year(dict_data: dict = {}) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_quantity(dict_data)} \n'
        str_return += f'- {format_data_view_total_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date_day_month_year(dict_data)} \n'

    return str_return


"""
Método responsável pela formatação de visualização de dados agrupados por mês e ano do módulo "Log de Execução de Sensores"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_month_year(dict_data: dict = {}) -> str:

    str_return = None

    if len(dict_data) > 0:

        str_return = ''
        str_return += f'- {format_data_view_quantity(dict_data)} \n'
        str_return += f'- {format_data_view_total_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date_month_year(dict_data)} \n'

    return str_return


"""
Método responsável pela exibição de cadastros do módulo "Log de Execução de Sensores"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com o sensor informado.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    object_f4gs_sensor_log_execution.set_select(['SLE.*', 'SNS.SNS_NAME'])
    object_f4gs_sensor_log_execution.set_table('F4_GS_SENSOR_LOG_EXECUTION SLE')
    object_f4gs_sensor_log_execution.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_GS_SENSOR SNS', 'str_where': 'SNS.SNS_ID = SLE.SLE_SNS_ID'}
    ])
    object_f4gs_sensor_log_execution.set_where([
        F4GsSensorLogExecution.get_params_to_active_data(),
        F4GsSensorLogExecution.get_params_to_sensor(int_sle_sns_id)
    ])
    object_f4gs_sensor_log_execution.set_order([{'str_column': 'SLE.SLE_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4gs_sensor_log_execution.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável pela exibição de logs por dia, mês e ano do módulo "Log de Execução de Sensores"
"""
def action_list_day_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com o sensor informado.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    dict_data_by_day_month_year = object_f4gs_sensor_log_execution.get_data_by_day_month_year(int_sle_sns_id = int_sle_sns_id)
    if dict_data_by_day_month_year['status'] == False:
        raise Exception(dict_data_by_day_month_year['message'])

    if dict_data_by_day_month_year['list_data'] == None:
        raise Exception('Não existem logs cadastrados para esse sensor.')

    for dict_data in dict_data_by_day_month_year['list_data']:

        print(format_data_view_day_month_year(dict_data))

    require_reload()


"""
Método responsável pela exibição de gráficos logs por dia, mês e ano do módulo "Log de Execução de Sensores"
"""
def action_graphic_day_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com o sensor informado.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    dict_data_by_day_month_year = object_f4gs_sensor_log_execution.get_data_by_day_month_year(str_order = 'ASC', int_sle_sns_id = int_sle_sns_id)
    if dict_data_by_day_month_year['status'] == False:
        raise Exception(dict_data_by_day_month_year['message'])

    if dict_data_by_day_month_year['list_data'] == None:
        raise Exception('Não existem logs cadastrados para esse sensor.')

    list_day_month_year = []
    list_quantity = []
    list_value = []

    for dict_data in dict_data_by_day_month_year['list_data']:

        list_day_month_year.append(dict_data['SLE_INSERT_DATE_DAY_MONTH_YEAR'])
        list_quantity.append(dict_data['SLE_QUANTITY'])
        list_value.append(dict_data['SLE_TOTAL_VALUE'])

    for xi, yi, str_title in zip(list_day_month_year, list_quantity, list_quantity):
        Pyplot.annotate(f'{str_title} kWh', (xi, yi), color = '#1C83EA', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')
    
    for xi, yi, str_title in zip(list_day_month_year, list_value, list_value):
        Pyplot.annotate(f'{str_title} kWh', (xi, yi), color = '#E31414', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')

    object_line1, = Pyplot.plot(list_day_month_year, list_quantity, marker = 'o', label = 'Total de execuções', color = '#1C83EA', markevery = 1)
    object_line2, = Pyplot.plot(list_day_month_year, list_value, marker = 'o', label = 'Valor total consumido', color = '#E31414', markevery = 1)
    Pyplot.title("Log de execuções por dia, mês e ano")
    Pyplot.xlabel("Dia, mês e ano")
    Pyplot.ylabel("Energia exibida em kWh")
    Pyplot.legend()
    Pyplot.grid(True, linestyle = ':')

    """object_cursor = mplcursors.cursor([object_line1], hover = True)
    object_cursor.connect('add', lambda sel: sel.annotation.set_text(
        f'Total: {sel.target[1]:.0f}'
    ))

    object_cursor = mplcursors.cursor([object_line2], hover = True)
    object_cursor.connect('add', lambda sel: sel.annotation.set_text(
        f'{sel.target[1]} kWh'
    ))"""

    Main.init_step()

    show_head_module()

    print('Visualizando gráfico...')

    Pyplot.show()

    Main.init_step()

    show_head_module()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável pela exibição de logs por mês e ano do módulo "Log de Execução de Sensores"
"""
def action_list_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com o sensor informado.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    dict_data_by_month_year = object_f4gs_sensor_log_execution.get_data_by_month_year(int_sle_sns_id = int_sle_sns_id)
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    if dict_data_by_month_year['list_data'] == None:
        raise Exception('Não existem logs cadastrados para esse sensor.')

    for dict_data in dict_data_by_month_year['list_data']:

        print(format_data_view_month_year(dict_data))

    require_reload()


"""
Método responsável pela exibição de gráficos logs por mês e ano do módulo "Log de Execução de Sensores"
"""
def action_graphic_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    print('Os dados serão exibidos de acordo com o sensor informado.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Carregando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    dict_data_by_month_year = object_f4gs_sensor_log_execution.get_data_by_month_year(str_order = 'ASC', int_sle_sns_id = int_sle_sns_id)
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    if dict_data_by_month_year['list_data'] == None:
        raise Exception('Não existem logs cadastrados para esse sensor.')

    list_month_year = []
    list_quantity = []
    list_value = []

    for dict_data in dict_data_by_month_year['list_data']:

        list_month_year.append(dict_data['SLE_INSERT_DATE_MONTH_YEAR'])
        list_quantity.append(dict_data['SLE_QUANTITY'])
        list_value.append(dict_data['SLE_TOTAL_VALUE'])

    for xi, yi, str_title in zip(list_month_year, list_quantity, list_quantity):
        Pyplot.annotate(f'{str_title} kWh', (xi, yi), color = '#1C83EA', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')
    
    for xi, yi, str_title in zip(list_month_year, list_value, list_value):
        Pyplot.annotate(f'{str_title} kWh', (xi, yi), color = '#E31414', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')

    object_line1, = Pyplot.plot(list_month_year, list_quantity, marker = 'o', label = 'Total de execuções', color = '#1C83EA', markevery = 1)
    object_line2, = Pyplot.plot(list_month_year, list_value, marker = 'o', label = 'Valor total consumido', color = '#E31414', markevery = 1)
    Pyplot.title("Log de execuções por mês e ano")
    Pyplot.xlabel("Mês e ano")
    Pyplot.ylabel("Energia exibida em kWh")
    Pyplot.legend()
    Pyplot.grid(True, linestyle = ':')

    """object_cursor = mplcursors.cursor([object_line1], hover = True)
    object_cursor.connect('add', lambda sel: sel.annotation.set_text(
        f'Total: {sel.target[1]:.0f}'
    ))

    object_cursor = mplcursors.cursor([object_line2], hover = True)
    object_cursor.connect('add', lambda sel: sel.annotation.set_text(
        f'{sel.target[1]} kWh'
    ))"""

    Main.init_step()

    show_head_module()

    print('Visualizando gráfico...')

    Pyplot.show()

    Main.init_step()

    show_head_module()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável por executar a ação de retorno de dados de um determinado log
"""
def get_data_by_id(int_sle_id: int = 0) -> dict:

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()

    object_f4gs_sensor_log_execution.set_select(['SLE.*', 'SNS.SNS_NAME'])
    object_f4gs_sensor_log_execution.set_table('F4_GS_SENSOR_LOG_EXECUTION SLE')
    object_f4gs_sensor_log_execution.set_join([
        {'str_type_join': 'INNER JOIN', 'str_table': 'F4_GS_SENSOR SNS', 'str_where': 'SNS.SNS_ID = SLE.SLE_SNS_ID'}
    ])
    object_f4gs_sensor_log_execution.set_where([

        {'str_column': 'SLE.SLE_ID', 'str_type_where': '=', 'value': int_sle_id},
        F4GsSensorLogExecution.get_params_to_active_data()

    ])

    dict_data = object_f4gs_sensor_log_execution.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_sle_id}.')

    return object_f4gs_sensor_log_execution


"""
Método responsável por executar a ação de retorno de dados de um determinado sensor
"""
def get_data_sensor_by_id(sns_id: int = 0) -> dict:

    object_f4gs_sensor = ModuleSensor.get_data_by_id(sns_id)
    dict_data = object_f4gs_sensor.get_one()

    return dict_data


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Log de Execução de Sensores"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do log.')
    print('')

    int_sle_sns_id = validate_sensor_id()

    print('')

    float_sle_value = validate_value()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['SLE_SNS_ID'] = int_sle_sns_id
    dict_data['SLE_VALUE'] = float_sle_value

    object_f4gs_sensor_log_execution = F4GsSensorLogExecution()
    object_f4gs_sensor_log_execution.insert(dict_data)

    int_sle_id = object_f4gs_sensor_log_execution.get_last_id()

    # Retorno de dados após o cadastro
    object_f4gs_sensor_log_execution = get_data_by_id(int_sle_id)
    dict_data = object_f4gs_sensor_log_execution.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Log de Execução de Sensores"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_sle_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = get_data_by_id(int_sle_id)
    dict_data = object_f4gs_sensor_log_execution.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal do log.')
    print('')

    int_sle_sns_id = validate_sensor_id(dict_data)

    print('')

    float_sle_value = validate_value(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_data['SLE_SNS_ID'] = int_sle_sns_id
    dict_data['SLE_VALUE'] = float_sle_value

    object_f4gs_sensor_log_execution.update(dict_data)

    # Retorno de dados após as atualizações
    object_f4gs_sensor_log_execution = get_data_by_id(int_sle_id)
    dict_data = object_f4gs_sensor_log_execution.get_one()

    print(format_data_view(dict_data = dict_data))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Log de Execução de Sensores"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_sle_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_sensor_log_execution = get_data_by_id(int_sle_id)
    dict_data = object_f4gs_sensor_log_execution.get_one()

    dict_data['SLE_STATUS'] = F4GsSensorLogExecution.STATUS_DELETED

    object_f4gs_sensor_log_execution.update(dict_data)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Log de Execução de Sensores"
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