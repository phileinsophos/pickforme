import pathlib
import hashlib
import sqlite3
import csv
from prettytable import PrettyTable
from getpass import getpass
from colorama import Fore, Style
from common.AppException import PickForMeException
from common import constants

from common.logger import logger
        
class UtilityFunctions:
    """
    UtilityFunctions class provides utility functions for various tasks
    """
    def hash_password(self, password):
        """
        Hashes the given password using SHA-256 algorithm.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        logger.info("generating hash value for provided string")
        return hashlib.sha256(password.encode()).hexdigest()

    def str_mstr_passwd(self, hashed_password):
        """
        Stores the hashed master password in the database.

        Args:
            hashed_password (str): The hashed master password.
        """
        # Connect to the SQLite database
        logger.info('connecting to the database')
        try:
            conn = sqlite3.connect(constants.DATABASE_LOCATION + constants.DATABASE_NAME)
            cursor = conn.cursor()
            logger.info('connected to the database')
            # Create a table to store the hashed master password if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS master_password (
                                id INTEGER PRIMARY KEY,
                                password_hash TEXT
                            )''')
            logger.info('created table if not exists')
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='master_password'")
            result = cursor.fetchone()
            logger.info('result of check, if the master password table was created or not : %s', result)
            if result is None:
                error_message = "failed to create master password table"
                logger.error(error_message)
                raise PickForMeException(error_message)
            
            # Insert or update the hashed master password in the database
            cursor.execute("INSERT OR REPLACE INTO master_password (id, password_hash) VALUES (1, ?)", (hashed_password,))
            logger.info('stored master password in the database')
            # Commit changes and close the connection
            conn.commit()
            logger.info('commited changes')
            conn.close()
            logger.info('connection closed')
        except Exception as e:
            logger.exception("An error occurred while storing the master password : %s", e)
            raise PickForMeException(e) from e

    def chk_mstr_passwd_cfgrd(self):
        """
        Check if the master password is already configured.

        Returns:
            bool: True if the master password is configured, False otherwise.
        """
        logger.info('checking if the tool is initialized')
        password_count = 0
        try:
            conn = sqlite3.connect(constants.DATABASE_LOCATION + constants.DATABASE_NAME)
            cursor = conn.cursor()
            logger.info("connected to the database")
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='master_password'")
            table_exists = cursor.fetchone()[0]
            logger.info("result of check if the master_password table exists : %s", table_exists)
            if not table_exists:
                logger.info("master_password table not found")
                return False

            cursor.execute("SELECT COUNT(*) FROM master_password")
            password_count = cursor.fetchone()[0]
            logger.info("master_password table found")
            conn.close()
            logger.info("result of check if the tool is initialized : %s", password_count)
        except Exception as e:
            logger.exception("An error occurred while checking if the tool is initialized : %s", e)
        return password_count > 0

    def export_to_csv(self):
        """
        Export the data to CSV format.

        This function exports the data from the database tables to CSV files. It creates a directory named 'pickforme_dbdump' if it doesn't exist. 
        Then, it connects to the database and fetches the data from each table. 
        The fetched data is stored in CSV files with the table name as the file name in the 'pickforme_dbdump' directory.

        This function does not return anything.

        Returns:
            None
        """
        logger.info('exporting data to csv')
        try:
            pathlib.Path('pickforme_dbdump').mkdir(parents=True, exist_ok=True)
            logger.info('created directory if not exists')
            conn = sqlite3.connect(constants.DATABASE_LOCATION + constants.DATABASE_NAME)
            cursor = conn.cursor()
            logger.info('connected to the database')
            for db_table in constants.DATABASE_TABLES:
                query = f"SELECT * FROM {db_table}"
                cursor.execute(query)
                rows = cursor.fetchall()
                logger.info('fetched data from the database')
                column_names = [description[0] for description in cursor.description]

                csv_file = f'pickforme_dbdump/{db_table}.csv'
                with open(csv_file, 'w', newline='') as csvfile:
                    logger.info('')
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)
                    writer.writerows(rows)
                    logger.info('data exported to csv')
            conn.close()
        except Exception as e:
            logger.exception("An error occurred while exporting data to csv : %s", e)

    def validate_master_password(self, provided_password_hash):
        """
        Validates the master password.

        Args:
            provided_password_hash (str): The provided password hash to validate.

        Returns:
            bool: True if the provided password hash matches the stored password hash, False otherwise.
        """
        logger.info('Connecting to the database')
        is_valid_password = False
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(constants.DATABASE_LOCATION + constants.DATABASE_NAME)
            cursor = conn.cursor()
            logger.info('Connected to the database')

            # Retrieve the hashed master password from the database
            cursor.execute("SELECT password_hash FROM master_password WHERE id = 1")
            stored_password_hash = cursor.fetchone()
            if stored_password_hash is None:
                error_message = "Master password not found in the database"
                logger.error(error_message)
                raise PickForMeException(error_message)
            
            # Compare the provided password hash with the stored password hash
            if provided_password_hash == stored_password_hash[0]:
                logger.info('Provided password hash matches the stored password hash')
                is_valid_password = True
            else:
                logger.info('Provided password hash does not match the stored password hash')
                is_valid_password = False

            # Close the database connection
            conn.close()
            logger.info('Database connection closed')
        except Exception as e:
            logger.exception("An error occurred while validating the master password: %s", e)
            raise PickForMeException(e)
        return is_valid_password
    
    def prompt_master_auth(self):
        """
        Prompt the user for the master password and validate it.

        Returns:
            bool: True if the master password is valid, False otherwise.
        """
        logger.info('prompting for master password')
        password = getpass("Enter master password: ")
        hashed_password = self.hash_password(password)
        if self.validate_master_password(hashed_password):
            logger.info('master password is valid')
            return True
        else:
            logger.info('master password is not valid')
            print(Fore.RED + "Invalid master password. Please try again." + Style.RESET_ALL)
            return False
        
    def display_tabular_data(self, table_data, table_headers):
        """
        Display the given table data in a tabular format using the PrettyTable library.

        Args:
            table_data (list): The data to be displayed in a tabular format.
            table_headers (list): The headers for the table.

        Returns:
            None

        Raises:
            Exception: If there is an error while displaying the tabular data.
        """
        logger.info('displaying tabular data')
        try:
            table = PrettyTable()
            table.field_names = table_headers
            for row in table_data:
                table.add_row(row)
            print(table)        
            logger.info('displayed tabular data')
        except Exception as e:
            logger.exception('An error occurred while displaying tabular data : %s', e)
            