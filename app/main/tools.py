from uuid import uuid4
import boto
import os.path
from flask import current_app
from werkzeug import secure_filename

def s3_upload(source_file, acl='public-read'):
    source_filename = secure_filename(source_file.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension

    # Connect to S3
    conn = boto.connect_s3(current_app.config["S3_KEY"], current_app.config["S3_SECRET"])

    existing_buckets = [b.name for b in conn.get_all_buckets()]
    if current_app.config["S3_BUCKET"] not in existing_buckets:
        b = conn.create_bucket(current_app.config["S3_BUCKET"])
    else:
        b = conn.get_bucket(current_app.config["S3_BUCKET"])

    # Upload the File
    sml = b.new_key("/".join([current_app.config["S3_UPLOAD_DIRECTORY"], destination_filename]))
    sml.set_contents_from_string(source_file.read())

    # Set the file's permissions.
    sml.set_acl(acl)

    return source_filename, s3_url(destination_filename)

def s3_url(filename):
    return 'https://s3.amazonaws.com/' + '/'.join([current_app.config["S3_BUCKET"], current_app.config["S3_UPLOAD_DIRECTORY"], filename])