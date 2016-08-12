# encoding: utf-8
'''
Created on 2015年7月19日

@author: HCY
'''
from recommendations import critics, sim_distance, sim_pearson
import recommendations
#print(critics['Lisa Rose']['Lady in the Water'])
print(critics['Hcy'])

print(recommendations.sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
print(recommendations.sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))

print(recommendations.topMatches(critics, 'Hcy',n=3,similarity=sim_pearson))
print(recommendations.topMatches(critics, 'Hcy',n=3,similarity=sim_distance))

print(recommendations.getRecommendations(critics, 'Hcy'))