# imports
import fitz
import re
import spacy
import glob
import time

nlp = spacy.load('en_core_web_sm')

class Redactor:

	
	# constructor
	def __init__(self, path):
		self.path = path
	
	def check_conditions(self,sentence):
		if 'james' in sentence or 'glos' in sentence or (re.search(r'\d', sentence)):
			return False
		return True

	def get_ner_entities(self,page):
		words = []
		doc = nlp.pipe(page)
		for elements in doc:
			#doc = nlp(line.lower().replace('-',' '))
			for sentence in elements.ents:
				if sentence.label_ == 'PERSON' and self.check_conditions(sentence.orth_):
					print(sentence)
					words.append(sentence.text)
		return words

	def redaction(self,f):
		
		# opening the pdf
		doc = fitz.open(self.path)
		
		# iterating through pages
		for page in doc:
		
			
			sensitive_entities = self.get_ner_entities(page.getText("text").lower().replace('-',' ').split('\n'))
			for data in sensitive_entities:
				areas = page.searchFor(data)
				
				# drawing outline over sensitive datas
				[page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
				
			# applying the redaction
			page.apply_redactions()
			
		# saving it to a new pdf
		doc.save('/home/administrator/Desktop/mask/single/redacted.pdf')
		print("Successfully redacted")


if __name__ == "__main__":

	
	#path = '/home/administrator/Desktop/invoices/Adjust Training and Consultancy - Invoice.pdf'
	#path = '/home/administrator/Desktop/invoices/28038855_Illus new.pdf'
	start = time.time()
	path = r'/home/administrator/Desktop/mask/single'
	files = [f for f in glob.glob(path + "**/*.pdf", recursive=True)]
	for f in files:
		redactor = Redactor(f)
		redactor.redaction(f)
	end = time. time()
	print('Duration ',end-start)
