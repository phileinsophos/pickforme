import random
from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import StatementError

from pickforme.data_access.database import Activity, DatabaseConnections
from pickforme.common.logger import logger

class ActivityManager(DatabaseConnections):
    """Class to manage activities."""
    def __init__(self):
        logger.info('Initializing ActivityManager')
        super().__init__()
        logger.info('ActivityManager initialized, and its dependencies initialized')
        self.session = self.get_db_connection_session(session_for='ActivityManager')
        logger.info('ActivityManager initialized, and its dependencies initialized')
        

    def create_activity(self, name, location, suggested_by, category_id, group_id):
        """Create a new activity."""
        logger.info('Creating activity: %s', name)
        activity = Activity(name=name, location=location, suggested_by=suggested_by, category_id=category_id, group_id=group_id)
        self.session.add(activity)
        self.session.commit()
        logger.info('Activity created: %s', name)

    def list_activities(self,category_id, group_id ,include_deleted=False):
        """List all activities."""
        logger.info('Listing activities present under group: %s and category: %s', group_id, category_id)
        activities = []
        try:
            if include_deleted:
                logger.info('Including deleted activities')
                activities = self.session.query(Activity.id, Activity.name,Activity.location, Activity.suggested_by).filter_by(
                    group_id=group_id,
                    category_id=category_id
                    ).all()
            else:
                logger.info('Excluding deleted activities')
                activities = self.session.query(Activity.id, Activity.name,Activity.location, Activity.suggested_by).filter_by(
                    is_deleted=False,
                    was_selected=False,
                    group_id=group_id,
                    category_id=category_id
                    ).all()
            logger.info('activities records fetched from database')
        except StatementError as e:
            logger.exception('An error occurred while fetching activities from database : %s', e)
        activities_list = [[act.id, act.name, act.location, act.suggested_by] for act in activities]
        logger.info('fetched activities from database, total records : %s', len(activities_list))
        return activities_list

    def delete_activity(self, activity_id, category_id, group_id):
        """Soft delete an activity by setting is_deleted to True."""
        logger.info('Deleting activity: %s', activity_id)
        activity = self.session.query(Activity).filter(
                Activity.id == activity_id,
                Activity.category_id == category_id,
                Activity.group_id == group_id
            ).one()
        activity.is_deleted = True
        activity.deleted_timestamp = datetime.now(timezone.utc)
        activity.updated_timestamp = datetime.now(timezone.utc)
        self.session.commit()
        logger.info('Activity deleted: %s', activity_id)
    
    def pick_activity(self, category_id, group_id):
        """Randomly pick an activity and update its was_selected field to True."""
        logger.info('Picking a random activity for group ID: %s and category ID: %s', group_id, category_id)

        if category_id is None or group_id is None:
            logger.error('Category ID or Group ID is None.')
            return None

        try:
            activities = self.session.query(Activity).filter(
                Activity.group_id == group_id,
                Activity.category_id == category_id,
                Activity.is_deleted == False,
                Activity.was_selected == False
            ).all()
            
            if not activities:
                logger.warning('No activities found for group ID: %s and category ID: %s', group_id, category_id)
                return None

            selected_activity = random.choice(activities)
            selected_activity.was_selected = True
            timestamp = datetime.now(timezone.utc)
            selected_activity.select_timestamp = timestamp
            selected_activity.updated_timestamp = timestamp
            logger.info('Activity selected: %s', selected_activity.id)
            self.session.add(selected_activity)
            self.session.commit()
            logger.info('updated selected activity record details')
            return selected_activity

        except StatementError as e:
            logger.exception('A database error occurred while picking a random activity: %s', e)
            self.session.rollback()
            return None
        except Exception as e:
            logger.exception('An unexpected error occurred: %s', e)
            self.session.rollback()
            return None
        
    def truncate_activities(self):
        """
        Truncates the activities table by deleting all records from the table.

        This function deletes all records from the activities table. It does not return any value.

        Returns:
            None
        """
        logger.info('Truncating activities table')
        self.session.query(Activity).delete()
        self.session.commit()
        logger.info('Activities table truncated')

    def chk_if_valid_actv_slt(self, activity_id, category_id, group_id):
        """Check if the selected activity is valid."""
        logger.info('Checking if the selected activity is valid: %s present under group: %s and category: %s', activity_id, group_id, category_id)
        try:
            activity_id = int(activity_id)
            activity_check = self.session.query(Activity).filter(
                    Activity.id == activity_id,
                    Activity.group_id == group_id,
                    Activity.category_id == category_id,
                    Activity.is_deleted == False
                ).one_or_none()
            if activity_check is None:
                logger.warning('Activity with ID %s does not exist or is marked as deleted', activity_id)
                return False
            else:
                logger.info('Selected Activity is valid: %s and is present under group: %s and category: %s', activity_id, group_id, category_id)
                return True
        except (MultipleResultsFound, NoResultFound) as excp:
            logger.exception('An error occurred while checking if the selected activity is valid : %s', excp)
            print(f'Invalid activity ID: {activity_id}')
            return False

    def delete_actv_with_cat_and_grpid(self,category_id, group_id):
        """
        Mark activities as deleted for a given category ID and group ID.

        Args:
            category_id (int): The ID of the category.
            group_id (int): The ID of the group.

        Returns:
            None

        Raises:
            Exception: If an error occurs while marking activities as deleted.

        Notes:
            - This function updates the 'is_deleted', 'deleted_timestamp', and 'updated_timestamp' fields
              of the activities table for the given category ID and group ID.
            - The function commits the changes to the session and rolls back the session in case of an error.
        """
        exception_statement = 'An error occurred while marking activities as deleted:'
        try:
            logger.info('Marking activities as deleted for category ID: %s and group ID: %s', category_id, group_id)
            activities_deleted = self.session.query(Activity).filter(
                    Activity.category_id==category_id, 
                    Activity.group_id==group_id,
                    Activity.is_deleted is False
                ).update({
                    'is_deleted': True,
                    'deleted_timestamp': datetime.now(timezone.utc),
                    'updated_timestamp':datetime.now(timezone.utc)
                }, synchronize_session=False)
            self.session.commit()
            logger.info('Marked %s activities as deleted for category ID: %s and group ID: %s', activities_deleted, category_id, group_id)
        except StatementError as statement_error:
            logger.exception('%s %s', exception_statement, statement_error)
            self.session.rollback()

    def delete_actv_with_grp_id(self, group_id):
        """
        Soft delete activities by setting 'is_deleted' to True for a given group ID.

        Args:
            group_id (int): The ID of the group.

        Returns:
            None

        Raises:
            Exception: If an error occurs while marking activities as deleted.

        Notes:
            - This function updates the 'is_deleted', 'deleted_timestamp', and 'updated_timestamp' fields
            of the activities table for the given group ID.
            - The function commits the changes to the session and rolls back the session in case of an error.
        """
        exception_statement = 'An error occurred while marking activities as deleted for id:'
        try:
            logger.info('Marking activities as deleted for group ID: %s', group_id)
            activities_deleted = self.session.query(Activity).filter_by(group_id=group_id).update({
                'is_deleted': True,
                'deleted_timestamp': datetime.now(timezone.utc),
                'updated_timestamp':datetime.now(timezone.utc)
            }, synchronize_session=False)
            self.session.commit()
            logger.info('Marked %s activities as deleted for group ID: %s', activities_deleted, group_id)
        except StatementError as e:
            logger.exception('%s %s : %s', exception_statement, group_id, e)
            self.session.rollback()

