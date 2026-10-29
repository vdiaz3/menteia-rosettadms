#!/bin/bash
# Usage: ./deploy/deploy.sh <droplet-ip> [ssh-key]
set -e
IP=$1; KEY=${2:-~/.ssh/rosettadms}
cd "$(dirname "$0")/.."
SSH="ssh -i $KEY -o StrictHostKeyChecking=accept-new root@$IP"
$SSH 'cloud-init status --wait >/dev/null; mkdir -p /var/www/rosettadms'
scp -i $KEY site/* root@$IP:/var/www/rosettadms/
scp -i $KEY deploy/nginx.conf root@$IP:/etc/nginx/sites-available/rosettadms
scp -i $KEY deploy/auto-https.sh root@$IP:/usr/local/bin/auto-https.sh
$SSH 'ln -sf /etc/nginx/sites-available/rosettadms /etc/nginx/sites-enabled/rosettadms; chmod +x /usr/local/bin/auto-https.sh;
  echo "*/5 * * * * root /usr/local/bin/auto-https.sh >> /var/log/auto-https.log 2>&1" > /etc/cron.d/auto-https;
  nginx -t && systemctl reload nginx'
echo "Deployed to http://$IP"
