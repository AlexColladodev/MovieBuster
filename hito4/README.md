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

