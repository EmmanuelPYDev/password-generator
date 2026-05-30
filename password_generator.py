import secrets
import string
from datetime import datetime

def generate_password(lenght, use_numbers, use_symbols):
    password_chars = []
    
    password_chars.append(secrets.choice(string.ascii_letters))
    
    if use_numbers:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))
    
    characters = string.ascii_letters
    
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation
        
    while len(password_chars) < lenght:
        password_chars.append(secrets.choice(characters))
        
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)

def check_strenght(password):
    score = 0 
    if len(password) >= 8:
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(not char.isalnum() for char in password):
        score += 1
        
    if score <= 2:
        return "Weak"
    if score == 3:
        return "Medium"
    if score == 4:
        return "Strong"
    else:
        return "Very Strong"
    
def save_passwords(passwords):
    try:
        with open("passwords.txt", "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"==== Batch Generated {timestamp}====\n")
            for password in passwords:
                file.write(password + "\n")
        print(f"[*] \nPasswords saved to passwords.txt")
    except OSError as e:
        print(f"Fatal: could not save passwords: {e}")  
           
def main():
    print("=" * 40)
    print("     Password Generator")
    print("=" * 40)
   
    while True:
        try:
            lenght = int(input("Enter Password lenght: "))
            if lenght < 4:
                print(f"[*] Password lenght must be at least 4")
                continue
            break
            
        except ValueError:
            print(f"[!] Please enter a valid number")
    
    while True:            
        try:
            amount = int(input("Enter number of password to be generated: "))
            if amount < 1:
                print(f"[!] amount must be atleast 1")
                continue
            break
        except ValueError:
            print(f"[*] Enter a vaid amount")
        
    numbers = input("Include numbers? (yes/no): ").strip().lower()
    symbols = input("include symbols? (yes/no): ").strip().lower()
    
    use_numbers = numbers in ["yes", "y"]
    use_symbols = symbols in ["yes", "y"]
    
    passwords = []
    strong_count = 0
    very_strong_count = 0
    
    print(f"[*] Generated password\n")
    for i in range(amount):
        password = generate_password(lenght, use_numbers, use_symbols)
                       
        strenght = check_strenght(password)
        if strenght == "Strong":
            strong_count += 1
        elif strenght == "Very Strong":
            very_strong_count += 1 
            
        passwords.append(f"{password} ({strenght})")
               
        print(f"{i + 1} {password} "
            f"({strenght})")  
                
    print("\n==== Statistics ====")
    print(f"[*] Strong Password: {strong_count}")
    print(f"[*] Very Strong Passwords: {very_strong_count}")
        
    save_choice = input("\n Save passwords to a file? (yes/no): ").strip().lower()
    
    if save_choice in ["yes", "y"]:
        save_passwords(passwords)   
   
if __name__ == "__main__":
    main()    
