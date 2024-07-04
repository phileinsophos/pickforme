from colorama import Fore, Style

from pickforme.common.utils import UtilityFunctions
from pickforme.common import constants
from pickforme.business_logic.category import CategoryManager
from pickforme.business_logic.activity import ActivityManager
from pickforme.common.logger import logger

class PresentCategory(UtilityFunctions, CategoryManager):
    def __init__(self):
        """
        Initializes an instance of the PresentCategory class.

        This constructor initializes an instance of the PresentCategory class.
        It calls the parent class constructor with no arguments.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('Initializing PresentCategory')
        super().__init__()
        logger.info('PresentCategory initialized, and its dependencies initialized')
        
    def present_cat_list(self, selected_group):
        """
        Present the category list to the user.

        Args:
            selected_group (int): The ID of the selected group.

        Returns:
            None
        """
        logger.info('Presenting category list')
        categories = self.list_categories(selected_group)
        logger.info('Category list fetched')
        headers=["Id", "Name"]
        self.display_tabular_data(categories, headers)
        logger.info('Category list presented')
    
    def present_cat_add(self, selected_group):
        """
        Present the user interface for deleting a category.

        Args:
            selected_group (int): The ID of the selected group.

        Returns:
            None
        """
        logger.info('adding category')
        try:
            name = input('Enter category name: ')
            if name:
                logger.info('adding category name: %s', name)
                self.create_category(name, selected_group)
                logger.info('category name added: %s', name)
                print(f"Category '{name}' added successfully.")
            else:
                print(Fore.LIGHTRED_EX + "Error: Category name cannot be empty." + Style.RESET_ALL)
                logger.info('provided empty name for category')
        except Exception as e:
            logger.exception('An error occurred while adding category : %s', e)
            print(Fore.LIGHTRED_EX + "Error occurred while adding category" + Style.RESET_ALL)
            
    def present_cat_delete(self, selected_group):
        """
        Delete a category by prompting the user for the category ID and performing the necessary operations.

        Args:
            selected_group (int): The ID of the selected group.

        Returns:
            None
        """
        # Prompt the user for the category ID to delete
        category_id = int(input("Enter category ID to delete: "))
        
        # Check if the master password is authenticated
        if not self.prompt_master_auth():
            # Log a warning if the master password is not authenticated
            logger.warning('Master password not authenticated, skipping delete operation for category id : %s', category_id)
            # Print an error message if the master password is not authenticated
            print(Fore.LIGHTRED_EX + "Error: Master password not authenticated." + Style.RESET_ALL)
            return
        
        # Check if the category ID is valid
        if self.chk_if_valid_ctr_slt(selected_group, category_id):
            # Delete the category and its associated activities
            activity_manager = ActivityManager()
            activity_manager.delete_actv_with_cat_and_grpid(category_id, selected_group)
            self.delete_category(category_id)
            # Log the deletion of the category
            logger.info('Category deleted: %s', category_id)
            # Print a success message if the category is deleted
            print(f"Category ID '{category_id}' deleted successfully.")
        else:
            # Log an error if the category ID is invalid
            logger.error('Invalid category id: %s', category_id)
            # Print an error message if the category ID is invalid
            print(Fore.LIGHTRED_EX + "Error: Invalid category id." + Style.RESET_ALL)
        
    def present_cat_select(self, group_id):
        """
        Selects a category present under a given group.

        Args:
            group_id (int): The ID of the group.
        
        Returns:
            tuple: A tuple containing the selected category ID and the current category.
                - selected_category_id (int): The ID of the selected category.
                - current_category (str): The name of the current category.
        """
        logger.info('Selecting category present under group: %s', group_id)
        category_id = input("Enter category ID to select: ")
        
        try:
            category_id = int(category_id)
        except ValueError:
            logger.error('Invalid category ID entered: %s', category_id)
            print(Fore.LIGHTRED_EX + "Invalid category ID entered. Please try again." + Style.RESET_ALL)
            return None, None
        
        selected_category = None
        current_category = None
        if self.chk_if_valid_ctr_slt(group_id, category_id):
            logger.info('selected category id is valid: %s', category_id)
            selected_category = category_id
            current_category = self.get_catg_nm_by_id(selected_category)
            logger.info('selected category id is: %s', category_id)
        else:
            logger.info('selected category id is invalid: %s', category_id)
            print(Fore.LIGHTRED_EX + "Invalid category ID entered. Please try again." + Style.RESET_ALL)
        return selected_category, current_category
    
    def present_invalid_operation(self, command):
        """
        Logs an error message for an invalid operation choice and prints it to the console.

        Args:
            command (str): The invalid operation choice.

        Returns:
            None
        """
        formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_CATEGORY_OPERATIONS)
        error_string = f"invalid choice: '{command}' (choose from {formatted_operations})"
        logger.error(error_string)
        print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)
            