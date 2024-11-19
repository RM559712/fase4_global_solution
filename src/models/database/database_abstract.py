from abc import ABC, abstractmethod
from custom.config import Config

class DatabaseAbstract(ABC):

    __object_connection_database = None

    def __init__(self):

        pass


    @abstractmethod
    def execute_query(self):

        pass


    @abstractmethod
    def connect(self):

        pass


    @property
    def object_connection_database(self):
        return self.__object_connection_database

    @object_connection_database.setter
    def object_connection_database(self, object_connection_database = None):

        if type(object_connection_database) == type(None):
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "object_connection_database".')
        self.__object_connection_database = object_connection_database

    @object_connection_database.getter
    def object_connection_database(self):
        return self.__object_connection_database


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[DatabaseAbstract] {str_message}')


    def __get_db_config(self) -> dict:

        object_config = Config()
        dict_config_db = object_config.get_db()
        if dict_config_db['status'] == False:
            self.exception(dict_config_db['message'])

        return dict_config_db['dict_data']


    def get_user_by_db_config(self) -> str:

        dict_db_config = self.__get_db_config()
        if 'user' not in dict_db_config or dict_db_config['user'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a key "user" não foi definida nas configurações do banco de dados.')

        return dict_db_config['user'].strip()


    def get_password_by_db_config(self) -> str:

        dict_db_config = self.__get_db_config()
        if 'password' not in dict_db_config or dict_db_config['password'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a key "password" não foi definida nas configurações do banco de dados.')

        return dict_db_config['password'].strip()


    def get_dsn_by_db_config(self) -> str:

        dict_db_config = self.__get_db_config()
        if 'dsn' not in dict_db_config or dict_db_config['dsn'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a key "dsn" não foi definida nas configurações do banco de dados.')

        return dict_db_config['dsn'].strip()


