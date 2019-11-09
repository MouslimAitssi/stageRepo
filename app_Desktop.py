from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import pandas as pd
import csv
import dateparser
from tkinter import *
from functools import partial
import webbrowser
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import geopandas as gpd
import matplotlib.pyplot as plt
from descartes import PolygonPatch


cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
cities.head()
data = pd.read_csv('stopWords.csv', low_memory=False, encoding='utf-8')
stopwords = data.loc[:,"stop_words"].tolist()
#print(stopwords)
def get_stop_words():
    with open('stop.txt', 'r') as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
    return frozenset(stop_set)

def plotCountryPatch(axes, country_name, fcolor):
    # plot a country on the provided axes
    nami = world[world.name == country_name]
    namigm = nami.__geo_interface__['features']  # geopandas's geo_interface
    namig0 = {'type': namigm[0]['geometry']['type'], \
              'coordinates': namigm[0]['geometry']['coordinates']}
    axes.add_patch(PolygonPatch( namig0, fc=fcolor, ec="black", alpha=0.85, zorder=2 ))

def plot_show(s):
	artic = pd.DataFrame(data = s)
	#freq=list(articles.groupby('country').count())
	SS=[list(artic.groupby('country')['country'].transform('count')), artic['country'].tolist()]
	keys = SS[1]
	values = SS[0]
	dictio = dict(zip(keys, values))
	ax2 = world.plot(figsize=(25,25), edgecolor=u'gray', cmap='Pastel1')
	for x in dictio:
	  print(x)
	  plotCountryPatch(ax2, x, 'red')

	plt.ylabel('Latitude')
	plt.xlabel('Longitude')
	plt.show()

def home(window):
	window.destroy()
	window = Tk()
	window.title("CCME Application")
	window.geometry("1240x1000")
	window.minsize(480, 360)
	window.iconbitmap("mediainsight.ico")
	window.config(background = "black")
	width = 500
	height = 500
	canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
	image = PhotoImage(master = canvas, file = "ccme.png")
	canvas.create_image(width/2, height/2, image = image)
	canvas.pack(expand = YES)
	frame = Frame(window, bg = "black")

	label_title = Label(window, text = "Bienvenue sur notre application", font = ("courrier", 30), bg = 'black', fg = "red")
	label_title.pack(expand = YES)

	b1 = Button(frame, text = "Recherche syntaxique", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(recherche_syntaxique, window)).pack(expand = YES, fill = X)
	b2 = Button(frame, text = "Recherche thematique", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(recherche_thematique, window)).pack(expand = YES, fill = X)
	frame.pack(expand = YES)
	window.mainloop()

