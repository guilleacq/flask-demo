from flask import Flask, request, jsonify

from utils.horoscopo_util import calcular_signo_zodiacal, SIGNO_POKEMON
from services.pokemon_service import obtener_datos_pokemon, buscar_pokemon
from services import favoritos_service

app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return "<h1> Aguante pokemon papá </h1>"

# Endpoint que recibe nombre y fecha de nacimiento y devuelve el pokemon asociado al horoscopo
@app.route('/horoscopo', methods=['POST'])
def endpoint_consultar_horoscopo():

    datos = request.get_json()

    if not datos or 'nombre' not in datos or 'fecha_nacimiento' not in datos:
        return jsonify({"error": "Faltan datos. Necesito 'nombre' y 'fecha_nacimiento'."}), 400

    nombre_usuario = datos['nombre']
    fecha_nacimiento = datos['fecha_nacimiento']

    if not nombre_usuario.strip(): 
        return jsonify({"error": "El nombre no puede estar vacío."}), 400

    signo = calcular_signo_zodiacal(fecha_nacimiento)

    if not signo:
        return jsonify({"error": "La fecha de nacimiento no es válida. Usá el formato YYYY-MM-DD."}), 400

    nombre_pokemon = SIGNO_POKEMON[signo]

    pokemon_info = obtener_datos_pokemon(nombre_pokemon)

    if not pokemon_info:
        return jsonify({"error": "No se pudo encontrar el Pokémon para tu signo."})
    

    respuesta = {
        "usuario": nombre_usuario,
        "signo_zodiacal": signo,
        "pokemon_asignado": pokemon_info
    }

    return jsonify(respuesta)

# endpoint para buscar pokemon, acepta un nombre y tipo
@app.route('/pokemon', methods=['GET'])
def endpoint_buscar_pokemon():

    # request.args porque es un GET
    nombre_pokemon = request.args.get('nombre')
    tipo_pokemon = request.args.get('tipo')

    if not nombre_pokemon and not tipo_pokemon:
        return jsonify({"error": "Tenés que mandar un 'nombre' o un 'tipo' para buscar."}), 400

    resultados = buscar_pokemon(nombre=nombre_pokemon, tipo=tipo_pokemon)

    return jsonify(resultados)

# Obtiene los favoritos de un usuario especifico
@app.route('/favoritos', methods=['GET'])
def endpoint_listar_favoritos():
    nombre_usuario = request.args.get('usuario')
    if not nombre_usuario:
        return jsonify({"error": "Falta el parámetro 'usuario'."}), 400
    
    favoritos = favoritos_service.listar_favoritos_por_usuario(nombre_usuario)
    return jsonify(favoritos)

# Actualiza los favoritos
@app.route('/favoritos', methods=['POST'])
def endpoint_agregar_favorito():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'pokemon' not in datos:
        return jsonify({"error": "Faltan datos. Necesito 'nombre' (de usuario) y 'pokemon'."}), 400

    nuevo_fav = favoritos_service.agregar_favorito(datos['nombre'], datos['pokemon'])
    
    if nuevo_fav is None:
        return jsonify({"error": "Ese Pokémon ya está en tus favoritos."})

    return jsonify(nuevo_fav)

# Dado un nombre de usuario y un id favorito, borro un favorito
@app.route('/favoritos', methods=['DELETE'])
def endpoint_eliminar_favorito():
    datos = request.get_json()
    if not datos or 'nombre' not in datos or 'id_favorito' not in datos:
        return jsonify({"error": "Faltan datos. Necesito 'nombre' (de usuario) y 'id_favorito'."}), 400

    try:
        id_fav = int(datos['id_favorito'])
    except ValueError:
        return jsonify({"error": "'id_favorito' tiene que ser un número."}), 400

    exito = favoritos_service.eliminar_favorito(datos['nombre'], id_fav)

    if exito:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "No se encontró el favorito o el usuario."}), 404 

# Dado un id de favorito y un usuario, devuelve los datos del pokemon
@app.route('/favoritos/<int:id_favorito>', methods=['GET'])
def endpoint_buscar_favorito_por_id(id_favorito):
    nombre_usuario = request.args.get('usuario')
    if not nombre_usuario:
        return jsonify({"error": "Falta el parámetro 'usuario'."}), 400
    
    favorito = favoritos_service.obtener_favorito_por_id(nombre_usuario, id_favorito)
    
    if not favorito:
        return jsonify({}), 404 

    # Si encontramos el favorito, buscamos sus datos completos en la PokeApi
    pokemon_completo = obtener_datos_pokemon(favorito['nombre_pokemon'])
    if not pokemon_completo:
        return jsonify({"error": "Se encontró el favorito, pero no se pudieron obtener los datos del Pokémon."}), 404

    return jsonify(pokemon_completo)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



