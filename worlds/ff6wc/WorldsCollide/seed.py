SEED_LENGTH = 12

def generate_seed():
    import secrets, string
    alpha_digits = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alpha_digits) for i in range(SEED_LENGTH))

def seed_rng(seed = None, flags = ""):
    if seed is None:
        seed = generate_seed()

    import random
    random.seed(seed + flags)
    return seed
