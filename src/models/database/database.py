import copy
from custom.config import Config
from models.database.orm_abstract import OrmAbstract
from models.database.oracle import Oracle

class Database(OrmAbstract):

    # Constantes referentes à status de exclusão
    STATUS_DELETED = 0
    STATUS_ACTIVE = 1

    __object_database = None

    def __init__(self, object_database = None):

        if object_database is not None:
            self.object_database = object_database
        else:
            self.__execute_connection_by_database()


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Database] {str_message}')


    @property
    def object_database(self):
        return self.__object_database

    @object_database.setter
    def object_database(self, object_database = None):

        if type(object_database) == type(None):
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "object_database".')
        self.__object_database = object_database

    @object_database.getter
    def object_database(self):
        return self.__object_database


    def __get_database_by_config(self) -> str:

        object_config = Config()
        dict_config_db = object_config.get_db()
        if dict_config_db['status'] == False:
            self.exception(dict_config_db['message'])

        if 'database' not in dict_config_db['dict_data'] or dict_config_db['dict_data']['database'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a key "database" não foi definida nas configurações do banco de dados.')

        return dict_config_db['dict_data']['database'].strip()


    def __execute_connection_by_database(self):

        str_database = self.__get_database_by_config()

        if str_database not in globals() or isinstance(globals()[str_database], type) == False:
            self.exception('Não foi possível concluir o processo pois a key "database" foi definida com um banco de dados inválido.')

        object_class = globals()[str_database]
        self.object_database = object_class()
        self.object_database.connect()


    def test_connection_by_database(self):

        self.__execute_connection_by_database()


    def __reset_data(self):

        self.data = None


    def execute_query(self, str_query: str = None):

        list_data = self.object_database.execute_query(str_query)

        if type(list_data) == list and len(list_data) > 0:
            self.data = list_data

        return self


    def get_data(self):

        self.__reset_data()

        str_query = self.generate_sql_query().sql_query
        self.execute_query(str_query)

        return self


    def get_list(self):

        if type(self.data) == type(None):
            self.get_data()

        return self.data

    def get_one(self, bool_reset_data: bool = True):

        if bool_reset_data == True:
            self.__reset_data()

        list_data = self.get_list()

        if type(list_data) == list and len(list_data) > 0:
            self.data = list_data[0]
        
        return self.data


    def get_data_by_id(self, id: int = 0) -> dict:

        if type(id) == int:

            if type(self.primary_key_column) == type(None):
                self.exception('Não foi possível concluir o processo pois o parâmetro "primary_key_column" da tabela não foi definido para retorno dos dados por ID.')

            self.set_where([{'str_column': self.primary_key_column, 'str_type_where': '=', 'value': id}])
            return self.get_one()


    def update(self, dict_data: dict = {}):

        str_query = self.generate_sql_query_update(dict_data).sql_query
        self.execute_query(str_query)

        return self


    def insert(self, dict_data: dict = {}):

        str_query = self.generate_sql_query_insert(dict_data).sql_query
        self.execute_query(str_query)

        return self

    def get_last_id(self):

        str_query = self.generate_sql_query_get_last_id().sql_query
        self.execute_query(str_query)

        dict_data = self.get_one(False)

        return dict_data['LAST_ID'] if 'LAST_ID' in dict_data else 0


