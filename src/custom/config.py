import json
import os

class Config:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Config] {str_message}')


    def get_current_path_dir(self) -> str:

        return os.path.dirname(os.path.dirname(__file__))


    def get_system_path_dir(self) -> str:

        return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


    def get_db(self) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            str_current_dir_path = self.get_system_path_dir()

            with open(f'{str_current_dir_path}{os.sep}config{os.sep}db.json', 'r', encoding = 'utf-8-sig') as file_json:
                dict_return['dict_data'] = json.load(file_json)

        except Exception as error:

            dict_return = {'status': False, 'message': error}
        
        return dict_return


    def get_params(self) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            str_current_dir_path = self.get_system_path_dir()

            with open(f'{str_current_dir_path}{os.sep}config{os.sep}params.json', 'r', encoding = 'utf-8-sig') as file_json:
                dict_return['dict_data'] = json.load(file_json)

        except Exception as error:

            dict_return = {'status': False, 'message': error}
        
        return dict_return


    def get_params_by_open_weather(self) -> dict:

        dict_params = self.get_params()
        if dict_params['status'] == False:
            self.exception(dict_params['message'])

        dict_return = dict_params['dict_data']['open_weather'] if 'open_weather' in dict_params['dict_data'] else {}
        return dict_return


    