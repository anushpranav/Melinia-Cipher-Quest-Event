import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_noisy_homicide_records(n_records):
    # Initialize lists to store data
    records = []
    
    # Define possible values for categorical features based on your sample
    states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", 
              "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
              "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
              "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
              "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
              "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
              "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
              "Wisconsin", "Wyoming"]
    
    agency_types = ["Municipal police", "County police", "Sheriff", "State police", "Special police", 
                   "Constable", "Federal agency", "Other state agency", "Other"]
    
    sources = ["FBI", "Local agency", "State agency", "Other"]
    
    solved_options = ["Yes", "No", "Unknown"]
    
    years = [str(y) for y in range(1950, 2025)]  # Pre-convert to strings
    
    months = ["January", "February", "March", "April", "May", "June", "July", 
              "August", "September", "October", "November", "December"]
    
    action_types = ["Normal update", "Adjustment", "Deletion", "Exceptional clearance", "Unfounded"]
    
    homicide_types = ["Murder and non-negligent manslaughter", "Negligent manslaughter", 
                     "Justifiable homicide", "Voluntary manslaughter", "Involuntary manslaughter"]
    
    situations = ["Single victim/single offender", "Single victim/unknown offender", 
                 "Single victim/multiple offenders", "Multiple victims/single offender",
                 "Multiple victims/multiple offenders", "Multiple victims/unknown offender"]
    
    sexes = ["Male", "Female", "Unknown"]
    
    races = ["White", "Black", "American Indian or Alaskan Native", "Asian", 
            "Native Hawaiian or Pacific Islander", "Unknown"]
    
    ethnics = ["Hispanic or Latino", "Not Hispanic or Latino", "Unknown or not reported"]
    
    weapons = ["Handgun - pistol, revolver, etc", "Rifle", "Shotgun", "Other firearm", 
              "Knife or cutting instrument", "Blunt object", "Personal weapons (hands, feet, etc.)",
              "Poison", "Pushed or thrown out window", "Explosives", "Fire", "Narcotics and drugs",
              "Drowning", "Strangulation - hanging", "Asphyxiation", "Other weapon or not stated"]
    
    relationships = ["Husband", "Wife", "Mother", "Father", "Son", "Daughter", "Brother", "Sister",
                    "In-law", "Stepfather", "Stepmother", "Stepson", "Stepdaughter", "Other family",
                    "Neighbor", "Acquaintance", "Boyfriend", "Girlfriend", "Ex-husband", "Ex-wife",
                    "Friend", "Other - known to victim", "Stranger", "Relationship not determined"]
    
    circumstances = ["Rape", "Robbery", "Burglary", "Larceny", "Motor vehicle theft", 
                    "Arson", "Prostitution", "Other sex offense", "Narcotic drug laws",
                    "Gambling", "Other - not specified", "Suspected felony type unknown", 
                    "Lover's triangle", "Child killed by babysitter", "Brawl due to alcohol",
                    "Brawl due to drugs", "Argument over money or property", "Other arguments",
                    "Gangland killing", "Juvenile gang killing", "Institutional killing",
                    "Sniper attack", "Victim shot in hunting accident", "Gun-cleaning death",
                    "Children playing with gun", "Other negligent handling of gun",
                    "Other negligent killing", "Other", "Unknown or not reported"]
    
    # Cities by state for more realistic data
    cities_by_state = {
        "Alaska": ["Anchorage", "Fairbanks", "Juneau", "Sitka", "Ketchikan"],
        "Alabama": ["Birmingham", "Montgomery", "Mobile", "Huntsville", "Tuscaloosa"],
        "California": ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "Oakland"],
        # Add more as needed for other states
    }
    
    # For states not explicitly defined, use a default list
    default_cities = ["Springfield", "Franklin", "Clinton", "Georgetown", "Salem", "Madison", "Washington"]
    
    # Generate records
    for i in range(n_records):
        # Create noisy records
        year = random.choice(years)  # Already a string
        month = random.choice(months)
        state = random.choice(states)
        
        # Get cities for this state or use default
        if state in cities_by_state:
            city = random.choice(cities_by_state[state])
        else:
            city = random.choice(default_cities)
            
        # Create a made-up but realistic ORI (Originating Agency Identifier)
        state_code = state[:2].upper()
        ori = f"{state_code}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
        
        # Generate realistic CNTYFIPS (County FIPS code)
        county_fips = f"{city}, {state}"
        
        # Create unique incident ID - ensure it's a string
        incident_num = str(random.randint(1, 20))
        
        # Generate a unique ID that follows the pattern in your data
        unique_id = f"{year}{month[:3].lower()}{int(incident_num):03d}{ori}"
        
        # Determine ages with potential noise/outliers - ensure they're strings
        vic_age = str(max(0, min(120, int(np.random.normal(35, 15)))))
        
        # Sometimes make offender age missing or add noise
        if random.random() < 0.15:  # 15% chance of unknown
            off_age = "Unknown"
        else:
            # Add some correlation with victim age, but with noise
            # Convert vic_age to float for calculation, then back to string
            temp_vic_age = float(vic_age) if vic_age.isdigit() else 35.0
            off_age = str(max(12, min(90, int(temp_vic_age * random.uniform(0.7, 1.3)))))
        
        # Randomly decide whether ages should be suspicious/noisy
        if random.random() < 0.05:  # 5% chance of suspicious age
            if random.random() < 0.5:
                vic_age = str(random.randint(100, 130))
            else:
                off_age = str(random.randint(4, 10))
        
        # Sometimes introduce conflicting information (e.g., unsolved case with offender details)
        solved = random.choice(solved_options)
        if solved == "No" and random.random() < 0.7:
            # Unsolved case should typically have unknown offender details
            off_sex = "Unknown"
            off_race = "Unknown"
            off_ethnic = "Unknown or not reported"
        else:
            off_sex = random.choice(sexes)
            off_race = random.choice(races)
            off_ethnic = random.choice(ethnics)
            
        # Create inconsistencies in relationship and situation fields
        situation = random.choice(situations)
        relationship = random.choice(relationships)
        
        # Create inconsistency between situation and relationship
        if "unknown offender" in situation.lower() and relationship != "Relationship not determined" and random.random() < 0.8:
            # This creates noise - having relationship info despite unknown offender
            pass
        
        # Deliberately introduce some typos or formatting issues in categorical fields
        if random.random() < 0.05:  # 5% chance of typo
            weapon = random.choice(weapons)
            if " " in weapon:
                parts = weapon.split(" ", 1)
                weapon = parts[0] + " " + parts[1].replace(" ", "")
        else:
            weapon = random.choice(weapons)
            
        # Make victim and offender counts as strings
        vic_count = "0"
        off_count = "0"
        if random.random() < 0.1:  # 10% chance
            vic_count = "0"  # Still "0" as string
            off_count = "0"  # Still "0" as string
        elif random.random() < 0.05:  # 5% chance of inconsistency
            # Multiple victims situation but single victim count
            if "multiple victims" in situation.lower():
                vic_count = "1"  # String "1"
            else:
                vic_count = "0"  # String "0"
            off_count = "0"  # String "0"
            
        # Generate file date (sometimes in incorrect format or future date)
        if random.random() < 0.05:  # 5% chance of wrong format
            file_date = f"{random.randint(1, 12)}{random.randint(1, 30)}{str(random.randint(70, 99))}"
        elif random.random() < 0.02:  # 2% chance of future date
            file_date = f"{random.randint(1, 12)}{random.randint(1, 30)}{random.randint(25, 30)}"
        else:
            # Format as in your sample: MMDDYY
            file_date = f"{random.randint(1, 12):02d}{random.randint(1, 28):02d}{str(random.randint(70, 99))}"
            
        # Create record - all fields as strings
        record = {
            "ID": unique_id,
            "CNTYFIPS": county_fips,
            "Ori": ori,
            "State": state,
            "Agency": city,
            "Agentype": random.choice(agency_types),
            "Source": random.choice(sources),
            "Solved": solved,
            "Year": year,  # Already a string
            "Month": month,
            "Incident": incident_num,  # Already a string
            "ActionType": random.choice(action_types),
            "Homicide": random.choice(homicide_types),
            "Situation": situation,
            "VicAge": vic_age,  # Already a string
            "VicSex": random.choice(sexes),
            "VicRace": random.choice(races),
            "VicEthnic": random.choice(ethnics),
            "OffAge": off_age,  # Already a string
            "OffSex": off_sex,
            "OffRace": off_race,
            "OffEthnic": off_ethnic,
            "Weapon": weapon,
            "Relationship": relationship,
            "Circumstance": random.choice(circumstances),
            "Subcircum": "",  # Empty string
            "VicCount": vic_count,  # String
            "OffCount": off_count,  # String
            "FileDate": file_date,
            "MSA": f"{city}, {state}"
        }
        
        records.append(record)
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Ensure ALL columns are explicitly converted to strings
    for col in df.columns:
        df[col] = df[col].astype(str)
    
    return df

