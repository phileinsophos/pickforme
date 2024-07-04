import os
from cmd import Cmd
import sys
import re
from getpass import getpass
from colorama import Fore, Style
from pickforme.common.banner import display_banner
from pickforme.common import constants
from pickforme.data_access.database import DatabaseConnections
from pickforme.common.logger import logger
from pickforme.presentation.present_group import PresentGroup
from pickforme.presentation.present_category import PresentCategory
from pickforme.presentation.present_activity import PresentActivity
from pickforme.common.utils import UtilityFunctions

class PickForMeCmd(Cmd):
    """
    This class represents the command-line interface (CLI) for the PickForMe tool.

    Attributes:
        intro (str): The banner message displayed at the start of the CLI session.
        prompt (str): The prompt displayed to the user for input.
        selected_group (str): The currently selected group.
        selected_category (str): The currently selected category.
        selected_activity (str): The currently selected activity.
        is_database_initialized (bool): Indicates whether the database is initialized.
        activity_manager (ActivityManager): The manager for activities.
        category_manager (CategoryManager): The manager for categories.
        utility_functions (UtilityFunctions): The utility functions for the CLI
    """
    
    intro = display_banner()
    prompt = '>> '
    selected_group = None
    selected_category = None
    is_database_initialized = False
    current_group = None
    current_category = None
    current_application_level = -1
    
    def __init__(self):
        """
        Initializes an instance of the PickForMeCmd class.

        This constructor initializes an instance of the PickForMeCmd class. It sets up the necessary attributes and
        establishes the database connection.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('Initializing PickForMeCmd')
        super().__init__()
        self.present_group = PresentGroup()
        self.present_activity = PresentActivity()
        self.present_category = PresentCategory()
        self.utility_functions = UtilityFunctions()
        logger.info('PickForMeCmd initialized, and its dependencies initialized')
        
    def do_help(self, arg):
        logger.info('Showing help for %s', arg)
        if arg == 'groups':
            print(constants.HELP_STRING_GROUPS)
        elif arg == 'categories':
            print(constants.HELP_STRING_CATEGORIES)
        elif arg == 'activities':
            print(constants.HELP_STRING_ACTIVITIES)
        elif not self.is_database_initialized:
            print(constants.HELP_STRING_NO_INIT)
        elif self.is_database_initialized :
            print(constants.HELP_STRING_TOOL_INIT)

    def do_init(self, arg): 
        """
        Initializes the application.

        This function initializes the application by setting up the master password and creating the necessary tables in the database.

        Parameters:
            arg (str): The argument passed to the function.

        Returns:
            None
        """
        
        if self.is_database_initialized:
            logger.warning('application already initialized, invalid init command')
            print(Fore.LIGHTRED_EX + 'Invalid command entered' + Style.RESET_ALL)  
        else:    
            logger.info("Master password not configured. Please set a master password:")
            master_password = getpass("Enter master password: ")
            confirm_password = getpass("Re-enter master password: ")
            if master_password == confirm_password:
                # Save master password to database
                logger.info('Storing master password in the database')
                database_connections = DatabaseConnections()
                database_connections.create_all_tables()
                logger.info('created all tables in the database')
                hashed_password = self.utility_functions.hash_password(master_password)
                self.utility_functions.str_mstr_passwd(hashed_password)
                logger.info("Master password configured successfully.")
                print("\nMaster password configured successfully.")
                logger.info("Database tables created successfully.")
                self.is_database_initialized = self.utility_functions.chk_mstr_passwd_cfgrd()
                self.current_application_level = 0
                print('Application initialized successfully.\n')
                logger.info('Application initialized successfully.')            
            else:
                logger.error("Passwords do not match. Please try again.")
                print("Passwords do not match. Please try again.")

    def do_clear_db(self, arg):
        """
        Clears all data from the database.

        This function clears all data from the database. It prompts the user for the master password and then performs the
        necessary truncation of activities, categories, and groups tables. If the master password is not authenticated,
        it logs an error and prints an error message. If the master password is authenticated, it truncates the
        activities, categories, and groups tables, logs a success message, and prints a success message.

        Parameters:
            arg (str): The argument passed to the function. It is not used in this function.

        Returns:
            None
        """
        logger.info('Clearing all data from the database')
        # Implementation for clearing the database   
        if not self.utility_functions.prompt_master_auth():
            logger.error('Master password not authenticated, skipping clearing database')
            print(Fore.LIGHTRED_EX + "Error: Master password not authenticated." + Style.RESET_ALL)
        else:
            self.present_activity.truncate_activities()
            self.present_category.truncate_categories()
            self.present_group.truncate_groups()
            logger.info('Database contents cleared, tool is now reset')
            print("All database contents cleared. The tool is now reset.")

    def do_initapp(self, arg):
        """
        Manage groups.

        This function prompts the user to enter commands related to managing groups. It presents a prompt to the user
        to enter a command and executes the corresponding functionality based on the command entered.

        Parameters:
            arg (str): The argument passed to the function.

        Returns:
            None

        """
        if not self.utility_functions.chk_mstr_passwd_cfgrd():
            logger.warning('Master password not configured, skipping group management')
            print(Fore.CYAN + "Error: Master password not configured, Please configure master password before proceeding" + Style.RESET_ALL)
            return
        
        self.current_application_level = 1
        while True:
            command = input("(Groups) Enter command (type 'help groups' for options): ")
            if command == 'list':
                self.present_group.pesent_grp_list()
            elif command == 'add':
                self.present_group.present_grp_add()
            elif command == 'delete':
                self.present_group.present_grp_delete()
            elif command == 'select':
                self.selected_group, self.current_group = self.present_group.present_grp_select()
            elif command == 'back':
                self.selected_group = None
                logger.info("Going back to main menu, Group selection cancelled.")
                break
            elif command == 'quit':
                self.do_quit('')
            elif command == 'help':
                self.do_help('groups')
            elif command == '':
                logger.warning('No command entered as argument for groups command')
            else:
                self.present_group.present_invalid_operation(command)
                self.do_help('groups')

            # If a group is selected, move to the category level
            if self.selected_group:
                logger.info('Selected group: %s, moving to categories', self.selected_group)
                self.do_categories('')
                logger.info('returned to groups prompt, back from categories')
                self.prompt = '>> '
            
    def do_categories(self, arg):
        """
        Executes the 'categories' command in the PickForMeCmd class.

        This function executes the 'categories' command in the PickForMeCmd class. It presents a prompt to the user
        to enter a command related to managing categories. It validates the input and executes the corresponding functionality
        based on the command entered by the user.

        Parameters:
            self (PickForMeCmd): The PickForMeCmd instance.
            arg (str): The argument passed to the function (not used)

        Returns:
            None
        """

        if not self.selected_group:
            logger.warning('Please select a group first before using categories command')
            print(Fore.CYAN + "Please select a group first before using 'categories' command." + Style.RESET_ALL)
            return

        self.current_application_level = 2
        while True:
            command = input('''(Categories) Enter command (type 'help categories' for options): ''')
            if command == 'list':
                self.present_category.present_cat_list(self.selected_group)
            elif command == 'add':
                self.present_category.present_cat_add(self.selected_group)
            elif command == 'delete':
                self.present_category.present_cat_delete(self.selected_group)
            elif command == 'select':
                self.selected_category, self.current_category = self.present_category.present_cat_select(self.selected_group)
            elif command == 'back':
                logger.info('Returning to previous menu, Category selection cancelled.')
                self.selected_category = None
                self.selected_group = None
                break
            elif command == 'quit':
                self.do_quit('')
            elif command == 'help':
                self.do_help('categories')
            elif command == '':
                logger.warning('No command entered as argument for groups command')
            else:
                self.present_category.present_invalid_operation(command)
                self.do_help('categories')
            
            # If a category is selected, move to the activity level
            if self.selected_category:
                logger.info('Selected category: %s, moving to activities', self.selected_category)
                self.do_activities('')
                logger.info('returned to categories prompt, back from activities')
                self.prompt = '>> '

    def do_activities(self, arg):
        """
        Executes the 'activities' command in the PickForMeCmd class.

        This function executes the 'activities' command in the PickForMeCmd class. It presents a prompt to the user
        to enter a command related to managing activities. It validates the input and executes the corresponding functionality
        based on the command entered by the user.

        Parameters:
            arg (str): The argument passed to the function (not used)

        Returns:
            None
        """

        logger.info('Managing activities, arg: %s', arg)
        if (not self.selected_category) and (not self.selected_group):
            logger.info('Please select a group and a category first')
            print(Fore.CYAN + "Please select a group and a category first, before using 'activities' command." + Style.RESET_ALL)
            return

        self.current_application_level = 3
        while True:
            command = input("(Activities) Enter command (type 'help activities' for options): ")
            if command == 'current':
                logger.info('displaying current selections')
                print(f"{'Group':>10} : {self.current_group:>10}\n{'Category':>10} : {self.current_category:>10}")
            elif command == 'list':
                self.present_activity.pesent_act_list(self.selected_group, self.selected_category)
            elif command == 'add':
                self.present_activity.present_act_add(self.selected_group, self.selected_category)
            elif command == 'delete':
                self.present_activity.present_act_delete(self.selected_group, self.selected_category)
            elif command == 'pick':
                self.present_activity.present_act_pick(self.selected_group, self.selected_category)
            elif command == 'back':
                logger.info('Returning to previous menu, Activity selection cancelled.')
                self.selected_category = None
                break
            elif command == 'quit':
                self.do_quit('')
            elif command == 'help':
                self.do_help('activities')
            elif command == '':
                logger.info('No command entered as argument for activities command')
            else:
                self.present_activity.present_invalid_operation(command)
                self.do_help('activities')
        logger.info('returned to activities prompt, back from activities')

    def do_quit(self, arg):
        """
        Exit the tool.

        Args:
            self (PickForMeCmd): The PickForMeCmd instance.
            arg (str): The argument passed to the function.

        Returns:
            None
        """
        print("Exiting PickForMe Tool. Goodbye!")
        logger.info("Exiting PickForMe Tool. Goodbye!")
        sys.exit(0)
        
    def do_dump(self, arg):
        """
        Dump the data to CSV format.

        This function dumps all the records to files in CSV format. It exports the data from the database tables to CSV files. 
        It creates a directory named 'pickforme_dbdump' if it doesn't exist. 
        Then, it connects to the database and fetches the data from each table. 
        The fetched data is stored in CSV files with the table name as the file name in the 'pickforme_dbdump' directory.

        This function does not return anything.

        Parameters:
            arg (str): The argument passed to the function (not used)

        Returns:
            None
        """
        logger.info('dumping all the records to files')
        self.utility_functions.export_to_csv()
        logger.info('dumped all the records to files')
    
    def do_path(self, arg):
        print('\n')
        print(Fore.LIGHTYELLOW_EX + os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + Style.RESET_ALL)
        print('\n')
        
    def default(self, line):
        """
        Handle the default case for the command line input.

        This function handles the default case for the command line input. 
        It checks the current application level and the line input to determine the appropriate error message and prints it to the console. 

        Parameters:
            line (str): The line input from the user.

        Returns:
            None
        """
        if self.current_application_level == -1:
            formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_NO_INIT_OPERATIONS)
            error_string = f"invalid choice: '{line}' (choose from {formatted_operations})"
            logger.error(error_string)
            print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
        elif self.current_application_level == 0:
            formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_TOOL_INIT_OPERATIONS)
            error_string = f"invalid choice: '{line}' (choose from {formatted_operations})"
            logger.error(error_string)
            print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
        elif self.current_application_level == 1:
            formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_GROUP_OPERATIONS)
            error_string = f"invalid choice: '{line}' (choose from {formatted_operations})"
            logger.error(error_string)
            print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
        elif self.current_application_level == 2:
            formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_CATEGORY_OPERATIONS)
            error_string = f"invalid choice: '{line}' (choose from {formatted_operations})"
            logger.error(error_string)
            print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
        elif self.current_application_level == 3:
            formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_ACTIVITY_OPERATIONS)
            error_string = f"invalid choice: '{line}' (choose from {formatted_operations})"
            logger.error(error_string)
            print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
        else:
            logger.error("Command prefix not recognized. Invalid command: %s", line)
            print(Fore.LIGHTRED_EX + 'Command prefix not recognized. Invalid command: {}'.format(line) + Style.RESET_ALL)
        
    
    def emptyline(self):
        """
        Logs that an empty command was received.

        Returns:
            bool: True
        """
        logger.info("Empty command")
        return True
    
    def precmd(self, line):
        """Validate input before executing command."""
        logger.info('validating input : %s', line)
        if not re.match("^[a-zA-Z0-9_?]*$", line):
            logger.error("Invalid characters in input : %s", line)
            print(Fore.RED + "Error: Invalid characters in input." + Style.RESET_ALL)
            return ""
        return line