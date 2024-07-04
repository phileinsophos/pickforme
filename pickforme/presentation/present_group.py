from colorama import Fore, Style

from pickforme.common.utils import UtilityFunctions
from pickforme.common import constants
from pickforme.business_logic.group import GroupManager
from pickforme.business_logic.category import CategoryManager
from pickforme.business_logic.activity import ActivityManager
from pickforme.common.logger import logger

class PresentGroup(GroupManager, UtilityFunctions):
    
    def __init__(self):
        """
        Initializes an instance of the PresentGroup class.

        This constructor initializes an instance of the PresentGroup class.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('Initializing PresentGroup')
        super().__init__()
        logger.info('PresentGroup initialized, and its dependencies initialized')
    
    def pesent_grp_list(self):
        """
        Present the group list to the user.

        This method presents the group list to the user by fetching the groups using the `list_groups` method, 
        setting the headers to `["Id", "Name"]`, and displaying the tabular data using the 
        `display_tabular_data` method.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('presenting group list')
        groups = self.list_groups()
        logger.info('group list fetched')
        headers = ["Id", "Name"]
        self.display_tabular_data(groups, headers)
        logger.info('group list presented')
        
    def present_grp_add(self):
        """
        Adds a new group to the database.

        This function prompts the user to enter a group name and then adds the group to the database using the
        `create_group` method. If the group name is empty, an error message is displayed. If the group name
        is not empty, the group is added to the database and a success message is displayed.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('adding group')
        try:
            name = input("Enter group name: ")
            if name:
                logger.info('adding group name: %s', name)
                self.create_group(name)
                logger.info('group name added: %s', name)
                print(f"Group '{name}' added successfully.")
            else:
                print(Fore.LIGHTRED_EX + "Error: Group name cannot be empty." + Style.RESET_ALL)
                logger.info('provided empty name for group')
        except Exception as e:
            logger.exception('An error occurred while adding group : %s', e)
            print(Fore.LIGHTRED_EX + "Error occurred while adding group" + Style.RESET_ALL)
            
    def present_grp_delete(self):
        """
        Deletes a group by prompting the user for the group ID and performing the necessary operations to delete the group and its associated activities and categories.

        Returns:
            None
        """
        logger.info('deleting group')
        try:
            group_id = int(input("Enter group ID to delete: "))
            if not self.prompt_master_auth():
                logger.warning('Master password not authenticated, skipping delete operation for group id : %s', group_id)
                print(Fore.LIGHTRED_EX + "Error: Master password not authenticated." + Style.RESET_ALL)
                return
            
            if self.chk_if_valid_grp_slt(group_id):
                logger.info('valid group id provided: %s', group_id)
                activity_manager = ActivityManager()
                category_manager = CategoryManager()
                activity_manager.delete_actv_with_grp_id(group_id)
                category_manager.delete_catg_with_grp_id(group_id)
                self.delete_group(group_id)
                logger.info('deleted group: %s', group_id)
                print(f"Group ID '{group_id}' deleted successfully.")
            else:
                logger.info('invalid group id: %s', group_id)
                print(Fore.LIGHTRED_EX + "Error: Invalid group ID." + Style.RESET_ALL)
        except Exception as e:
            logger.exception('An error occurred while deleting group : %s', e)
            print(Fore.LIGHTRED_EX + "Error occurred while deleting group" + Style.RESET_ALL)
            
    def present_grp_select(self):
        """
        Selects a group for further operations.

        This method prompts the user to select a group by entering the group ID. It checks if the provided group ID is valid using the `chk_if_valid_grp_slt` method. If the group ID is valid, it sets the `selected_group` and `current_group` variables accordingly. If the group ID is invalid, it displays an error message and returns `None` for both variables.

        Returns:
            tuple: A tuple containing the selected group ID and the current group object.
                - selected_group (str): The ID of the selected group.
                - current_group (Group): The current group object.
        """
        logger.info('selecting group')
        selected_group = None
        current_group = None
        group_id = input("Enter group ID to select: ")
        if self.chk_if_valid_grp_slt(group_id):
            logger.info('selected group id is valid: %s', group_id)
            selected_group = group_id
            current_group = self.get_grp_nm_by_id(selected_group)
            logger.info('selected group id: %s', group_id)
        else:
            logger.info('selected group id is invalid: %s', group_id)
            print(Fore.LIGHTRED_EX + "Invalid group ID entered. Please try again." + Style.RESET_ALL)
        return selected_group, current_group
            
    def present_invalid_operation(self, command):
        """
        Logs an error message for an invalid operation choice.

        This function logs an error message for an invalid operation choice. It formats the error message by replacing placeholders with appropriate values.

        Parameters:
            self (PresentGroup): The instance of the PresentGroup class.
            command (str): The invalid operation choice.

        Returns:
            None
        """
        formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_GROUP_OPERATIONS)
        error_string = f"invalid choice: '{command}' (choose from {formatted_operations})"
        logger.error(error_string)
        print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)