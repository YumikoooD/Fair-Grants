import logging
import pandas as pd
import sys
import numpy as np
from dotenv import dotenv_values
from sbdata.FlipsideApi import FlipsideApi
from sbutils import LoadData


config = dotenv_values(".env")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PATH_TO_TX_DATA = config.get("PATH_TO_TX_DATA")
FLIPSIDE_API_KEY = config.get("FLIPSIDE_API_KEY")

flipside_api = FlipsideApi(FLIPSIDE_API_KEY, max_address=200)


def extract_transactions(array_unique_address, chain='ethereum', extract_all=False):
    """
    list_network = ["ethereum", "polygon",
                        "arbitrum", "avalanche", "gnosis", "optimism"]
    """

    loader = LoadData.LoadData(PATH_TO_TX_DATA)
    list_files = loader.get_files_in_address(chain, array_unique_address)
    list_files = [str(f).replace('_tx.csv', '') for f in list_files]

    not_in = np.setdiff1d(array_unique_address, np.array(list_files))

    if extract_all:
        logger.info('Extracting all transactions')
        to_extract = array_unique_address
    else:
        logger.info('Extracting transactions not yet extracted')
        to_extract = not_in

    # extract transactions to the path
    logger.info('Extracting transactions, number of addresses: %d', len(to_extract))
    flipside_api.extract_transactions_net(PATH_TO_TX_DATA, to_extract, chain)
    logger.info("End mining transactions")


def get_token_prices(tokens_address):
    """
    retrieve pricing information for the given token symbols
    """
    logger.info("executing query: {}".format(sys._getframe().f_code.co_name))
    
    tokens_concatenated = ",".join(["'" + t + "'" for t in tokens_address])

    query_token_prices = '''
        SELECT
            DATE_TRUNC('DAY', HOUR) day,
            TOKEN_ADDRESS,
            MEDIAN(price) AS price_usd
        FROM
            ethereum.core.fact_hourly_token_prices
        WHERE
            TOKEN_ADDRESS IN (%s)
            AND DATE_TRUNC('DAY', HOUR) = DATE('2023-06-10')
        GROUP BY
            day,
            SYMBOL,
            TOKEN_ADDRESS;
     ''' % (tokens_concatenated)

    return flipside_api.execute_query(query_token_prices)


def get_pool_address(blockchain):

    label_query = '''
    SELECT ADDRESS, CREATOR, LABEL_TYPE, ADDRESS_NAME, PROJECT_NAME
    FROM crosschain.core.address_labels 
    WHERE BLOCKCHAIN=%s
    AND label_type = 'cex'
    ;''' % (blockchain)
    
    df_label = flipside_api.execute_query(label_query)

    return df_label


def get_toxic_address(blockchain):
    label_query = '''
        SELECT ADDRESS, CREATOR, LABEL_TYPE, ADDRESS_NAME, PROJECT_NAME
        FROM crosschain.core.address_labels 
        WHERE BLOCKCHAIN=%s
        AND LABEL_SUBTYPE = 'toxic'
        ;''' % (blockchain)
    df_toxic = flipside_api.execute_query(label_query)
    return df_toxic

def get_airdrop_master_address(blockchain):
    label_query = '''
        SELECT ADDRESS, CREATOR, LABEL_TYPE, ADDRESS_NAME, PROJECT_NAME
        FROM crosschain.core.address_labels 
        WHERE BLOCKCHAIN=%s
        AND LABEL_SUBTYPE = 'airdrop master'
        ;''' % (blockchain)
    df_airdrop_master = flipside_api.execute_query(label_query)
    return df_airdrop_master

def get_tornado_address(blockchain):
    label_query = '''
        SELECT DISTINCT PROJECT_NAME, ADDRESS
        FROM crosschain.core.address_labels 
        WHERE BLOCKCHAIN=%s
        AND PROJECT_NAME LIKE '%tornado%'
        ;
        ''' % (blockchain)
    df_tornado = flipside_api.execute_query(label_query)
    return df_tornado

def get_cex_addresses(blockchain):
    label_query = '''
        SELECT ADDRESS, CREATOR, LABEL_TYPE, ADDRESS_NAME, PROJECT_NAME
        FROM crosschain.core.address_labels 
        WHERE BLOCKCHAIN=%s
        AND label_type = 'cex'
        ;''' % (blockchain)
    df_cex = flipside_api.execute_query(label_query)
    return df_cex