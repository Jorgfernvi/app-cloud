# Usa la imagen oficial de swaggerapi/swagger-ui como base
FROM swaggerapi/swagger-ui

# Copia todos los archivos .yaml del directorio catalog al directorio /usr/share/nginx/html/swagger/
COPY ./catalog /usr/share/nginx/html/
# Configura la aplicación para usar el archivo de índice de catálo
