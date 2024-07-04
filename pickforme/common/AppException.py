import sys
from colorama import Fore, Style

from pickforme.common.logger import logger

class PickForMeException(Exception):
    def __init__(self, *args: object) -> None:
        """
        Initializes a new instance of the PickForMeException class.

        Args:
            *args (object): The positional and keyword arguments for the PickForMeException constructor.

        Returns:
            None
        """
        super().__init__(*args)
        error_message = "Error occurred during execution, Exiting PickForMe Tool. Goodbye!"
        logger.error(error_message)
        print(Fore.RED + error_message + Style.RESET_ALL)
        sys.exit(0)  