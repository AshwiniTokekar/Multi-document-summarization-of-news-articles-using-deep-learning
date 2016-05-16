#!/usr/bin/python3
import sys
import math
import jsonrpclib
from json import loads
from collections import defaultdict
server = jsonrpclib.Server("http://127.0.0.1:8080")
tf=defaultdict(int)
df=defaultdict(int)
idf=defaultdict(float)
number=defaultdict(bool)
max_sent_len=defaultdict(int)
avg_tf=defaultdict(float)
avg_idf=defaultdict(float)
avg_df=defaultdict(float)
stopword_ratio=defaultdict(float)
number_ratio=defaultdict(float)
length_sent=defaultdict(int)
position=defaultdict(float)
noun=defaultdict(int)
adjective=defaultdict(int)
verb=defaultdict(int)
adverb=defaultdict(int)
sent_depth=defaultdict(int)
sub_sent=defaultdict(int)
max_sub_sent=defaultdict(int)
max_depth=defaultdict(int)
stopwords=set(("a","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","just","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","wouldn't","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","zero","keyword","keywords"))

def finddepth(parse_tree):
	length=len(parse_tree)
	stack=[]
	max_len=-1
	for i in range(length):
		if parse_tree[i]=="(":
			stack.append("(")
			if max_len<len(stack):
				max_len=len(stack)
		elif parse_tree[i]==")":
			stack.pop()	
	return max_len

def findsubsentences(parse_tree):
	count_s=0
	parse_tree=parse_tree.split(' ')
	length=len(parse_tree)
	for i in range(length):
		if parse_tree[i]=="(S":
			count_s+=1
	return count_s
def word_level(lines,nod):
	i=1
	for line in lines:		
		text=line["text"]
		position[text]=1-float((i-1)/(len(lines)-1))
		te=text.strip('.')
		words=text.split()
		for word in words:
			tf[word]+=1
		words_set=set(words)	
		for word in words_set:
			df[word]+=1
			number[word]=word.isdigit()
		if len(words)>max_sent_len[word]:
			max_sent_len[word]=len(words)
		i+=1		
	for word in df:
		idf[word]=math.log(float(nod)/df[word])

def POS_tags(line):
	words=line["words"]
	Noun={"NN","NNS","NNP","NNPS"}
	Adverb={"RB","RBR","RBS"}
	Verb={"VB","VBD","VBN","VBP","VBZ"}
	Adjective={"JJ","JJR","JJS"}
	for w,des in words:
		if des["PartOfSpeech"] in Noun:
			noun[w]+=1
		elif des["PartOfSpeech"] in Adjective:
			adjective[w]+=1
		elif des["PartOfSpeech"] in Verb:
			verb[w]+=1
		elif des["PartOfSpeech"] in Adverb:
			adverb[w]+=1			

def sent_level(line):
	i=0
	text=line["text"]
	if len(text)>0:				
			i+=1
			words=text.split()
			length_sent[text]=len(words)
			sent_depth[text]=finddepth(line["parsetree"])
			sub_sent[text]=findsubsentences(line["parsetree"])
			temp_tf=0
			temp_idf=0
			temp_df=0
			num=0
			stop=0
			for word in words:
				if max_depth[word]<sent_depth[text]:
					max_depth[word]=sent_depth[text]
				if max_sub_sent[word]<sub_sent[text]:
					max_sub_sent[word]=sub_sent[text]	
				temp_tf+=tf[word]
				temp_df+=df[word]
				temp_idf+=idf[word]
				if number[word]:
					num+=1
				if word in stopwords:
					stop+=1	
			avg_tf[text]=temp_tf/len(words)
			avg_idf[text]=temp_idf/len(words)
			avg_df[text]=temp_df/len(words)	
			stopword_ratio[text]=stop/len(words)
			number_ratio[text]=num/len(words)
def normalize(feature):
	max_key=max(x,key=x.get)
	print max_key

def getallfeatures(filename):
	reader = open(filename)
	i=1
	docs_lines=[]
	docs=reader.readlines()
	for doc in docs:
		print("Processing doc number:"+(str(i)))
		doc=doc.strip()
		lines=loads(server.parse(doc))["sentences"]
		docs_lines.extend(lines)
		word_level(lines,len(docs))
		i+=1
	i=0	
	for line in docs_lines:		
		sent_level(line)
		POS_tags(line)
		i+=1
	normalize(tf)	
	
def main():
	print "Finding All Features"
	getallfeatures(sys.argv[1])
main()			

	