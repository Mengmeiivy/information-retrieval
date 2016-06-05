import math 
import numpy as np
from scipy import spatial

# process query 
def process (current_list, query_index):
	new_list = []
	for word in current_list:
		if word in closed_class_stop_words:
			continue
		if word.isalnum() == False:
			continue
		if word.isdigit():
			continue
		if word not in new_list:
			new_list.append(word)

		if word not in query_words:
			query_words[word] = {}
		query_words[word][query_index] = query_words[word].get(query_index, 0.0) + 1

	for word in new_list:
		query_words[word]['SUM'] = query_words[word].get('SUM', 0.0) + 1

	query_text.append(new_list)

# process abstract 	
def process2 (current_list, abstract_index):

	#if (abstract_index == 575):
	#	print (current_list)

	new_list = []
	for word in current_list:
		if word in closed_class_stop_words:
			continue
		if word.isalnum() == False:
			continue
		if word.isdigit():
			continue
		if word not in new_list:
			new_list.append(word)

		if word not in abstract_words:
			abstract_words[word] = {}
		abstract_words[word][abstract_index] = abstract_words[word].get(abstract_index, 0.0) + 1

	for word in new_list:
		abstract_words[word]['SUM'] = abstract_words[word].get('SUM', 0.0) + 1


# main program starts here 
query_words = {}
abstract_words = {}
query_text = []
query_score = []

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\
                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\
                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\
                           'via','vs','with','that','can','cannot','could','may','might','must',\
                           'need','ought','shall','should','will','would','have','had','has','having','be',\
                           'is','am','are','was','were','being','been','get','gets','got','gotten',\
                           'getting','seem','seeming','seems','seemed',\
                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \
                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\
                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\
                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\
                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\
                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\
                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\
                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\
                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \
                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\
                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\
                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\
                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\
                           'you','your','yours','me','my','mine','I','we','us','much','and/or'
                           ]


# query 
f = open('cran.qry', 'r')
current_list = []
query_index = 0

for line in f:

	string_list = line.split()

	if string_list[0] == '.I':
		if current_list != []:
			process (current_list, query_index)
			current_list = []
			query_index += 1
	elif string_list[0] == '.W':
		continue
	else:
		current_list += string_list

process (current_list, query_index)

for i in range(225):
	score_list = []
	for word in query_text[i]:
		tf = query_words[word][i]
		idf = math.log(225.0/query_words[word]['SUM'])
		score_list.append(tf*idf)
	query_score.append(score_list)

f.close()


# abstract 
f = open('cran.all.1400', 'r')
current_list = []
abstract_index = -1

for line in f:

	string_list = line.split()

	if string_list[0] == '.I':
		first_w = True
		if current_list != []:
			process2 (current_list, abstract_index)
		abstract_index += 1

	elif string_list[0] == '.W':
		if (first_w == True):
			current_list = []
			first_w = False 
	else:
		current_list += string_list

process2 (current_list, abstract_index)

f.close()


# cosine similarity 
f = open('output.txt', 'w')
for i in range (225):
	abstract_similarity = []
	for j in range (1400):
		abstract_score = []
		for word in query_text[i]:
			if word not in abstract_words:
				tf = 0.0
				idf = 0.0
			else:
				tf = abstract_words[word].get(j, 0.0)
				idf = math.log(1400.0/abstract_words[word]['SUM'])
			abstract_score.append(tf*idf)

		
		similarity = np.dot(query_score[i], abstract_score)
	
		if similarity != 0: 
			similarity /= math.sqrt((np.dot(query_score[i], query_score[i]))*(np.dot(abstract_score, abstract_score)))

		abstract_similarity.append(similarity)


	abstract_similarity_index = sorted(range(len(abstract_similarity)), \
		key = lambda k: abstract_similarity[k], reverse = True)
	abstract_similarity.sort(reverse = True)

	for j in range (1400):
		query_num = str(i+1)
		abstract_num = str(abstract_similarity_index[j] + 1)
		similarity = '{0:.15f}'.format(abstract_similarity[j])
		if i == 0 and j == 0:
			f.write(query_num + ' ' + abstract_num + ' ' + similarity)
		else: 
			f.write('\n' + query_num + ' ' + abstract_num + ' ' + similarity)

f.close()
















