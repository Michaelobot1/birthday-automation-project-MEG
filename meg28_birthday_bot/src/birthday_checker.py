import datetime
import logging

def check_birthdays(records):
    """
    Scans the records and returns a list of dictionaries 
    representing the people celebrating TODAY.
    """
    today = datetime.datetime.now()
    current_day = today.day
    current_month = today.month
    
    celebrants = []

    for person in records:
        dob_str = str(person.get('date_of_birth', ''))
        
        # Skip empty DOBs
        if not dob_str or dob_str.lower() == 'nan':
            continue

        try:
            # Parse DD/MM/YYYY
            # Note: Google Forms usually exports dates as YYYY-MM-DD or DD/MM/YYYY depending on locale.
            # We will try to be robust. 
            
            # Assuming DD/MM/YYYY as per prompt
            if '/' in dob_str:
                parts = dob_str.split('/')
                b_day = int(parts[0])
                b_month = int(parts[1])
            elif '-' in dob_str:
                # Handle YYYY-MM-DD just in case
                parts = dob_str.split('-')
                b_month = int(parts[1])
                b_day = int(parts[2])
            else:
                logging.warning(f"Skipping invalid date format: {dob_str} for {person.get('first_name')}")
                continue

            # CHECK MATCH
            if b_day == current_day and b_month == current_month:
                celebrants.append(person)

        except (ValueError, IndexError) as e:
            logging.warning(f"Error parsing date {dob_str} for {person.get('first_name')}: {e}")
            continue

    if celebrants:
        logging.info(f"🎉 Found {len(celebrants)} birthday(s) today!")
    else:
        logging.info("No birthdays found today.")

    return celebrants

# --- Test Block ---
if __name__ == "__main__":
    # Mock data representing a CSV loaded record
    mock_records = [
        {'first_name': 'Michael', 'date_of_birth': '25/12/2000'}, # Should match if today is Dec 25
        {'first_name': 'Jane', 'date_of_birth': '01/01/2002'},    # Should not match
    ]
    
    # FORCE DATE FOR TESTING (Uncomment to test specific dates)
    # import unittest.mock
    # with unittest.mock.patch('datetime.datetime') as mock_date:
    #     mock_date.now.return_value = datetime.datetime(2025, 12, 25)
    #     mock_date.side_effect = datetime.datetime
    
    # Running normally uses system time
    print(check_birthdays(mock_records))