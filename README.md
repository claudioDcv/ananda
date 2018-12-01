# INSTRUCCIONES

## Build de front 
- copiar los archivos desde maquina local a el servidor
scp -r ./build/build.zip   ananda@69.164.194.50:/home/ananda/ananda_project
unzip build.zip -d ananda_front


# Envs
- las credenciales se crean en un archivo llamado env.txt
- definir las siguientes propiedaes para Django
APP_KEY
DB_NAME
DB_USER
DB_PASSWORD
DB_SERVIDOR

## Actualizar django
sh ananda_project/reload.sh

## Reiniciar Server
sudo systemctl restart nginx

## Editar archivo de nginx
sudo nano /etc/nginx/sites-available/ananda_project

