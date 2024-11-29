# Diseño de microservicios

## 🤔 Justificación Técnica del Framework Elegido 🤔

Flask fue seleccionado como framework para este proyecto debido a su simplicidad, flexibilidad y eficiencia, cualidades que se alinean perfectamente con los objetivos del desarrollo. Su diseño ligero y modular permite construir microservicios altamente personalizables, asegurando una estructura clara y un diseño por capas que separa la lógica de negocio de las rutas de la API.

La extensa y bien organizada documentación de Flask facilita tanto el desarrollo como la resolución de problemas. Su enfoque minimalista permite implementar únicamente las funcionalidades necesarias, evitando sobrecargar la aplicación con características innecesarias.

## 🤖 Diseño de la API 🤖

El diseño de la API se estructura utilizando Blueprints, una funcionalidad nativa de Flask que permite dividir la aplicación en módulos independientes. Cada Blueprint representa una funcionalidad autónoma de la API, lo que no solo mejora la organización del código, sino que también facilita el mantenimiento y la escalabilidad del proyecto.

Esta división modular asegura que cada funcionalidad esté claramente definida y encapsulada, conectando directamente con las funcionalidades implementadas y testeadas en el hito anterior. De esta manera, se logra un diseño por capas que desacopla de forma efectiva la lógica de negocio de las rutas de la API, garantizando que las operaciones sean consistentes y coherentes en todo el sistema.

## 🗂️ Uso de logs 🗂️

En la API implementada se utilizó un sistema de logs basado en el módulo estándar logging de Python, configurado específicamente para registrar tanto las actividades relacionadas con las solicitudes HTTP como los eventos importantes del sistema.

Para el registro de las solicitudes HTTP, se emplearon manejadores de logs, incluyendo un RotatingFileHandler, que almacena los logs en un archivo llamado api_access.log. Este manejador está configurado para rotar los archivos automáticamente cuando alcanzan un tamaño de 1 MB, garantizando un manejo eficiente del almacenamiento y manteniendo los registros organizados.

El logger de werkzeug, que es la biblioteca utilizada por Flask para manejar solicitudes, fue personalizado para capturar los accesos a los endpoints de la API, proporcionando información detallada sobre las rutas accedidas, los códigos de estado HTTP generados y las direcciones IP de los clientes.

Al lanzar la API mostrará todas las llamadas que se realicen, esto se puede ver en api_access.log:

```
127.0.0.1 - - [29/Nov/2024 03:47:27] "GET /actividades/672fe01e1c4f4f114d6bc9cb HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2024 03:47:28] "GET /actividades/672fe01e1c4f4f114d6bc9cb HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2024 03:47:29] "GET /actividades/672fe01e1c4f4f114d6bc9cb HTTP/1.1" 200 -
```

## ☢️ Ejecución de Test ☢️

Los tests de los endpoints se realizan utilizando pytest y unittest.mock que es utilizado para crear mocks de las interacciones básicas con la base de datos y aislar las pruebas del entorno externo.

Los tests son organizados, como en el hito anterior, en las distintas entidades del proyecto. Y nuevamente se utilizan los mocks para simular las interacciones con la base de datos, permitiendo un entorno controlado que no afecte a la base de datoso real.

Las llamadas HTTP para probar los endpoints de la API se realizan utilizando el cliente de prueba que proporciona Flask. Este cliente permite simular solicitudes HTTP hacia la aplicación sin necesidad de ejecutarla en un servidor real. De esta manera, se garantiza un entorno controlado y reproducible para las pruebas.

Cada llamada HTTP se configura según el tipo de solicitud (como GET, POST, PUT, DELETE) y se acompaña de los datos necesarios en el caso de métodos que los requieran, como POST o PUT. El cliente envía la solicitud al endpoint correspondiente, y se analiza la respuesta recibida para verificar su corrección en cuanto a códigos de estado, estructura de datos y mensajes retornados.

Por ejemplo, el test para el endpoint POST /usuario_generico verifica que la creación de un nuevo usuario genérico se realice correctamente. Se utiliza el cliente de prueba de Flask para simular la llamada HTTP y un mock para evitar interacciones reales con la base de datos.

```
def test_crear_usuario_generico(client, mock_mongo):
    # Configuración del mock para simular la base de datos
    mock_mongo.usuarios_genericos.insert_one.return_value.inserted_id = "672fa7d59bb2e4ad65f9a1b7"
    
    # Cuerpo de la solicitud enviado al endpoint
    payload = {
        "nombre": "Alexander Endpoint",
        "nombre_usuario": "Alex_endpoint",
        "password": "contraseña123",
        "email": "alex@correo.com",
        "telefono": "12345678",
        "fecha_nac": "2000-09-25",
        "preferencias": "cine, teatro"
    }
    
    # Realización de la solicitud POST al endpoint
    response = client.post("/usuario_generico", json=payload)
    
    # Verificación del código de estado de la respuesta
    assert response.status_code == 200
    
    # Obtención de los datos retornados por el endpoint
    data = response.get_json()
    
    # Verificación de que el id retornado sea el esperado
    assert data["id"] == "672fa7d59bb2e4ad65f9a1b7"

```
Se puede comprobar en GitHub Actions que todo funciona correctamente, ya que este sistema de integración continua ejecuta automáticamente los tests definidos en el proyecto.
