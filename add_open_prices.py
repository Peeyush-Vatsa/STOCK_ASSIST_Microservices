from datetime import datetime
import time
import numpy as np
from yahoo_fin import stock_info
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
authenticator = IAMAuthenticator('ObS4zAIXYNIHz6Jd1VFLpe6vRM-Msa6U6zL9R-A6xFbE')

service = CloudantV1(authenticator=authenticator)
service.set_service_url("https://apikey-v2-1sze7al3kdvwa7kpyakvn6mo0w30iin2jkrf52u89ik:5a1100c37e8c1cb37325c60f56aa1763@b61bc075-d5fd-436b-a84d-e390752abb53-bluemix.cloudantnosqldb.appdomain.cloud")


def main(params):
    cur_date = str(datetime.now()).split()[0]
    response = service.post_all_docs(
        db='stock-to-find',
        include_docs=True,
    ).get_result()

    stocks = response['rows'][0]['doc']['equities']
    existing_open_response = service.post_all_docs(
        db='day-open-prices',
        include_docs=True
    ).get_result()
    rev = existing_open_response['rows'][0]['doc']['_rev']
    existing_open = existing_open_response['rows'][0]['doc']['open_prices']
    existing_open_keys = existing_open.keys()
    open = {}
    for stock in stocks:
        if stock in existing_open_keys:
            open[stock] = existing_open[stock]
            continue
        stock_data = stock_info.get_quote_table(stock)
        open[stock] = np.round(stock_data['Previous Close'], 2)
        time.sleep(0.2)
    open_prices = Document(
        open_prices=open
    )
    for a in range(8):
        try:
            res1 = service.delete_document(
                db='day-open-prices',
                doc_id='OPEN_PRICES',
                rev=rev,
            ).get_result()
            break
        except:
            res1 = {'Error': 'Not found 404'}
            time.sleep(0.1)
            continue

    for a in range(8):
        try:
            res2 = service.put_document(
                db='day-open-prices',
                document=open_prices,
                doc_id='OPEN_PRICES',
            ).get_result()
            break
        except:
            res2 = {'Error': 'Conflict 409'}
            time.sleep(1)
            continue

    return {'DELETE': res1 , 'PUT': res2}