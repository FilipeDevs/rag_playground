from pydantic import BaseModel
from datetime import datetime


class FileUpload(BaseModel):
    name: str
    uploaded_at: datetime
    signature: str = None
    original_file_id: str = None
    is_original: bool = False
