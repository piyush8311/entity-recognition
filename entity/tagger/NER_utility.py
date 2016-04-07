from nltk.tag.stanford import StanfordNERTagger
import nltk

def get_continuous_chunks(tagged_sent):
	continuous_chunk = []
	current_chunk = []

	for token, tag in tagged_sent:
		if tag != 'O':
			current_chunk.append((token,tag))
		elif current_chunk:
			continuous_chunk.append(current_chunk)
			current_chunk = []

	if current_chunk:
		continuous_chunk.append(current_chunk)

	return continuous_chunk

st = StanfordNERTagger('/home/paladin/Desktop/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz', '/home/paladin/Desktop/stanford-ner-2015-12-09/stanford-ner.jar')
