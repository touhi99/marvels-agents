import os 

def check_data_exists(directory="data"):
    """Check if there is any data file in the specified directory."""
    return any(os.path.isfile(os.path.join(directory, f)) for f in os.listdir(directory))