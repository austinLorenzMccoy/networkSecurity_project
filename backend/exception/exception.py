import sys
from logging.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        self.line_number = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occurred in python script name [{0}] line number [{1}] with error message [{2}]".format(
            self.file_name, self.line_number, self.error_message)

if __name__ == "__main__":
    try:
        logger.info("This is a test log message")
        a = 1 / 0  # This will cause an exception
    except Exception as e:
        error = NetworkSecurityException(e, sys)
        logger.error(str(error))  # Log the error
