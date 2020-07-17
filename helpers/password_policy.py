def verify(password):
    rules = [
        lambda s: any(x.isupper() for x in password),   # must have at least one uppercase
        lambda s: any(x.islower() for x in password),   # must have at least one lowercase
        lambda s: any(x.isdigit() for x in password),   # must have at least one digit
        lambda s: len(s) >= 8                           # must be at least 8 characters
    ]

    if all(rule(password) for rule in rules):
        return True
    return False