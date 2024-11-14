# Integración Continua

## 🔧 Instalación 🔧

Antes que nada, asegurarse de tener instalado python en el dispositivo:

```bash
python --version
```

### 🗿 Creación del Entorno Virtual 🗿

Un entorno virtual es útil ya que mantiene las dependencias de cada proyecto separadas, evitando problemas con otras aplicaciones o versiones de librerías que tengas en el sistema. Así se asegura que todo funcione bien en cualquier equipo y que las versiones sean las correctas, sin conflictos inesperados.

Para la creación del entorno virtual se siguen los siguientes pasos:

```bash
pip install virtualenv
```
```bash
python -m venv env
```
```bash
.\env\Scripts\activate
```

### 🔩 Instalación de Dependencias 🔩

Como se mencionó en el Hito 1, el proyecto usará el framework Flask junto con MongoDB, gracias a Pymongo. Es importante instalar todas las dependencias necesarias, que están listadas en el archivo requirements.txt con sus versiones específicas. Para instalar las dependencias, simplemente ejecuta:

```bash
pip install -r requirements.txt
```

## 🛠️ Creación del BackEnd 🛠️

Para estructurar el proyecto, he creado tres directorios principales:

<p align="center">
  <img src="https://github.com/user-attachments/assets/e916e5bf-8d38-4d86-a635-407e6b78eadb" alt="image">
</p>

**Models:** Este directorio contiene los modelos de datos y las funciones principales que interactúan con la base de datos. Aquí se realizan las consultas y operaciones necesarias sobre los datos.

**Service:** En este directorio se definen los endpoints de la aplicación. Cada archivo maneja la validación de los datos de entrada y luego llama a las funciones de Models para ejecutar las acciones requeridas.

**Schema:** Aquí se definen los esquemas de los datos de entrada. Estos esquemas especifican el tipo de dato esperado y cualquier otra condición necesaria para garantizar la integridad de la información.

**Tests:** Este directorio contiene todos los tests necesarios para verificar las funcionalidades de los archivos en la carpeta models. Es importante aclarar que aquí se están probando las funciones internas del modelo de datos, no los endpoints de la API.

Dentro de los archivos del proyecto, se encuentran las siguientes entidades, que representan los elementos clave de la aplicación:

**Usuario Genérico:** Representa al usuario que usará la aplicación móvil.

**Administrador de Cine:** Persona responsable de administrar la información del cine, como datos, películas y horarios.

**Cine:** Entidad que representa el lugar donde se proyectan películas.

**Película:** Cada filme que se proyectará en un cine.

**Actividad:** Permite a los usuarios crear actividades para participar con otros usuarios.

**Reviews:** Reseñas que los usuarios pueden hacer sobre las películas.

Cada una de estas entidades tiene implementadas las instrucciones CRUD necesarias para su funcionamiento en la aplicación. Todas las funciones/endpointes han sido probados mediante Postman.

Además de los archivos en los directorios principales, también existen archivos de configuración importantes para la aplicación, como app.py, db.py y config.py.

El archivo app.py configura y ejecuta la aplicación Flask para la API de MovieBuster. Inicializa la app de Flask, configurando la URI de MongoDB y habilitando CORS para permitir conexiones desde diferentes dominios. Luego, conecta la aplicación con MongoDB mediante init_mongo y define la API usando flask_restx. Importa y registra múltiples servicios (como usuario_generico_service, cine_service, review_service, entre otros) a través de blueprints, organizando los endpoints según sus funciones. Finalmente, ejecuta la aplicación en el puerto 5000.

## ☢️ Tests ☢️

Para realizar estos tests, se han creado 47 pruebas que verifican las funciones básicas, su correcto funcionamiento y el manejo de errores. Se utiliza mocker, una herramienta que permite simular el comportamiento de componentes externos, como la base de datos, reemplazándolos por objetos simulados. Esto es útil para evitar dependencias reales con MongoDB, lo que agiliza los tests y permite probar funcionalidades específicas en aislamiento. Además, el uso de mocker mejora la fiabilidad de las pruebas al enfocarse exclusivamente en la lógica interna, sin interferencias de servicios externos o problemas de conexión.

Algunos de los tests implementados son:

test_insertar_usuario_generico: Este test verifica que un usuario genérico se cree correctamente en la base de datos simulada y confirma que el mensaje de éxito y el ID del usuario se devuelvan correctamente.

test_insertar_usuario_generico_fecha_invalida: En este caso, se prueba que el sistema genere un error cuando se intenta insertar un usuario con una fecha de nacimiento en un formato incorrecto, esperando un ValueError debido a la fecha inválida.

