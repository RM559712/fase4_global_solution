from models.database.database import Database
from custom.helper import Helper

class F4GsLocationAddress(Database):

    def __init__(self, object_database = None):

        super().__init__(object_database)

        self.table_name = Helper.convert_camel_to_snake_case(self.__class__.__name__)
        self.primary_key_column = 'LAD_ID'


    @staticmethod
    def get_params_to_active_data() -> dict:

        # Regras: Os registros são excluídos de forma lógica
        return {'str_column': 'LAD_STATUS', 'str_type_where': '=', 'value': Database.STATUS_ACTIVE}


    def validate_exists_data(self) -> bool:

        self.set_select([f'COUNT({self.primary_key_column}) as LENGTH'])
        self.set_where([self.get_params_to_active_data()])
        list_data = self.get_list()

        return False if len(list_data) == 0 or 'LENGTH' not in list_data[0] or list_data[0]['LENGTH'] == 0 else True


