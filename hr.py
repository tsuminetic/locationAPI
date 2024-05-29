import math

def viralAdvertising(days):
    toShare=5
    totalLikers=0
    for day in range(days):
        likers=math.floor(toShare/2)
        totalLikers+=likers
        toShare = likers*3
    return totalLikers


print(viralAdvertising(5))