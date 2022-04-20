import nltk
from nltk import RegexpTokenizer
from gensim.parsing.preprocessing import preprocess_string
import string
import re

def preprocess(file, new_name):
  myfile = open(file)
  text = myfile.read()

  #remove whitespaces
  text = text.strip()
  # remove numbers
  text_nonum = re.sub(r'\d+', '', text)
  # remove punctuations and convert characters to lower case
  text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation]) 
  # substitute multiple whitespace with single whitespace
  # Also, removes leading and trailing whitespaces
  cleaned_text = '\n'.join([i for i in text_nopunct.split('\n') if len(i) > 0])
  #remove only empty lines but preserve lines as units
  # re.sub('\s+', ' ', text_nopunct).strip()

  #cleaned_text = clean_text(text)
  tokens = nltk.word_tokenize(cleaned_text)
  # tokenizer = RegexpTokenizer('\w+')
  # tokens = tokenizer.tokenize(text)
  #print(tokens)
  print(file)
  print(new_name)
  print(cleaned_text[0:100])
  my_new_file = open(new_name, 'w')
  my_new_file.write(cleaned_text)
#preprocess('Aeneid_(Dryden).txt', 'pre_Aeneid_(Dryden).txt')
#preprocess('Aeneid_(Williams).txt', 'pre_Aeneid_(Williams).txt')
#preprocess('Aeneid_(Conington_1866).txt', 'pre_Aeneid_(Conington).txt')

#pivot to topic models, and use KL-divergence. 
#or: train several WE models, and compare top-n similar. 
#assumes more or less the output of preprocess, but with Book (number) as a line at the start of each book
def by_line_to_by_book(file, newfile):
  myfile = open(file)
  text = myfile.read()
  cleaned_text = ""
  for i in text.split('\n'):
    
    if len(i) > 0:
      i = i.split()
      if i[0] == "Book":
        cleaned_text+= '\n'
      else:  
        cleaned_text+= ' '
        cleaned_text+= ' '.join(i)
  my_new_file = open(newfile, 'w')
  my_new_file.write(cleaned_text)

def perseusTEI_toCards(file, newfile):
  myfile = open(file)
  text = myfile.read()
  #remove whitespaces
  text = text.strip()
  text= re.sub('<l n="tr">', "", text)
  text= re.sub('<placeName.*?">', "", text)
  text= re.sub('</placeName>', "", text)
  text = re.sub('</l>', '', text)
  text = re.sub('“', '', text)
  text = re.sub('”', '', text)
  text= re.sub('‘', '', text)
  text= re.sub('’', '', text)
  text= re.sub('—', '', text)
  text= re.sub('<div1 type="Book" n="[0-9]+" org="uniform" sample="complete">', '', text) #dont need the book markers
  text = re.sub("\n", ' ', text) #remove new lines, we are going to want different line breaks
  text= re.sub('<milestone ed="p" n="[0-9]+" unit="card"/>', "\n", text)
  text = "".join([char.lower() for char in text if char not in string.punctuation])
  my_new_file = open(newfile, 'w')
  my_new_file.write(text)

def find_different_matches(file1, file2):
  pattern= re.compile('<milestone ed="p" n="[0-9]+" unit="card"/>')
  text1= open(file1).read()
  text2= open(file2).read()
  match1= re.findall (pattern, text1)
  match2= re.findall (pattern, text2)
  for i in range(395):
    if match1[i]!=match2[i]:
      print(match1[i], match2[i])
      error = 0/0
    else:
      pass
file1="Perseus_text_1999.02.0054.xml"
file2="WilliamsPerseusCard.txt"
perseusTEI_toCards(file1, file2)
