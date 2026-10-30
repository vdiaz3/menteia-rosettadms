"""Uploads the intro videos to DigitalOcean Spaces and prints their public URLs.

Reads SPACES_KEY and SPACES_SECRET from the environment (never commit them).
Usage: python3 deploy/upload-media.py [bucket] [region]
"""
import os, sys
import boto3

bucket = sys.argv[1] if len(sys.argv) > 1 else "rosettadms"
region = sys.argv[2] if len(sys.argv) > 2 else "nyc3"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

s3 = boto3.client("s3", region_name=region, endpoint_url=f"https://{region}.digitaloceanspaces.com",
                  aws_access_key_id=os.environ["SPACES_KEY"], aws_secret_access_key=os.environ["SPACES_SECRET"])

if bucket not in [b["Name"] for b in s3.list_buckets().get("Buckets", [])]:
    s3.create_bucket(Bucket=bucket)

files = {
    "media/rosettadms-intro-30s.mp4": "video/mp4",
    "media/intro-720.mp4": "video/mp4",
    "media/intro-720.webm": "video/webm",
    "media/intro-poster.jpg": "image/jpeg",
}
for rel, ctype in files.items():
    key = "intro/" + os.path.basename(rel)
    s3.upload_file(os.path.join(root, rel), bucket, key,
                   ExtraArgs={"ACL": "public-read", "ContentType": ctype, "CacheControl": "public, max-age=31536000"})
    print(f"https://{bucket}.{region}.cdn.digitaloceanspaces.com/{key}")
