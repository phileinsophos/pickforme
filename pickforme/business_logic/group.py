from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import StatementError

from pickforme.data_access.database import Group, DatabaseConnections
from pickforme.common.logger import logger

class GroupManager(DatabaseConnections):
    """Class to manage groups."""
    def __init__(self):
        """
        Initializes an instance of the GroupManager class.

        This constructor initializes an instance of the GroupManager class.

        Parameters:
            None

        Returns:
            None
        """
        logger.info('Initializing GroupManager')
        super().__init__()
        logger.info('GroupManager initialized, and its dependencies initialized')
        self.session = self.get_db_connection_session(session_for='GroupManager')
        logger.info('GroupManager initialized, database connection established')

    def create_group(self, name):
        """Create a new group."""
        logger.info('Creating group: %s', name)
        group = Group(name=name)
        self.session.add(group)
        self.session.commit()
        logger.info('Group created: %s', name)

    def list_groups(self, include_deleted=False):
        """List all groups."""
        logger.info('Listing groups')
        groups = []
        try:
            if include_deleted:
                logger.info('Including deleted groups')
                groups = self.session.query(Group.id, Group.name).all()
            else:
                logger.info('Excluding deleted groups')
                groups = self.session.query(Group.id, Group.name).filter_by(is_deleted=False).all()
            logger.info('Groups listed')
        except StatementError as e:
            logger.exception('An error occurred while listing groups : %s', e)
        groups_list = [[grp.id, grp.name] for grp in groups]
        logger.info('fetched groups from database, total records : %s', len(groups_list))
        return groups_list

    def delete_group(self, group_id):
        """Soft delete a group by setting is_deleted to True."""
        logger.info('Deleting group: %s', group_id)
        group = self.session.query(Group).filter(Group.id == group_id).one()
        group.is_deleted = True
        group.deleted_timestamp = datetime.now(timezone.utc)
        group.updated_timestamp = datetime.now(timezone.utc)
        self.session.commit()
        logger.info('Group deleted: %s', group_id)

    def truncate_groups(self):
        """Truncate groups table."""
        logger.info('Truncating groups table')
        self.session.query(Group).delete()
        self.session.commit()
        logger.info('Groups table truncated')
        
    def chk_if_valid_grp_slt(self, group_id):
        """Check if the selected group is valid."""
        logger.info('Checking if the selected group is valid: %s', group_id)
        try:
            group_id = int(group_id)
            group_check = self.session.query(Group).filter(
                    Group.id == group_id,
                    Group.is_deleted == False
                ).one_or_none()
        
            if group_check is None:
                logger.warning('Group with ID %s does not exist', group_id)
                return False
            else:
                logger.info('Selected group is valid: %s', group_id)
                return True
        except (NoResultFound, MultipleResultsFound, StatementError) as excp:
            logger.exception('An error occurred while checking if the selected group is valid : %s', excp)
            print(f'Invalid group ID: {group_id}')
            
    def get_grp_nm_by_id(self, group_id):
        """Get the name of a group by its ID."""
        logger.info('')
        group = self.session.query(Group).filter(Group.id == group_id).filter(Group.is_deleted == False).one_or_none()
        if group:
            return group.name
        else:
            return None