import hashlib

def generate_hash_id(first_name, last_name, dob):
    """
    Generates a unique hash ID based on the provided first name, last name, and date of birth.
    
    Args:
        first_name (str): The person's first name.
        last_name (str): The person's last name.
        dob (str): The person's date of birth in the format "DD-MM-YYYY".
    
    Returns:
        str: The generated hash ID.
    """
    # Split the date of birth into its components
    day, month, year = dob.split("-")
    
    # Concatenate the components in the desired order
    input_string = f"{first_name.lower()}{last_name.lower()}{day}{month}{year}"
    
    # Compute the SHA-256 hash and return the hexadecimal string
    hash_object = hashlib.sha256(input_string.encode())
    hash_id = hash_object.hexdigest()
    
    # Print the length of the hash ID
    print(f"The length of the hash ID is: {len(hash_id)}")
    
    return hash_id

# Get user input
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
dob = input("Enter your date of birth in the format DD-MM-YYYY: ")

# Generate the hash ID
hash_id = generate_hash_id(first_name, last_name, dob)
print(f"Your hash ID is: {hash_id}")