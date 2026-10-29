"""Builds a self-contained cloud-init (site + nginx + auto-HTTPS) for a fresh droplet."""
import base64, io, os, re, tarfile

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b64 = lambda p: base64.b64encode(open(os.path.join(root, p), "rb").read()).decode()

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as t:
    for f in sorted(os.listdir(os.path.join(root, "site"))):
        path = os.path.join(root, "site", f)
        if f.endswith(".html"):
            # user_data is capped at 64 KiB, so ship the page without indentation
            html = re.sub(r"\n[ \t]+", "\n", open(path, encoding="utf-8").read())
            html = re.sub(r"\s*([{};])\s*", r"\1", html.split("</style>")[0]) + "</style>" + html.split("</style>", 1)[1]
            data = html.encode()
            info = tarfile.TarInfo(f); info.size = len(data); info.mode = 0o644
            t.addfile(info, io.BytesIO(data))
        else:
            t.add(path, arcname=f)
site = base64.b64encode(buf.getvalue()).decode()

print(f"""#cloud-config
package_update: true
packages: [nginx, certbot, python3-certbot-nginx, ufw, dnsutils]
write_files:
  - path: /root/site.tgz
    encoding: b64
    content: {site}
  - path: /etc/nginx/sites-available/rosettadms
    encoding: b64
    content: {b64("deploy/nginx.conf")}
  - path: /usr/local/bin/auto-https.sh
    encoding: b64
    permissions: '0755'
    content: {b64("deploy/auto-https.sh")}
  - path: /etc/cron.d/auto-https
    content: "*/2 * * * * root /usr/local/bin/auto-https.sh >> /var/log/auto-https.log 2>&1\\n"
runcmd:
  - mkdir -p /var/www/rosettadms && tar xzf /root/site.tgz -C /var/www/rosettadms
  - rm -f /etc/nginx/sites-enabled/default
  - ln -sf /etc/nginx/sites-available/rosettadms /etc/nginx/sites-enabled/rosettadms
  - ufw allow OpenSSH && ufw allow 'Nginx Full' && ufw --force enable
  - systemctl enable nginx && systemctl reload nginx
""")
