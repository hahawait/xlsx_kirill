from fastapi import APIRouter, File, UploadFile, Response

from apps.app.service import Service

files_router = APIRouter(
    tags=["XLSX | CSV"],
)


@files_router.post("/get_photos")
async def get_sub_unsub_count(
    sheet_names: list[str] = ['Заявки 2024', 'Апрель24', 'Май24'],
    target_numbers_file: UploadFile = File(..., description="Файл в формате .txt с IDs"),
    brand_filters_file: UploadFile = File(..., description="Файл в формате .txt с названиями брендов"),
    xlsx_file: UploadFile = File(..., description="Файл в формате .xlsx"), 
    csv_file: UploadFile = File(..., description="Файл в формате .csv"),
):

    sheet_names_list = [name.strip() for name in sheet_names[0].split(',')]
    xlsx_content = await xlsx_file.read()
    cvs_content = await csv_file.read()
    target_numbers_content = await target_numbers_file.read()
    brand_filters_content = await brand_filters_file.read()

    # Преобразовать данные в списки
    target_numbers = [int(line) for line in target_numbers_content.decode().split("\n") if line.strip()]
    brand_filters = [line.strip() for line in brand_filters_content.decode().split("\n") if line.strip()]

    archive = Service().get_photos(xlsx_content, cvs_content, target_numbers, brand_filters, sheet_names_list)
    return Response(content=archive.getvalue(), media_type="application/zip", headers={"Content-Disposition": "attachment; filename=result.zip"})
