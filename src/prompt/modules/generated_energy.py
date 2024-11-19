import datetime
import os
import sys

# > Importante: A definição abaixo referente ao diretório raiz deve ser efetuada antes das importações de arquivos do sistema.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as Pyplot
import prompt.main as Main
from custom.helper import Helper
from models.f4_gs_generated_energy import F4GsGeneratedEnergy

"""
Método responsável pela exibição do cabeçalho do módulo
"""
def show_head_module():

    print('-= Energia Limpa =-')
    print('')


"""
Método responsável por verificar se existem energias cadastradas
"""
def validate_exists_data():

    object_f4gs_generated_energy = F4GsGeneratedEnergy()
    bool_exists_data = object_f4gs_generated_energy.validate_exists_data()

    if bool_exists_data == False:
        raise Exception('Não existem energias cadastradas.')


"""
Método responsável por recarregar o módulo "Energia Limpa"
"""
def require_reload():

    input(f'\nPressione <enter> para voltar ao menu do módulo "Energia Limpa"...')
    action_main()


"""
Método responsável por retornar as opções de menu do módulo "Energia Limpa"

Return: list
"""
def get_menu_options() -> list:

    return [
        {
            'code': 1,
            'title': 'Visualizar energias geradas',
            'action': action_list
        },{
            'code': 2,
            'title': 'Visualizar energias geradas por mês e ano',
            'action': action_list_month_year
        },{
            'code': 3,
            'title': 'Visualizar gráfico com energias geradas por mês e ano',
            'action': action_graphic_month_year
        },{
            'code': 4,
            'title': 'Visualizar saldo por mês e ano',
            'action': action_balance_month_year
        },{
            'code': 5,
            'title': 'Cadastrar energia gerada',
            'action': action_insert
        },{
            'code': 6,
            'title': 'Editar energia gerada',
            'action': action_update
        },{
            'code': 7,
            'title': 'Excluir energia gerada',
            'action': action_delete
        },{
            'code': 8,
            'title': 'Voltar ao menu principal',
            'action': Main.init_system
        }
    ]


"""
Método responsável por retornar os códigos das opções de menu do módulo "Energia Limpa"

Return: list
"""
def get_menu_options_codes() -> list:

    list_return = []

    list_menu_options = get_menu_options()

    for dict_menu_option in list_menu_options:
        list_return.append(dict_menu_option['code'])

    return list_return


