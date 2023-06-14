import requests
from UnleashClient import UnleashClient


token = "default:development.unleash-insecure-api-token"


client = UnleashClient(
url="http://localhost:4242/api",
app_name="my-python-app",
custom_headers={'Authorization': token}
)


client.initialize_client()



def obtener_coordenadas(nombre_lugar,email):

    
    app_context = {"userId": email}
    isnuevocalculo = client.is_enabled("experiment", app_context)
    if(isnuevocalculo):
        print("nominatim")
        url = f"https://nominatim.openstreetmap.org/search?q={nombre_lugar}&format=json"
        response = requests.get(url)
        data = response.json()    
        if data:
            latitud = data[0]['lat']
            longitud = data[0]['lon']        
            return latitud, longitud
        else:
            return None, None
    
    else:
        print("geocoding")
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={nombre_lugar},peru"
        response = requests.get(url)
        data = response.json()    
        if data:
            latitud = data["results"][0]["latitude"]
            longitud = data["results"][0]["longitude"]
            return latitud, longitud
        else:
            return None, None

            
            

def obtener_clima(latitud, longitud):
    url_diario = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&forecast_days=2&daily=temperature_2m_max&timezone=PST"
    url_horario = f"https://api.open-meteo.com/v1/forecast?latitude={latitud}&longitude={longitud}&forecast_days=2&hourly=temperature_2m&timezone=PST"

    response_diario = requests.get(url_diario)
    response_horario = requests.get(url_horario)

    data_diario = response_diario.json()
    data_horario = response_horario.json()


    clima_diario = data_diario['daily']['temperature_2m_max'][1]
    clima_horario = data_horario['hourly']['temperature_2m'][24]
    
    return clima_diario, clima_horario


def obtener_restaurantes_cercanos(latitud, longitud):
    bbox = f"{float(longitud)-0.01},{float(latitud)-0.01},{float(longitud)+0.01},{float(latitud)+0.01}"
    url = f"https://api.openstreetmap.org/api/0.6/map.json?bbox={bbox}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        lugares_cercanos = []
        
        if 'elements' in data:
            elementos = data['elements']
            
            for elemento in elementos:
                if 'tags' in elemento and 'amenity' in elemento['tags'] and elemento['tags']['amenity'] == 'restaurant':
                    if 'name' in elemento['tags']:
                        lugares_cercanos.append(elemento['tags']['name'])
        
        return lugares_cercanos
    
    else:
        print("Error al realizar la solicitud:", response.status_code)
        return []


# Obtener coordenadas del lugar
nombre_lugar = (input())
email = (input())

latitud, longitud = obtener_coordenadas(nombre_lugar,email)
# #obtener_restaurantes_cercanos(latitud,longitud)

if latitud and longitud:
     # Obtener el clima
    clima_diario, clima_horario = obtener_clima(latitud, longitud)
    print("Clima para mañana:", clima_diario)
    print("Clima para las próximas 24 horas:", clima_horario)

     # Obtener restaurantes cercanos
    restaurantes = obtener_restaurantes_cercanos(latitud, longitud)
    print("Sugerencia de restaurantes:")
    count = 0
    for restaurante in restaurantes:

        print(restaurante)
        count = count + 1
        if count == 3:
            break
else:
    print("No se encontraron coordenadas para el lugar especificado.")



#nombre_lugar = "jesus maria"
#email = "3@utec.edu.pe"
#print(obtener_coordenadas(nombre_lugar,email))