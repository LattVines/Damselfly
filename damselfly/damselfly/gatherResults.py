import json
import re

f_name = "spammers.json"
results = []

with open(f_name) as json_data:
  d = json.load(json_data)
  #print(d)

for element in d:
    element['score'] = 0

def count_links (the_list):
    '''Every url link gets 1 point'''
    for content in the_list:
        content['score'] +=  content['link count']


def inspect_for_keywords(the_list):
    '''these are words that seem unusual for itch
    and also seem to appear in a lot of the spam accounts.
    I assign a single point for each appearance of those words
    '''
    keywords = [
        'advertising',
        'specialist',
        'industry',
        'track record',
        'market',
        'consult',
        'business',
        'international',
        'career',
        'professional',
        'education',
        ' dr. ',
        'sucess',
        'it',
        'university',
        'experience'
        'client',
        'job',
        'health','supplement',
        'respected',
        'risk',
        'firm',
        'hospital',
        'financial',
        'expert',
        'cybersecurity',
        'realtor',
        'ceo',
        'learn more',
        'medium.com' #seriously, gamedevs don't link to medium...
        'natural',
        'contracting',
        'employs',
        'refrigeration',
        'appliances',
        'equipment'
        'phone',
        'services',
        'office'
             ]

    for content in the_list:
        '''
        print()
        print("-------")
        print("content : " + str(content['profile content']))
        print()
        print('current score: ' + str( content['score']))
        print("-------")
        input()
        '''
        total = 0
        for word in keywords:
            thiscount = str(content['profile content']).lower().count(word)
            total += thiscount
            #print("\t" + word + ":> this word's count : " + str(thiscount))
        content['score'] +=  total
        #print('final score: ' + str(content['score']))
        


def inspect_for_phone_numbers(the_list):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    for content in the_list:
        profile = str(content['profile content'])
        result = r.findall(profile)
        #print("result\t" + str(result))
        if(result != None and len(result) >= 1):
            content['score'] += 10
            #print("------")
            #print("profile " + profile)
            #print()
            #numbers = ""
            #for s in result:
             #   numbers += s + " "
            #print("result : \t" + str(result))
            #print("------")
            #input()
    

inspect_for_keywords(d)
count_links(d)
inspect_for_phone_numbers(d)
#d.close()

        

print("-------------------------------------")
print("*****itch.io spam crawl*******")
print("crawled this many: " + str(len(d)))
print("url\t\t\t\tlink count")
for r in d:
    if(r['score'] >= 9):
        print(r['profile url'] + "\t" + str(r['score']))


