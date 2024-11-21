import json
import requests
from custom.config import Config
from custom.helper import Helper

class Correios:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Correios] {str_message}')


    def __get_params_by_correios(self) -> dict:

        object_config = Config()
        return object_config.get_params_by_correios()


    def __get_url(self) -> str:

        dict_params_correios = self.__get_params_by_correios()

        if 'url' not in dict_params_correios or dict_params_correios['url'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a url do serviço não foi definida.')

        return dict_params_correios['url'].strip()


    def __execute_request(self, str_url = None) -> dict:

        if type(str_url) == type(None) or type(str_url) != str:
            self.exception('Não foi possível concluir o processo pois a url para execução do serviço não foi definida.')

        object_request = requests.get(str_url)
        dict_return = object_request.json()

        if object_request.status_code not in [200]:

            str_exception = f'Não foi possível concluir o processo devido ao código de erro retornado: {object_request.status_code}.'

            str_error_request = dict_return.get('message')

            if type(str_error_request) != type(None):
                str_exception += f' Erro retornado: {str_error_request}'

            self.exception(str_exception)

        return dict_return


    """
    Método responsável por retornar o endereço a patir de um determinado CEP

    Arguments:
    - int_cep: CEP para retorno dos dados de endereço ( int )
   
    """
    def get_address_data_by_cep(self, int_cep: int = None) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            if type(int_cep) == None or Helper.is_int(int_cep) == False:
                self.exception('Para retornar o endereço, deve ser definido um CEP válido.')

            str_cep = str(int_cep).rjust(8, '0')

            str_url = self.__get_url()
            str_url = str_url.replace('{int_cep}', str_cep)

            dict_return['dict_data'] = self.__execute_request(str_url)

            if 'erro' in dict_return['dict_data'] and dict_return['dict_data']['erro'] == 'true':
                raise Exception(f'Nenhum endereço foi localizado com o CEP {str_cep}.')

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


    @staticmethod
    def format_data_view(dict_params: dict = {}) -> str:

        str_return = None

        str_return = f'Endereço: {dict_params['logradouro'].strip()}, {dict_params['bairro'].strip()}, {dict_params['localidade'].strip()}, {dict_params['estado'].strip()}, CEP {str(dict_params['cep']).rjust(8, '0')}'

        return str_return


