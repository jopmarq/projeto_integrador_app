import datetime as dt
import meteomatics.api as api
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Credenciais da API da Meteomatics
username = 'univag_marques_joopedro'
password = 'h1ynW1zZN1'

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city_name)
        if location:
            return (location.latitude, location.longitude)
        else:
            print("Coordenadas não encontradas para a cidade fornecida.")
            return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print("Erro ao obter as coordenadas:", e)
        return None

def get_weather(coordinates, startdate_ts, enddate_ts, interval_ts, username, password):
    try:
        # Parâmetros básicos disponíveis para a conta
        parameters = ['t_2m:C']  # Apenas temperatura a 2 metros em Celsius
        # Fazendo a solicitação à API da Meteomatics
        response = api.query_time_series(
            coordinate_list=[coordinates],  # Corrigido aqui para ser uma lista de tuplas
            startdate=startdate_ts,
            enddate=enddate_ts,
            interval=interval_ts,
            parameters=parameters,
            username=username,
            password=password
        )
        return response
    except Exception as e:
        print("Erro ao obter dados meteorológicos:", e)
        return None

def main():
    # Pedir ao usuário para inserir o nome da cidade
    city_name = input("Digite o nome da cidade: ")
    coordinates = get_coordinates(city_name)
    if not coordinates:
        print("Não foi possível obter as coordenadas para a cidade de", city_name)
        return

    # Pedindo ao usuário para inserir a data inicial (dia/mês/ano)
    date_input = input("Digite a data inicial (dia/mês/ano), separados por '/' (ex: 13/5/2024): ")
    try:
        day, month, year = map(int, date_input.split('/'))
    except ValueError:
        print("Formato de data inválido. Use o formato dia/mês/ano.")
        return

    # Pedindo ao usuário para inserir a hora inicial (0-23)
    try:
        hour_input = input("Digite a hora inicial (0-23): ")
        hour = int(hour_input)
    except ValueError:
        print("Hora inválida. Use um valor entre 0 e 23.")
        return

    # Criando o objeto datetime com a data e hora inseridas
    startdate_ts = dt.datetime(year, month, day, hour, tzinfo=dt.timezone.utc)

    # Calculando a data final (1 dia após a data inicial)
    enddate_ts = startdate_ts + dt.timedelta(days=1)

    # Definindo o intervalo de tempo
    interval_ts = dt.timedelta(hours=1)

    # Obter dados meteorológicos usando a API da Meteomatics
    weather_info = get_weather(coordinates, startdate_ts, enddate_ts, interval_ts, username, password)
    
    # Verificar se o DataFrame retornado não está vazio
    if weather_info is not None and not weather_info.empty:
        print(f"Dados meteorológicos para {city_name} no intervalo de {startdate_ts} a {enddate_ts} com intervalos de {interval_ts} horas:")
        print(weather_info)
    else:
        print("Não foi possível obter dados meteorológicos.")

if __name__ == "__main__":
    main()
