import os
from pathlib import Path
import numpy as np
import pandas as pd

from sbdata.FlipsideApi import FlipsideApi
from sblegos.TransactionAnalyser import TransactionAnalyser as txa
from sbutils import LoadData

config = dotenv_values(".env")
PATH_TO_TX_DATA = config.get("PATH_TO_TX_DATA")
FLIPSIDE_API_KEY = config.get("FLIPSIDE_API_KEY")


def extract_transaction_features(array_unique_address):
    # Load data
    data_loader = LoadData.LoadData(PATH_TO_TX_DATA)
    df_tx = data_loader.create_df_tx('ethereum', array_unique_address)

    df_tx.EOA.nunique()

    tx_analyser = txa(df_tx, df_address=pd.DataFrame(np.intersect1d(df_tx.EOA.unique(), array_unique_address), columns=['address']))

    df_matching_address = pd.DataFrame(df_tx.EOA.unique(), columns=["address"])

    df_matching_address['seed_same_naive'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_same_seed_naive(x))
    df_matching_address['seed_same'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_same_seed(x))
    df_matching_address['seed_suspicious'] = df_matching_address.loc[:, 'seed_same_naive'].ne(df_matching_address.loc[:, 'seed_same'])
    df_matching_address['less_5_tx'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_less_than_n_transactions(x, 5))
    df_matching_address['less_10_tx'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_less_than_n_transactions(x, 10))
    df_matching_address['interacted_other_ctbt'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.has_interacted_with_other_contributor(x))
    df_matching_address['number_transaction'] = df_matching_address.loc[:, 'address'].apply(lambda x : get_number_transaction(x, tx_analyser))
    df_matching_address['unique_address'] = df_matching_address.loc[:, 'address'].apply(lambda x : get_unique_address(x, tx_analyser))
    df_matching_address['time_first_transaction'] = df_matching_address.loc[:, 'address'].apply(lambda x : get_time_first_transaction(x, tx_analyser))
    df_matching_address['time_last_transaction'] = df_matching_address.loc[:, 'address'].apply(lambda x : get_time_last_transaction(x, tx_analyser))
    # df_matching_address['transaction_similitude'] = df_matching_address.loc[:, 'address'].apply(lambda x : tx_analyser.transaction_similitude_pylcs(x))

    return df_matching_address

def get_number_transaction(address, tx_analyser):
    df_address = tx_analyser.gb_EOA_sorted.get(address)
    return df_address.shape[0]


def get_unique_address(address, tx_analyser):
    df_address = tx_analyser.gb_EOA_sorted.get(address)
    unique_address = np.unique(np.concatenate([df_address["from_address"].values, df_address["to_address"].values]))
    return len(unique_address - 1)

def get_time_first_transaction(address, tx_analyser):
    df_address = tx_analyser.gb_EOA_sorted.get(address)
    return df_address["block_timestamp"].values[0]

def get_time_last_transaction(address, tx_analyser):
    df_address = tx_analyser.gb_EOA_sorted.get(address)
    return df_address["block_timestamp"].values[-1]

