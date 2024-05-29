def rev(number):
    numberinlist = []
    for digit in str(number):
        numberinlist.append(digit)
    numberinlist.reverse()
    result = ""
    for digit in numberinlist:
        result+=digit
    return int(result)

def beautifulDays(startingDay, endingDay, divisor):
    resultDays = 0
    for day in range(startingDay,endingDay+1):
        if ((day - rev(day))/divisor).is_integer():
            resultDays+=1
    return resultDays
  
print(beautifulDays(20, 23, 6))

