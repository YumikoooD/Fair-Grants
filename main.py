import logging
import importlib
import importlib.util
import yaml

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_path = 'src/jobs/grant_data_extract/'
function_name = 'run_job'

spec=importlib.util.spec_from_file_location("run", "src/jobs/grant_data_extract/run.py")
module = importlib.util.module_from_spec(spec)
#function = getattr(module, function_name)
#result = function()

# convention to call/write functions
RUN_MODULE = "jobs.{}.run"  # placeholder for the job name
RUN_METHOD = "run_job"

IO_MODULE = "jobs.{}.io"
IO_METHOD = "get_data"


def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


def main():
    config = load_config()

    for job_config in config["jobs"]:
        job_name = job_config['name']
        spec.loader.exec_module(module)
        #module = importlib.import_module(RUN_MODULE.format(job_name))
        #function = getattr(module, RUN_METHOD)
        #function(job_config['id'], job_config.get('inputs', []), job_config.get('params', {}))


if __name__ == "__main__":
    main()
