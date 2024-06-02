def findDigits(number):
    result = 0
    for letter in list(str(number)):
        num = int(letter)
        try:
            if number % num == 0:
                result+=1
        except ZeroDivisionError as err:
            pass
    return result
    
print(findDigits(1012))