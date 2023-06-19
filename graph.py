import requests
from pprint import pprint
import mysql.connector
import datetime
from src.data.fetch import fetch_flipside
import pandas as pd
import logging


def store_value(value):
    filename = '.value'
    
    with open(filename, 'w') as file:
        file.write(str(value))

def get_value():
    filename = '.value'
    with open(filename, "r") as file:
        value = file.read()
    return int(value)

def getTokenInfo(tokens_address):
    return fetch_flipside.get_token_prices(tokens_address)

def insert_record(record, token_price, cursor, connection, logger):
    insert_query = """
    INSERT INTO votes (id, token, amount, voter, applicationIndex, blockTimestamp, blockNumber, grantAddress, projectId, roundAddress, transactionHash, amountUsd)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    logger.info("Inserting SubGraph record in database...")
    dt = datetime.datetime.fromtimestamp(int(record['blockTimestamp']))
    formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
    amount = int(record['amount'])
    values = (
        record['id'],
        record['token'],
        amount,
        record['voter'],
        record['applicationIndex'],
        formatted_timestamp,
        record['blockNumber'],
        record['grantAddress'],
        record['projectId'],
        record['roundAddress'],
        record['transactionHash'],
        amount * float(token_price[0])
    )
    cursor.execute(insert_query, values)
    connection.commit()


# function to use requests.post to make an API call to the subgraph url
def run_query(query, API_KEY):
    # endpoint where you are making the request
    request = requests.post('https://api.studio.thegraph.com/query/48157/test-fairtrade/0.0.1',
                            json={'query': query},
                            headers={'Authorization': f'Bearer {API_KEY}'})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed. Return code is {}. {}'.format(request.status_code, query))

def get_contract_data(cursor, connection, API_KEY, logger):
    skip_amount = get_value()

    query = """
    {
    voteds(first: 5, skip: %s, where: {token_not_contains: "0x0000"}) {
    id
    token
    amount
    voter
    applicationIndex
    blockTimestamp
    blockNumber
    grantAddress
    projectId
    roundAddress
    transactionHash
        }
    }
    """ % skip_amount
    logger.info("Query request for SubGraph API: %s", query)
    result = run_query(query, API_KEY)
    tokens = [item['token'] for item in result['data']['voteds']]
    logger.info("Getting tokens values using SubGraph datas: %s", tokens)
    token_price = getTokenInfo(tokens)
    for record in result['data']['voteds']:
        insert_record(record, token_price['price_usd'].tolist(), cursor, connection, logger)
    store_value(skip_amount + 5)
    logger.info("Storing block index: %s", skip_amount + 5)

def start_fetching_data():
    API_KEY = "dec9470f53568776e096e1223bb00400"
    print("Fetching data...")
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="epytodo",
        database="graph"
    )

    cursor = connection.cursor()

    get_contract_data(cursor, connection, API_KEY, logger)

    query = "SELECT amountUsd, token FROM votes"
    cursor.execute(query)
    rows = cursor.fetchall() 
    for row in rows:
        print(row)

    cursor.close()
    connection.close()

#start_fetching_data()