"""
Método responsável pela validação do parâmetro "Opção do menu" do módulo "Energia Limpa"

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
Método responsável pela formatação de visualização do ID do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_id(dict_data: dict = {}) -> str:

    str_return = 'ID: '
    str_return += f'{dict_data['GNE_ID']}' if 'GNE_ID' in dict_data and type(dict_data['GNE_ID']) != None and Helper.is_int(dict_data['GNE_ID']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "ID"

Return: int
"""
def validate_id() -> int:

    int_return = input(f'Informe o ID da energia: ')

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
Método responsável pela formatação de visualização do valor do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_value(dict_data: dict = {}) -> str:

    str_return = 'Valor da energia gerada: '
    str_return += f'{dict_data['GNE_VALUE']} kWh' if 'GNE_VALUE' in dict_data and type(dict_data['GNE_VALUE']) != None and Helper.is_float(dict_data['GNE_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela validação do parâmetro "Valor da energia gerada"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def validate_value(dict_data: dict = {}) -> float:

    bool_is_update = ('GNE_ID' in dict_data and type(dict_data['GNE_ID']) == int)

    str_label = f'O valor de energia gerada será exibido no formato [valor] kWh ( ex.: 12 kWh, 21 kWh, etc. )\n\n'
    str_label += f'Importante: Caso deseje manter o valor da energia gerada atual ( abaixo ), basta ignorar o preenchimento.\n{format_data_view_value(dict_data)}\n' if bool_is_update == True else ''
    str_label += f'Informe o valor da energia gerada em formato numérico ( ex.: 123, 123.45 ou 123,45 ): '
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
Método responsável pela formatação de visualização da data de cadastro do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date(dict_data: dict = {}) -> str:

    str_return = 'Data de cadastro: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['GNE_INSERT_DATE'])}' if 'GNE_INSERT_DATE' in dict_data and type(dict_data['GNE_INSERT_DATE']) != None and type(dict_data['GNE_INSERT_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização da data de atualização do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_update_date(dict_data: dict = {}) -> str:

    str_return = 'Data de atualização: '
    str_return += f'{Helper.convert_date_to_pt_br(dict_data['GNE_UPDATE_DATE'])}' if 'GNE_UPDATE_DATE' in dict_data and type(dict_data['GNE_UPDATE_DATE']) != None and type(dict_data['GNE_UPDATE_DATE']) == datetime.datetime else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do valor total do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_total_value(dict_data: dict = {}) -> str:

    str_return = 'Valor total de energia gerada: '
    str_return += f'{dict_data['GNE_TOTAL_VALUE']} kWh' if 'GNE_TOTAL_VALUE' in dict_data and type(dict_data['GNE_TOTAL_VALUE']) != None and Helper.is_float(dict_data['GNE_TOTAL_VALUE']) == True else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização do mês e ano do módulo "Energia Limpa"

Arguments:
- dict_data: Dict contendo os dados conforme retorno do banco de dados ( dictionary )

Return: str
"""
def format_data_view_insert_date_month_year(dict_data: dict = {}) -> str:

    str_return = 'Mês e ano: '
    str_return += f'{dict_data['GNE_INSERT_DATE_MONTH_YEAR']}' if 'GNE_INSERT_DATE_MONTH_YEAR' in dict_data and type(dict_data['GNE_INSERT_DATE_MONTH_YEAR']) != None else 'N/I'

    return str_return


"""
Método responsável pela formatação de visualização de dados do módulo "Energia Limpa"

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
        str_return += f'- {format_data_view_value(dict_data)} \n'
        str_return += f'- {format_data_view_insert_date(dict_data)} \n' if bool_show_insert_date == True else ''
        str_return += f'- {format_data_view_update_date(dict_data)} \n' if bool_show_update_date == True else ''

    return str_return


"""
Método responsável pela formatação de visualização de dados agrupados por mês e ano do módulo "Energia Limpa"

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
Método responsável pela exibição de cadastros do módulo "Energia Limpa"
"""
def action_list():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4gs_generated_energy = F4GsGeneratedEnergy()

    object_f4gs_generated_energy.set_where([F4GsGeneratedEnergy.get_params_to_active_data()])
    object_f4gs_generated_energy.set_order([{'str_column': 'GNE_ID', 'str_type_order': 'ASC'}])
    list_data = object_f4gs_generated_energy.get_data().get_list()

    for dict_data in list_data:

        print(format_data_view(dict_data))
    
    require_reload()


"""
Método responsável pela exibição de cadastros do módulo "Energia Limpa"
"""
def action_list_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4gs_generated_energy = F4GsGeneratedEnergy()

    dict_data_by_month_year = object_f4gs_generated_energy.get_data_by_month_year()
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    for dict_data in dict_data_by_month_year['list_data']:

        print(format_data_view_month_year(dict_data))

    require_reload()


"""
Método responsável pela exibição de gráficos do módulo "Energia Limpa"
"""
def action_graphic_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    object_f4gs_generated_energy = F4GsGeneratedEnergy()

    dict_data_by_month_year = object_f4gs_generated_energy.get_data_by_month_year(str_order = 'ASC')
    if dict_data_by_month_year['status'] == False:
        raise Exception(dict_data_by_month_year['message'])

    list_month_year = []
    list_value = []

    """if len(dict_data_by_month_year['list_data']) == 0:
        raise Exception('Não existem energias cadastradas para geração do gráfico.')"""

    for dict_data in dict_data_by_month_year['list_data']:

        list_month_year.append(dict_data['GNE_INSERT_DATE_MONTH_YEAR'])
        list_value.append(dict_data['GNE_TOTAL_VALUE'])

    for xi, yi, str_title in zip(list_month_year, list_value, list_value):
        Pyplot.annotate(str_title, (xi, yi), color = '#1C83EA', fontsize = 8, textcoords = 'offset points', xytext = (0, 10), ha = 'center')

    Pyplot.plot(list_month_year, list_value, marker = 'o', color = '#1C83EA')
    Pyplot.title("Energia gerada por mês e ano")
    Pyplot.xlabel("Mês e ano")
    Pyplot.ylabel("Energia gerada em kWh")
    Pyplot.grid(True, linestyle = ':')
    Pyplot.show()

    print('Gráfico gerado e visualizado com sucesso.')

    require_reload()


"""
Método responsável pela exibição de saldo por mês e ano do módulo "Energia Limpa"
"""
def action_balance_month_year():

    Main.init_step()

    validate_exists_data()

    show_head_module()

    # <PENDENTE>
    print('Em desenvolvimento...')

    require_reload()


"""
Método responsável por executar a ação de retorno de dados de uma determinada energia
"""
def get_data_by_id(int_gne_id: int = 0) -> dict:

    object_f4gs_generated_energy = F4GsGeneratedEnergy()

    object_f4gs_generated_energy.set_where([

        {'str_column': 'GNE_ID', 'str_type_where': '=', 'value': int_gne_id},
        F4GsGeneratedEnergy.get_params_to_active_data()

    ])

    dict_data = object_f4gs_generated_energy.get_data().get_one()

    if type(dict_data) == type(None):
        raise Exception(f'Nenhum registro foi localizado com o ID {int_gne_id}.')

    return object_f4gs_generated_energy


# ... Demais parâmetros...


"""
Método responsável pela exibição da funcionalidade de cadastro do módulo "Energia Limpa"
"""
def action_insert():

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da energia gerada.')
    print('')

    float_gne_value = validate_value()

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 2
    # -------

    Main.init_step()

    show_head_module()

    dict_data = {}

    dict_data['GNE_VALUE'] = float_gne_value

    object_f4gs_generated_energy = F4GsGeneratedEnergy()
    object_f4gs_generated_energy.insert(dict_data)

    int_gne_id = object_f4gs_generated_energy.get_last_id()

    # Retorno de dados após o cadastro
    object_f4gs_generated_energy = get_data_by_id(int_gne_id)
    dict_data = object_f4gs_generated_energy.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_id = False, bool_show_insert_date = False, bool_show_update_date = False))

    print('Registro cadastrado com sucesso.')

    require_reload()


"""
Método responsável pela exibição da funcionalidade de atualização do módulo "Energia Limpa"
"""
def action_update():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_gne_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_generated_energy = get_data_by_id(int_gne_id)
    dict_data = object_f4gs_generated_energy.get_one()

    print('Os dados abaixo representam o cadastro atual do registro informado.')
    print('')

    print(format_data_view(dict_data))

    input(f'Pressione <enter> para continuar...')

    # -------
    # Etapa 3
    # -------

    Main.init_step()

    show_head_module()

    print('Os parâmetros abaixo fazem parte do cadastro principal da energia.')
    print('')

    float_gne_value = validate_value(dict_data)

    Main.loading('Salvando dados, por favor aguarde...')

    # -------
    # Etapa 4
    # -------

    Main.init_step()

    show_head_module()

    dict_data['GNE_VALUE'] = float_gne_value

    object_f4gs_generated_energy.update(dict_data)

    # Retorno de dados após as atualizações
    object_f4gs_generated_energy = get_data_by_id(int_gne_id)
    dict_data = object_f4gs_generated_energy.get_one()

    print(format_data_view(dict_data = dict_data, bool_show_update_date = False))

    print('Registro atualizado com sucesso.')
    
    require_reload()


"""
Método responsável pela exibição da funcionalidade de exclusão do módulo "Energia Limpa"
"""
def action_delete():

    Main.init_step()

    show_head_module()

    validate_exists_data()

    int_gne_id = validate_id()

    # -------
    # Etapa 2
    # -------

    Main.loading('Verificando dados, por favor aguarde...')

    Main.init_step()

    show_head_module()

    object_f4gs_generated_energy = get_data_by_id(int_gne_id)
    dict_data = object_f4gs_generated_energy.get_one()

    dict_data['GNE_STATUS'] = F4GsGeneratedEnergy.STATUS_DELETED

    object_f4gs_generated_energy.update(dict_data)

    print('Registro excluído com sucesso.')

    require_reload()


"""
Método responsável pela exibição padrão do módulo "Energia Limpa"
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