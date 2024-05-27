
def climbingLeaderboard(ranked, player):
    unique_ranks = sorted(set(ranked), reverse=True)
    results = []
    l = len(unique_ranks)
    for score in player:
        while l > 0 and score >= unique_ranks[l - 1]:
            l -= 1
        results.append(l + 1)
    
    return results

print(climbingLeaderboard([100,100,50,40,40,20,10],[5,25,50,120]))