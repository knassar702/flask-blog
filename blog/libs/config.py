#!/usr/bin/env python3
from secrets import token_urlsafe
# Config
SECRET_KEY = token_urlsafe(50)
MYSQL_USER = 'admin'
MYSQL_PASSWORD = 'password'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'website'
UPLOAD_FOLDER = 'blog/static/image/'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024