# Flask demo: Pokemon horóscopo y favoritos
Una API RESTful desarrollada en Python con Flask, que permite descubrir tu Pokémon según tu signo zodiacal, buscar entre cientos de Pokémon y gestionar una lista de favoritos. El proyecto está *dockerizado* para una ejecución y despliegue súper sencillos.

## ¿En qué consiste la API?
La idea es simple: **ofrecer una serie de endpoints para interactuar con el universo Pokémon**. La API te permite:
*   **Obtener tu Pokémon zodiacal**: Enviás tu nombre y fecha de nacimiento, y te devuelve el Pokémon que te corresponde.
*   **Buscar Pokémon**: Podés buscar por nombre, por tipo o combinar ambos filtros.
*   **Gestionar favoritos**: Cada usuario puede tener su propia lista de Pokémon favoritos, guardarlos, verlos y eliminarlos.

## Endpoints de la API
La API cuenta con los siguientes endpoints para interactuar:

#### 1. Horóscopo Pokémon
*   **Endpoint**: `POST /horoscopo`
*   **Descripción**: Recibe un nombre y una fecha de nacimiento, y devuelve el signo zodiacal con su Pokémon asignado y toda la info de la PokeAPI.
*   **Body (JSON)**:
    ```json
    {
        "nombre": "Ash Ketchum",
        "fecha_nacimiento": "1997-04-01"
    }
    ```

#### 2. Buscar Pokémon
*   **Endpoint**: `GET /pokemon`
*   **Descripción**: Busca Pokémon por nombre y/o tipo. Si no se manda ninguno, devuelve un error.
*   **Parámetros (Query)**:
    *   `nombre` (opcional): Parte o nombre completo del Pokémon.
    *   `tipo` (opcional): Tipo del Pokémon (ej: "fire", "water").
*   **Ejemplos**:
    *   `GET /pokemon?nombre=pika`
    *   `GET /pokemon?tipo=electric`
    *   `GET /pokemon?nombre=char&tipo=fire`

#### 3. Gestión de Favoritos
*   **Listar favoritos**: `GET /favoritos?usuario=<nombre>`
    *   Devuelve la lista de Pokémon favoritos para ese usuario.
*   **Agregar favorito**: `POST /favoritos`
    *   Guarda un Pokémon en la lista de un usuario.
    *   **Body (JSON)**:
        ```json
        {
            "nombre": "Misty",
            "pokemon": "psyduck"
        }
        ```
*   **Eliminar favorito**: `DELETE /favoritos`
    *   Borra un Pokémon de la lista usando su ID de favorito.
    *   **Body (JSON)**:
        ```json
        {
            "nombre": "Misty",
            "id_favorito": 1
        }
        ```
*   **Ver detalle de un favorito**: `GET /favoritos/<id_favorito>?usuario=<nombre>`
    *   Obtiene la ficha completa de un Pokémon guardado en favoritos.

## Dependencias
- **Flask**: para montar la API.
- **Requests**: para consumir la PokeAPI externa.
- **Docker y Docker Compose**: para correr todo el entorno de forma aislada y sin dramas de instalación.

## ¿Cómo instalar y ejecutar?
Gracias a Docker, no necesitás instalar Python ni las dependencias directamente en tu máquina.

1.  Asegurate de tener **Docker** y **Docker Compose** instalados.
2.  Cloná este repositorio en tu computadora.
3.  Abrí una terminal en la carpeta raíz del proyecto y ejecutá:
    ```bash
    docker-compose up --build
    ```
¡Y listo! La API estará corriendo y accesible en `http://localhost:8080`.

## Notas adicionales
- El sistema de favoritos guarda los datos en un archivo `favoritos.json` que se crea automáticamente en la raíz del proyecto. Si querés reiniciar los favoritos, simplemente borrá ese archivo.
- La lógica para calcular el signo zodiacal es una simplificación y se encuentra en `utils/horoscopo_util.py`. ¡No la uses para tu carta astral!
- El código fue desarrollado como una demo funcional y rápida, por lo que puede que no siga las prácticas más puristas de desarrollo de software.
- La interacción con la PokeAPI está encapsulada en el `services/pokemon_service.py`.
