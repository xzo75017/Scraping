#!/usr/bin/env python
# coding: utf-8

# In[4]:


# A partir de ces trois listes, créer un DataFrame nommé sens_critique.

from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup 
import pandas 

#urlopen pour récupérer le code HTML et socker la variable 
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}
req = Request("https://www.senscritique.com/films/tops/top111", headers=headers)
page_SC = urlopen(req)


# In[5]:


#Instance soup de la classe BeautifulSoup pour décrypter ce code HTML 

soup = BeautifulSoup(page_SC, 'html.parser')


# In[29]:


#méthode findAll, l'argument name contient la balise et on renseigne dans l'argument 
#la classe qui permet d'identifier les éléments qu'on cherche à récupérer 
noms_SC = soup.find_all(name ='a', attrs = {'class': 'Text__SCText-sc-14ie3lm-0 Link__SecondaryLink-sc-1vfcbn2-1 dGWsbQ jLGgsY ProductListItem__StyledProductTitle-sc-ico7lo-3 ivaIVy'})
print(noms_SC)


# In[30]:


#pour extraire uniquement le texte, on se sert de l'attribut text.
#L'attribut ne peut être utilisé que pour un seul élément à la fois, 
#on fait donc une boucle 
titre_SC = [] #On crée une liste vide qui contiendra tous les titres propres
for element in noms_SC:
    titre_SC.append(element.text)


# In[31]:


#Afficher contenu de la liste titre_SC
print(titre_SC)


# In[22]:


#Liste et boucle pour année de sortie 
annee_sortie_SC = []
for element in soup.findAll(name = 'span', attrs = {'data-testid':'date-release'} ):
    annee_sortie_SC.append(element.text.strip("()")) #On retire les parenthèses
print(annee_sortie_SC)


# In[34]:


note_SC = []
for element in soup.findAll('div', attrs={'class':'Rating__GlobalRating-sc-1rkvzid-4 lhCdNc Poster__GlobalRating-sc-1jujjag-6 dDuFLw globalRating'}):
    note_SC.append(element.text.strip()) #On retire les parenthèses inutiles
    
print(note_SC)    


# In[36]:


#Creation du DataFrame 

sens_critique = pandas.DataFrame(list(zip(titre_SC, annee_sortie_SC,note_SC)), columns=["Titre", "Annee_sortie_SC","Note_SC"])
sens_critique.head()


# In[37]:


#urlopen pour récupérer le code HTML et socker la variable 
user_agent = 'Mozilla/5.0'
headers = {'User-Agent': user_agent}
req = Request("https://www.imdb.com/chart/top/", headers=headers)
page_imdb = urlopen(req)


# In[38]:


soup = BeautifulSoup(page_imdb, 'html.parser')

##Titre 
#Renseigne ensuite ce chemin CSS dans la méthode select 
noms_imdb = soup.select(".titleColumn a")

#Récupérer les titres propres, on utilise l'attribut text et la boucle 
titre_imdb= []
for element in noms_imdb:
    titre_imdb.append(element.text)

##Annee_Sortie_imdb
#Renseigne ensuite ce chemin CSS dans la méthode select

annee_imdb = soup.select(".titleColumn .secondaryInfo")


# In[53]:


#Récupérer les titres propres, on utilise l'attribut text et la boucle
Annee_sortie_imdb = []
for element in annee_imdb:
    Annee_sortie_imdb.append(element.text.strip("()"))
    
    
#Note_imdb
#Renseigne ensuite ce chemin CSS dans la méthode select

note_imdb = soup.select(".imdbRating strong")
#Récupérer les titres propres, on utilise l'attribut text et la bouche
Note_imdb = []
for element in note_imdb:
    Note_imdb.append(element.text)

#Création de la data frame

imdb = pandas.DataFrame(list(zip(titre_imdb,Annee_sortie_imdb,Note_imdb)), columns = ["Titre","Annee_sortie_imdb","Note_imdb"])
imdb.head()


# In[54]:


from scipy.stats import ttest_rel


# In[55]:


#Retirer les accents de la colonne "Titre"
imdb["Titre"] = imdb["Titre"].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')
sens_critique["Titre"] =sens_critique["Titre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[56]:


#mettre tout en majuscule 
imdb["Titre"] =imdb["Titre"].str.upper()
sens_critique["Titre"] = sens_critique["Titre"].str.upper()

#merge

note_finale = imdb.merge(sens_critique, how ="inner", left_on = "Titre", right_on = "Titre", )
note_finale["Note_imdb"] = pandas.to_numeric(note_finale["Note_imdb"])
note_finale["Note_SC"] = pandas.to_numeric(note_finale["Note_SC"])


# In[57]:





# In[ ]:





# In[ ]:




