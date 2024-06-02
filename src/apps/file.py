import os
import zipfile
import requests

def download_and_extract_archives(photo_urls, ids, output_folder):
    output_folder = 'result/' + output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # folder_created = False

    for url, photo_id in zip(photo_urls, ids):
        id_folder = os.path.join(output_folder, str(photo_id))
        if not os.path.exists(id_folder):
            os.makedirs(id_folder)
        if isinstance(url, float):
            continue
        filename = url.split('/')[-1]
        r = requests.get(url)
        if r.status_code == 200:
            temp_zip_file = os.path.join(id_folder, filename)
            with open(temp_zip_file, 'wb') as f:
                f.write(r.content)
            with zipfile.ZipFile(temp_zip_file, 'r') as zip_ref:
                zip_ref.extractall(id_folder)
            os.remove(temp_zip_file)
            # folder_created = True
            print(f"Архив {filename} успешно скачан и распакован в папку {id_folder}.")
        else:
            print(f"Не удалось скачать архив {filename} по ссылке {url}.")

    # if folder_created:
    #     return True
    # else:
    #     os.rmdir(output_folder)
    #     return False