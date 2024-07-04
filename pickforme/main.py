import os
import pathlib
from pickforme.presentation.cli import PickForMeCmd
from pickforme.common.logger import logger

def main():
    """
    Main function for starting the PickForMe Tool.

    This function starts the PickForMe Tool by initializing the necessary attributes and establishing the database connection.
    It then runs the command loop to execute the commands provided by the user.

    Returns:
        None
    """
    logger.info('Starting PickForMe Tool')
    try:
        project_install_path = os.path.dirname(os.path.abspath(__file__))
        app_db_dir = os.path.join(project_install_path, 'app_database')
        pathlib.Path(app_db_dir).mkdir(parents=True, exist_ok=True)
        cli = PickForMeCmd()
        logger.info('starting CLI loop')
        cli.is_database_initialized = cli.utility_functions.chk_mstr_passwd_cfgrd()
        if cli.is_database_initialized:
            cli.current_application_level = 0
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Exiting PickForMe Tool. Goodbye!")
        logger.info("Keyboard interrupt. Exiting PickForMe Tool. Goodbye!")
    except Exception as e:
        logger.exception('An error occurred while running the CLI : %s', e)
        raise

if __name__ == '__main__':
    logger.info('Starting main function for the tool')
    main()
