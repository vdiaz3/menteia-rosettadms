# RosettaDMS

La piedra Rosetta de los DMS automotrices: conecta a una marca con todos sus dealers sin importar el DMS que usen, sin APIs, sin modificar software legado y sin costo para el dealer.

- **Sitio:** https://rosettadms.menteia.com (droplet `rosettadms-web`, 167.71.109.119, nyc3)
- **Visión y arquitectura:** [docs/arquitectura.md](docs/arquitectura.md)

## Estructura
```
site/     Landing SaaS estática (HTML/CSS/JS sin build)
deploy/   nginx, cloud-init, auto-HTTPS y script de despliegue
docs/     Visión, arquitectura y roadmap del producto
```

## Despliegue
El droplet se aprovisionó con `deploy/cloud-init.generated.yaml` (nginx + sitio + certbot).
`auto-https.sh` corre cada 5 min por cron: cuando el registro DNS `rosettadms.menteia.com` apunte a la IP del droplet, emite el certificado de Let's Encrypt y activa la redirección a HTTPS.

Para actualizar el sitio desde una máquina con SSH:
```bash
./deploy/deploy.sh 167.71.109.119 ~/.ssh/<tu-llave>
```
El formulario de contacto abre un correo a `CONTACT_EMAIL` (definido en `site/index.html`).