test_eliminar_usuario_generico: Verifica que un usuario existente pueda ser eliminado correctamente, asegurándose de que se devuelva un mensaje de confirmación de eliminación exitosa.

test_eliminar_usuario_no_encontrado: Este test confirma que el sistema maneje adecuadamente el intento de eliminar un usuario que no existe, generando un ValueError con el mensaje "Usuario no encontrado".

test_actualizar_usuario_sin_cambios: Comprueba que el sistema responda correctamente cuando se intenta actualizar un usuario sin realizar cambios, devolviendo un mensaje indicando que no se realizaron modificaciones.

test_actualizar_usuario_con_cambios: Verifica que la información de un usuario se actualice correctamente y que se devuelva un mensaje de éxito indicando que el usuario ha sido actualizado.

test_invitacion_actividad_id_inexistente: Prueba el caso en que se intenta invitar a un usuario a una actividad inexistente. Se espera que el sistema genere un ValueError con el mensaje "La actividad especificada no existe".

## 📖 Gestor de Tareas 📖

Para la gestión de tareas en el proyecto, se ha utilizado un archivo Makefile, el cual facilita la automatización de comandos. Este archivo incluye instrucciones específicas para instalar las dependencias necesarias y ejecutar los tests del proyecto de manera sencilla y uniforme.

```makefile
install:
    pip install -r requirements.txt

test:
    PYTHONPATH=src pytest --maxfail=1 --disable-warnings -v
```


Instalación de dependencias
```bash
make install
```

Ejecución de tests
```bash
make test
```

Elegí usar Makefile como gestor de tareas porque simplifica la organización de los comandos para instalar dependencias y ejecutar pruebas. Con make, puedo asegurar que las tareas se ejecuten de forma consistente en todos los entornos de desarrollo, incluyendo los de integración continua (CI).

## 📚 Biblioteca de Aserciones 📚

Pytest es un marco de pruebas fácil de usar para Python, diseñado para facilitar la escritura de pruebas pequeñas y escalables. Con una sintaxis intuitiva y soporte para muchos plugins.

Se ha utilizado pytest por los motivos mencionados anteriormente, ya que su facilidad de uso y capacidad para descubrir y ejecutar tests de forma eficiente lo convierten en una herramienta ideal para este proyecto. Además, como se comentó en el apartado de tests, el uso del plugin pytest-mock permite realizar simulaciones de funciones y objetos fácilmente. Esto resulta especialmente útil para probar la lógica de negocio, asegurando que cada componente funcione como se espera al simular dependencias externas sin necesidad de implementarlas directamente en los tests.

## 👨‍🔬 Marco de Pruebas 👨‍🔬

Se sigue usando pytest, que no solo sirve como biblioteca de aserciones, sino también como marco de prueba para ejecutar los tests. Con pytest, es fácil organizar y correr pruebas unitarias de manera rápida y eficiente. Además, su compatibilidad con herramientas de CI y sus plugins lo hacen muy práctico para manejar y ejecutar los tests en diferentes entornos.

<p align="center">
  <img src="https://github.com/user-attachments/assets/d618deaa-9ba4-444a-9b88-f059f9810531" alt="image">
</p>

## 🤞 Integración Continua Funcionando 🤞

La integración continua de este proyecto se realiza mediante **GitHub Actions**, que permite ejecutar automáticamente los tests cada vez que se hace un push o se crea un pull request en la rama principal. El archivo integracion.yml define el flujo de trabajo necesario para configurar el entorno de pruebas, instalar las dependencias y ejecutar los tests. A continuación, se muestra el contenido del archivo integracion.yml

```yaml
name: Integración Continua

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12.3'

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install dependencies
        run: make -C hito2/api install

      - name: Set PYTHONPATH and Run tests
        run: |
          export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
          pytest --maxfail=1 --disable-warnings -v
        working-directory: hito2/api
```

**Desencadenadores (on):** Este flujo de trabajo se activa en cada push o pull request a la rama main.

**Configuración del Entorno:** Utiliza ubuntu-latest como entorno de ejecución y establece Python en la versión 3.12.3.

**Instalación de Dependencias:** Usa make install para instalar las dependencias del proyecto desde requirements.txt.

**Ejecución de Tests:** Configura PYTHONPATH para que apunte al directorio src y ejecuta los tests usando pytest.

Se puede observar el correcto funcionamiento en la pestaña Actions del repositorio:

![image](https://github.com/user-attachments/assets/3460e400-8d8f-40aa-afe1-e74d5c8b9222)

![image](https://github.com/user-attachments/assets/567be14d-edc6-48f9-8b52-17bf52123a20)

