'''
Created on 2015年7月19日

@author: HCY
'''
import math

# 影片评价数据集
critics = {
'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Hcy': {'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}}

# 返回一个有关person1与person2的基于距离的相似度评价
def sim_distance(prefs, person1, person2):
    # 得到shared_items列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    # 如果两者没有共同评价的影片则返回0
    if len(si) == 0:return 0
    # 计算欧几里德距离(多维空间中两点的距离，如两点记为(p1,p2,p3),(q1,q2,q3),即((p1-q1)**2+(p2-q2)**2+(p3-q3)**2)**0.5)
    distince = math.sqrt(sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]]))
    
    return 1 / (1 + distince)

# 返回p1和p2的皮尔逊相关系数
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]: 
        if item in prefs[p2]: si[item] = 1
    # if they are no ratings in common, return 0
    if len(si) == 0: return 0
    # Sum calculations
    n = len(si)
    # Sums of all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sums of the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])    
    # Sum of the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / n)
    den = math.sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den
    return r

# Returns the best matches for person from the prefs dictionary. 
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs, person, other),other) for other in prefs if other!=person]
    scores.sort(reverse=True)
    return scores[0:n]
#根据影片评分的加权平均值，推荐影片    
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    #对其他人循环处理
    for other in prefs:
        if other == person: continue
        sim=similarity(prefs, person, other)
        #忽略相似度<=0的人
        if sim <=0:continue
        
        for item in prefs[other]:
            #对自己还未曾看过的影片进行评分
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                #累加同一部影片的相似度*评价值，{'Just My Luck',12.89}
                totals[item]+=prefs[other][item]*sim
                #累加同一部影片的相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim
    #每部影片的rank值，以元组的形式存放在列表中
    rangkings=[(total/simSums[item]) for total,item in totals.items()]
    
    rangkings.sort(reverse=True)
    
    return rangkings



















