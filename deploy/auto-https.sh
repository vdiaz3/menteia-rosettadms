#!/bin/bash
# Runs every 5 min until DNS for the domain points at this droplet, then issues a Let's Encrypt cert once.
DOMAIN=rosettadms.menteia.com
[ -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ] && exit 0
MYIP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/public/0/ipv4/address)
DNSIP=$(dig +short A $DOMAIN @1.1.1.1 | tail -n1)
[ "$MYIP" = "$DNSIP" ] || exit 0
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect
