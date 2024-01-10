FROM ibmfunctions/action-python-v3.7

RUN pip install --upgrade pip

RUN pip3 install python-dotenv ibmcloudant yahoo_fin