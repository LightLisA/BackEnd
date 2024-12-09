from fastapi import APIRouter, UploadFile
import shutil
from app.tasks.tasks import process_picture

router = APIRouter(
    prefix="/images",
    tags=["Upload files"]
)


@router.post("/hotels")
async def add_hotel_images(name: int, file: UploadFile):
    image_path = f"app/frontend/static/images/{name}.webp"
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(image_path)
