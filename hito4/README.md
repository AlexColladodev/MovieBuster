# Composición de servicios

## 🐋 Docker Desktop 🐋

Docker es una plataforma de contenedorización que permite a los desarrolladores empaquetar aplicaciones y sus dependencias en contenedores ligeros y portátiles. Estos contenedores garantizan que las aplicaciones se ejecuten de manera uniforme en diferentes entornos, ya sea en desarrollo, pruebas o producción. Docker Desktop es una herramienta que simplifica la instalación y el uso de Docker en sistemas operativos como Windows y macOS, ofreciendo una interfaz gráfica y soporte completo para la gestión de imágenes, contenedores, redes y volúmenes.

## 📦 Estructura del clúster de contenedores 📦

La estructura del clúster de contenedores se basa en tres contenedores principales: uno para la API, otro para la base de datos MongoDB y un tercero para la ejecución de los tests automatizados.

La separación de tareas permite que cada contenedor cumpla con su función específica, lo que hace que el sistema sea más fácil de mantener y ampliar en el futuro. Además, usar contenedores asegura que el entorno sea siempre el mismo, ya sea en desarrollo, pruebas o producción, sin importar en qué computadora se ejecute. Por otro lado, el uso de un volumen para MongoDB garantiza que los datos estén seguros incluso en caso de problemas inesperados, y el contenedor dedicado a las pruebas automatizadas asegura que todo funcione correctamente.

### Contenedor para la API

El contenedor de la API ejecuta la lógica principal de la aplicación. Se conecta a la base de datos MongoDB para gestionar las operaciones relacionadas con los datos y expone el puerto 5000, permitiendo que los usuarios accedan al servicio desde el host o desde otros contenedores. Este contenedor incluye un volumen que monta el código fuente de manera directa, facilitando actualizaciones en tiempo real durante el desarrollo.

### Contenedor para la Base de Datos

El segundo contenedor proporciona el servicio de base de datos MongoDB, esencial para almacenar y gestionar los datos utilizados por la API. Este contenedor utiliza la imagen oficial de MongoDB, garantizando compatibilidad y estabilidad. Para evitar conflictos con otras instancias de MongoDB en el sistema local, el contenedor mapea el puerto interno 27017 al puerto 27018 del host. Además, incluye un volumen persistente que asegura que los datos no se pierdan incluso si el contenedor se reinicia o detiene.

### Contenedor para los tests

El tercer contenedor está dedicado exclusivamente a la ejecución de tests automatizados. Este contenedor se construye de manera similar al de la API, garantizando que las pruebas se ejecuten en un entorno idéntico al de desarrollo. Utiliza pytest para realizar validaciones automatizadas sobre las funcionalidades de la API, incluyendo operaciones con la base de datos. Este contenedor también depende de MongoDB, lo que permite realizar pruebas completas que incluyen operaciones reales sobre la base de datos. Al compartir el mismo código que la API, se asegura consistencia entre lo que se desarrolla y lo que se prueba

## 🪧 Justificación y configuración de contenedores 🪧

### 🎞️ Contenedor moviebuster-api 🎞️

- **`build` y `context`:**
  - El contexto `./api` indica el directorio donde se encuentra el código fuente de la API y el `Dockerfile`. Esto asegura que la imagen del contenedor se construya directamente desde el código actualizado.

- **`ports`:**
  - El puerto `5000` del contenedor se expone al host, permitiendo que otros servicios o usuarios accedan a la API.
  - Se utiliza este puerto porque es el estándar común para aplicaciones Flask, lo que facilita la configuración y compatibilidad con otros entornos.

- **`environment`:**
  - Variables como `MONGO_URI` y `JWT_SECRET_KEY` se configuran aquí.
    - `MONGO_URI`: Define la conexión con MongoDB, asegurando que la API pueda comunicarse con la base de datos.
    - `JWT_SECRET_KEY`: Garantiza la seguridad en el manejo de autenticación y tokens. (Actualmente no se usa pero para la expansión de la aplicación será necesaria)

- **`volumes`:**
  - Se monta el directorio `./api/src` como `/app/src` dentro del contenedor. Los cambios realizados en el código fuente local se ven reflejados en el contenedor.

- **`depends_on`:**
  - Declara la dependencia del contenedor `mongo`.

- **`command`:**
  - El comando `python src/app.py` ejecuta la aplicación Flask al iniciar el contenedor. La API se inicie automáticamente cuando el contenedor está activo, simplificando el despliegue.

- **Imagen base:** Se utiliza una imagen basada en Python (definida en el `Dockerfile`).
- **Esto porque:**
  - La API está desarrollada en Python, por lo que una imagen de Python proporciona un entorno listo para ejecutar el código.
  - La versión específica de Python elegida garantiza compatibilidad con las dependencias del proyecto definidas en `requirements.txt`.

El contenedor `moviebuster-api` se comunica directamente con el contenedor de MongoDB (`mongo`) para realizar operaciones de lectura/escritura. La dependencia explícita mediante `depends_on` asegura que MongoDB esté disponible cuando la API lo necesite. Esto permite mantener la cohesión y garantizar que los datos se manejen de manera eficiente.

### 💾 Contenedor mongo 💾

- **`image`:**
  - Se utiliza la imagen oficial `mongo:6.0` como base para este contenedor. Ya que esta es una imagen oficial que garantiza estabilidad y compatibilidad con lo necesario para la aplicación.

- **`ports`:**
  - El puerto `27017` del contenedor se mapea al puerto `27018` en el host. Este mapeo permite que el servicio de MongoDB sea accesible desde el host local o por otros contenedores del clúster. Cambiar el puerto externo a `27018` evita conflictos con posibles instancias locales de MongoDB que puedan estar ejecutándose en el sistema.

- **`volumes`:**
  - Se define un volumen llamado `mongo_data` que mapea al directorio interno `/data/db` en el contenedor. MongoDB utiliza `/data/db` para almacenar los datos. Este volumen asegura persistencia, lo que significa que los datos se conservarán incluso si el contenedor se detiene o reinicia. 

### ☢️ Contenedor moviebuster-test ☢️

- **`build` y `context`:**
  - El contexto `./api` indica que el contenedor se construye desde el mismo directorio que la API.

- **`environment`:**
  - Se definen tres variables de entorno:
    - `MONGO_URI`: URI para conectar con el contenedor de MongoDB.
    - `JWT_SECRET_KEY`: Clave de seguridad para pruebas relacionadas con autenticación y tokens.
    - `PYTHONPATH`: Define el directorio `/app/src` como raíz del proyecto en el contenedor.

- **`volumes`:**
  - El volumen `./api/src:/app/src` monta el código fuente del proyecto en el directorio `/app/src` dentro del contenedor.

- **`depends_on`:**
  - Declara una dependencia del contenedor `mongo`.

- **`command`:**
  - Ejecuta el comando `pytest src/tests/` al iniciar el contenedor.
