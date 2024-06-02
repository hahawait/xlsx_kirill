import io, os
import shutil
import zipfile

from apps.cvs import CvsService
from apps.xlsx import ExcelService
from apps.file import download_and_extract_archives

class Service:
    def __init__(self):
        self.cvs_service = CvsService()
        self.excel_service = ExcelService()

    def get_photos(self, xlsx_file, cvs_file, target_numbers: list[int], brand_filters: list[str], sheet_names: list[str]):
        for sheet_name in sheet_names:
            numbers = self.excel_service.get_numbers(xlsx_file, sheet_name, brand_filters)
            for key, value in numbers.items():
                if len(value) > 0:
                    target = [num for num in target_numbers if num in value]
                    photo_urls = self.cvs_service.get_photos_data(target, cvs_file)
                    download_and_extract_archives(photo_urls['Photos'], photo_urls['IDs'], f'{sheet_name} {key}')

        return self.create_final_archive()

    def create_final_archive(self):
        memory_zip = io.BytesIO()
        with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for foldername, _, filenames in os.walk('result'):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, 'result')
                    zf.write(filepath, arcname=arcname)
        # Удаление папки result и её содержимого
        shutil.rmtree('result')
        memory_zip.seek(0)
        return memory_zip