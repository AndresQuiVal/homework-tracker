"""
Defines general settings, attributes and functions for the proyect
"""
from os import system, name
from helpers import db

VERSION = "1.0"
TASKS_FIELDS = ['activity','estimated_time','deliver_date']
LAPSE_TASKS_FIELDS = ['name', 'start', 'end']
TASKS_FILE_NAME = 'tasks.csv'
LAPSE_TASLS_FILE_NAME = 'lapse_tasks.csv'

def set_general_config():
    """
    Sets general configuration for the project
    """
    db.create_file_if_doesnt_exist(TASKS_FILE_NAME, TASKS_FIELDS) 
    db.create_file_if_doesnt_exist(LAPSE_TASLS_FILE_NAME, LAPSE_TASKS_FIELDS)

def clear_console():
    """
    Cleans the console completely
    """
    if name == 'nt': # Windows 
        system('cls')
    else: # Unix / Linux
        system('clear')
