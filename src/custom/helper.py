from datetime import datetime
import re

class Helper:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Helper] {str_message}')


    @staticmethod
    def is_int(int_value) -> bool:

        try:

            int_value = int(int_value)

            return True

        except Exception as error:

            return False


    @staticmethod
    def is_float(float_value) -> bool:

        try:

            float_value = float(float_value)

            return True

        except Exception as error:

            return False


    @staticmethod
    def format_float(str_value) -> str:

        str_value = f'{str_value:_.2f}'
        str_value = str_value.replace('.',',').replace('_','.')
        return str_value


    @staticmethod
    def convert_camel_to_snake_case(camel_str: str = None) -> str:

        str_return = re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).upper()
        return str_return


    @staticmethod
    def get_datetime_object_by_date_oracle(str_datetime: str = None) -> datetime:

        return datetime.strptime(str_datetime, '%Y-%m-%d %H:%M:%S')


    @staticmethod
    def convert_date_to_pt_br(object_datetime: datetime = None) -> str:

        str_return = object_datetime.strftime("%d/%m/%Y às %H:%M:%S")
        return str_return


    @staticmethod
    def get_current_datetime_to_pt_br(bool_microsecond: bool = False) -> str:

        object_datetime = datetime.now()
        return f'{object_datetime.strftime("%d/%m/%Y %H:%M:%S")},{object_datetime.microsecond}' if bool_microsecond == True else f'{object_datetime.strftime("%d/%m/%Y %H:%M:%S")}'


    @staticmethod
    def get_current_datetime_to_en_us(bool_microsecond: bool = False) -> str:

        object_datetime = datetime.now()
        return f'{object_datetime.strftime("%Y-%m-%d %H:%M:%S")},{object_datetime.microsecond}' if bool_microsecond == True else f'{object_datetime.strftime("%Y-%m-%d %H:%M:%S")}'


    @staticmethod
    def get_current_datetime_to_oracle(bool_microsecond: bool = False) -> str:

        object_datetime = datetime.now()
        return f'{object_datetime.strftime("%d/%m/%Y %H:%M:%S")},{object_datetime.microsecond}' if bool_microsecond == True else f'{object_datetime.strftime("%d/%m/%Y %H:%M:%S")}'


