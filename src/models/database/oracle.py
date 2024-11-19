import oracledb
from models.database.database_abstract import DatabaseAbstract

class Oracle(DatabaseAbstract):

    __user = None
    __password = None
    __dsn = None

    def __init__(self):

        pass

    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Oracle] {str_message}')


    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, str_user = str):

        if str_user.strip() == '':
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "user".')
        self.__user = str_user

    @user.getter
    def user(self):
        return self.__user


    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, str_password = str):

        if str_password.strip() == '':
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "password".')
        self.__password = str_password

    @password.getter
    def password(self):
        return self.__password


    @property
    def dsn(self):
        return self.__dsn

    @dsn.setter
    def dsn(self, str_dsn = str):

        if str_dsn.strip() == '':
            self.exception('Deve ser definido um conteúdo válido para o parâmetro "dsn".')
        self.__dsn = str_dsn

    @dsn.getter
    def dsn(self):
        return self.__dsn


    def connect(self):

        str_user = self.user
        if type(str_user) == type(None) or str_user.strip() == '':
            str_user = self.get_user_by_db_config()

        str_password = self.password
        if type(str_password) == type(None) or str_password.strip() == '':
            str_password = self.get_password_by_db_config()

        str_dsn = self.dsn
        if type(str_dsn) == type(None) or str_dsn.strip() == '':
            str_dsn = self.get_dsn_by_db_config()

        self.object_connection_database = oracledb.connect(user = str_user, password = str_password, dsn = str_dsn)


    def validate_connection(self):

        try:

            self.object_connection_database.ping()

        except oracledb.Error as e:

            self.connect()


    def execute_query(self, str_query: str = None, bool_commit: bool = True) -> list:

        try:

            self.validate_connection()

            object_cursor = self.object_connection_database.cursor()
            object_cursor.execute(str_query)

            if(bool_commit == True):
                self.object_connection_database.commit()

            list_data = []

            if type(object_cursor.description) == list:

                list_columns = [col[0] for col in object_cursor.description]
                object_data_query = object_cursor.fetchall()
                list_data = [dict(zip(list_columns, linha)) for linha in object_data_query]

            return list_data
        
        except Exception as error:

            if(bool_commit == True):
                self.object_connection_database.rollback()

            self.exception(f'{error}')
        
        finally:

            if object_cursor:
                object_cursor.close()

            if self.object_connection_database:
                self.object_connection_database.close()


