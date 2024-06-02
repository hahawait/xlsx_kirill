import pandas as pd
from io import BytesIO

class ExcelService:
    @staticmethod
    def get_numbers(filename: str, sheet_name: str, brand_filters: list[str]) -> dict[str, list[int]]:
        if isinstance(filename, bytes):
            filename = BytesIO(filename)

        # Загрузка файла Excel с указанием индексов колонок
        df = pd.read_excel(filename, sheet_name=sheet_name, header=None, skiprows=1)
        # Отфильтровать записи, у которых в столбце 8 (Дата доставки) стоит именно дата и значение в столбце 4 соответствует одному из указанных брендов
        df_filtered = df[pd.to_datetime(df[8], errors='coerce').notnull() & df[4].isin(brand_filters)].copy()

        # Определение группы по значению в столбце 2 (Название ИМ)
        def define_group(name):
            if 'ozon' in name.lower():
                return 'OZON'
            elif 'wildberries' in name.lower():
                return 'WB'
            else:
                return 'Другое'

        # Применение функции для определения группы без предупреждения SettingWithCopyWarning
        df_filtered.loc[:, 'Группа'] = df_filtered[2].apply(define_group)

        # Группировка по созданной группе и получение списков значений из столбца 1 (WR), преобразование значений в целые числа
        ozon_list = df_filtered[df_filtered['Группа'] == 'OZON'][1].astype(int, errors='ignore').tolist()
        wb_list = df_filtered[df_filtered['Группа'] == 'WB'][1].astype(int, errors='ignore').tolist()
        other_list = df_filtered[df_filtered['Группа'] == 'Другое'][1].astype(int, errors='ignore').tolist()

        # ozon_list = df_filtered[df_filtered['Группа'] == 'OZON'][1].apply(int).tolist()
        # wb_list = df_filtered[df_filtered['Группа'] == 'WB'][1].apply(int).tolist()
        # other_list = df_filtered[df_filtered['Группа'] == 'Другое'][1].apply(int).tolist()

        return {'OZON': ozon_list, 'WB': wb_list, 'Другое': other_list}