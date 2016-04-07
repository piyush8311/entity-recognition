import MySQLdb as mysql
import NER_utility as neru

# tagged_data = neru.st.tag(neru.nltk.word_tokenize('Narendra Modi is visiting Bangladesh while Rahul is eating in Delhi.'))

# print "Given sentence: Narendra Modi is visiting Bangladesh while Rahul is eating in Delhi.\n"

# named_entities = neru.get_continuous_chunks(tagged_data)
# named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
# print named_entities_str_tag


# DATABASE RElATED
search_query = "SELECT * FROM NEW_ENTITY.entity_count WHERE entity_name = '%s'"
insert_query = "INSERT INTO NEW_ENTITY.entity_count VALUES ('%s', %d, %d, %d)"
update_query = "UPDATE NEW_ENTITY.entity_count SET person_count = %d, location_count = %d, organization_count = %d WHERE entity_name = '%s'"

db = mysql.connect('localhost', 'root', 'boss@123', 'NEW_ENTITY')
cursor = db.cursor()

# cursor.execute('SELECT newsHeadline FROM NEW_ENTITY.local_information_repository LIMIT 1000')
# headlines = cursor.fetchall()

for z in xrange(7, 18):
	print "Doing connected_headlines"+str(z)+"..."
	file = open('connected_headlines'+str(z))
	headlines = file.read()

	tagged_data = neru.st.tag(neru.nltk.word_tokenize(headlines))
	named_entities = neru.get_continuous_chunks(tagged_data)
	named_entities_str_tag = [(" ".join([token for token,tag in ne]), ne[0][1]) for ne in named_entities if "'" not in ne]

	for e in named_entities_str_tag:

		try:
			cursor.execute(search_query % e[0])
			data = cursor.fetchall()

			if len(data)>0:	# means entity alredy exists
				p_cnt = data[0][1] + (1 if e[1]=='PERSON' else 0)
				l_cnt = data[0][2] + (1 if e[1]=='LOCATION' else 0)
				o_cnt = data[0][3] + (1 if e[1]=='ORGANIZATION' else 0)

				cursor.execute( update_query % (p_cnt, l_cnt, o_cnt, e[0]) )

			else:	# need to insert new entity
				p, l, o =  + (1 if e[1]=='PERSON' else 0),  + (1 if e[1]=='LOCATION' else 0),  + (1 if e[1]=='ORGANIZATION' else 0)

				cursor.execute( insert_query % (e[0], p, l, o) )
		except:
			continue
		
		db.commit()
