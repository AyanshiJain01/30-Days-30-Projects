import string

try:
    import pyperclip
except ImportError:
    pyperclip = None


def check_strength(password):
    score = 0

    has_lower = any(ch.islower() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_symbol = any(ch in string.punctuation for ch in password)

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Medium"
    else:
        return "Strong"
    

def give_suggestions(password):
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if len(password) < 12:
        suggestions.append("Use 12 or more characters for better security")
    if not any(ch.islower() for ch in password):
        suggestions.append("Add lowercase letters.")
    if not any(ch.isupper() for ch in password):
        suggestions.append("Add uppercase letters.")
    if not any(ch.isdigit() for ch in password):
        suggestions.append("Add numbers.")
    if not any(ch in string.punctuation for ch in password):
        suggestions.append("Add special characters.")

    return suggestions

def copy_clipboard(password):
    if pyperclip is None:
        print("\nClipboard feature not available.")
        print("Install it using: pip install pyperclip")
    else:
        pyperclip.copy(password)
        print("\nPassword copied to clipboard!")


def main():
    print("\n ==== Password Strength Checker ====")

    password = input("Enter your Password: ")

    strength = check_strength(password)
    suggestions = give_suggestions(password)

    print("\nPassword: ",password)
    print("Strength: ",strength)

    if suggestions:
        print("\nSuggestions: ")
        for suggestion in suggestions:
            print("-", suggestion)
    else:
        print("\nGreat ! Your password is strong.")

    copy_choice = input("\nDo you want to copy this password? (y/n): ").lower()

    if copy_choice == "y":
        copy_clipboard(password)
    else:
        print("Password not copied.")

main()
