# ✈️ Despliegue de la aplicación en un PaaS ✈️

## ✔️ Justificación PaaS utilizado ✔️

Para el despliegue del proyecto, se optó por las siguientes plataformas como servicios (PaaS), seleccionadas por su facilidad de uso y su disponibilidad gratuita:

1. **Render**  
   - Elegido para el despliegue de la API gracias a su soporte nativo para Docker, lo que permitió reutilizar el `Dockerfile` configurado previamente.  
   - Aunque se consideró el uso de Fly.io, se descartó debido a la necesidad de proporcionar información de tarjeta de crédito incluso para su plan gratuito.

2. **MongoDB Atlas**  
   - Utilizado para desplegar la base de datos, la cual está inicialmente vacía y se llenará progresivamente con datos relevantes.  
   - Se decidió usar MongoDB Atlas para evitar problemas relacionados con el despliegue de la base de datos mediante un contenedor Docker en Render, que generaba errores relacionados con SSL.

![image](https://github.com/user-attachments/assets/903007fd-21b3-4dd1-8d6c-c713136a1769)

## ✔️ Descripción PaaS ✔️

En Render, tras crear una cuenta, hay que seleccionar la opción New Web Service. Render ofrece integración con GitHub, lo que permite conectar directamente tu cuenta y elegir el repositorio donde se encuentra alojado el proyecto.

![image](https://github.com/user-attachments/assets/a896c9f9-5620-479d-b9d3-31fde39022c0)

### Configuración Render

1. **Configuración de variables de entorno**
   - Es necesario configurar las variables de entorno para que el servicio funcione correctamente. En este caso, se configuraron las siguientes:
     ```plaintext
     PYTHONPATH = src
     MONGO_URI = mongodb+srv://AlexColladodev:Alex-25-MovieBuster@moviebuster.lezf0.mongodb.net/MovieBuster?retryWrites=true&w=majority&appName=MovieBuster
     ```
     - **PYTHONPATH**: Define la ruta al directorio principal del código.
     - **MONGO_URI**: Es la URI de conexión a la base de datos en MongoDB Atlas. Esta variable es necesaria para la comunicación con la base de datos.

2. **Selección del servidor**
   - Elige la ubicación del servidor donde se desplegará el servicio. En este caso, se seleccionó **Frankfurt EU**.

3. **Despliegue del servicio web**
   - Con la configuración lista, Render procederá a desplegar el servicio web.
  
![image](https://github.com/user-attachments/assets/57169d8d-aab8-4bc7-8b7f-e672a475139c)

---

### Configuración de la base de datos en MongoDB Atlas

Debido a problemas al intentar desplegar la base de datos mediante un contenedor Docker (errores relacionados con SSL), se optó por usar **MongoDB Atlas** para alojar la base de datos. Los pasos realizados fueron:

1. Accede a [MongoDB Atlas](https://www.mongodb.com/atlas) y crea una cuenta (si no tienes una).
2. Crea un nuevo **cluster** y una base de datos dentro del mismo.
3. Obtén la URI de conexión:
   - En el panel de MongoDB Atlas, selecciona **Connect** -> **Drivers**.
   - Sigue las instrucciones proporcionadas para obtener el URI necesario para conectarte.
  
![image](https://github.com/user-attachments/assets/c2b9703c-0035-48a0-89d4-11c95e6eca85)

Con esta URI configurada en la variable de entorno `MONGO_URI`, la aplicación puede comunicarse correctamente con la base de datos.

## Descripción de la configuración para el despliegue automático

Como se ha mencionado, Render se conecta directamente con GitHub. Existe la opción de configurar el servicio de manera que, cada vez que se realice un push o un cambio en la rama `main` (o en cualquier rama seleccionada), se realice automáticamente un nuevo despliegue con el código actualizado.

![image](https://github.com/user-attachments/assets/472fb797-d219-4e28-973e-8445e806651b)

Se puede observar que luego de haber hecho un cambio en el commit el Log del despliegue me aparece:

![image](https://github.com/user-attachments/assets/38011d13-ac91-45e5-96aa-75104c40890f)

## Funcionamiento Correcto

Se prueban algunos endpoints para la configuración correcta del despliegue tanto de la API como de la base de datos. Se prueba mediante POSTMAN los siguientes endpoints:

![image](https://github.com/user-attachments/assets/f5b7744c-3d61-4204-bd78-fbca8bf3da77)

![image](https://github.com/user-attachments/assets/78b89fe9-33e0-4000-91b2-ba08e2d625f0)

![image](https://github.com/user-attachments/assets/dc695bd7-afd3-4a20-81d0-c1136aba31ff)

