import copy
from custom.helper import Helper
from abc import ABC, abstractmethod

class OrmAbstract(ABC):

    __table_name = None
    __primary_key_column = None
    __select = None
    __table = None
    __join = None
    __where = None
    __order = None
    __offset = None
    __first_rows = None
    __next_rows = None
    __group = None
    __having = None
    __limit = None
    __data = None
    __sql_query = None

    def __init__(self):

        pass


    @abstractmethod
    def execute_query():

        pass


    @abstractmethod
    def get_data(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[OrmAbstract] {str_message}')


    @property
    def table_name(self):
        return self.__table_name

    @table_name.setter
    def table_name(self, table_name = None):

        if type(table_name) == type(None) or type(table_name) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "table_name".')
        self.__table_name = table_name

    @table_name.getter
    def table_name(self):
        return self.__table_name


    @property
    def primary_key_column(self):
        return self.__primary_key_column

    @primary_key_column.setter
    def primary_key_column(self, primary_key_column = None):

        if type(primary_key_column) == type(None) or type(primary_key_column) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "primary_key_column".')
        self.__primary_key_column = primary_key_column

    @primary_key_column.getter
    def primary_key_column(self):
        return self.__primary_key_column


    @property
    def select(self):
        return self.__select

    @select.setter
    def select(self, select = None):

        if type(select) == type(None) or type(select) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "select".')
        self.__select = select

    @select.getter
    def select(self):
        return self.__select


    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table = None):

        if type(table) == type(None) or type(table) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "table".')
        self.__table = table

    @table.getter
    def table(self):
        return self.__table


    @property
    def join(self):
        return self.__join

    @join.setter
    def join(self, join = None):

        if type(join) == type(None) or type(join) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "join".')
        self.__join = join

    @join.getter
    def join(self):
        return self.__join


    @property
    def where(self):
        return self.__where

    @where.setter
    def where(self, where = None):

        if type(where) == type(None) or type(where) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "where".')
        self.__where = where

    @where.getter
    def where(self):
        return self.__where


    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order = None):

        if type(order) == type(None) or type(order) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "order".')
        self.__order = order

    @order.getter
    def order(self):
        return self.__order


    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, offset = None):

        if type(offset) == type(None) or type(offset) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "offset".')
        self.__offset = offset

    @offset.getter
    def offset(self):
        return self.__offset


    @property
    def first_rows(self):
        return self.__first_rows

    @first_rows.setter
    def first_rows(self, first_rows = None):

        if type(first_rows) == type(None) or type(first_rows) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "first_rows".')
        self.__first_rows = first_rows

    @first_rows.getter
    def first_rows(self):
        return self.__first_rows


    @property
    def next_rows(self):
        return self.__next_rows

    @next_rows.setter
    def next_rows(self, next_rows = None):

        if type(next_rows) == type(None) or type(next_rows) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "next_rows".')
        self.__next_rows = next_rows

    @next_rows.getter
    def next_rows(self):
        return self.__next_rows


    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group = None):

        if type(group) == type(None) or type(group) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "group".')
        self.__group = group

    @group.getter
    def group(self):
        return self.__group


    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit = None):

        if type(limit) == type(None) or type(limit) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "limit".')
        self.__limit = limit

    @limit.getter
    def limit(self):
        return self.__limit


    @property
    def having(self):
        return self.__having

    @having.setter
    def having(self, having = None):

        if type(having) == type(None) or type(having) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "having".')
        self.__having = having

    @having.getter
    def having(self):
        return self.__having


    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data = None):

        # Regras: Essa validação não deve ser efetuada pois, eventualmente, os dados deverão ser "resetados" ( ex.: novas execuções de queries com a necessidade de retorno de novos dados )
        """if type(data) == type(None) or (type(data) != list and type(data) != dict):
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "data".')"""
        self.__data = data

    @data.getter
    def data(self):
        return copy.copy(self.__data)


    @property
    def sql_query(self):
        return self.__sql_query

    @sql_query.setter
    def sql_query(self, sql_query = None):

        if type(sql_query) == type(None) or type(sql_query) != str:
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "sql_query".')
        self.__sql_query = sql_query

    @sql_query.getter
    def sql_query(self):

        if type(self.__sql_query) == type(None):
            self.generate_sql_query()

        return self.__sql_query


    def set_select(self, list_columns: list = []):

        str_query = None

        if len(list_columns) == 0:
            str_query = f'*'

        else:
            str_query = f',' . join(list_columns)

        self.select = f'SELECT {str_query}'
        return self

        
    def set_table(self, str_table: str = None):

        str_query = None

        if type(str_table) == str and str_table.strip() != '':
            str_query = f'FROM {str_table.strip()}'

        else:
            str_query = f'FROM {self.table_name.strip()}'

        self.table = str_query
        return self


    def set_join(self, list_join: list = []):

        str_query = None

        if len(list_join) > 0:

            list_query = []

            for dict_join in list_join:

                if 'str_type_join' not in dict_join or type(dict_join['str_type_join']) != str or dict_join['str_type_join'].strip() == '':
                    self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_type_join" do join.')
                str_type_join = dict_join['str_type_join'].strip()

                if 'str_table' not in dict_join or type(dict_join['str_table']) != str or dict_join['str_table'].strip() == '':
                    self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_table" do join.')
                str_table = dict_join['str_table'].strip()

                if 'str_where' not in dict_join or type(dict_join['str_where']) != str or dict_join['str_where'].strip() == '':
                    self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_where" do join.')
                str_where = dict_join['str_where'].strip()

                list_query.append(f'{str_type_join} {str_table} ON {str_where}')

            str_query = ' ' . join(list_query)

        if type(str_query) == str and str_query.strip() != '':
            self.join = str_query

        return self


    def set_where(self, list_where: list = []):

        str_query = None

        if len(list_where) > 0:

            str_query = 'WHERE '
            list_query = []

            for dict_where in list_where:

                if 'str_condition_sql' in dict_where and type(dict_where['str_condition_sql']) == str and dict_where['str_condition_sql'].strip() != '':

                    list_query.append(dict_where['str_condition_sql'].strip())

                else:

                    if 'str_column' not in dict_where or type(dict_where['str_column']) != str or dict_where['str_column'].strip() == '':
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_column" das condições where.')
                    str_column = dict_where['str_column'].strip()

                    if 'str_type_where' not in dict_where or type(dict_where['str_type_where']) != str or dict_where['str_type_where'].strip() == '':
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_type_where" das condições where.')
                    str_type_where = dict_where['str_type_where'].strip()

                    if 'value' not in dict_where:
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "value" das condições where.')
                    value = dict_where['value']

                    if type(value) == int:
                        list_query.append(f'{str_column} {str_type_where} {value}')
                    else:

                        # Regras: Para essa ação, os valores devem ser formatados com aspas duplas
                        list_query.append(f"{str_column} {str_type_where} '{value}'")

            str_query += ' AND ' . join(list_query)

        if type(str_query) == str and str_query.strip() != '':
            self.where = str_query

        return self


    def set_order(self, list_order: list = []):

        str_query = None

        if len(list_order) > 0:

            str_query = 'ORDER BY '
            list_query = []

            for dict_order in list_order:

                if 'str_column' not in dict_order or type(dict_order['str_column']) != str or dict_order['str_column'].strip() == '':
                    self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_column" da ordenação.')
                str_column = dict_order['str_column'].strip()

                if 'str_type_order' not in dict_order or type(dict_order['str_type_order']) != str or dict_order['str_type_order'].strip() == '':
                    self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_type_order" da ordenação.')
                str_type_order = dict_order['str_type_order'].strip()

                list_query.append(f'{str_column} {str_type_order}')

            str_query += ', ' . join(list_query)

        if type(str_query) == str and str_query.strip() != '':
            self.order = str_query

        return self


    def set_offset(self, int_offset: int = 0):

        str_query = None

        if type(int_offset) == int and int_offset >= 0:
            str_query = f'OFFSET {int_offset} ROWS'

        if type(str_query) == str and str_query.strip() != '':
            self.offset = str_query

        return self


    def set_first_rows(self, int_first_rows: int = 0):

        str_query = None

        if type(int_first_rows) == int and int_first_rows > 0:
            str_query = f'FETCH FIRST {int_first_rows} ROWS ONLY'

        if type(str_query) == str and str_query.strip() != '':
            self.first_rows = str_query

        return self


    def set_next_rows(self, int_next_rows: int = 0):

        str_query = None

        if type(int_next_rows) == int and int_next_rows > 0:
            str_query = f'FETCH NEXT {int_next_rows} ROWS ONLY'

        if type(str_query) == str and str_query.strip() != '':
            self.next_rows = str_query

        return self


    def set_group(self, list_group: list = []):

        str_query = None

        if len(list_group) > 0:

            str_query = 'GROUP BY '
            list_query = []

            for str_group in list_group:

                if type(str_group) == str and str_group.strip() != '':
                    list_query.append(str_group.strip())

            str_query += ', ' . join(list_query)

        if type(str_query) == str and str_query.strip() != '':
            self.group = str_query

        return self


    def set_limit(self, int_limit = 0):

        str_query = None

        if type(int_limit) == int and int_limit > 0:
            str_query = f'LIMIT {int_limit}'

        if type(str_query) == str and str_query.strip() != '':
            self.limit = str_query

        return self


    def set_having(self, list_having: list = []):

        str_query = None

        if len(list_having) > 0:

            str_query = 'HAVING '
            list_query = []

            for dict_having in list_having:

                if 'str_condition_sql' in dict_having and type(dict_having['str_condition_sql']) == str and dict_having['str_condition_sql'].strip() != '':

                    list_query.append(dict_having['str_condition_sql'].strip())

                else:

                    if 'str_column' not in dict_having or type(dict_having['str_column']) != str or dict_having['str_column'].strip() == '':
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_type_join" das condições having.')
                    str_column = dict_having['str_column'].strip()

                    if 'str_type_where' not in dict_having or type(dict_having['str_type_where']) != str or dict_having['str_type_where'].strip() == '':
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "str_type_where" das condições having.')
                    str_type_where = dict_having['str_type_where'].strip()

                    if 'value' not in dict_having:
                        self.exception('Deve ser definido um conteúdo válido para o parâmetro "value" das condições having.')
                    value = dict_having['value']

                    if type(value) == int or Helper.is_float(value) == True:
                        list_query.append(f'{str_column} {str_type_where} {value}')
                    else:

                        # Regras: Para essa ação, os valores devem ser formatados com aspas duplas
                        list_query.append(f'{str_column} {str_type_where} "{value}"')

            str_query += ' AND ' . join(list_query)

        if type(str_query) == str and str_query.strip() != '':
            self.having = str_query

        return self


    def generate_sql_query(self):

        str_return = None

        if type(self.select) == type(None):
            self.set_select()

        if type(self.table) == type(None):
            self.set_table()

        str_return = f'{self.select} {self.table}'

        if type(self.join) != type(None):
            str_return += f' {self.join}'

        if type(self.where) != type(None):
            str_return += f' {self.where}'

        if type(self.offset) != type(None):
            str_return += f' {self.offset}'
        
        if type(self.first_rows) != type(None):
            str_return += f' {self.first_rows}'
        
        if type(self.next_rows) != type(None):
            str_return += f' {self.next_rows}'
        
        if type(self.group) != type(None):
            str_return += f' {self.group}'

        if type(self.order) != type(None):
            str_return += f' {self.order}'

        if type(self.limit) != type(None):
            str_return += f' {self.limit}'

        if type(self.having) != type(None):
            str_return += f' {self.having}'

        self.sql_query = str_return

        return self


    def generate_sql_query_update(self, dict_data: dict = {}):

        if type(self.primary_key_column) == type(None):
                self.exception('Não foi possível concluir o processo pois o parâmetro "primary_key_column" da tabela não foi definido para atualização dos dados.')

        if type(dict_data) != dict or len(dict_data) == 0:
            self.exception('Não foi possível concluir o processo pois os parâmetros para atualização não foram definidos.')

        dict_data_update = {}

        for str_column, value in dict_data.items():

            # Regras: A coluna PK não deverá ser atualizada por se tratar da chave principal da tabela
            if str_column.strip() == self.primary_key_column:
                continue

            # Regras: Apenas os itens presentes no objeto de dados original deverão ser atualizados
            if str_column in self.data and self.data[ str_column ] != value:

                dict_data_update[ str_column ] = value

        if len(dict_data_update) > 0:

            str_query = f'UPDATE {self.table_name.strip()} SET '
            list_query = []

            for str_column, value in dict_data_update.items():

                if type(value) == int or Helper.is_float(value) == True:
                    list_query.append(f'{str_column} = {value}')

                # Regras: Caso sejam definidos outros métodos para serem executados na query, basta adicioná-los abaixo
                elif value.find('TO_TIMESTAMP') != -1 or value.find('TO_DATE') != -1:
                    list_query.append(f'{str_column} = {value}')

                else:

                    # Regras: Para essa ação, os valores devem ser formatados com aspas simples
                    list_query.append(f"{str_column} = '{value}'")

            str_query += ', ' . join(list_query)
            str_query += f' WHERE {self.primary_key_column} = {self.data[ self.primary_key_column ]}'

            self.sql_query = str_query

        return self


    def generate_sql_query_insert(self, dict_data: dict = {}):

        if type(dict_data) != dict or len(dict_data) == 0:
            self.exception('Não foi possível concluir o processo pois os parâmetros para cadastro não foram definidos.')
        
        list_columns_insert = []
        list_values_insert = []

        for str_column, value in dict_data.items():

            # Regras: A coluna PK não deverá ser cadastrada por se tratar da chave principal da tabela que, por sua vez, é gerada automaticamente
            if str_column.strip() == self.primary_key_column:
                continue

            list_columns_insert.append(str_column)

            if type(value) == int or Helper.is_float(value) == True:
                list_values_insert.append(value)

            # Regras: Caso sejam definidos outros métodos para serem executados na query, basta adicioná-los abaixo
            elif value.find('TO_TIMESTAMP') != -1 or value.find('TO_DATE') != -1:
                list_values_insert.append(f'{str_column} = {value}')

            else:

                # Regras: Para essa ação, os valores devem ser formatados com aspas simples
                list_values_insert.append(f"'{value}'")

        if len(list_columns_insert) > 0 and len(list_values_insert) > 0 and len(list_columns_insert) == len(list_values_insert):

            str_query = f'INSERT INTO {self.table_name.strip()} ('
            str_query += ', ' . join(list_columns_insert)
            str_query += ') VALUES ('
            str_query += ', ' . join(map(str, list_values_insert))
            str_query += ')'

            self.sql_query = str_query

        return self


    def generate_sql_query_get_last_id(self):

        self.sql_query = f'SELECT {self.primary_key_column} as LAST_ID FROM {self.table_name.strip()} WHERE ROWNUM = 1 ORDER BY {self.primary_key_column} DESC'

        return self


