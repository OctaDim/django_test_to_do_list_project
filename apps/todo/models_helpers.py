import random


def create_default_description():
    random_value = random.randrange(1, 1_000_001)
    return f"THIS IS DEFAULT RANDOM VALUE NO. {random_value}"
