import requests

def check_password_breach(password):
    url = f"https://api.pwnedpasswords.com/range/{password[:5]}"
    response = requests.get(url)
    hashes = response.text.splitlines()
    for hash in hashes:
        if password[5:].upper() in hash:
            return True
    return False