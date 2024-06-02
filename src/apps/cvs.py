import pandas as pd
import io


class CvsService:
    @staticmethod
    def get_photos_data(numbers: list[int], file_content: bytes) -> dict:
        # Преобразование байтового содержимого файла в объект StringIO для чтения pandas
        file_stream = io.StringIO(file_content.decode('utf-8'))
        # Загрузка CSV файла из потока, разделитель - точка с запятой, первая строка используется как заголовок
        df = pd.read_csv(file_stream, sep=';', header=0)

        # Фильтрация данных по ID, указанным в списке numbers
        filtered_df = df[df['Id'].isin(numbers)]
        # Возвращаем словарь с ID и соответствующими URL фотографий
        return {"IDs": filtered_df['Id'].to_list(), "Photos": filtered_df['Photo'].to_list()}

