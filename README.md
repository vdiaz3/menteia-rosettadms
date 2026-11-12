# RosettaDMS

La piedra Rosetta de los DMS automotrices: conecta a una marca con todos sus dealers sin importar el DMS que usen, sin APIs, sin modificar software legado y sin costo para el dealer.

- **Sitio:** https://rosettadms.menteia.com (droplet `rosettadms-web-5`, IP reservada 45.55.123.185, nyc3)
- **Visión y arquitectura:** [docs/arquitectura.md](docs/arquitectura.md)

## Estructura
```
site/     Landing SaaS estática (HTML/CSS/JS sin build); es lo que sirve nginx
media/    Video de intro (30 s) y su animación fuente
brand/    Logos en alta resolución
deploy/   cloud-init, nginx, auto-HTTPS y sincronización con GitHub
docs/     Arquitectura y correos de presentación
```

## Publicar cambios
Basta con hacer push a `main`. El droplet ejecuta `deploy/sync-site.sh` cada 5 minutos, trae la última versión del repositorio y nginx sirve `site/` directamente.

## Crear un servidor nuevo
Solo hace falta si se pierde el droplet. Se crea con `python3 deploy/build-cloud-init.py` como user_data y se le asigna la IP reservada 45.55.123.185, a la que apunta el DNS.
`auto-https.sh` corre cada 2 min: cuando `rosettadms.menteia.com` resuelve a la IP del droplet, emite el certificado de Let's Encrypt y activa la redirección a HTTPS. Let's Encrypt permite 5 certificados por semana para el mismo dominio, así que conviene no recrear el servidor seguido.

El formulario de contacto abre un correo a `CONTACT_EMAIL` (definido en `site/index.html`).
El video del intro se sirve desde jsDelivr a partir de este repositorio público.
