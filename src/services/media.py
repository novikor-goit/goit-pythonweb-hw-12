import cloudinary  # type: ignore[import-untyped]
import cloudinary.uploader  # type: ignore[import-untyped]
from cloudinary.utils import cloudinary_url  # type: ignore[import-untyped]
from fastapi import UploadFile

from src.conf.config import settings


class MediaStorage:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET.get_secret_value(),
        )

    @staticmethod
    def upload_file(file: UploadFile, username: str) -> str:
        public_id = f"RestApp/{username}"
        r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        src_url, _ = cloudinary_url(
            public_id,
            fetch_format="auto",
            quality="auto",
            width=500,
            height=500,
            crop="auto",
        )
        return src_url
