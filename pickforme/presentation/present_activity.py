from random import choice
from colorama import Fore, Style

from pickforme.common.utils import UtilityFunctions
from pickforme.common import constants
from pickforme.business_logic.activity import ActivityManager
from pickforme.common.logger import logger

class PresentActivity(UtilityFunctions, ActivityManager):
    def __init__(self):
        """
        Initializes an instance of the PresentActivity class.

        This constructor initializes an instance of the PresentActivity class.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('Initializing PresentActivity')
        super().__init__()
        logger.info('PresentActivity initialized, and its dependencies initialized')
        
    def pesent_act_list(self, group_id, category_id):
        """
        Presents the activity list to the user.

        Args:
            group_id (int): The ID of the group.
            category_id (int): The ID of the category.

        Returns:
            None

        Prints:
            - The randomly selected activity name.
            - A message if no activities are available to pick.
        """
        logger.info('presenting activity list')
        activities = self.list_activities(category_id, group_id)
        logger.info('activity list fetched')
        headers=["Id", "Name", "Location", "Suggested by"]
        self.display_tabular_data(activities, headers)
        logger.info('activity list presented')
        
    def present_act_add(self, selected_group, selected_category):
        """
        Adds an activity to the database.

        Args:
            selected_group (int): The ID of the group to which the activity belongs.
            selected_category (int): The ID of the category to which the activity belongs.

        Returns:
            None
        """
        logger.info('adding activity')
        try:
            name = input("Enter activity name: ")
            location = input("Enter location: ")
            suggested_by = input("Enter suggested by: ")
            if not name:
                print(Fore.LIGHTRED_EX + "Error: Activity name cannot be empty." + Style.RESET_ALL)
                logger.info('provided empty name for activity')
                return
            
            if not location:
                print(Fore.LIGHTRED_EX + "Error: Location cannot be empty." + Style.RESET_ALL)
                logger.info('provided empty location for activity')
                return
            
            if not suggested_by:
                print(Fore.LIGHTRED_EX + "Error: Suggested by cannot be empty." + Style.RESET_ALL)
                logger.info('provided empty suggested by for activity')                
                return
                
            logger.info('adding activity: %s', name)
            self.create_activity(name, location, suggested_by, selected_category, selected_group)
            print(f"Activity '{name}' added successfully.")              
            logger.info('activity added: %s', name)
        except Exception as e:
            logger.exception('An error occurred while adding activity : %s', e)
            print(Fore.LIGHTRED_EX + "Error occurred while adding activity" + Style.RESET_ALL)
            
    def present_act_delete(self, group_id, category_id):
        """
        Deletes an activity with the given group ID and category ID.

        Args:
            group_id (int): The ID of the group.
            category_id (int): The ID of the category.

        Returns:
            None

        Raises:
            Exception: If an error occurs while deleting the activity.

        """
        logger.info('deleting activity')
        try:
            entered_actv_id = int(input("Enter activity ID to delete: "))
            if not self.prompt_master_auth():
                logger.warning('Master password not authenticated, skipping delete operation for activity id : %s', group_id)
                print(Fore.LIGHTRED_EX + "Error: Master password not authenticated." + Style.RESET_ALL)
                return
            
            if self.chk_if_valid_actv_slt(entered_actv_id, category_id, group_id):
                logger.info('valid activity id provided: %s', entered_actv_id)
                self.delete_activity(entered_actv_id, category_id, group_id)
                logger.info('deleted activity: %s', entered_actv_id)
                print(f"Activity ID '{entered_actv_id}' deleted successfully.")
            else:
                logger.error('invalid activity id: %s', entered_actv_id)
                print(Fore.LIGHTRED_EX + "Error: Invalid activity id." + Style.RESET_ALL)
        except Exception as e:
            logger.exception('An error occurred while deleting activity : %s', e)
            print(Fore.LIGHTRED_EX + "Error occurred while deleting activity" + Style.RESET_ALL)
    
    def present_act_pick(self, group_id, category_id):
        """
        Pick a random activity from the given group and category.

        Args:
            group_id (int): The ID of the group.
            category_id (int): The ID of the category.

        Returns:
            None

        Prints:
            - The randomly selected activity name.
            - A message if no activities are available to pick.
        """
        picked_activity = self.pick_activity(category_id, group_id)
        if picked_activity:
            headers=["Id", "Name", "Location", "Suggested by"]
            picked_data = [[picked_activity.id, picked_activity.name, picked_activity.location, picked_activity.suggested_by]]
            self.display_tabular_data(picked_data, headers)
        else:
            print(Fore.LIGHTRED_EX + "No activities available to pick" + Style.RESET_ALL)
            
    def present_invalid_operation(self, command):
        """
        Logs an error message for an invalid operation command and prints it to the console.

        Args:
            command (str): The invalid operation command.

        Returns:
            None

        """
        formatted_operations = ", ".join(f"'{operation}'" for operation in constants.SUPPORTED_ACTIVITY_OPERATIONS)
        error_string = f"invalid choice: '{command}' (choose from {formatted_operations})"
        logger.error(error_string)
        print(Fore.LIGHTRED_EX + error_string + Style.RESET_ALL)