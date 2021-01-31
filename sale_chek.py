import requests
import json
from utils.db_api import Base
from loguru import logger

base = Base()

QIWI_TOKEN = 'cf8c9e9923b9165e221096c9e5b40998'
QIWI_ACCOUNT = '+79119009060'

def sale_chek_qiwi():
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
    parameters = {'rows': '50'}
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments', params=parameters)
    req = json.loads(h.text)
    print(req)
    indif = []
    com = Base().read_tasks('tasks')

    for i in range(len(req['data'])):
        if req['data'][i]['comment'] == f'{com[1]}':
            if req['data'][i]['sum']['amount'] == 100:
                indif.append(1)
                logger.info(indif)
                break

    return indif
