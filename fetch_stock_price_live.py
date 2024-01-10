from yahoo_fin import stock_info
import time
from datetime import datetime
import numpy as np

from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('ObS4zAIXYNIHz6Jd1VFLpe6vRM-Msa6U6zL9R-A6xFbE')

service = CloudantV1(authenticator=authenticator)
service.set_service_url('https://apikey-v2-1sze7al3kdvwa7kpyakvn6mo0w30iin2jkrf52u89ik:5a1100c37e8c1cb37325c60f56aa1763@b61bc075-d5fd-436b-a84d-e390752abb53-bluemix.cloudantnosqldb.appdomain.cloud')
#Get stocks required from cloudant
def main(params):
    response = service.post_all_docs(
            db='stock-to-find',
            include_docs=True
        ).get_result()
    stocks = response['rows'][0]['doc']['equities']
    req_stocks = {}
    for stock in stocks:
        req_stocks[stock] = np.round(stock_info.get_live_price(stock),2)
        time.sleep(0.3)
    live_price = Document(
        price = req_stocks
    )
    curtime = datetime.now().strftime('%H:%M')
    res = service.put_document(
        db='day-stock-price',
        doc_id= curtime,
        document=live_price
    ).get_result()
    return res