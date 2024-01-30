import pandas as pd
import os, sys
import shutil
import zstandard

import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# current_dir = os.getcwd()
# root_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, root_dir)


class LocalFilesManager:
    
    def __init__(self, file_types, dir_name=None) -> None:
        self.__current_dir = os.getcwd()
        self.__root_dir = os.path.abspath(os.path.join(self.__current_dir, '..'))
        sys.path.insert(0, self.__root_dir)
        
        if type(file_types) == str:
            self.__file_types = [file_types]
        else:
            self.__file_types = file_types
            
        self.__dir_name = dir_name
        if self.__dir_name:
            self.__target_dir = os.path.abspath(os.path.join(self.__current_dir, self.__dir_name))
        else:
            self.__target_dir = self.__current_dir
        
        self.__files_hash = dict()
        
    def find_all_files(self):
        
        for file_type in self.__file_types:
            for path, sub_dirs, files in os.walk(self.__target_dir):
                for file in files:
                    if(file.endswith('.' + file_type) or 
                        file.endswith('.' + file_type.lower()) or 
                        file.endswith('.' + file_type.title()) or 
                        file.endswith('.' + file_type.upper())):
                        self.__files_hash[file] = os.path.join(path, file)
                        
        logging.info(f"Found {len(self.__files_hash)} files.")  
                        
        return self.__files_hash
    
    def find_files_with_keywords(self, inclusive_keywords=None, exclusive_keywords=None):
        
        new_files_hash = self.__files_hash.copy()
        file_keys = self.__files_hash.keys()
        
        if inclusive_keywords:
            if type(inclusive_keywords) == str:
                inclusive_keywords = [inclusive_keywords]
                
            for key in file_keys:
                for ik in inclusive_keywords:
                    if ik not in key:
                        new_files_hash.pop(key)
                    
        if exclusive_keywords:
            if type(exclusive_keywords) == str:
                exclusive_keywords = [exclusive_keywords]
                
            for key in file_keys:
                for ek in exclusive_keywords:
                    if ek in key:
                        new_files_hash.pop(key)
                        
        logging.info(f"There are {len(new_files_hash)} files matched keywords.")
        return new_files_hash
    
    
    @staticmethod
    def concat_txt_files(files_hash, output_file):
    
        # with open(output_file, 'w') as outfile:
        #     for key in files_hash.keys():
        #         with open(files_hash[key]) as infile:
        #             for line in infile:
        #                 outfile.write(line)
                        
        with open(output_file, 'wb') as outfile:
            for key in files_hash.keys():
                with open(files_hash[key], 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)
    
        
    @property
    def current_dir(self):
        return self.__current_dir
    
    @property
    def root_dir(self):
        return self.__root_dir
    
    @property
    def target_dir(self):
        return self.__target_dir
        
            
        


