from models.database.database import Database
from custom.helper import Helper

class F4GsConsumedEnergy(Database):

    def __init__(self, object_database = None):

        super().__init__(object_database)

        self.table_name = Helper.convert_camel_to_snake_case(self.__class__.__name__)
        self.primary_key_column = 'CNE_ID'


    @staticmethod
    def get_params_to_active_data() -> dict:

        # Regras: Os registros são excluídos de forma lógica
        return {'str_column': 'CNE_STATUS', 'str_type_where': '=', 'value': Database.STATUS_ACTIVE}


    def validate_exists_data(self) -> bool:

        self.set_select([f'COUNT({self.primary_key_column}) as LENGTH'])
        self.set_where([self.get_params_to_active_data()])
        list_data = self.get_list()

        return False if len(list_data) == 0 or 'LENGTH' not in list_data[0] or list_data[0]['LENGTH'] == 0 else True


    def get_data_by_month_year(self, str_order: str = 'DESC', str_cne_insert_date_month_year: str = None) -> dict:

        dict_return = {'status': True, 'list_data': []}

        try:

            self.set_select(['SUM(CNE_VALUE) AS CNE_TOTAL_VALUE', "TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY') AS CNE_INSERT_DATE_MONTH_YEAR"])
            self.set_table('F4_GS_CONSUMED_ENERGY')

            list_where = []
            list_where.append(self.get_params_to_active_data())

            if type(str_cne_insert_date_month_year) != None and type(str_cne_insert_date_month_year) == str:
                list_where.append({'str_column': "TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY')", 'str_type_where': '=', 'value': str_cne_insert_date_month_year})

            self.set_where(list_where)

            self.set_group([
                "TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY')"
            ])
            self.set_order([
                {'str_column': "TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY')", 'str_type_order': str_order}
            ])
            list_data = self.get_data().get_list()

            dict_return['list_data'] = list_data

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