def recherche_syntaxique(window):
	data = pd.read_csv('Articles.csv', low_memory = False, encoding = 'utf-8')
	list_links = data['URL']
	list_authors = data['Author']
	list_titles = data['Title']
	list_publications = data['Publication']
	list_dates = data['Date']
	list_content = data['Content']
	list_Ids = data['Id']
	list_languages = data['Language']
	list_countrys = data['Country']
	list_sentiments = data['sentiment']

	window.destroy()
	window = Tk()
	frame = Frame(window, bg = 'black')
	window.title("Recherche Syntaxique")
	window.geometry("1240x1000")
	window.minsize(480, 360)
	window.iconbitmap("mediainsight.ico")
	window.config(background = "black")
	"""#8acafe"""
	width = 500
	height = 500
	canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
	image = PhotoImage(master = canvas, file = "ccme.png")
	canvas.create_image(width/2, height/2, image = image)
	canvas.pack()
	label_title = Label(window, text = 'Veuillez donner la phrase que vous cherchez:', font = ("courrier", 30), bg = 'black', fg = "red")
	label_title.pack()
	words = StringVar()
	my_input = Entry(window, textvariable = words, font = ("Helvetica", 30), bg = 'white', fg = "black")
	my_input.pack()

	def get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, V_date, V_pays):
		answer = []
		answer2 = pd.DataFrame(columns = ['Author'])
		countrys = []
		contents = []
		answer3 = pd.DataFrame(columns = ['Country'])
		if V_pays == None:
		    
		    for i in range(0, len(list_Ids)):

		        list_inputs[0] = list_inputs[0].lower()
		        if type(list_content[i]).__name__ == 'str':
		        	res = list_content[i].lower().find(list_inputs[0])
		        	if res != -1 and pd.to_datetime(list_dates[i]) >= V_date:
		        		answer.append(["Title : " + str(list_titles[i]), "Publication : " + str(list_publications[i]), "Author : " + str(list_authors[i]), "Date : " + str(list_dates[i]), ("URL : ", str(list_links[i])), "Language : " + str(list_languages[i]), "Country : " + str(list_countrys[i]), "sentiment : " + str(list_sentiments[i])])
		        		answer2 = answer2.append({'Author' : list_authors[i]}, ignore_index = True, verify_integrity = False)
		        		answer3 = answer3.append({'Country' : list_countrys[i]}, ignore_index = True, verify_integrity = False)
		        		countrys.append(list_countrys[i])
		        		contents.append(list_content[i])
		    return answer, answer2, countrys, contents, answer3

		for i in range(0, len(list_Ids)):
			list_inputs[0] = list_inputs[0].lower()
			if type(list_content[i]).__name__ == 'str':
				res = list_content[i].lower().find(list_inputs[0])
				if res != -1 and pd.to_datetime(list_dates[i]) >= V_date and V_pays == list_countrys[i]:
					answer.append(["Title : " + str(list_titles[i]), "Publication : " + str(list_publications[i]), "Author : " + str(list_authors[i]), "Date : " + str(list_dates[i]), ("URL : ", str(list_links[i])), "Language : " + str(list_languages[i]), "Country : " + str(list_countrys[i]), "sentiment : " + str(list_sentiments[i])])
					answer2 = answer2.append({'Author' : list_authors[i]}, ignore_index = True, verify_integrity = False)
					answer3 = answer3.append({'Country' : list_countrys[i]}, ignore_index = True, verify_integrity = False)
					countrys.append(list_countrys[i])
					contents.append(list_content[i])
		return answer, answer2, countrys, contents, answer3

	def date(window):
	    list_inputs = [str(words.get())]
	    if list_inputs[0] == '':
	    	list_inputs[0] = 'dchvbvbvazd'
	    #print(list_inputs)
	    window.destroy()
	    window = Tk()
	    frame = Frame(window, bg = 'black')
	    window.title("Recherche Syntaxique")
	    window.geometry("1240x1000")
	    window.minsize(480, 360)
	    window.iconbitmap("mediainsight.ico")	    
	    window.config(background = "black")
	    label_title = Label(frame, text = "Voulez vous préciser une date comme début de la recherche ?", font = ("Courrier", 30), bg = 'black', fg = 'red')
	    label_title.pack(expand = YES)
	    
	    def oui_func(window):
	        window.destroy()
	        window = Tk()
	        frame = Frame(window, bg = 'black')
	        date = StringVar()
	        window.title("Recherche Syntaxique")
	        window.geometry("1240x1000")
	        window.minsize(480, 360)
	        window.iconbitmap("mediainsight.ico")
	        window.config(background = "black")
	        label_title = Label(frame, text = "Saisissez la date depuis laquelle vous voulez commencer la recherche (aaaa/mm/jj ou aaaa-mm-jj):", font = ("Courrier", 20), bg = 'black', fg = 'red')
	        label_title.pack(expand = YES)
	        entry = Entry(frame, textvariable = date, font = ("Helvetica", 30), bg = 'white', fg = "black").pack(expand = YES)
	        
	        def execution(window):
	            window.destroy()
	            window = Tk()
	            window.title("Recherche Syntaxique")
	            window.geometry("1240x1000")
	            window.minsize(480, 360)
	            window.iconbitmap("mediainsight.ico")
	            window.config(background = "black")
	            print(str(date.get()))
	            V_date = pd.to_datetime(str(date.get()))
	            if V_date > datetime.now():
	            	window.destroy()
	            	window = Tk()
	            	window.title("Recherche Syntaxique")
	            	window.geometry("1240x1000")
	            	window.minsize(480, 360)
	            	window.iconbitmap("mediainsight.ico")
	            	window.config(background = "black")
	            	label = Label(window, text = "Cette date n'est pas valide, Veuillez ressaisir.", font = ("Courrier", 20), bg = 'black', fg = 'red').pack(expand = YES)
	            	retype_button = Button(window, text = "Ressaisir la date", font = "courrier", width = 40, height = 5, bg = 'gray', command = partial(oui_func, window)).pack(expand = YES)
	            	syntaxic_button = Button(window, text = "Revenir à la recherche syntaxique", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
	            	home_button = Button(window, text = "Tendances", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(home, window)).pack(expand = YES)
	            	window.mainloop()
	            	return

	            out_put = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, V_date, None)
	            if len(out_put[0]) == 0:
	                label_title = Label(window, text = "Malheureusement on n'a pas pu trouvé les résultats souhaités, Veuillez effectuer la recherche avec d'autres termes", font = ("Courrier", 18), bg = 'black', fg = 'red').pack(expand = YES)
	                home_button = Button(window, text = "Page principale", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(home, window)).pack(expand = YES)
	                restart_button = Button(window, text = "Recommencer \n(Recherche syntaxique)", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
	            else:
	                fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'sentiment']
	                scroll = Scrollbar(window)
	                scroll.pack(side = RIGHT, fill = Y)
	                listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                scroll.config(command = listbox.yview)
	                label_title = Label(window, text = "Les articles contenants votre phrase sont: (" + str(len(out_put[0]))+ " resultats)", font = ("courrier", 25), bg = 'black', fg = "red")
	                label_title.pack()
	                S = {'id' : [], 'country' : []}
	                comp = 0
	                for k in out_put[0]:
	                    listbox.insert(comp, "************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************")
	                    comp = comp + 1
	                    for i in k:
	                        listbox.insert(comp, i)
	                        comp = comp + 1
	                        
	                S['country'] = out_put[2]
	                for c in S['country']:
	                	if c == 'Morocco':
	                		S['country'].append('W. Sahara')

	                for l in range (len(out_put[2])):
	                	S['id'].append(l+1)

	                def access():
	                    webbrowser.open_new(str(listbox.get('active')[1]))

	                def showstatisticscountry(good_result):
	                    ax2 = plt.subplot(121, aspect = 'equal') 
	                    good_result['Country'].value_counts()[:10].plot.pie()
	                    plt.show()

	                def showstatistics(good_result, good_result2):
	                    ax1 = plt.subplot(121, aspect = 'equal') 
	                    good_result['Author'].value_counts()[:10].plot.pie()
	                    plt.show()
	                    showstatisticscountry(good_result2)

	                def tendances():
	                	window = Toplevel()
	                	window.title("Tendances")
	                	window.geometry("1240x1000")
	                	window.minsize(480, 360)
	                	window.iconbitmap("mediainsight.ico")
	                	window.config(background = "black")

	                	def pre_process(text):
	                		text = text[0]
	                		text = text.lower()
	                		#remove tags
	                		text = re.sub("</?.*?>"," <> ",text)
	                		# remove special characters and digits
	                		text = re.sub("(\\d|\\W)+"," ",text)
	                		return text

	                	def sort_coo(coo_matrix):
	                		tuples = zip(coo_matrix.col, coo_matrix.data)
	                		return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

	                	def extract_topn_from_vector(feature_names, sorted_items, topn):
	                		sorted_items = sorted_items[:topn]
	                		score_vals = []
	                		feature_vals = []

	                		for idx, score in sorted_items:
	                			fname = feature_names[idx] 
	                			score_vals.append(round(score, 3))
	                			feature_vals.append(feature_names[idx])

	                		results = {}
	                		for idx in range(len(feature_vals)):
	                			results[feature_vals[idx]]=score_vals[idx]

	                		return results

	                	def tendances_global(window):
	                		window.destroy()
	                		window = Toplevel()
	                		window.geometry("1240x1000")
	                		window.minsize(480, 360)
	                		window.iconbitmap("mediainsight.ico")
	                		window.config(background = "black")
	                		window.title("Tous les tendances")
	                		contents = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, V_date, None)[3]
	                		for i in range(len(contents)):
	                			text = [contents[i]]
	                			contents[i] = pre_process(text)
	                		vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, smooth_idf=True)
	                		cv = vectorizer.fit(contents)
	                		feature_names = cv.get_feature_names()
	                		tf_idf_vector = []
	                			
	                		for i in range(len(contents)):
	                			text = [contents[i]]
	                			tf_idf_vector = vectorizer.transform(text)

	                			if i == 0 :
	                				final_element = tf_idf_vector
	                			else:
	                				final_element = final_element + tf_idf_vector

	                		sorted_items = sort_coo(final_element.tocoo())
	                		keywords = extract_topn_from_vector(feature_names, sorted_items, 28)
	                		label_country = Label(window, text = "Tous les themes tendances sont:", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)
	                		#scroll = Scrollbar(window)
	                		#scroll.pack(side = RIGHT, fill = Y)
	                		listTendances = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                		#scroll.config(command = listTendances.yview)
	                		cp = 0
	                		for k in keywords:
	                			
	                			listTendances.insert(cp, (k, keywords[k]))
	                			cp = cp + 1

	                		listTendances.pack(expand = YES)
	                		window.mainloop()

	                	def tendances_country(window):
	                		pays = StringVar()
	                		window.destroy()
	                		window = Toplevel()
	                		window.title("Tendances relatives à un pays")
	                		window.geometry("1240x1000")
	                		window.minsize(480, 360)
	                		window.iconbitmap("mediainsight.ico")
	                		window.config(background = "black")
	                		choice_label = Label(window, text = "Veuillez spécifier le pays:", font = ("courrier", 30), bg = 'black', fg = "red").pack(expand = YES)
	                		frame = Frame(window, bg = 'black')
	                		label_entry = Label(frame, text = "Veuillez préciser le pays sur le quel vous voulez effectuer votre recherche :", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)  		
	                		country_entry = Entry(frame, textvariable = pays, font = ("Helvetica", 30), bg = 'white', fg = "black").pack(expand = YES)

	                		def results(window):
	                			V_pays = str(pays.get())
	                			print(V_pays)
	                			window.destroy()
	                			window = Toplevel()
	                			window.geometry("1240x1000")
	                			window.minsize(480, 360)
	                			window.iconbitmap("mediainsight.ico")
	                			window.config(background = "black")
	                			window.title("Tendances relatives au " + V_pays)
	                			contents = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, V_date, V_pays)[3]
	                			for i in range(len(contents)):
	                				text = [contents[i]]
	                				contents[i] = pre_process(text)

	                			vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, smooth_idf=True)
	                			cv = vectorizer.fit(contents)
	                			feature_names = cv.get_feature_names()
	                			tf_idf_vector = []

	                			for i in range(len(contents)):
	                				text = [contents[i]]
	                				tf_idf_vector = vectorizer.transform(text)

	                				if i == 0 :
	                					final_element = tf_idf_vector
	                				else:
	                					final_element = final_element + tf_idf_vector

	                			sorted_items = sort_coo(final_element.tocoo())
	                			keywords = extract_topn_from_vector(feature_names, sorted_items, 28)
	                			label_country = Label(window, text = "Les themes tendances relatives au " + V_pays + " sont:", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)
	                			#scroll = Scrollbar(window)
	                			#scroll.pack(side = RIGHT, fill = Y)
	                			listTendances = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                			#scroll.config(command = listTendances.yview)
	                			cp = 0
	                			for k in keywords:
	                				listTendances.insert(cp, (k, keywords[k]))
	                				cp = cp + 1

	                			listTendances.pack(expand = YES)
	                			window.mainloop()

	                		search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(results, window)).pack(expand = YES)
	                		frame.pack(expand = YES)
	                		window.mainloop()

	                	frame = Frame(window, bg = 'black')
	                	choice_label = Label(frame, text = "Veuillez spécifier quelle type de tendances vous voulez:", font = ("courrier", 30), bg = 'black', fg = "red").pack()
	                	country_button = Button(frame, text = "Tendances relatives à un pays spécifque", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(tendances_country, window)).pack(expand = YES, fill = X)
	                	global_button = Button(frame, text = "Tous les tendances", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(tendances_global, window)).pack(expand = YES, fill = X)
	                	frame.pack(expand = YES)
	                	window.mainloop()
	                
	                right_frame = Frame(window, bg = "black")
	                right_frame.pack(side = RIGHT)
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)
	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, out_put[1], out_put[4]))
	                statistics_button.pack()
	                plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(plot_show, S)).pack(expand = YES)
	                restart_button = Button(right_frame, text = "Recommencer \n(Recherche syntaxique)", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
	                thematic_button = Button(right_frame, text = "Recherche thematique", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_thematique, window)).pack(expand = YES)
	                tendances_button = Button(right_frame, text = "Tendances", font = "courrier", width = 20, height = 5, bg = "gray", command = tendances).pack(expand = YES)
	            
	            window.mainloop()
	        
	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(execution, window)).pack(expand = YES)
	        frame.pack(expand = YES)
	        window.mainloop()
	    
	    def non_func(window):
	        date = datetime(2019, 1, 1, 1, 1)

	        def execution(window):
	            window.destroy()
	            window = Tk()
	            window.title("Recherche Syntaxique")
	            window.geometry("1240x1000")
	            window.minsize(480, 360)
	            window.iconbitmap("mediainsight.ico")
	            window.config(background = "black")
	            out_put = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, date, None)
	            
	            if len(out_put[0]) == 0:    
	                label_title = Label(window, text = "Malheureusement on n'a pas pu trouvé les résultats souhaités, Veuillez effectuer la recherche avec d'autres termes", font = ("Courrier", 18), bg = 'black', fg = 'red').pack(expand = YES)
	                home_button = Button(window, text = "Page principale", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(home, window)).pack(expand = YES)
	                restart_button = Button(window, text = "Recommencer \n(Recherche syntaxique)", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
	            
	            else:
	                fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'sentiment']
	                scroll = Scrollbar(window)
	                scroll.pack(side = RIGHT, fill = Y)
	                listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                scroll.config(command = listbox.yview)
	                label_title = Label(window, text = "Les articles contenants votre phrase sont: (" + str(len(out_put[0]))+ " resultats)", font = ("courrier", 25), bg = 'black', fg = "red")
	                label_title.pack()
	                S = {'id' : [], 'country' : []}
	                comp = 0
	                for k in out_put[0]:
	                    listbox.insert(comp, "************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************")
	                    comp = comp + 1
	                    for i in k:
	                        listbox.insert(comp, i)
	                        comp = comp + 1
	                        
	                S['country'] = out_put[2]
	                for c in S['country']:
	                	if c == 'Morocco':
	                		S['country'].append('W. Sahara')

	                for l in range (len(out_put[2])):
	                	S['id'].append(l+1)

	                def access():
	                    webbrowser.open_new(str(listbox.get('active')[1]))

	                def showstatisticscountry(good_result):
	                    ax2 = plt.subplot(121, aspect = 'equal') 
	                    good_result['Country'].value_counts()[:10].plot.pie()
	                    plt.show()

	                def showstatistics(good_result, good_result2):
	                    ax1 = plt.subplot(121, aspect = 'equal')
	                    print(good_result['Author'].value_counts()[:10])
	                    good_result['Author'].value_counts()[:10].plot.pie()
	                    plt.show()
	                    showstatisticscountry(good_result2)

	                def tendances():
	                	window = Toplevel()
	                	window.title("Tendances")
	                	window.geometry("1240x1000")
	                	window.minsize(480, 360)
	                	window.iconbitmap("mediainsight.ico")
	                	window.config(background = "black")

	                	def pre_process(text):
	                		text = text[0]
	                		text = text.lower()
	                		#remove tags
	                		text = re.sub("</?.*?>"," <> ",text)
	                		# remove special characters and digits
	                		text = re.sub("(\\d|\\W)+"," ",text)
	                		return text

	                	def sort_coo(coo_matrix):
	                		tuples = zip(coo_matrix.col, coo_matrix.data)
	                		return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

	                	def extract_topn_from_vector(feature_names, sorted_items, topn):
	                		sorted_items = sorted_items[:topn]
	                		score_vals = []
	                		feature_vals = []

	                		for idx, score in sorted_items:
	                			fname = feature_names[idx] 
	                			score_vals.append(round(score, 3))
	                			feature_vals.append(feature_names[idx])

	                		results = {}
	                		for idx in range(len(feature_vals)):
	                			results[feature_vals[idx]]=score_vals[idx]

	                		return results

	                	def tendances_global(window):
	                		window.destroy()
	                		window = Toplevel()
	                		window.geometry("1240x1000")
	                		window.minsize(480, 360)
	                		window.iconbitmap("mediainsight.ico")
	                		window.config(background = "black")
	                		window.title("Tous les tendances")
	                		contents = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, date, None)[3]
	                		for i in range(len(contents)):
	                			text = [contents[i]]
	                			contents[i] = pre_process(text)
	                		
	                		vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, smooth_idf=True)
	                		cv = vectorizer.fit(contents)
	                		feature_names = cv.get_feature_names()
	                		tf_idf_vector = []
	                			
	                		for i in range(len(contents)):
	                			text = [contents[i]]
	                			tf_idf_vector = vectorizer.transform(text)

	                			if i == 0 :
	                				final_element = tf_idf_vector
	                			else:
	                				final_element = final_element + tf_idf_vector

	                		sorted_items = sort_coo(final_element.tocoo())
	                		keywords = extract_topn_from_vector(feature_names, sorted_items, 28)
	                		label_country = Label(window, text = "Tous les themes tendances sont:", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)
	                		#scroll = Scrollbar(window)
	                		#scroll.pack(side = RIGHT, fill = Y)
	                		listTendances = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                		#scroll.config(command = listTendances.yview)
	                		cp = 0
	                		for k in keywords:
	                			
	                			listTendances.insert(cp, (k, keywords[k]))
	                			cp = cp + 1

	                		listTendances.pack(expand = YES)
	                		window.mainloop()

	                	def tendances_country(window):
	                		pays = StringVar()
	                		window.destroy()
	                		window = Toplevel()
	                		window.title("Tendances relatives à un pays")
	                		window.geometry("1240x1000")
	                		window.minsize(480, 360)
	                		window.iconbitmap("mediainsight.ico")
	                		window.config(background = "black")  		
	                		choice_label = Label(window, text = "Veuillez spécifier le pays:", font = ("courrier", 30), bg = 'black', fg = "red").pack(expand = YES)
	                		frame = Frame(window, bg = 'black')
	                		label_entry = Label(frame, text = "Veuillez préciser le pays sur le quel vous voulez effectuer votre recherche :", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)  		
	                		country_entry = Entry(frame, textvariable = pays, font = ("Helvetica", 30), bg = 'white', fg = "black").pack(expand = YES)

	                		def results(window):
	                			V_pays = str(pays.get())
	                			print(V_pays)
	                			window.destroy()
	                			window = Toplevel()
	                			window.geometry("1240x1000")
	                			window.minsize(480, 360)
	                			window.iconbitmap("mediainsight.ico")
	                			window.config(background = "black")
	                			window.title("Tendances relatives au " + V_pays)
	                			contents = get_outputs(list_inputs, list_links, list_content, list_titles, list_dates, date, V_pays)[3]
	                			for i in range(len(contents)):
	                				text = [contents[i]]
	                				contents[i] = pre_process(text)

	                			vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, smooth_idf=True)
	                			cv = vectorizer.fit(contents)
	                			feature_names = cv.get_feature_names()
	                			tf_idf_vector = []

	                			for i in range(len(contents)):
	                				text = [contents[i]]
	                				tf_idf_vector = vectorizer.transform(text)

	                				if i == 0 :
	                					final_element = tf_idf_vector
	                				else:
	                					final_element = final_element + tf_idf_vector

	                			sorted_items = sort_coo(final_element.tocoo())
	                			keywords = extract_topn_from_vector(feature_names, sorted_items, 28)
	                			label_country = Label(window, text = "Les themes tendances relatives au " + V_pays + " sont:", font = ("courrier", 25), bg = 'black', fg = "red").pack(expand = YES)
	                			#scroll = Scrollbar(window)
	                			#scroll.pack(side = RIGHT, fill = Y)
	                			listTendances = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
	                			#scroll.config(command = listTendances.yview)
	                			cp = 0
	                			for k in keywords:
	                				
	                				listTendances.insert(cp, (k, keywords[k]))
	                				cp = cp + 1

	                			listTendances.pack(expand = YES)
	                			window.mainloop()

	                		search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(results, window)).pack(expand = YES)
	                		frame.pack(expand = YES)
	                		window.mainloop()

	                	frame = Frame(window, bg = 'black')
	                	choice_label = Label(frame, text = "Veuillez spécifier quelle type de tendances vous voulez:", font = ("courrier", 30), bg = 'black', fg = "red").pack()
	                	country_button = Button(frame, text = "Tendances relatives à un pays spécifque", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(tendances_country, window)).pack(expand = YES, fill = X)
	                	global_button = Button(frame, text = "Tous les tendances", font = ("courrier", 20), bg = 'gray', fg = 'red', command = partial(tendances_global, window)).pack(expand = YES, fill = X)
	                	frame.pack(expand = YES)
	                	window.mainloop()

	                right_frame = Frame(window, bg = "black")
	                right_frame.pack(side = RIGHT)  
	                access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
	                access_button.pack(expand = YES)
	                listbox.pack(expand = YES)

	                statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, out_put[1], out_put[4]))
	                statistics_button.pack()

	                plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(plot_show, S)).pack(expand = YES)
	                restart_button = Button(right_frame, text = "Recommencer\n(Recherche syntaxique)", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
	                thematic_button = Button(right_frame, text = "Recherche thematique", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_thematique, window)).pack(expand = YES)
	                tendances_button = Button(right_frame, text = "Tendances", font = "courrier", width = 20, height = 5, bg = "gray", command = tendances).pack(expand = YES)

	            window.mainloop()

	        search_button = Button(frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(execution, window)).pack(expand = YES, fill = X)

	    Oui = Button(frame, text = "Oui", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(oui_func, window)).pack(expand = YES, fill = X)
	    Non = Button(frame, text = "Non", font = ("Helvetica", 30), bg = 'gray', fg = 'black', command = partial(non_func, window)).pack(expand = YES, fill = X)

	    frame.pack(expand = YES)
	    window.mainloop()

	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg = 'gray', fg = "black", command = partial(date, window))
	search_button.pack()
	#search_button = Button(right_frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black")
	#right_frame.grid(row = 0, column = 1, sticky = W)
	#frame.grid()
	frame.pack(expand = YES)
	window.mainloop()


