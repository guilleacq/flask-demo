from flask import Flask, request, jsonify

from utils.horoscopo_util import calcular_signo_zodiacal, SIGNO_POKEMON
from services.pokemon_service import obtener_datos_pokemon, buscar_pokemon

app = Flask(__name__)

@app.route('/')
def hola_mundo():
    return "<h1> Aguante pokemon papá </h1>"

# Endpoint que recibe nombre y fecha de nacimiento y devuelve el pokemon asociado al horoscopo
@app.route('/horoscopo', methods=['POST'])
def consultar_horoscopo():

    # obtengo datos
    datos = request.get_json()

    if not datos or 'nombre' not in datos or 'fecha_nacimiento' not in datos:
        return jsonify({"error": "Faltan datos. Necesito 'nombre' y 'fecha_nacimiento'."}), 400

    nombre_usuario = datos['nombre']
    fecha_nacimiento = datos['fecha_nacimiento']

    if not nombre_usuario.strip(): 
        return jsonify({"error": "El nombre no puede estar vacío."}), 400

    # ----- Ahora si puedo calcular el signo
    signo = calcular_signo_zodiacal(fecha_nacimiento)

    if not signo:
        return jsonify({"error": "La fecha de nacimiento no es válida. Usá el formato YYYY-MM-DD."}), 400

    nombre_pokemon = SIGNO_POKEMON[signo]

    pokemon_info = obtener_datos_pokemon(nombre_pokemon)

    if not pokemon_info:
        return jsonify({"error": "No se pudo encontrar el Pokémon para tu signo."}), 500
    

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

    # tiene que existir o nombre o tipo (pero al menos uno)
    if not nombre_pokemon and not tipo_pokemon:
        return jsonify({"error": "Tenés que mandar un 'nombre' o un 'tipo' para buscar."}), 400

    # Usamos nuestro servicio para hacer la búsqueda
    resultados = buscar_pokemon(nombre=nombre_pokemon, tipo=tipo_pokemon)

    return jsonify(resultados)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



