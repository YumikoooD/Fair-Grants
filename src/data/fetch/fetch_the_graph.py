import logging
import os
import requests
import pandas as pd
from dotenv import dotenv_values


config = dotenv_values(".env")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

GRAPH_GITCOIN_GRANTS_URL = config.get("GRAPH_GITCOIN_GRANTS_URL")

def fetch_the_graph(grant_address, start_block):
    return
