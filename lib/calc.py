OPERATORS = {
    '+': lambda a, b : a + b,
    '-': lambda a, b : a - b,
    '*': lambda a, b : a * b,
    '**': lambda a, b : a ** b,
    '/': lambda a, b : a / b
}

def calculate(command):
    command_splitted = command.split(',')

    arg1 = command_splitted[0]
    operator = command_splitted[1]
    arg2 = command_splitted[2]

    if operator in OPERATORS:
        return OPERATORS[operator](int(arg1), int(arg2)), 0, 'OK'
    else:
        return -1, 11, 'Некорректный оператор'
