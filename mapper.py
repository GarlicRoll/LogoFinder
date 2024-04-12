import pandas as pd
import warnings


# Gets label from the image (from logo)
# Returns index of the place on the map

def mapper(label):
    Objacts_base = pd.read_csv('datasets/base.csv')
    NN_base = pd.read_csv('datasets/glebs_data.csv')
    DB = DataBase(Objacts_base, NN_base)

    index = DB.map(label)  # Coca-Cola ! mcdonald's ! KFC

    if index == -1:
        print("No data")

    return index


class KeyTypeValueError(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f'key must be {type(str)} not {type(self.key)}'


class DataBaseTypeValueError(Exception):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return f'{self.name} must be {pd.DataFrame}, not {type(self.data)}'


class DataBase(object):
    base = pd.DataFrame()
    NN_base = pd.DataFrame()

    def __init__(self, Objacts_base, NN_base):
        if not isinstance(Objacts_base, pd.DataFrame):
            raise DataBaseTypeValueError("Objacts_base", Objacts_base)

        if not isinstance(NN_base, pd.DataFrame):
            raise DataBaseTypeValueError("NN_base", NN_base)

        self.base = Objacts_base
        self.NN_base = NN_base

        if Objacts_base.empty:
            warnings.warn('Objacts_base is empty')

        if NN_base.empty:
            warnings.warn('NN_base is empty')

    def is_valid_key(self, key):

        if not isinstance(key, str):
            raise KeyTypeValueError(key)

        return True
    # reduction - вспомогательная функция для приведения ключа
    #             объекта к единой форме

    def reduction(self, key):
        key = key.lower()

        symbols = ["[", "'", "-", "–",
                   ":", ">", "’", "#",
                   "%", "<", ",", "+",
                   "²", "!", " ", ".",
                   "?", "&", "]", '"',
                   "(", ")"]

        for sym in symbols:
            key = key.replace(f"{sym}", '')

        if key and key[0].isalpha():
            key = key[0].upper() + key[1:]

        return key

    # map - функция, которая возвращает ключи объекта(-ов) на карте,
    #       соответствующие вводимому ключу
    #
    #     return | (if coordinates=False) Одномерный список или строку, с
    #               уникальными ключами объектов;
    #               ['string', ...] / 'string'
    #            | (if coordinates=True) Двумерный или одномерный список, с
    #               ключами объектов и координатами;
    #               [[lat, lon, key], ...] или [lat, lon, key]
    #            | -1, если объект не был найден
    #
    #       > key         - (string) ключ, для поиска объекта
    #       > coordinates - (Bool) default: False; Флаг для вывода координат
    #                       объектов

    def map(self, key, coordinates=False):

        if not self.is_valid_key(key):
            print("Invalid key")
            return -1

        key = self.reduction(key)

        if self.NN_base['name'].isin([f'{key}']).any():
            if self.base['name'].isin([f'{key}']).any():

                fields = self.base[self.base['name'] == f'{key}']

                if coordinates:
                    fields = fields[['lat', 'lon', 'name']]
                    result = fields.values.tolist()
                else:
                    result = [key]

                return result

            else:
                object_type = self.NN_base[self.NN_base['name'] == f'{key}']['type'].values[0]
                fields = self.base[self.base['type'] == f'{object_type}']
                if coordinates:
                    fields = fields[['lat', 'lon', 'name']]
                    result = fields.values.tolist()
                else:
                    result = list(fields['name'].unique())
                    # result = fields.values.tolist()

                return result

        else:
            print(f"Значение {key} не найдено")
            return -1

if __name__ == '__main__':
    print(mapper("Mcdonalds"))
    print(mapper("Cocacolazero"))