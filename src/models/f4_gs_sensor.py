from models.database.database import Database
from custom.helper import Helper

class F4GsSensor(Database):

    # Constantes referentes aos tipos de sensores
    TYPE_PRESENCE = 1
    TYPE_LIGHT = 2

    def __init__(self, object_database = None):

        super().__init__(object_database)

        self.table_name = Helper.convert_camel_to_snake_case(self.__class__.__name__)
        self.primary_key_column = 'SNS_ID'


    @staticmethod
    def get_params_to_active_data() -> dict:

        # Regras: Os registros são excluídos de forma lógica
        return {'str_column': 'SNS_STATUS', 'str_type_where': '=', 'value': Database.STATUS_ACTIVE}


    def validate_exists_data(self) -> bool:

        self.set_select([f'COUNT({self.primary_key_column}) as LENGTH'])
        self.set_where([self.get_params_to_active_data()])
        list_data = self.get_list()

        return False if len(list_data) == 0 or 'LENGTH' not in list_data[0] or list_data[0]['LENGTH'] == 0 else True


    @staticmethod
    def get_type_options(int_code: int = 0) -> list:

        dict_types = [
            {
                'code': F4GsSensor.TYPE_PRESENCE,
                'title': 'Sensor de Presença'
            },{
                'code': F4GsSensor.TYPE_LIGHT,
                'title': 'Sensor de Luminosidade'
            }
        ]

        if int_code > 0:

            for dict_type in dict_types:

                if dict_type['code'] == int_code:
                    return dict_type

        return dict_types


    @staticmethod
    def get_type_options_codes() -> list:

        list_return = []

        list_type_options = F4GsSensor.get_type_options()

        for dict_type_option in list_type_options:
            list_return.append(dict_type_option['code'])

        return list_return


