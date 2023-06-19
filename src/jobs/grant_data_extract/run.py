import logging
import graph

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def run_job(lego_name):
    
    #print("Running job: " + lego_name)
    #logger.info("Running job: " + lego_name)
    graph.start_fetching_data()

run_job("grant_data_extract")