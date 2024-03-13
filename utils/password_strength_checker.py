import string
def check_password_strength(password):
    length = len(password)
    has_uppercase = any(c.isupper() for c in password)
    has_lowercase = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = 0

    # Length
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    # Character types
    if has_uppercase:
        score += 1
    if has_lowercase:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1

    return score