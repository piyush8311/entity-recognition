import NER_utility as neru
from bs4 import BeautifulSoup # oh, you beautiful, beautiful thing <3
import requests
import MySQLdb as mysql
import sys

# Here we will get a new headline and then we find whether the entities in it are new or not
# by searching in our entity_count database

def recognize_entities(headline):
	headline_date = None

	db = mysql.connect('localhost', 'root', 'piyush123', 'NEW_ENTITY')
	cursor = db.cursor()

	tagged_data = neru.st.tag(neru.nltk.word_tokenize(headline))
	named_entities = neru.get_continuous_chunks(tagged_data)
	named_entities_str_tag = [(" ".join([token for token,tag in ne]), ne[0][1]) for ne in named_entities]
	entities = []
	search_query = "SELECT * FROM NEW_ENTITY.entity_count WHERE entity_name = '%s'"

	for e in named_entities_str_tag:
		print "Iterating for entity", e
		if e[1] == 'PERSON':	# since we are only checking for people
			try:
				print "Trying to search in database..."
				cursor.execute(search_query % e[0])
				data = cursor.fetchall()

				if len(data)>0:	# this means entity alredy exists in our database
					entities.append( (e[0], "old") )
					print "The entity", e[0], "is not a new entity. It alredy exists in our database."

				else:
					# try to find the entity in wikidump
					#
					# if found, not new entity
					# else, new entity
					url = 'https://en.wikipedia.org/wiki/'+e[0].title().replace(' ','_')
					print "Seaching for", url
					r = requests.get(url)

					if 'Wikipedia does not have an article with this exact name' in r.content:
						# let's be honest, we'll never reach here( given that e[0] is a proper name)
						entities.append( (e[0], "new") )
						print "The entity '"+e[0]+"' was not found in our database or in wikipedia."

					else:	# article exists, so let's check the date it was created
						history_url = 'https://en.wikipedia.org/w/index.php?title='+e[0].title().replace(' ','_')+'&dir=prev&action=history'
						history_page = requests.get(history_url)

						soup = BeautifulSoup(history_page.content, 'lxml')	# the best parser is lxml
						ul = soup.find_all('ul', attrs={'id':'pagehistory'})[0]
						li = ul.find_all('li')[-1]

						date_of_creation = li.find_all('a')[1].text
						creator = li.find_all('a')[2].text

						entities.append( (e[0], "was created on " + date_of_creation + " by " + creator) )
						print date_of_creation, creator
			except:
				print "An error"
				print sys.exc_info()[0]
				continue
	return entities