# -*- coding: utf-8 -*-
import shutil
import requests
import config
import os


def download_smile(url, full_file_name):
    response = requests.get(url, stream=True)
    with open(full_file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

# Самый дубовый вариант - качаем синхронно.
# Минусы - при первом запуске и отсутствии смайлов приложение
# ждет окончания загрузки. Если первую, самую тяжелую загрузку
# делать асинхронно, то в окне сообщений смайлы отобразиться 
# еще не смогут, придется делать развесистую схему с сигналами,
# чего пока не хочется.
def sync_smiles(smiles):
    if not os.path.exists(config.SMILES_DIR):
        os.makedirs(config.SMILES_DIR)

    for smile in smiles:
        url = smile['image']
        file_name = os.path.basename(url)
        full_file_name = os.path.join(config.SMILES_DIR, file_name)
        if os.path.isfile(full_file_name):
            continue
        download_smile(url, full_file_name)

