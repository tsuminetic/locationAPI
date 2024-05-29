def saveThePrisoner(prisoners, candies, startFrom):
    return ((startFrom+candies-2)%prisoners)+1
    
print(saveThePrisoner(4,6,2))