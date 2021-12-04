"""
Defines helpers for database manipulation
"""

import csv
import os

def create_file_if_doesnt_exist(file_name, headers):
    """
    Creates the .csv file if doesnt exist under data/ folder
    """
    if not os.path.exists(f'./data/{file_name}'): 
        with open(f'./data/{file_name}','w') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

