##ERRO DE DADOS NÃO DISPONÍVEIS



import datetime as dt
import meteomatics.api as api
import requests

# Funcao para obter o tempo usando a API fornecida
def get_weather_data(api_url, username, password):
    response = requests.get(api_url, auth=(username, password))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erro ao obter informações meteorológicas:", response.text)
        return None

# Funcao para validar a entrada do usuário
def get_valid_input(prompt, input_type):
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print("Por favor, insira um valor válido.")

# Pedindo ao usuario para inserir o nome da cidade
city_name = input("Digite o nome da cidade: ")

# Obtendo as coordenadas do local
# Supondo que get_coordinates seja uma funcao valida que retorna as coordenadas da cidade
coordinates = (0, 0)  # Apenas para exemplo, voce precisa implementar esta funcao

if coordinates:
    latitude, longitude = coordinates

    # Construindo a URL da API com as coordenadas do local e a data e hora fornecidas pelo usuario
    api_url_base = f"https://api.meteomatics.com/2024-05-13T17:05:00.000-04:00/t_2m:C,precip_type:idx/{latitude},{longitude}/json?model=mix"
    username = 'univag_marques_joo'
    password = 'mFdH3C51ad'

    # Pedindo ao usuario para inserir a data e hora inicial
    day = get_valid_input("Digite o dia da data inicial (ex: 13): ", int)
    month = get_valid_input("Digite o mês da data inicial (ex: 5 para maio): ", int)
    year = get_valid_input("Digite o ano da data inicial (ex: 2024): ", int)
    hour = get_valid_input("Digite a hora da data inicial (0-23): ", int)
    minute = get_valid_input("Digite os minutos da data inicial (0-59): ", int)

    startdate_ts = dt.datetime(year, month, day, hour, minute, tzinfo=dt.timezone.utc)

    # Calculando a data final
    enddate_ts = startdate_ts + dt.timedelta(days=1)

    # Definindo o intervalo de tempo
    interval_ts = dt.timedelta(hours=1)

    print("Local:", city_name)
    print("Data inicial:", startdate_ts)
    print("Data final:", enddate_ts)
    print("Intervalo de tempo:", interval_ts)

    weather_data = get_weather_data(api_url_base, username, password)

if weather_data:
    # Verificando se 'data' esta presente nos dados
    if 'data' in weather_data:
        data = weather_data['data']

        # Verificando se 't_2m' esta presente nos dados
        if 't_2m' in data:
            temperature = data['t_2m']['C']
            print("Temperatura:", temperature, "°C")
        else:
            print("Temperatura não disponível nos dados.")

        # Verificando se 'precip_type' esta presente nos dados
        if 'precip_type' in data:
            precipitation = data['precip_type']['idx']
            print("Tipo de precipitação:", precipitation)
        else:
            print("Tipo de precipitação não disponível nos dados.")
    else:
        print("Dados meteorológicos não encontrados.")
else:
    print("Erro ao obter informações meteorológicas.")

