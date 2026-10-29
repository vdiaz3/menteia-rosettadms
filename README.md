# RosettaDMS

La piedra Rosetta de los DMS automotrices: conecta a una marca con todos sus dealers sin importar el DMS que usen, sin APIs, sin modificar software legado y sin costo para el dealer.

- **Sitio:** https://rosettadms.menteia.com (droplet `rosettadms-web-2`, IP reservada 45.55.123.185, nyc3)
- **Visión y arquitectura:** [docs/arquitectura.md](docs/arquitectura.md)

## Estructura
```
site/     Landing SaaS estática (HTML/CSS/JS sin build)
deploy/   nginx, cloud-init, auto-HTTPS y script de despliegue
docs/     Visión, arquitectura y roadmap del producto
```

## Despliegue
Cada versión se despliega en un droplet nuevo creado con `python3 deploy/build-cloud-init.py` como user_data (nginx + sitio + certbot), y se le mueve la IP reservada 45.55.123.185, así el DNS nunca cambia.
`auto-https.sh` corre cada 2 min por cron: cuando el registro DNS `rosettadms.menteia.com` apunte a la IP del droplet, emite el certificado de Let's Encrypt y activa la redirección a HTTPS.

Para actualizar el sitio desde una máquina con SSH:
```bash
./deploy/deploy.sh 45.55.123.185 ~/.ssh/<tu-llave>
```
El formulario de contacto abre un correo a `CONTACT_EMAIL` (definido en `site/index.html`).