#list_content = pd.read_csv('Articles_.csv')
#articles3.head()
#articles = articles3.loc[0:1000,['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'sentiment'] ]
#articles.shape
#list_content = articles

def score_content(my_theme, content):
    result = []
    vectorizer = TfidfVectorizer(stop_words = stopwords, use_idf = True, smooth_idf = True)
    vectorizer.fit(content+my_theme)
    vector_list_contents = vectorizer.transform(content)
    vector_my_theme = vectorizer.transform(my_theme)
    #print(vector_list_contents)
    result = linear_kernel(vector_my_theme, vector_list_contents)
    score = sum(result)/len(result)
    return score

def recherche_thematique(window):
	list_content = pd.read_csv('Articles.csv')
	window.destroy()
	window = Tk()
	#frame = Frame(window, bg = 'black')
	window.title("Recherche thematique")
	window.geometry("1240x1000")
	window.minsize(480, 360)
	window.iconbitmap("mediainsight.ico")
	window.config(background = "black")
	"""#8acafe"""
	width = 500
	height = 500
	canvas = Canvas(window, width = width, height = height, bg = 'black', bd = 0, highlightthickness = 0)
	image = PhotoImage(master = canvas, file = "ccme.png")
	canvas.create_image(width/2, height/2, image = image)
	#canvas.grid(row = 0, column = 0, sticky = W)
	canvas.pack()

	#right_frame = Frame(frame, bg = 'black')

	#label_title = Label(right_frame, text = "Veuillez saisir votre theme:", font = ("Helvetica", 30), bg = 'black', fg = "red")
	#label_title.pack()
	label_title = Label(window, text = "Veuillez saisir votre theme:", font = ("courrier", 30), bg = 'black', fg = "red")
	label_title.pack()

	#my_input = Entry(right_frame, font = ("Helvetica", 30), bg = 'white', fg = "black")
	ment = StringVar()
	my_input = Entry(window, textvariable = ment, font = ("Helvetica", 30), bg = 'white', fg = "black")
	my_input.pack()
	#search_button = Button(right_frame, text = "Rechercher", font = ("Helvetica", 30), bg = 'white', fg = "black")
	#right_frame.grid(row = 0, column = 1, sticky = W)

	#frame.grid()
	#frame.pack(expand = YES)

	def execution(window):
		my_input = [str(ment.get())]
		print(my_input[0])
		fieldnames = ['Id', 'Title', 'Publication', 'Author', 'Date', 'URL', 'Content', 'Language', 'Country', 'score', 'sentiment']
		window.destroy()
		window = Tk()
		window.title("Recherche thematique")
		window.geometry("1240x1000")
		window.minsize(480, 360)
		window.iconbitmap("mediainsight.ico")
		window.config(background = "black")
		themes_publishers = []
		for k in range(0, len(list_content['Id'])):
			if type(list_content['Content'][k]).__name__ == 'str':
				S = score_content(my_input, [list_content['Content'][k]])
				themes_publishers.append(S[0])
			else:
				themes_publishers.append(0)
		list_content['score'] = themes_publishers 
		list_content.sort_values(by = ["score"], inplace = True, ascending = False)
		print(list_content.loc[list_content.index[0], "score"])
		if list_content.loc[list_content.index[0], "score"] < 0.001:

			label_title = Label(window, text = "Malheureusement, on n'a pas pu trouver une recommandation convenable.", font = ("courrier", 20), bg = 'black', fg = "red")
			label_title.pack()
			home_button = Button(window, text = "Page principale", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(home, window)).pack(expand = YES)
			restart_button = Button(window, text = "Recommencer \n(Recherche thématique)", font = "courrier", width = 40, height = 5, bg = "gray", command = partial(recherche_thematique, window)).pack(expand = YES)
		
		else:
			S = {'id' : [], 'country' : []}
			scroll = Scrollbar(window)
			scroll.pack(side = RIGHT, fill = Y)
			listbox = Listbox(window, width = 170, height = 40, selectmode = EXTENDED, yscrollcommand = scroll.set)
			scroll.config(command = listbox.yview)
			
			def access():
				webbrowser.open_new(str(listbox.get('active')[1]))

			right_frame = Frame(window, bg = "black")
			right_frame.pack(side = RIGHT)	
			access_button = Button(right_frame, text = "Accès au URL", font ="courrier", width = 20, height = 5, bg = "gray", command = access)
			access_button.pack(expand = YES)

			def showstatisticscountry(good_result):
				ax2 = plt.subplot(121, aspect = 'equal')
				good_result['Country'].value_counts()[:10].plot.pie()
				plt.show()

			def showstatistics(good_result):
				good_result.hist(column = 'score')
				plt.title("Affichage des statistiques", color = 'r')
				plt.xlabel("Score", color = 'blue')
				plt.ylabel("Nombre d'articles", color ='blue')
				plt.figure(figsize = (16, 8))
				ax1 = plt.subplot(121, aspect = 'equal') 
				good_result['Author'].value_counts()[:10].plot.pie()
				plt.show()
				showstatisticscountry(good_result)

			statistics_button = Button(right_frame, text = "Statistiques", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(showstatistics, list_content[list_content['score']>0]))
			statistics_button.pack()
			restart_button = Button(right_frame, text = "Recommencer \n(Recherche thematique)", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_thematique, window)).pack(expand = YES)
			syntaxic_button = Button(right_frame, text = "Recherche syntaxique", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(recherche_syntaxique, window)).pack(expand = YES)
			home_button = Button(right_frame, text = "Page principale", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(home, window)).pack(expand = YES)
			comp = 0
			nbre = 0
			id = 1
			s = {'id' : [], 'country' : []}
			for i, element in list_content.iterrows():
				if(element["score"] >= 0.001):
					listbox.insert(comp, "*************************************************************************************************************************************************************************************************************************************************************************************")
					l = []
					comp = comp + 1
					for c in range (1, 9):
						if c != 6:
							listbox.insert(comp, (str(fieldnames[c]) + " : ", str(element[fieldnames[c]])))
							comp = comp + 1
							if c == 8:
								s['id'].append(id)
								s['country'].append(str(element[fieldnames[c]]))
								id = id + 1
								if element[fieldnames[c]] == 'Morocco':
									s['id'].append(id)
									s['country'].append('W. Sahara')
									id = id + 1
					listbox.insert(comp, "score = " + str("%.4f" % element['score']))
					comp = comp + 1
					listbox.insert(comp, "sentiment : " + str(element[fieldnames[10]]))
					comp = comp + 1
					nbre = nbre + 1
				else:
					break

			plot_button = Button(right_frame, text = "Dessiner la carte du monde", font = "courrier", width = 20, height = 5, bg = "gray", command = partial(plot_show, s)).pack(expand = YES)
			label_title = Label(window, text = "Les TOP articles traitants votre theme sont: (" + str(nbre) + " résultats)", font = ("courrier", 30), bg = 'black', fg = "red")
			label_title.pack()
			listbox.pack(expand = YES)
			
	search_button = Button(window, text = "Rechercher", font = ("Helvetica", 30), bg='gray', fg="black", command=partial(execution, window))
	search_button.pack()	
	window.mainloop()
	return

home(Tk())