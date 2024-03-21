import re

class Variable:
    def __init__(self, value):
        self.value = value

class NumberVariable(Variable):
    def __str__(self):
        return f"Number:[{self.value}]"

class SeparatorVariable(Variable):
    def __str__(self):
        return f"Separator:[]"

class CommaVariable(Variable):
    def __str__(self):
        return f"Comma:[, ]"

class SpaceVariable(Variable):
    def __str__(self):
        return f"Space:[{self.value}]"

class PeriodVariable(Variable):
    def __str__(self):
        return f"Period:[. ]"

class DecpointVariable(Variable):
    def __str__(self):
        return f"Decpoint:[.]"

class DecnumVariable(Variable):
    def __str__(self):
        return f"Decnum:[{self.value}]"

def classify_variables(input_string):
    variables = []
    parts = re.split(r'(,|\s|\.)', input_string)  # split by comma, space, and period, keeping them
    for i, part in enumerate(parts):
        if part == ',':
            # check if it's a separator variable
            if (i > 0 and isinstance(variables[-1], NumberVariable) and
                i < len(parts) - 1 and re.match(r'^\d{3}$', parts[i+1]) is not None):
                variables.append(SeparatorVariable(part))
            else:
                variables.append(CommaVariable(part))
        elif part == ' ':
            # check if the last stored variable was a SpaceVariable
            if not (variables and isinstance(variables[-1], SpaceVariable)):
                variables.append(SpaceVariable(part))
        elif part == '.':
            # check if it's a decpoint variable
            if (i > 0 and isinstance(variables[-1], NumberVariable) and
                i < len(parts) - 1 and re.match(r'^\d+$', parts[i+1]) is not None):
                variables.append(DecpointVariable(part))
            else:
                variables.append(PeriodVariable(part))
        elif re.match(r'\d+$', part) is not None:
            # check if it's a decnum variable
            if (i > 0 and isinstance(variables[-1], DecpointVariable)):
                variables.append(DecnumVariable(part))
            else:
                variables.append(NumberVariable(part))
    return variables

def main():
    while True:
        user_input = input("Enter your input or ~ to quit: ")
        if user_input == '~':
            break
        variables = classify_variables(user_input)
        print(''.join(str(variable) for variable in variables))
        print('Translation:')
        print(''.join(str(variable).split(':')[1].strip('[]') for variable in variables))

if __name__ == "__main__":
    main()