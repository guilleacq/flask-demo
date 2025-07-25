import json

# La ruta a donde guardo los datos
RUTA_ARCHIVO_FAVORITOS = 'favoritos.json'

#Función interna para leer el archivo JSON. Es para para no repetir código
def _leer_favoritos():
    try:
        with open(RUTA_ARCHIVO_FAVORITOS, 'r') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

#Función interna para escribir en el archivo JSON
def _guardar_favoritos(datos):
    with open(RUTA_ARCHIVO_FAVORITOS, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

# Devuelve la lista de favoritos de un usuario
def listar_favoritos_por_usuario(nombre_usuario):
    favoritos = _leer_favoritos()
    return favoritos.get(nombre_usuario, [])

# Agrega un nuevo Pokémon a la lista de favoritos de un usuario.
def agregar_favorito(nombre_usuario, nombre_pokemon):
    todos_los_favoritos = _leer_favoritos()
    
    favoritos_usuario = todos_los_favoritos.get(nombre_usuario, [])

    for fav in favoritos_usuario:
        if fav['nombre_pokemon'].lower() == nombre_pokemon.lower():
            return None

    # Calculando el nuevo ID. Si no hay favoritos es 1, si no, es el ultimo + 1
    nuevo_id = 1
    if favoritos_usuario:
        nuevo_id = max(f['id_favorito'] for f in favoritos_usuario) + 1

    nuevo_favorito = {
        "id_favorito": nuevo_id,
        "nombre_pokemon": nombre_pokemon
    }

    favoritos_usuario.append(nuevo_favorito)
    todos_los_favoritos[nombre_usuario] = favoritos_usuario
    _guardar_favoritos(todos_los_favoritos)
    
    return nuevo_favorito

# Elimina un favorito de la lista de un usuario por su ID.
def eliminar_favorito(nombre_usuario, id_favorito):
    todos_los_favoritos = _leer_favoritos()
    
    if nombre_usuario not in todos_los_favoritos:
        return False 

    favoritos_usuario = todos_los_favoritos[nombre_usuario]
    
    favoritos_filtrados = []
    for fav in favoritos_usuario:
        if fav['id_favorito'] != id_favorito:
            favoritos_filtrados.append(fav)

    if len(favoritos_filtrados) == len(favoritos_usuario): 
        return False 

    todos_los_favoritos[nombre_usuario] = favoritos_filtrados
    _guardar_favoritos(todos_los_favoritos)
    
    return True

#Busca un Pokémon favorito especifico por su id de favorito.
def obtener_favorito_por_id(nombre_usuario, id_favorito):
    favoritos_usuario = listar_favoritos_por_usuario(nombre_usuario)
    for fav in favoritos_usuario:
        if fav['id_favorito'] == id_favorito:
            return fav # Devuelve el diccionario con el id favorito y el nombre del que buscamos
    return None 