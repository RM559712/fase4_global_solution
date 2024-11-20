from models.database.database import Database
from custom.helper import Helper

class F4GsGeneratedEnergy(Database):

    def __init__(self, object_database = None):

        super().__init__(object_database)

        self.table_name = Helper.convert_camel_to_snake_case(self.__class__.__name__)
        self.primary_key_column = 'GNE_ID'


    @staticmethod
    def get_params_to_active_data() -> dict:

        # Regras: Os registros são excluídos de forma lógica
        return {'str_column': 'GNE_STATUS', 'str_type_where': '=', 'value': Database.STATUS_ACTIVE}


    def validate_exists_data(self) -> bool:

        self.set_select([f'COUNT({self.primary_key_column}) as LENGTH'])
        self.set_where([self.get_params_to_active_data()])
        list_data = self.get_list()

        return False if len(list_data) == 0 or 'LENGTH' not in list_data[0] or list_data[0]['LENGTH'] == 0 else True


    def get_data_by_month_year(self, str_order: str = 'DESC', str_gne_insert_date_month_year: str = None) -> dict:

        dict_return = {'status': True, 'list_data': []}

        try:

            self.set_select(['SUM(GNE_VALUE) AS GNE_TOTAL_VALUE', "TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY') AS GNE_INSERT_DATE_MONTH_YEAR"])
            self.set_table('F4_GS_GENERATED_ENERGY')

            list_where = []
            list_where.append(self.get_params_to_active_data())

            if type(str_gne_insert_date_month_year) != None and type(str_gne_insert_date_month_year) == str:
                list_where.append({'str_column': "TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY')", 'str_type_where': '=', 'value': str_gne_insert_date_month_year})

            self.set_where(list_where)

            self.set_group([
                "TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY')"
            ])
            self.set_order([
                {'str_column': "TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY')", 'str_type_order': str_order}
            ])
            list_data = self.get_data().get_list()

            dict_return['list_data'] = list_data

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


    def get_balance_by_month_year(self, str_order: str = 'DESC', str_insert_date_month_year: str = None) -> dict:

        dict_return = {'status': True, 'list_data': []}

        try:

            str_sql_query_filter_month_year_gne = ''
            str_sql_query_filter_month_year_cne = ''

            if type(str_insert_date_month_year) != None and type(str_insert_date_month_year) == str:
                str_sql_query_filter_month_year_gne = f"AND TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY') = '{str_insert_date_month_year}'"
                str_sql_query_filter_month_year_cne = f"AND TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY') = '{str_insert_date_month_year}'"

            # > Importante: Por se tratar de um processo específico, a query abaixo será definida em formato SQL
            str_sql_query = f"""
            
                WITH 
                    GENERATED_ENERGY AS (
                        SELECT
                            SUM(GNE_VALUE) AS GNE_TOTAL_VALUE,
                            TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY') AS GNE_INSERT_DATE_MONTH_YEAR
                        FROM F4_GS_GENERATED_ENERGY
                        WHERE
                            GNE_STATUS = {self.STATUS_ACTIVE}
                            {str_sql_query_filter_month_year_gne}
                        GROUP BY 
                            TO_CHAR(GNE_INSERT_DATE, 'MM/YYYY')
                    ),
                    CONSUMED_ENERGY AS (
                        SELECT
                            SUM(CNE_VALUE) AS CNE_TOTAL_VALUE,
                            TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY') AS CNE_INSERT_DATE_MONTH_YEAR
                        FROM F4_GS_CONSUMED_ENERGY
                        WHERE
                            CNE_STATUS = {self.STATUS_ACTIVE}
                            {str_sql_query_filter_month_year_cne}
                        GROUP BY 
                            TO_CHAR(CNE_INSERT_DATE, 'MM/YYYY')
                    )
                SELECT
                    COALESCE(GNE.GNE_INSERT_DATE_MONTH_YEAR, CNE.CNE_INSERT_DATE_MONTH_YEAR) AS INSERT_DATE_MONTH_YEAR,
                    COALESCE(GNE.GNE_TOTAL_VALUE, 0) AS TOTAL_VALUE_GENERATED,
                    COALESCE(CNE.CNE_TOTAL_VALUE, 0) AS TOTAL_VALUE_CONSUMED,
                    COALESCE(GNE.GNE_TOTAL_VALUE, 0) - COALESCE(CNE.CNE_TOTAL_VALUE, 0) AS TOTAL_BALANCE
                FROM
                    GENERATED_ENERGY GNE
                FULL OUTER JOIN CONSUMED_ENERGY CNE ON GNE.GNE_INSERT_DATE_MONTH_YEAR = CNE.CNE_INSERT_DATE_MONTH_YEAR
                ORDER BY
                    INSERT_DATE_MONTH_YEAR {str_order}
            
            """;

            list_data = self.execute_query(str_sql_query).get_list()

            dict_return['list_data'] = list_data

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


    def get_total_balance(self) -> dict:

        dict_return = {'status': True, 'list_data': []}

        try:

            # > Importante: Por se tratar de um processo específico, a query abaixo será definida em formato SQL
            str_sql_query = f"""

                SELECT
                    NVL(SUM(GNE.GNE_VALUE), 0) - NVL(SUM(CNE.CNE_VALUE), 0) AS TOTAL_BALANCE
                FROM F4_GS_GENERATED_ENERGY GNE
                FULL OUTER JOIN F4_GS_CONSUMED_ENERGY CNE ON GNE.GNE_ID = CNE.CNE_ID AND CNE.CNE_STATUS = {self.STATUS_ACTIVE}
                WHERE
                    GNE.GNE_STATUS = {self.STATUS_ACTIVE}

            """;

            list_data = self.execute_query(str_sql_query).get_list()

            dict_return['list_data'] = list_data

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


