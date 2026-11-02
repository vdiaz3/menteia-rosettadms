"""Builds the cloud-init for a fresh droplet: nginx + auto-HTTPS + a cron that pulls the site from GitHub.

After the droplet exists, publishing is just `git push` to main; the droplet picks it up within 5 minutes,
so droplets (and their Let's Encrypt certificates) don't need to be recreated for content changes.
"""
import base64, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b64 = lambda p: base64.b64encode(open(os.path.join(root, p), "rb").read()).decode()

print(f"""#cloud-config
package_update: true
packages: [nginx, certbot, python3-certbot-nginx, ufw, dnsutils, git]
write_files:
  - path: /etc/nginx/sites-available/rosettadms
    encoding: b64
    content: {b64("deploy/nginx.conf")}
  - path: /usr/local/bin/auto-https.sh
    encoding: b64
    permissions: '0755'
    content: {b64("deploy/auto-https.sh")}
  - path: /usr/local/bin/sync-site.sh
    encoding: b64
    permissions: '0755'
    content: {b64("deploy/sync-site.sh")}
  - path: /etc/cron.d/rosettadms
    content: |
      */2 * * * * root /usr/local/bin/auto-https.sh >> /var/log/auto-https.log 2>&1
      */5 * * * * root /usr/local/bin/sync-site.sh >> /var/log/sync-site.log 2>&1
runcmd:
  - /usr/local/bin/sync-site.sh
  - rm -rf /var/www/rosettadms && ln -s /opt/rosettadms/site /var/www/rosettadms
  - rm -f /etc/nginx/sites-enabled/default
  - ln -sf /etc/nginx/sites-available/rosettadms /etc/nginx/sites-enabled/rosettadms
  - ufw allow OpenSSH && ufw allow 'Nginx Full' && ufw --force enable
  - systemctl enable nginx && systemctl reload nginx
""")
