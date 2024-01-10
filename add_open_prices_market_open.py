from datetime import datetime
import time
import numpy as np
from yahoo_fin import stock_info
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):
    authenticator = IAMAuthenticator('ObS4zAIXYNIHz6Jd1VFLpe6vRM-Msa6U6zL9R-A6xFbE')

    service = CloudantV1(authenticator=authenticator)
    service.set_service_url('https://apikey-v2-1sze7al3kdvwa7kpyakvn6mo0w30iin2jkrf52u89ik:5a1100c37e8c1cb37325c60f56aa1763@b61bc075-d5fd-436b-a84d-e390752abb53-bluemix.cloudantnosqldb.appdomain.cloud')

    cur_date = str(datetime.now()).split()[0]
    response = service.post_all_docs(
        db='stock-to-find',
        include_docs=True,
    ).get_result()

    stocks = response['rows'][0]['doc']['equities']
    open = {}
    for stock in stocks:
        stock_data = stock_info.get_quote_table(stock)
        open[stock] = np.round(stock_data['Previous Close'], 2)
        time.sleep(0.2)
    open_prices = Document(
        open_prices=open
    )
    for a in range(8):
        try:
            res = service.put_document(
                db='day-open-prices',
                document=open_prices,
                doc_id='OPEN_PRICES',
            ).get_result()
            break
        except:
            res = {'error': 'Conflict 409'}
            continue
    return res
