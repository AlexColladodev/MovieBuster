# ℹ️ Descripción de la Aplicaciónℹ ℹ️

Como se ha descrito en el [README](../README.md), se desarrollará una aplicación móvil pensada para los amantes del cine, que les permitirá conectar con otros que comparten sus mismos gustos en géneros cinematográficos. Podrán organizarse para ver películas tanto en el cine como en casa, convirtiendo la app en una red social perfecta para quienes disfrutan de la compañía al ver una buena película.

## ⚙️ Funcionalidades de la Aplicación ⚙️

1. Poder encontrar los cines cercanos, con su cartelera y horarios.
2. Los cines pueden incluir y eliminar películas de su cartelera, así como editar los horarios de las que estén actualmente
3. Organización de grupos con amigos, ya sea para ir al cine o para ver una película en casa de alguien.
4. Especificar los géneros preferidos por el usuario para personalizar la recomendación de películas en la aplicación.
5. Cada película tendrá un sistema de reseñas donde los usuarios pueden escribir su experiencia con esa película.

## 🎯 Objetivo 🎯

El objetivo principal de la aplicación es proporcionar una herramienta que ayude al usuario a conectar con personas con gustos similares en el cine y organizar quedadas fácilmente, ya sea para ver películas en el cine o en casa, mejorando así la experiencia de compartir el cine de una manera social y personalizada.

## 👤 Usuarios 👤

La aplicación solo admitirá ser usada por usuarios registrados en el sistema. La aplicación tendrá **dos** usuarios principales:

**Usuarios genéricos:** Estos son los usuarios principales de la aplicación, las personas normales que buscan un sitio para compartir el ver una película. Los usuarios genéricos pueden:
1. Consultar la información de cines y carteleras.
2. Crear actividades, como por ejemplo, ir al cine a ver una película.
3. Crear "cine en casa", es decir, invitar a otros usuarios a casa a ver una película

**Administradores de Cine:** Estos son los usuarios que se encargan de mantener la información del cine actualizada, estos usuarios pueden gestionar (Crear, eliminar y editar) una película que se emitirá en un cine.

Como se ha descrito anteriormente, ambos tipos de usuarios deben autenticarse para utilizar la aplicación.

## 👨‍💻 Tecnologías 👨‍💻

 Para el desarrollo de la aplicación móvil, se ha optará por una arquitectura cliente-servidor basada en una arquitectura orientada a servicios (SOA) debido a su capacidad para facilitar la comunicación entre el servidor y la aplicación móvil. La API, desarrollada en **Python y Flask**, maneja las solicitudes del cliente. Los usuarios realizan peticiones desde la aplicación móvil  al servidor, y este responde con la información solicitada.

Para almacenar los datos, se utilizará MongoDB, que es una base de datos NoSQL que trabaja con documentos en formato JSON. Para la comunicación con la API esta estructura de datos es la adecuada.

Por parte del frontend, se intentará realizar una interfaz utilizando React Native.

