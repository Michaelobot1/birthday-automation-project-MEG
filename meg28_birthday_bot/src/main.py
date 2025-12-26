import os
from csv_reader import load_csv_data
from birthday_checker import check_birthdays
# IMPORT YOUR GENERATOR
from poster_generator import generate_birthday_poster 

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'birthdays.csv')

# ASSET PATHS - This is where you tell it to use Poppins
TEMPLATE_PATH = os.path.join(BASE_DIR, 'assets', 'poster_template.png')
FONT_PATH = os.path.join(BASE_DIR, 'assets', 'Poppins-Bold.ttf')
OUTPUT_DIR = os.path.join(BASE_DIR, 'posters', 'generated')

def run_bot():
    print("--- MEG 28 BIRTHDAY BOT STARTING ---")
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Load Data
    records = load_csv_data(CSV_PATH)
    if not records:
        print("❌ No records found or CSV error. Exiting.")
        return

    # 2. Check Birthdays
    celebrants = check_birthdays(records)
    
    if not celebrants:
        print("🎂 MEG 28 Birthday Bot: No birthdays today.")
        return

    # 3. Handle Celebrants
    for person in celebrants:
        name = f"{person['first_name']}_{person['surname']}"
        print(f"✅ Processing Birthday for: {name}")
        
        # Define the output file name for this specific person
        output_file = os.path.join(OUTPUT_DIR, f"{name}_birthday.jpg")
        
        # CALL THE GENERATOR
        poster_path = generate_birthday_poster(
            person=person,
            template_path=TEMPLATE_PATH,
            output_path=output_file,
            font_path=FONT_PATH
        )

        if poster_path:
            print(f"✨ Poster saved to: {poster_path}")
        else:
            print(f"❌ Failed to generate poster for {name}")

if __name__ == "__main__":
    run_bot()