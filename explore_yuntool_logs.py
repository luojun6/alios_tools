import pandas as pd
import os, sys

# current_dir = os.path.dirname(__file__)
current_dir = os.getcwd()
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, root_dir)

def get_file_by_suffix(suffix_name, dir_name=None, inclusive_keyword=None, exclusive_keyword=None):
    if dir_name:
        target_dir = os.path.abspath(os.path.join(current_dir, dir_name))
    else:
        target_dir = current_dir
        
    if type(suffix_name) is not str:
        suffix_name = str(suffix_name)
        
    paths_hash = dict()
    
    if inclusive_keyword:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if((file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper()))) and (inclusive_keyword in file):
                    paths_hash[file] = os.path.join(path, file)
    
    elif exclusive_keyword:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if((file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper()))) and (exclusive_keyword not in file):
                    paths_hash[file] = os.path.join(path, file)
                    
    else:
        for path, sub_dirs, files in os.walk(target_dir):
            for file in files:
                if(file.endswith('.' + suffix_name) or 
                    file.endswith('.' + suffix_name.lower()) or 
                    file.endswith('.' + suffix_name.title()) or 
                    file.endswith('.' + suffix_name.upper())):
                    paths_hash[file] = os.path.join(path, file)
                
    return paths_hash

log_type_col = "log_type"

cpu = "cpu"
date = 'date'
timestamp = 'timestamp'
appid = 'appid'
ctxid = 'ctxid'
level = "level"
payload = 'payload'
payload_ext = "payload_ext"
cols = [date, timestamp, appid, ctxid, level, payload, payload_ext]
rename_cols = dict()
for i in range(len(cols) - 1):
    rename_cols[i] = cols[i]

rename_zst_cols = dict()
zst_cols = [date, timestamp, cpu, appid, ctxid, level, payload, payload_ext]
for i in range(len(zst_cols) - 1):
    rename_zst_cols[i] = zst_cols[i]


def extract_zst_files(dir_name, log_type):
    all_gz_dict = get_file_by_suffix("txt.zst", dir_name=dir_name,  inclusive_keyword=log_type)
    count = len(all_gz_dict)
    i = 0
    print(f"Found {count} txt.zst files.")
    for key in all_gz_dict.keys():
        i += 1
        try:
            print(f"Extracting {key} with completion {i}/{count}.")
            log = pd.read_fwf(all_gz_dict[key], 
                              compression={'method': 'zstd'},
                              # compression="gzip", 
                              # skiprows=3,
                              colspecs="infer", 
                              header=None,
                              encoding = "ISO-8859-1")
            file_path = os.path.join(dir_name, key.replace("txt.zst", "csv"))
            log.rename(columns=rename_zst_cols, inplace=True)
            log.to_csv(file_path, encoding = "ISO-8859-1", index=None)
        except pd.errors.EmptyDataError:
                print(f"Note: {key} was empty. Skipping.")
                continue # will skip the rest of the block and move to next file
    print("Extraction completed.")

def extract_gz_files(dir_name, log_type):
    all_gz_dict = get_file_by_suffix("txt.gz", dir_name=dir_name,  inclusive_keyword=log_type)
    count = len(all_gz_dict)
    i = 0
    print(f"Found {count} txt.gz files.")
    for key in all_gz_dict.keys():
        i += 1
        try:
            print(f"Extracting {key} with completion {i}/{count}.")
            log = pd.read_fwf(all_gz_dict[key], 
                                   compression="gzip", 
                                   skiprows=3,
                                   colspecs="infer", 
                                   header=None,
                                   encoding = "ISO-8859-1")
            file_path = os.path.join(dir_name, key.replace("txt.gz", "csv"))
            log.rename(columns=rename_cols, inplace=True)
#             log[log_type_col] = log_type
            log.to_csv(file_path, encoding = "ISO-8859-1", index=None)
        except pd.errors.EmptyDataError:
                print(f"Note: {key} was empty. Skipping.")
                continue # will skip the rest of the block and move to next file
    print("Extraction completed.")
    
def merge_log_csv_files(dir_name, inclusive_keyword=None):
    all_csv_dict = get_file_by_suffix("csv", dir_name=dir_name,  inclusive_keyword=inclusive_keyword)
    all_log = pd.DataFrame()
    count = len(all_csv_dict)
    i = 0
    print(f"Found {count} txt.gz files.")
    
    for key in all_csv_dict.keys():
        i += 1
        print(f"Merging {key} with completion {i}/{count}.")
        temp_log = pd.read_csv(all_csv_dict[key], encoding = "ISO-8859-1", low_memory=False)
        all_log = pd.concat([all_log, temp_log])
    all_log.sort_values(by=["timestamp"], inplace=True)
    print("Merging compeleted.")
    
    if inclusive_keyword is None:
        inclusive_keyword = "all_log"
    output_file_path = inclusive_keyword + ".csv"
    all_log.to_csv(output_file_path, encoding = "ISO-8859-1", index=None)
    return all_log