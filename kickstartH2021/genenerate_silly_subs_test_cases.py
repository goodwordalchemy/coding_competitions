import random

N_test_cases = 100

MAX_SIZE = 100

digits = list("0123456789")

def generate_digit_string(length):
    return "".join(random.choices(digits, k=length))

for i in range(N_test_cases):
    length = random.randint(1,MAX_SIZE)
    if length == 0:
        continue
    result = generate_digit_string(length)

    print(length)
    print(result)


