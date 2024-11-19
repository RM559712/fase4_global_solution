import json
import requests
from custom.config import Config
from custom.helper import Helper

class OpenWeather:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[OpenWeather] {str_message}')


    def __get_params_by_open_weather(self) -> dict:

        object_config = Config()
        return object_config.get_params_by_open_weather()


    def __get_url(self) -> str:

        dict_params_open_weather = self.__get_params_by_open_weather()

        if 'url' not in dict_params_open_weather or dict_params_open_weather['url'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a url do serviço não foi definida.')

        return dict_params_open_weather['url'].strip()


    def __get_app_id(self) -> str:

        dict_params_open_weather = self.__get_params_by_open_weather()

        if 'app_id' not in dict_params_open_weather or dict_params_open_weather['app_id'].strip() == '':
            self.exception('Não foi possível concluir o processo pois a key de autenticação não foi definida.')

        return dict_params_open_weather['app_id'].strip()


    def __get_url_part_standard(self) -> str:

        str_return = None

        str_app_id = self.__get_app_id()
        str_return = f'&appid={str_app_id}&lang=pt_br&units=metric'

        return str_return


    def __execute_request(self, str_url = None) -> dict:

        if type(str_url) == type(None) or type(str_url) != str:
            self.exception('Não foi possível concluir o processo pois a url para execução do serviço não foi definida.')

        str_url = f'{self.__get_url()}{str_url}'

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
    Método responsável por retornar os parâmetros atuais de meteorologia a patir de uma determinada localização

    > Documentação: https://openweathermap.org/current

    Arguments:
    - str_city_state_country: Nome da cidade, sigla do estado/província e nome do país no formato [nome_cidade],[sigla_estado_província],[sigla_país] ( str )
    - int_latitude: Latitude da região ( int )
    - int_longitude: Longitude da região ( int )
   
    """
    def get_weather_data_by_location(self, str_city_state_country: str = None, float_latitude: float = 0.00, float_longitude: float = 0.00) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            str_url_city = ''
            if type(str_city_state_country) != type(None) and type(str_city_state_country) == str:
                str_url_city = f'&q={str_city_state_country}'
            
            str_url_latitude = ''
            if type(float_latitude) != type(None) and type(float_latitude) == float:
                str_url_latitude = f'&lat={float_latitude}'

            str_url_longitude = ''
            if type(float_longitude) != type(None) and type(float_longitude) == float:
                str_url_longitude = f'&lon={float_longitude}'

            str_url = f'/weather?{self.__get_url_part_standard()}{str_url_city}{str_url_latitude}{str_url_longitude}'
            dict_return['dict_data'] = self.__execute_request(str_url)

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


    """
    Método responsável por retornar os parâmetros atuais de meteorologia a patir de uma determinada localização

    > Documentação: https://openweathermap.org/forecast5

    Arguments:
    - str_city_state_country: Nome da cidade, sigla do estado/província e nome do país no formato [nome_cidade],[sigla_estado_província],[sigla_país] ( str )
    - int_latitude: Latitude da região ( int )
    - int_longitude: Longitude da região ( int )
   
    """
    def get_weather_forecast_data_by_location(self, str_city_state_country: str = None, float_latitude: float = 0.00, float_longitude: float = 0.00) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            str_url_city = ''
            if type(str_city_state_country) != type(None) and type(str_city_state_country) == str:
                str_url_city = f'&q={str_city_state_country}'

            str_url_latitude = ''
            if type(float_latitude) != type(None) and type(float_latitude) == float:
                str_url_latitude = f'&lat={float_latitude}'

            str_url_longitude = ''
            if type(float_longitude) != type(None) and type(float_longitude) == float:
                str_url_longitude = f'&lon={float_longitude}'

            str_url = f'/forecast?{self.__get_url_part_standard()}{str_url_city}{str_url_latitude}{str_url_longitude}'
            dict_return['dict_data'] = self.__execute_request(str_url)

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


    def execute_forecast_calc(self, dict_weather_forecast_data: dict = {}, dict_params_calc: dict = {}) -> dict:

        dict_return = {'status': True, 'dict_data': {}}

        try:

            if type(dict_weather_forecast_data) != dict or len(dict_weather_forecast_data) == 0:
                self.exception('Não foi possível concluir o processo de cálculo pois os parâmetros pois os parâmetros de meteorologia não foram definidos.')

            if type(dict_params_calc) != dict or len(dict_params_calc) == 0:
                self.exception('Não foi possível concluir o processo de cálculo pois os parâmetros para execução do cálculo não foram definidos.')

            dict_return['dict_data']['str_city'] = dict_weather_forecast_data.get('city', {}).get('name', 'N/I')
            dict_return['dict_data']['str_country'] = dict_weather_forecast_data.get('city', {}).get('country', 'N/I')
            dict_return['dict_data']['float_latitude'] = dict_weather_forecast_data.get('city', {}).get('coord', {}).get('lat', 'N/I')
            dict_return['dict_data']['float_longitude'] = dict_weather_forecast_data.get('city', {}).get('coord', {}).get('lon', 'N/I')

            dict_return['dict_data']['list_weather'] = []

            # Lista de dados padrão ( intervalos de 3h )
            #list_weather_forecast_data = dict_weather_forecast_data['list']

            # Lista de dados personalizada com intervalos de 6h
            list_weather_forecast_data = [dict_weather for dict_weather in dict_weather_forecast_data['list'] if (
                '03:00:00' in dict_weather['dt_txt'] or 
                '09:00:00' in dict_weather['dt_txt'] or 
                '15:00:00' in dict_weather['dt_txt'] or 
                '21:00:00' in dict_weather['dt_txt']
            )]

            for dict_weather in list_weather_forecast_data:

                dict_calc = {

                    'str_datetime': dict_weather.get('dt_txt', 'N/I'),
                    'str_weather_description': dict_weather['weather'][0]['description'] if 'weather' in dict_weather and type(dict_weather['weather']) == list and len(dict_weather['weather']) == 1 else 'N/I',
                    'dict_temp': {'str_title': f'Temperatura', 'str_analysis': None, 'list_additional_info': []}, 
                    'dict_umidity': {'str_title': f'Umidade', 'str_analysis': None, 'list_additional_info': []}, 
                    'dict_wind_speed': {'str_title': f'Velocidade do vento', 'str_analysis': None, 'list_additional_info': []}, 
                    'dict_rain': {'str_title': f'Chuva', 'str_analysis': None, 'list_additional_info': []},
                    'dict_conclusion': {'str_conclusion': None}

                }

                # Cálculos de temperatura
                try:

                    bool_temp = True
                    list_analysis_temp = []
                    list_additional_info_temp = []

                    dict_calc['dict_temp']['float_temp'] = float(dict_weather.get('main', {}).get('temp', 0))
                    dict_calc['dict_temp']['float_temp_min'] = float(dict_weather.get('main', {}).get('temp_min', 0))
                    dict_calc['dict_temp']['float_temp_max'] = float(dict_weather.get('main', {}).get('temp_max', 0))
                    dict_calc['dict_temp']['float_feels_like'] = float(dict_weather.get('main', {}).get('feels_like', 0))
                    dict_calc['dict_temp']['float_pressure'] = float(dict_weather.get('main', {}).get('pressure', 0))

                    if (
                        'float_temp_min' in dict_params_calc and type(dict_params_calc['float_temp_min']) == float and
                        dict_calc['dict_temp']['float_temp'] < dict_params_calc['float_temp_min']
                    ):
                        list_analysis_temp.append(f'A temperatura está abaixo do mínimo ideal ( {dict_calc['dict_temp']['float_temp']}°C ).')
                        bool_temp = False

                    elif (
                        'float_temp_max' in dict_params_calc and type(dict_params_calc['float_temp_max']) == float and
                        dict_calc['dict_temp']['float_temp'] > dict_params_calc['float_temp_max']
                    ):
                        list_analysis_temp.append(f'A temperatura está acima do máximo ideal ( {dict_calc['dict_temp']['float_temp']}°C ).')
                        bool_temp = False

                    else: list_analysis_temp.append(f'A temperatura está ideal ( {dict_calc['dict_temp']['float_temp']}°C ).')

                    list_additional_info_temp.append(f'As temperaturas mínima e máxima serão, respectivamente, {dict_calc['dict_temp']['float_temp_min']}°C e {dict_calc['dict_temp']['float_temp_max']}°C, com sensação térmica de {dict_calc['dict_temp']['float_feels_like']}°C.')
                    list_additional_info_temp.append(f'A pressão atmosférica será de {dict_calc['dict_temp']['float_pressure']} hPa.')

                    dict_calc['dict_temp']['str_analysis'] = ' ' . join(list_analysis_temp)
                    dict_calc['dict_temp']['list_additional_info'] = list_additional_info_temp

                except Exception as error:

                    dict_calc['dict_temp']['str_analysis'] = error

                # Cálculos de umidade
                try:

                    bool_umidity = True
                    list_analysis_umidity = []
                    list_additional_info_umidity = []

                    dict_calc['dict_umidity']['float_humidity'] = float(dict_weather.get('main', {}).get('humidity', 0))

                    if (
                        'float_humidity_min' in dict_params_calc and type(dict_params_calc['float_humidity_min']) == float and
                        dict_calc['dict_umidity']['float_humidity'] < dict_params_calc['float_humidity_min']
                    ):
                        list_analysis_umidity.append(f'A umidade está abaixo do mínimo ideal ( {dict_calc['dict_umidity']['float_humidity']}% ).')
                        bool_umidity = False

                    elif (
                        'float_humidity_max' in dict_params_calc and type(dict_params_calc['float_humidity_max']) == float and
                        dict_calc['dict_umidity']['float_humidity'] > dict_params_calc['float_humidity_max']
                    ):
                        list_analysis_umidity.append(f'A umidade está acima do máximo ideal ( {dict_calc['dict_umidity']['float_humidity']}% ).')
                        bool_umidity = False

                    else: list_analysis_umidity.append(f'A umidade está ideal ( {dict_calc['dict_umidity']['float_humidity']}% ).')

                    dict_calc['dict_umidity']['str_analysis'] = ' ' . join(list_analysis_umidity)
                    dict_calc['dict_umidity']['list_additional_info'] = list_additional_info_umidity

                except Exception as error:

                    dict_calc['dict_umidity']['str_analysis'] = error

                # Cálculos de velocidade do vento
                try:

                    bool_umidity_wind_speed = True
                    list_analysis_wind_speed = []
                    list_additional_info_wind_speed = []

                    dict_calc['dict_wind_speed']['float_wind_speed'] = float(dict_weather.get('wind', {}).get('speed', 0))
                    dict_calc['dict_wind_speed']['float_wind_speed_direction'] = float(dict_weather.get('wind', {}).get('deg', 0))

                    if (
                        'float_wind_speed_min' in dict_params_calc and type(dict_params_calc['float_wind_speed_min']) == float and
                        dict_calc['dict_wind_speed']['float_wind_speed'] < dict_params_calc['float_wind_speed_min']
                    ):
                        list_analysis_wind_speed.append(f'A velocidade do vento está abaixo do mínimo ideal ( {dict_calc['dict_wind_speed']['float_wind_speed']} m/s ).')
                        bool_umidity_wind_speed = False

                    elif (
                        'float_wind_speed_max' in dict_params_calc and type(dict_params_calc['float_wind_speed_max']) == float and
                        dict_calc['dict_wind_speed']['float_wind_speed'] > dict_params_calc['float_wind_speed_max']
                    ):
                        list_analysis_wind_speed.append(f'A velocidade do vento está acima do máximo ideal ( {dict_calc['dict_wind_speed']['float_wind_speed']} m/s ).')
                        bool_umidity_wind_speed = False

                    else: list_analysis_wind_speed.append(f'A velocidade do vento está ideal ( {dict_calc['dict_wind_speed']['float_wind_speed']} m/s ).')

                    list_additional_info_wind_speed.append(f'A direção do vento será de {dict_calc['dict_wind_speed']['float_wind_speed_direction']}°.')

                    dict_calc['dict_wind_speed']['str_analysis'] = ' ' . join(list_analysis_wind_speed)
                    dict_calc['dict_wind_speed']['list_additional_info'] = list_additional_info_wind_speed

                except Exception as error:

                    dict_calc['dict_wind_speed']['str_analysis'] = error

                # Cálculos de chuva
                try:

                    bool_umidity_rain = True
                    list_analysis_rain = []
                    list_additional_info_rain = []

                    dict_calc['dict_rain']['float_rain'] = float(dict_weather.get('rain', {}).get('3h', 0))
                    dict_calc['dict_rain']['float_rain_probability'] = float(dict_weather.get('pop', 0)) * 100
                    dict_calc['dict_rain']['float_rain_clouds'] = float(dict_weather.get('clouds', {}).get('all', 0))

                    if (
                        'float_rain_min' in dict_params_calc and type(dict_params_calc['float_rain_min']) == float and
                        dict_calc['dict_rain']['float_rain'] < dict_params_calc['float_rain_min']
                    ):
                        list_analysis_rain.append(f'A quantidade de chuva está abaixo do mínimo ideal ( {dict_calc['dict_rain']['float_rain']} mm ).')
                        bool_umidity_rain = False

                    elif (
                        'float_rain_max' in dict_params_calc and type(dict_params_calc['float_rain_max']) == float and
                        dict_calc['dict_rain']['float_rain'] > dict_params_calc['float_rain_max']
                    ):
                        list_analysis_rain.append(f'A quantidade de chuva está acima do máximo ideal ( {dict_calc['dict_rain']['float_rain']} mm ).')
                        bool_umidity_rain = False

                    else: list_analysis_rain.append(f'A quantidade de chuva está ideal ( {dict_calc['dict_rain']['float_rain']} mm ).')

                    list_additional_info_rain.append(f'A probabilidade de chuva será de {dict_calc['dict_rain']['float_rain_probability']:.2f}%.')
                    list_additional_info_rain.append(f'A cobertura de núveus será de {dict_calc['dict_rain']['float_rain_clouds']:.2f}%.')

                    dict_calc['dict_rain']['str_analysis'] = ' ' . join(list_analysis_rain)
                    dict_calc['dict_rain']['list_additional_info'] = list_additional_info_rain

                except Exception as error:

                    dict_calc['dict_rain']['str_analysis'] = error

                # Demais possíveis cálculos...

                # Conclusão final
                dict_calc['dict_conclusion']['str_conclusion'] = 'Condições ideais para o plantio' if bool_temp == True and bool_umidity == True and bool_umidity_wind_speed == True and bool_umidity_rain == True else 'Existem condições desfavoráveis para o plantio'

                dict_return['dict_data']['list_weather'].append(dict_calc)

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


