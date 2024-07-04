
HELP_STRING_GROUPS = """
    Available group operations:
    
    list          List all groups.
    add           Add a new group.
    delete        Delete an existing group.
    select        Select a group to manage categories and activities.
    back          Go back to the main menu.
    quit          Exit the tool.
                """
                
HELP_STRING_CATEGORIES = """
    Available category operations:
    
    list          List all categories.
    add           Add a new category.
    delete        Delete an existing category.
    select        Select a category to manage activities.
    back          Go back to the previous menu.
    quit          Exit the tool.
                """

HELP_STRING_ACTIVITIES = """
    Available activity operations:
    
    current       View current selections
    list          List all activities.
    add           Add a new activity.
    delete        Delete an existing activity.
    pick          Pick a random activity.
    back          Go back to the previous menu.
    quit          Exit the tool.
                """

HELP_STRING_NO_INIT = """
    Available initialization operations:
    
    init          Initialize the tool and configure master password.
    quit          Exit the tool.
                """
                
HELP_STRING_TOOL_INIT = """
    Available operations:
    
    clear_db      Clear all data from the database.
    initapp       Manage groups.
    quit          Exit the tool.
                """
                
DATABASE_NAME = 'pickforme.db'
DATABASE_LOCATION = 'app_database'

DATABASE_TABLES = [
    'activities',
    'categories',
    'groups',
    'master_password'
]

SUPPORTED_GROUP_OPERATIONS = [
    'list',
    'add',
    'delete',
    'select',
    'back',
    'quit',
    'help'
]

SUPPORTED_ACTIVITY_OPERATIONS = [
    'current',
    'list',
    'add',
    'delete',
    'pick',
    'back',
    'quit',
    'help'
]

SUPPORTED_CATEGORY_OPERATIONS = [
    'list',
    'add',
    'delete',
    'select',
    'back',
    'quit',
    'help'
] 

SUPPORTED_TOOL_INIT_OPERATIONS = [
    'clear_db',
    'initapp',
    'quit'
]

SUPPORTED_NO_INIT_OPERATIONS = [
    'init',
    'quit'
]

