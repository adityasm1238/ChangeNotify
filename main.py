import dotenv
import os

from app.utils.logger import config_logger
dotenv.load_dotenv()


from app.jobRunner.jobrunner import JobRunner
from app.jobs.visa import VisaDecisionJob


config_logger(
            {
                'ERROR_LOG_FILE': os.environ['ERROR_LOG_FILE'],
                'INFO_LOG_FILE': os.environ['INFO_LOG_FILE'],
                'DEBUG_LOG_FILE': os.environ['DEBUG_LOG_FILE'],
                'DISCORD_LOG_ERROR': os.environ['DISCORD_LOG_ERROR'],
                'DISCORD_LOG_SILENT': os.environ['DISCORD_LOG_SILENT']
            }
        )
jr = JobRunner()
jr.submit(VisaDecisionJob, 600)
jr.run()
