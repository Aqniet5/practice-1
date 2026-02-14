def solve(expression):
    # Mapping triplets to digits
    triplet_to_digit = {
        "ZER": "0",
        "ONE": "1",
        "TWO": "2",
        "THR": "3",
        "FOU": "4",
        "FIV": "5",
        "SIX": "6",
        "SEV": "7",
        "EIG": "8",
        "NIN": "9"
    }

    # Reverse mapping
    digit_to_triplet = {v: k for k, v in triplet_to_digit.items()}

    # Find operator
    if '+' in expression:
        operator = '+'
    elif '-' in expression:
        operator = '-'
    else:
        operator = '*'

    left, right = expression.split(operator)

    # Convert encoded number to normal number
    def decode(s):
        num = ""
        for i in range(0, len(s), 3):
            triplet = s[i:i+3]
            num += triplet_to_digit[triplet]
        return int(num)

    num1 = decode(left)
    num2 = decode(right)

    # Perform operation
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    else:
        result = num1 * num2

    # Convert result back
    result_str = str(result)
    encoded = ""
    for digit in result_str:
        encoded += digit_to_triplet[digit]

    return encoded


# Input
expression = input().strip()
print(solve(expression))
