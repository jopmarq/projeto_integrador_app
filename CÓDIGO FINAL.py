import datetime as dt
import meteomatics.api as api
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# Credenciais
username = 'univag_marques_joo'
password = 'mFdH3C51ad'

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

# Teste da função
city_name = input("Digite o nome da cidade: ")
coordinates = get_coordinates(city_name)
if coordinates:
    print("Coordenadas da cidade de", city_name, ":", coordinates)
else:
    print("Não foi possível obter as coordenadas para a cidade de", city_name)


# Pedindo ao usuário para inserir a data inicial (dia/mês/ano)
date_input = input("Digite a data inicial (dia/mês/ano), separados por '/' (ex: 13/5/2024): ")
day, month, year = map(int, date_input.split('/'))

# Pedindo ao usuário para inserir a hora inicial (0-23)
hour_input = input("Digite a hora inicial (0-23): ")
hour = int(hour_input)

# Criando o objeto datetime com a data e hora inseridas
startdate_ts = dt.datetime(year, month, day, hour, tzinfo=dt.timezone.utc)

# Calculando a data final (1 dia após a data inicial)
enddate_ts = startdate_ts + dt.timedelta(days=1)

# Definindo o intervalo de tempo
interval_ts = dt.timedelta(hours=1)

print("Data e hora inicial:", startdate_ts)
print("Data final:", enddate_ts)
print("Intervalo de tempo:", interval_ts)

coordinates_ts = [coordinates]
parameters_ts = ['t_2m:C', 'precip_1h:mm', 'precip_1h:mm', 'uv:idx', 'wind_speed_10m:ms'] #TEMPO. PRECIPITAÇÃO, UV, VELOCIDADE DO VENTO

print("time series:")
try:
    df_ts = api.query_time_series(coordinates_ts, startdate_ts, enddate_ts, interval_ts,
                                  parameters_ts, username, password)
    print(df_ts.head())
except Exception as e:
    print("Failed, the exception is {}".format(e))
