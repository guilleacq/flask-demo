import requests # La librería para hacer pedidos a internet

# La URL base de la API
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

# Agarra la ficha del pokemon de la api y devuelve un diccionario más prolijo (_ porque es privado)
def _preparar_ficha_pokemon(datos_api):
    if not datos_api:
        return {}

    # Me quedo con la lista de habilidades y tipos de la API
    habilidades = [h['ability']['name'] for h in datos_api['abilities']]

    tipos = [t['type']['name'] for t in datos_api['types']]

    ficha = {
        "nombre": datos_api['name'].capitalize(),
        "imagen": datos_api['sprites']['front_default'],
        "tipos": tipos,
        "altura": datos_api['height'] / 10,  # paso a metros
        "peso": datos_api['weight'] / 10,    # Paso a kilos
        "habilidades": habilidades
    }
    return ficha

# dado el nombre de un pokemon, obtiene sus datos de la API. Usa preparar_ficha_pokemon() para devolver un diccionario lindo
def obtener_datos_pokemon(nombre_pokemon):

    # https://pokeapi.co/api/v2/pokemon/pikachu
    url = f"{POKEAPI_BASE_URL}{nombre_pokemon.lower()}"
    
    print(f"Buscando en la pokeapi: {url}")

    try:
        respuesta = requests.get(url)
        # checkea el estado HTTP y va al exception si algo sale mal
        respuesta.raise_for_status() 
        
        # si todo va bien, agarra el json
        datos_crudos = respuesta.json()
        
        return _preparar_ficha_pokemon(datos_crudos)

    except requests.exceptions.RequestException as e:
        print(f"Error: no se pudo conectar con la Pokeapi: {e}")

        return None 


# busca pokemon por nombre y/o tipo
# - si se da solo el nombre, busca ese Pokémon.
# -si se da solo el tipo, trae todos los Pokémon de ese tipo.
# - Si se dan ambos, filtra los Pokémon del tipo dado por el nombre.
def buscar_pokemon(nombre=None, tipo=None):
    pokemones_encontrados = []

    # Escenario 1: busqueda por tipo (o tipo y nombre)
    if tipo:
        url_tipo = f"https://pokeapi.co/api/v2/type/{tipo.lower()}"
        print(f"Buscando por tipo en: {url_tipo}")
        try:
            respuesta_tipo = requests.get(url_tipo)
            respuesta_tipo.raise_for_status()
            datos_tipo = respuesta_tipo.json()

            # la API devuelve una lista de pokemon bajo la clave 'pokemon'
            lista_pokemones_por_tipo = [p['pokemon'] for p in datos_tipo['pokemon']]

            #ahora filtro esa lista
            for poke_info in lista_pokemones_por_tipo:
                # si recibo un nombre, y no coincide, lo salteamos
                if nombre and nombre.lower() not in poke_info['name']:
                    continue

                ficha = obtener_datos_pokemon(poke_info['name'])
                if ficha:
                    pokemones_encontrados.append(ficha)

        except requests.exceptions.RequestException as e:
            print(f"Error buscando por tipo '{tipo}': {e}")
            return [] 

    # Escenario 2: busqueda solo por nombre (si no se pasó un tipo)
    elif nombre:
        pokemon = obtener_datos_pokemon(nombre)
        if pokemon:
            pokemones_encontrados.append(pokemon)

    return pokemones_encontrados