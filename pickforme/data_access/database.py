import os
from datetime import datetime 

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, scoped_session

from pickforme.common.AppException import PickForMeException
from pickforme.common import constants
from pickforme.common.logger import logger

project_install_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_db_dir = os.path.join(project_install_path, constants.DATABASE_LOCATION)
app_db_path = os.path.join(project_db_dir, constants.DATABASE_NAME)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///'+app_db_path)

Base = declarative_base()

class Group(Base):
    """
    Model for groups.
    
    Attributes:
        id (int): The unique identifier for the group.
        name (str): The name of the group.
        is_deleted (bool): Indicates if the group is deleted.
        insert_timestamp (datetime): Datetime when this row was inserted.
        deleted_timestamp (datetime): Datetime when this row was deleted.
        updated_timestamp (datetime): Datetime when this row was last updated.
    """
    __tablename__ = 'groups'
    logger.info('Creating groups table')
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    insert_timestamp = Column(DateTime, default=datetime.utcnow)
    deleted_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    logger.info('Groups table created')

class Category(Base):
    """
    Model for categories.
    
    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category.
        group_id (int): The ID of the group to which the category belongs.
        is_deleted (bool): Indicates if the category is deleted.
        insert_timestamp (datetime): Datetime when this row was inserted.
        deleted_timestamp (datetime): Datetime when this row was deleted.
        updated_timestamp (datetime): Datetime when this row was last updated.
    """
    __tablename__ = 'categories'
    logger.info('Creating categories table')
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')
    is_deleted = Column(Boolean, default=False, nullable=False)
    insert_timestamp = Column(DateTime, default=datetime.utcnow)
    deleted_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    logger.info('Categories table created')

class Activity(Base):
    """
    Model for activities.
    
    Attributes:
        id (int): The unique identifier for the activity.
        name (str): The name of the activity.
        location (str): The location of the activity.
        suggested_by (str): The name of the person who suggested the activity.
        category_id (int): The ID of the category to which the activity belongs.
        is_deleted (bool): Indicates if the activity is deleted.
        insert_timestamp (datetime): Datetime when this row was inserted.
        deleted_timestamp (datetime): Datetime when this row was deleted.
        updated_timestamp (datetime): Datetime when this row was last updated.
    """
    __tablename__ = 'activities'
    logger.info('Creating activities table')
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    suggested_by = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    category = relationship('Category')
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    group = relationship('Group')
    is_deleted = Column(Boolean, default=False, nullable=False)
    was_selected = Column(Boolean, default=False, nullable=False)
    select_timestamp = Column(DateTime)
    insert_timestamp = Column(DateTime, default=datetime.utcnow)
    deleted_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    logger.info('Activities table created')

class MasterPassword(Base):
    """
    Model for storing the master password.

    Attributes:
        id (int): The unique identifier for the master password entry.
        password (str): The master password stored in the database.
        insert_timestamp (datetime): Datetime when this row was inserted.
        deleted_timestamp (datetime): Datetime when this row was deleted.
        updated_timestamp (datetime): Datetime when this row was last updated.
    """
    __tablename__ = 'master_password'
    logger.info('Creating master_password table')
    id = Column(Integer, primary_key=True)
    password_hash = Column(String, nullable=False)
    insert_timestamp = Column(DateTime, default=datetime.utcnow)
    deleted_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    logger.info('Master_password table created')

class DatabaseConnections:    
    def __init__(self):
        """
        Initializes the DatabaseConnections object.

        This method initializes the DatabaseConnections object with default values for its attributes.

        Returns:
            None
        """
        self.app_db_engine = None
        self.master_password_engine = None
        self.app_db_connection_session = None
        self.master_passwd_session = None

    def create_all_tables(self):
        """
        Create all tables in the database.
        """
        try:
            logger.info('Creating all tables')
            Base.metadata.create_all(self.get_engine())
            logger.info('All tables created')
        except Exception as e:
            logger.exception('An error occurred while creating all tables: %s', e)
            raise PickForMeException(e) from e
    
    def get_engine(self):
        """
        Returns a SQLAlchemy engine object that connects to the application database.
        """
        logger.info('Connecting to the application database')
        try:
            if self.app_db_engine is None:
                logger.info('Creating new connection to the application database')
                self.app_db_engine = create_engine(DATABASE_URL, connect_args={"timeout": 30})
                logger.info('Created application engine, connected to the application database')
            return self.app_db_engine
        except Exception as e:
            logger.exception('An error occurred while connecting to the application database: %s', e)
            raise PickForMeException(e) from e

    def get_db_connection_session(self, session_for=None):
        """
        Returns a SQLAlchemy session object that connects to the application database.
        """
        logger.info('Creating db session for: %s', session_for)
        try:
            if self.app_db_connection_session is None:
                logger.info('Creating new db session')
                self.app_db_connection_session = scoped_session(sessionmaker(bind=self.get_engine()))
                logger.info('Created new db session')
            else:
                logger.info('Db session already exists')
            return self.app_db_connection_session
        except Exception as e:
            logger.exception('An error occurred while creating the db session: %s', e)
            raise PickForMeException(e) from e
        
