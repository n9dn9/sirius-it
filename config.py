from dotenv import load_dotenv
import os

load_dotenv()


def create_sqlalchemy_link() -> str:
    PG_VARS = "PG_HOST", "PG_PORT", "PG_USER", "PG_PASSWORD", "PG_DBNAME"
    credentials = {var: os.environ.get(var) for var in PG_VARS}
    return (
        "postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/"
        "{PG_DBNAME}".format(**credentials)
    )


class Config:
    SQLALCHEMY_DATABASE_URI = create_sqlalchemy_link()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 mb
    UPLOAD_FOLDER = "static/uploads"
    ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]
