"""Service for handling file uploads and deletions using Cloudflare R2 storage."""

import os
from datetime import datetime

import requests
from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.utils import get_config


class R2UploadError(Exception):
    """Custom exception for R2 upload errors."""


class R2DeleteError(Exception):
    """Custom exception for R2 delete errors."""


class R2Service:
    """Service class for managing file operations with Cloudflare R2 storage."""

    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # Allowed file types
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}

    def __init__(self) -> None:
        """Initialize R2 service with Cloudflare credentials."""
        self.account_id = get_config("CLOUDFLARE", "ACCOUNT_ID")
        self.bucket = get_config("CLOUDFLARE", "R2_BUCKET_NAME")
        self.token = get_config("CLOUDFLARE", "API_TOKEN")
        self.public_url = get_config("CLOUDFLARE", "R2_PUBLIC_URL")

        # Validate configuration
        if not all([self.account_id, self.bucket, self.token, self.public_url]):
            current_app.logger.error("Missing required Cloudflare configuration")
            raise R2UploadError("Missing required Cloudflare configuration")

        current_app.logger.debug(f"Initialized R2Service with bucket: {self.bucket}")

    def _validate_file(self, file: FileStorage) -> None:
        """
        Validate file before upload.

        Args:
            file: The file to validate

        Raises:
            R2UploadError: If validation fails
        """
        if not file:
            raise R2UploadError("No file provided")

        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)

        if size > self.MAX_FILE_SIZE:
            raise R2UploadError(
                f"File size exceeds maximum limit of {self.MAX_FILE_SIZE/1024/1024}MB"
            )

        # Check file extension
        filename = file.filename or ""
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
        if ext not in self.ALLOWED_EXTENSIONS:
            raise R2UploadError(
                f"File type '{ext}' not allowed. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )

    def _generate_key(self, file: FileStorage, folder: str) -> str:
        """
        Generate a unique and secure key for the file.

        Args:
            file: The file to generate a key for
            folder: The folder to store the file in

        Returns:
            str: The generated key
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = file.filename or "unnamed_file"
        secure_name = secure_filename(filename)
        return f"{folder}/{timestamp}_{secure_name}"

    def upload_file(self, file: FileStorage, folder: str = "images") -> str:
        """
        Upload a file to R2 using direct PUT request.

        Args:
            file: The file to upload
            folder: The folder to upload to within the bucket

        Returns:
            str: The public URL of the uploaded file

        Raises:
            R2UploadError: If upload fails
        """
        try:
            self._validate_file(file)
            key = self._generate_key(file, folder)

            # Direct PUT to R2 bucket
            upload_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/r2/buckets/{self.bucket}/objects/{key}"
            current_app.logger.debug(f"Uploading file to: {upload_url}")

            # Read file data
            file_data = file.read()
            file.seek(0)  # Reset file pointer

            # Upload headers
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": file.content_type or "application/octet-stream",
            }

            # Make the PUT request
            response = requests.put(
                upload_url,
                headers=headers,
                data=file_data,
                timeout=30,
            )

            if response.status_code != 200:
                error_msg = response.json().get("errors", ["Unknown error"])[0]
                current_app.logger.error(f"R2 upload failed: {error_msg}")
                raise R2UploadError(f"Upload failed: {error_msg}")

            image_url = f"{self.public_url}/{key}"
            return image_url

        except requests.RequestException as e:
            current_app.logger.error(f"R2 upload error: {str(e)}", exc_info=True)
            raise R2UploadError(f"Failed to upload file: {str(e)}") from e
        except Exception as e:
            current_app.logger.error(
                f"Unexpected error during upload: {str(e)}", exc_info=True
            )
            raise R2UploadError(f"Unexpected error during upload: {str(e)}") from e

    def delete_file(self, url: str) -> bool:
        """
        Delete a file from R2 using its URL.

        Args:
            url: The public URL of the file to delete

        Returns:
            bool: True if deletion was successful

        Raises:
            R2DeleteError: If deletion fails
        """
        try:
            # Extract key from URL
            key = url.replace(f"{self.public_url}/", "")
            if not key or key == url:
                raise R2DeleteError("Could not extract valid key from URL")

            delete_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/r2/buckets/{self.bucket}/objects/{key}"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }

            response = requests.delete(delete_url, headers=headers, timeout=30)

            if response.status_code != 200:
                error_msg = response.json().get("errors", ["Unknown error"])[0]
                current_app.logger.error(f"R2 delete failed: {error_msg}")
                raise R2DeleteError(f"Delete failed: {error_msg}")

            return True

        except requests.RequestException as e:
            current_app.logger.error(f"R2 delete error: {str(e)}", exc_info=True)
            raise R2DeleteError(f"Failed to delete file: {str(e)}") from e
        except Exception as e:
            current_app.logger.error(
                f"Unexpected error during deletion: {str(e)}", exc_info=True
            )
            raise R2DeleteError(f"Unexpected error during deletion: {str(e)}") from e
