# Utilizar la imagen oficial de MongoDB
FROM mongo:6.0

# Configurar el directorio de trabajo para los datos de MongoDB
WORKDIR /data/db

# Exponer el puerto de MongoDB
EXPOSE 27017

# Comando para iniciar MongoDB sin opciones de SSL
CMD ["mongod", "--bind_ip_all", "--noauth"]