import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_csv_data(filepath):
    """
    Reads the CSV and standardizes the column names.
    Returns a list of dictionaries (one per student).
    """
    try:
        df = pd.read_csv(filepath)
        
        # 1. Clean Column Names (Strip whitespace, lower case)
        df.columns = df.columns.str.strip().str.lower()
        
        # 2. Map Google Form headers to our Internal Keys
        # Adjust the 'right' side of this map to match your ACTUAL Google Form CSV headers exactly
        column_mapping = {
            'timestamp': 'timestamp',
            'email address': 'email',
            'first name': 'first_name',
            'surname': 'surname',
            'date of birth': 'date_of_birth', # Expecting DD/MM/YYYY
            'your hobbies': 'hobbies',
            'your best pal(s)': 'best_pals',
            'summarize mechanical engineering': 'me_summary',
            'preferred picture': 'picture_link' 
        }
        
        # Rename columns based on map; ignore columns not in map
        # We use a partial rename to be safe against extra columns
        df.rename(columns=column_mapping, inplace=True)
        
        # Filter to only keep the columns we need
        needed_cols = list(column_mapping.values())
        
        # Check if critical columns exist
        missing_cols = [col for col in needed_cols if col not in df.columns]
        if missing_cols:
            # In a real scenario, we might just log a warning if non-criticals are missing
            # But name and DOB are non-negotiable.
            if 'date_of_birth' in missing_cols or 'first_name' in missing_cols:
                raise ValueError(f"Critical columns missing in CSV: {missing_cols}")

        # Convert to list of dicts for easier Python handling
        records = df.to_dict('records')
        
        logging.info(f"Successfully loaded {len(records)} records from {filepath}")
        return records

    except FileNotFoundError:
        logging.error(f"CSV file not found at: {filepath}")
        return []
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")
        return []

# --- Test Block (Run this file directly to test) ---
if __name__ == "__main__":
    # Create a dummy CSV for testing
    dummy_data = """Timestamp,Email Address,First Name,Surname,Date of Birth,Your Hobbies,Your Best Pal(s),Summarize Mechanical Engineering,Preferred Picture
2023/12/01,test@gmail.com,Michael,Ojo,25/12/2000,Coding, Robotics,None,Hard but fun,http://drive.google.com/fake"""
    
    with open("../data/birthdays.csv", "w") as f:
        f.write(dummy_data)
        
    data = load_csv_data("../data/birthdays.csv")
    print(data)