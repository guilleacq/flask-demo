from datetime import datetime

SIGNO_POKEMON = {
    "Aries": "mankey",
    "Tauro": "tauros",
    "Géminis": "doduo",
    "Cáncer": "krabby",
    "Leo": "litleo",
    "Virgo": "gardevoir",
    "Libra": "hitmonlee",
    "Escorpio": "skorupi",
    "Sagitario": "ponyta",
    "Capricornio": "sawsbuck",
    "Acuario": "psyduck",
    "Piscis": "magikarp"
}

# Recibe la fecha en formato YYYY-MM-DD
def calcular_signo_zodiacal(fecha_nacimiento_str):
    try: 
        fecha = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
        dia = fecha.day
        mes = fecha.month
    
    except ValueError:
        return None

    # Tal vez no es la mejor forma de calcular el zodiaco pero ya fue jajaj    

    if (mes == 3 and dia >= 21) or (mes == 4 and dia <= 19):
        return "Aries"
    elif (mes == 4 and dia >= 20) or (mes == 5 and dia <= 20):
        return "Tauro"
    elif (mes == 5 and dia >= 21) or (mes == 6 and dia <= 20):
        return "Géminis"
    elif (mes == 6 and dia >= 21) or (mes == 7 and dia <= 22):
        return "Cáncer"
    elif (mes == 7 and dia >= 23) or (mes == 8 and dia <= 22):
        return "Leo"
    elif (mes == 8 and dia >= 23) or (mes == 9 and dia <= 22):
        return "Virgo"
    elif (mes == 9 and dia >= 23) or (mes == 10 and dia <= 22):
        return "Libra"
    elif (mes == 10 and dia >= 23) or (mes == 11 and dia <= 21):
        return "Escorpio"
    elif (mes == 11 and dia >= 22) or (mes == 12 and dia <= 21):
        return "Sagitario"
    elif (mes == 12 and dia >= 22) or (mes == 1 and dia <= 19):
        return "Capricornio"
    elif (mes == 1 and dia >= 20) or (mes == 2 and dia <= 18):
        return "Acuario"
    elif (mes == 2 and dia >= 19) or (mes == 3 and dia <= 20):
        return "Piscis"