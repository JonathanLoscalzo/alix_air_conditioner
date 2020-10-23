import os 

def get_location():
    DATA_DIR = '../data'
    DATA_DIR_PROCESSED = os.path.join(DATA_DIR,'processed')

    INTERMEDIATE_RESULTS = os.path.join(DATA_DIR_PROCESSED, '01-intermediate_results.parquet')
    GROUP_INTERMEDIATE_RESULTS = os.path.join(DATA_DIR_PROCESSED, '03-intermediate_group_result.parquet')

    CLEANED_DS = os.path.join(DATA_DIR_PROCESSED, '01-clean_fi_dataset.parquet')

    TRAIN_RAW_FILE = 'raw/Entrenamieto_ECI_2020.csv'
    VALIDATION_RAW_FILE = 'raw/Validacion_ECI_2020.csv'
    TEMPLATE_SUBMIT='raw/random_first_submit.csv'
    
    return DATA_DIR, DATA_DIR_PROCESSED, INTERMEDIATE_RESULTS, GROUP_INTERMEDIATE_RESULTS, CLEANED_DS , TRAIN_RAW_FILE, VALIDATION_RAW_FILE, TEMPLATE_SUBMIT