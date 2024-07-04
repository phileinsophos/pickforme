from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import StatementError

from pickforme.data_access.database import Category, DatabaseConnections
from pickforme.common.logger import logger

class CategoryManager(DatabaseConnections):
    """Class to manage categories."""
    def __init__(self):
        logger.info('Initializing CategoryManager')
        super().__init__()
        logger.info('CategoryManager initialized, and its dependencies initialized')
        self.session = self.get_db_connection_session(session_for='CategoryManager')
        logger.info('CategoryManager initialized, and its dependencies initialized')

    def create_category(self, name, group_id):
        """Create a new category."""
        logger.info('Creating category: %s', name)
        category = Category(name=name, group_id=group_id)
        self.session.add(category)
        self.session.commit()
        logger.info('Category created: %s', name)

    def list_categories(self, group_id, include_deleted=False):
        """List all categories."""
        logger.info('Listing categories')
        categories = []
        try:
            if include_deleted:
                logger.info('Including deleted categories')
                categories = self.session.query(Category.id, Category.name).all()
            else:
                logger.info('Excluding deleted categories, getting all categories with group_id: %s', group_id)
                categories = self.session.query(Category.id, Category.name).filter_by(is_deleted=False, group_id=group_id).all()
            logger.info('Categories listed')
        except StatementError as e:
            logger.exception('An error occurred while listing categories : %s', e)
        categories_list = [[category.id, category.name] for category in categories]
        logger.info('fetched categories from database, total records : %s', len(categories_list))
        return categories_list

    def delete_category(self, category_id):
        """Soft delete a category by setting is_deleted to True."""
        logger.info('Deleting category: %s', category_id)
        category = self.session.query(Category).filter(Category.id == category_id).one()
        category.is_deleted = True
        category.deleted_timestamp = datetime.now(timezone.utc)
        self.session.commit()
        logger.info('Category deleted: %s', category_id)
        
    def truncate_categories(self):
        """
        Truncates the categories table by deleting all records.

        This function truncates the categories table by deleting all records. It does not return any value.

        Returns:
            None
        """
        logger.info('Truncating categories table')
        self.session.query(Category).delete()
        self.session.commit()
        logger.info('Categories table truncated')

    def chk_if_valid_ctr_slt(self,group_id, category_id):
        """Check if the selected category is valid."""
        logger.info('Checking if the selected category %s is valid, present under group ID: %s', category_id, group_id)
        try:
            category_id = int(category_id)
            category_check = self.session.query(Category).filter(
                    Category.id == category_id,
                    Category.group_id == group_id,
                    Category.is_deleted == False
                ).one_or_none()
        
            if category_check is None:
                logger.warning('Category with ID %s does not exists or is marked as deleted', category_id)
                return False
            else:
                logger.info('Selected category is valid: %s and present under group ID: %s', category_id, group_id)
                return True
        except (MultipleResultsFound, NoResultFound, StatementError) as e:
            logger.exception('An error occurred while checking if the selected category is valid : %s and present under group ID: %s : %s', category_id, group_id, e)
            print(f'Invalid category ID: {category_id}')
            return False
            
    def get_catg_nm_by_id(self, category_id):
        """Get category name by ID."""
        category = self.session.query(Category).filter(Category.id == category_id, Category.is_deleted is False).one_or_none()
        if category:
            return category.name
        else:
            return None
        
    def delete_catg_with_grp_id(self, group_id):
        """
        Soft delete categories by setting 'is_deleted' to True for a given group ID.

        Args:
            group_id (int): The ID of the group.

        Returns:
            None

        Raises:
            StatementError: If an error occurs while marking categories as deleted.
        """
        try:
            logger.info('Marking catogories as deleted for group ID: %s', group_id)
            categories_deleted = self.session.query(Category).filter_by(group_id=group_id).update({
                'is_deleted': True,
                'deleted_timestamp': datetime.now(timezone.utc),
                'updated_timestamp':datetime.now(timezone.utc)
            }, synchronize_session=False)
            self.session.commit()
            logger.info('Marked %s catogories as deleted for group ID: %s', categories_deleted, group_id)
        except StatementError as e:
            logger.exception('An error occurred while marking catogories as deleted: %s', e)
            self.session.rollback() 
