def is_positive_number(value):
    try:
        number_string = float(value)
        print(number_string)
    except ValueError:
        print('error')
        return False
    return number_string > 0.0