# Generate the noisy records
noisy_records = generate_noisy_homicide_records(10000)

# Double check for mixed types in each column - more robust checking
def check_column_types(df):
    issues = []
    for col in df.columns:
        # Check each value's type directly
        types = set(type(val).__name__ for val in df[col].values)
        if len(types) > 1:
            issues.append(f"Column '{col}' has mixed types: {types}")
    return issues

# Verify no mixed types
type_issues = check_column_types(noisy_records)
if type_issues:
    print("WARNING: Mixed types detected:")
    for issue in type_issues:
        print(f"  - {issue}")
    
    # Fix more aggressively by forcing string conversion
    for col in noisy_records.columns:
        noisy_records[col] = noisy_records[col].apply(lambda x: str(x))
    
    print("\nFixed all columns by explicitly converting each value to string.")
else:
    print("All columns have consistent string types.")

# Final verification - check for any non-string values that might have slipped through
for col in noisy_records.columns:
    if not all(isinstance(val, str) for val in noisy_records[col].values):
        print(f"WARNING: Non-string values still present in column '{col}'")
        # Force conversion once more
        noisy_records[col] = noisy_records[col].apply(str)

# Save to CSV
noisy_records.to_csv("noisy_homicide_records.csv", index=False)

# Display the first few rows
print("\nSample of generated data:")
print(noisy_records.head())