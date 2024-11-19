from datetime import datetime
import pprint
from custom.helper import Helper
from custom.openweather import OpenWeather
from models.f3_c1_sensor import F3C1Sensor

class Irrigation:

    def __init__(self):

        pass


    def exception(self, str_message: str = '') -> str:

        if str_message.strip() != '':
            raise Exception(f'[Irrigation] {str_message}')


    """
    Método responsável por verificar se uma determinada plantação deverá ser a irrigação iniciada automaticamente a partir de validações dos parâmetros preenchidos

    Arguments:
    - dict_filters_plantation: Parâmetros relacionados à plantação ( dict )
    - dict_measurement: Parâmetros relacionados à medição da plantação ( dict )
    - dict_filters_rain: Parâmetros relacionados à localização da plantação para verificação de chuvas ( dict )
   
    """
    def validate_begin_execution_by_plantation(self, dict_params: dict = {}) -> dict:

        dict_return = {'status': True, 'dict_data': {'dict_analysis_filters_plantation': {'status': False}, 'dict_analysis_filters_rain': {'status': False}}}

        try:

            dict_filters_plantation = dict_params.get('dict_filters_plantation', {})
            dict_measurement = dict_params.get('dict_measurement', {})
            dict_filters_rain = dict_params.get('dict_filters_rain', {})

            """
            Validação utilizando os filtros da plantação

            - Regras: A partir de parâmetros específicos, será possível verificar se uma irrigação automática poderá ou não ser iniciada.
            """

            # Parâmetros relacionados à medição que deverá ser utilizada na filtragem
            int_sensor_type = dict_measurement.get('int_sensor_type', None)
            float_value = dict_measurement.get('float_value', None)
            
            if type(int_sensor_type) != type(None):

                try:

                    dict_sensor = F3C1Sensor.get_type_options(int_sensor_type)

                    match int_sensor_type:

                        case F3C1Sensor.TYPE_TEMPERATURE:

                            float_temp_max = dict_filters_plantation.get('float_temp_max', None)

                            if type(float_temp_max) == type(None):
                                self.exception('A plantação não possui um limite máximo de temperatura configurada, portanto, a validação para iniciação da irrigação automática não será executada.')

                            if float_value < float_temp_max:
                                self.exception(f'De acordo com a medição informada ( {float_value}°C ), não será necessário iniciar a irrigação pois a temperatura está abaixo do limite máximo ( {float_temp_max}°C ).')

                        case F3C1Sensor.TYPE_HUMIDITY:

                            float_humidity_min = dict_filters_plantation.get('float_humidity_min', None)

                            if type(float_humidity_min) == type(None):
                                self.exception('A plantação não possui um limite mínimo de umidade configurada, portanto, a validação para iniciação da irrigação automática não será executada.')
                            
                            if float_value > float_humidity_min:
                                self.exception(f'De acordo com a medição informada ( {float_value}% ), não será necessário iniciar a irrigação pois a umidade está acima do limite mínimo ( {float_humidity_min}% ).')

                        case F3C1Sensor.TYPE_LIGHT:

                            float_light_max = dict_filters_plantation.get('float_light_max', None)

                            if type(float_light_max) == type(None):
                                self.exception('A plantação não possui um limite máximo de luminosidade configurada, portanto, a validação para iniciação da irrigação automática não será executada.')
                            
                            if float_value < float_light_max:
                                self.exception(f'De acordo com a medição informada ( {float_value} lux ), não será necessário iniciar a irrigação pois a luminosidade está abaixo do limite máximo ( {float_light_max} lux ).')

                        case F3C1Sensor.TYPE_RADIATION:
                           
                           float_radiation_max = dict_filters_plantation.get('float_radiation_max', None)

                           if type(float_radiation_max) == type(None):
                                self.exception('A plantação não possui um limite máximo de radiação configurada, portanto, a validação para iniciação da irrigação automática não será executada.')

                           if float_value < float_radiation_max:
                                self.exception(f'De acordo com a medição informada ( {float_value} W/m² ), não será necessário iniciar a irrigação pois a radiação está abaixo do limite máximo ( {float_radiation_max} W/m² ).')

                        case _:
                            self.exception(f'Não foi possível concluir o processo pois o tipo de sensor informado ( {dict_sensor['title']} ) não atende aos requisitos para irrigação automática.')

                    # Caso todas as validações tenham sido aprovadas, significa que a irrigação deverá ser iniciada
                    dict_return['dict_data']['dict_analysis_filters_plantation']['status'] = True

                except Exception as error:

                    dict_return['dict_data']['dict_analysis_filters_plantation'] = {'status': False, 'message': error}

            """
            Validação utilizando os filtros destinados à validação de chuva no local da plantação

            - Regras: A partir de parâmetros de geolocalização, será possível verificar se a região da plantação possui chuvas mapeadas e, caso positivo, se o limite atende às regras para iniciaçao de irrigação automática.
            """

             # Parâmetros relacionados aos filtros para validação de chuva
            float_latitude = dict_filters_rain.get('float_latitude', None)
            float_longitude = dict_filters_rain.get('float_longitude', None)

            if type(float_latitude) != type(None) and type(float_longitude) != type(None):

                try:

                    # Parâmetro referente à quantidade de horas que deverá ser considerada para análise
                    # > Padrão: 1h
                    int_next_hours_validate_rain = dict_filters_rain.get('int_next_hours_validate_rain', 4)

                    # Parâmetro referente à quantidade média máxima de chuva aceita para que a irrigação possa ser iniciada automaticamente
                    # > Padrão: 0 mm
                    float_max_average_rain_volume = dict_filters_rain.get('float_max_average_rain_volume', 0.00)

                    # Variável que irá armazenar a quantidade de chuva prevista para as horas definidas para validação
                    float_rain_volume = 0.00

                    object_open_weather = OpenWeather()

                    dict_data_open_weather = object_open_weather.get_weather_forecast_data_by_location(float_latitude = float(float_latitude), float_longitude = float(float_longitude))
                    if dict_data_open_weather['status'] == False: 
                        self.exception(str(dict_data_open_weather['message']))

                    for dict_weather in dict_data_open_weather['dict_data']['list'][:int_next_hours_validate_rain]:

                        float_rain_volume += dict_weather.get('rain', {}).get('3h', 0.00)

                    # Variável que irá armazenar a média de chuva prevista para as horas definidas para validação
                    float_average_rain_volume = (float_rain_volume / int_next_hours_validate_rain)

                    if float_average_rain_volume > float_max_average_rain_volume:
                        self.exception(f'A quantidade média de chuva prevista para para a(s) próxima(s) {int_next_hours_validate_rain} hora(s) é de {float_average_rain_volume:.2f} mm e está acima do máximo permitido ( {float_max_average_rain_volume:.2f} mm ).')

                    # Caso todas as validações tenham sido aprovadas, significa que a irrigação deverá ser iniciada
                    dict_return['dict_data']['dict_analysis_filters_rain']['status'] = True

                except Exception as error:

                    dict_return['dict_data']['dict_analysis_filters_rain'] = {'status': False, 'message': error}

        except Exception as error:

            dict_return = {'status': False, 'message': error}

        return dict_return


