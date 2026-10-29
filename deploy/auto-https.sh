#!/bin/bash
# Runs by cron until DNS for the domain points at this droplet (own or reserved IP), then issues a Let's Encrypt cert once.
DOMAIN=rosettadms.menteia.com
[ -f /etc/letsencrypt/live/$DOMAIN/fullchain.pem ] && exit 0
MD=http://169.254.169.254/metadata/v1
MYIPS="$(curl -s $MD/interfaces/public/0/ipv4/address) $(curl -s $MD/reserved_ip/ipv4/ip_address)"
DNSIP=$(dig +short A $DOMAIN @1.1.1.1 | tail -n1)
[ -n "$DNSIP" ] && [[ " $MYIPS " == *" $DNSIP "* ]] || exit 0
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email --redirect
