#!/usr/bin/env python
# coding: utf-8

# # Chargement des libraries
#The PyMongo distribution contains tools for interacting with MongoDB database from Python
import pymongo
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import functools
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns


def conjuction(*conditions):
    return functools.reduce(np.logical_and, conditions)

# Insertion du logo de supinfo 
logo = Image.open('im.png')
st.set_page_config(page_title='Supinfo_Big_Data_Platform', page_icon=logo)


# # Connection à notre base de donnée grâce à pymongo
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["supinfo"]
mycol = mydb["supinfo_data"]

st.title("Big Data and Data Science future platform for the school SUPINFO")

with st.beta_expander("The most successful students, depending on the region / institution of origin"):

    st.write("Exploration dataset")
    ### Visionner nos données sous forme de dataframe 
    curseur= mycol.find()
    table = pd.DataFrame(list(curseur))
    data =table.drop(['_id'], axis =1)
    data = data.drop(data.index[len(data)-1])
   

    # sidebar
    sidebar_option = st.sidebar.beta_expander('FILTERS')
    #1 - Who are the most successful students, depending on the region / institution of origin, etc.
    # Récupération des régions
    regions = data['Region d\'origine'].unique().tolist()

    region_selectbox = sidebar_option.multiselect(
        "Which region do you want to select?",
        (regions)
    )
    filter_region = []
    if region_selectbox:
        filter_region = data[(data['Region d\'origine'].isin(region_selectbox).to_list())]
        data = filter_region

    # Récupération des intitustions d'origine
    instituts = data['Institution d\'origine'].unique().tolist()

    institut_selectbox = sidebar_option.multiselect(
        "Select an institution of origin",
        (instituts)
    )
    filter_institut = []
    if institut_selectbox:
        filter_institut= data[(data['Institution d\'origine'].isin(institut_selectbox).to_list())] 
        data = filter_institut

    # Récupération des promos
    promos = data['Promo'].unique().tolist()

    promo_selectbox = sidebar_option.multiselect(
        "Select a promo",
        (promos)
    )

    
    filter_promo = []
    if promo_selectbox:
        filter_promo = data[(data['Promo'].isin(promo_selectbox).to_list())] 
        data = filter_promo


    # Récupération des crédits
    data = data.sort_values('Nombre de credits ECTS',ascending=False)
    
    min_credit = 0
    max_credit = 300
    credit_slider = sidebar_option.slider('How much credit do they have ?', min_credit, max_credit, value=(min_credit, max_credit))
    sidebar_option.markdown(credit_slider)
    #filter_min_credit = credits>= credit_slider[0]
    #filter_max_credit = credits<= credit_slider[1]

    filter_data = data
    st.write(filter_data)

container_2_show = st.beta_expander("Show basic count plots")
with container_2_show:
    container_2 = st.beta_container()

    if len(filter_data)>10:
        filter_data = filter_data.head(5)
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Best students')
    sns.countplot(data=filter_data, hue='Etudiants', y ='Region d\'origine')
    container_2.pyplot(fig)
#2 - Who are the students who stop their studies and why
with st.beta_expander("Who are the students who stop their studies and why"):
    
    container_3 = st.beta_container()
    col1, col2 = container_2.beta_columns([3,3])
    stop_student = data[data['Abandon des etudes']== 'Yes']
    #col.1.st.write(stop_student)
    
    
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.title('students have stopped study')
    sns.countplot(data=stop_student, hue='Etudiants', y ='Region d\'origine')
    container_3.pyplot(fig)

    #WHY
    st.write('''
    Les raisons probables sont les suivantes : les finances, la complexité de la formation, la santé, 
    un renvoi, un déménagement, un emploi et des raisons familiales ''')

#3 -  Why there are more students in one region and few in another
with st.beta_expander(" There are more students in one region and few in another"):
    #labels = data['Region d\'origine'].unique().tolist()
    t = pd.crosstab(data['Campus'], "freq", normalize = True)
    t = t.assign(campus = t.index, const = 1, percent = 100 * t.freq)
    st.write(t)

    container_4 = st.beta_container()
    fig1, ax = plt.subplots(figsize=(2, 3))
    labels = t.campus
    sizes = t.percent
    plt.pie(sizes,labels=labels)
    container_4.pyplot(fig1)

    st.write('''Les raisons du nombre d’étudiants s'explique par : la démographie des villes, les débouches, 
    le fait qu'il y ai eut plus de date de salon sur paris et donc plus de recrutement, la renommée des villes et du diplôme''')
#4 -  How to revitalize campuses
with st.beta_expander("How to revitalize campuses"):
    st.write('''D'après les données de notre étude pour revitaliser le campus nous devons organiser plus de salon,plus de porte ouvertes,
    faire des partenariats avec des entreprises , faire des enquêtes de satisfaction auprès des étudiants''')

    # 5 -  What is the impact of a student fair on recruitments
with st.beta_expander("What is the impact of a student fair on recruitments"):
    t = pd.crosstab(data['Recrute sur un salon etudiant'], "freq", normalize = True)
    t = t.assign(campus = t.index, const = 1, percent = 100 * t.freq)
    t = t.drop(t.campus[0])
    st.write(t)

    container_5= st.beta_container()
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.title('Pourcentage of students who have been hired on')
    sns.countplot(data=t, hue='campus', x ='percent')
    container_5.pyplot(fig)

#6 -  What is the average length of time graduates are hired
with st.beta_expander("What is the average length of time graduates are hired"):
    # duree pour etre embauche
     t = pd.crosstab(data['Duree de l\'embauche des diplômes'], "freq", normalize = True)
     t = t.assign(duree = t.index, const = 1, percent = 100 * t.freq)
     t  = t.drop(t.duree[len(t)-1])
     t  = t.drop(t.duree[len(t)-1])
     st.write(t)

     moy = t.mean()
     #st.write(moy)

#7 -  Which companies recruit the most students from supinfo
with st.beta_expander("Which companies recruit the most students from supinfo"):
     t = pd.crosstab(data['Entreprise'], "freq", normalize = True)
     t = t.assign(entreprise = t.index, const = 1, percent = 100 * t.freq)
     st.write(t)


#8 - How to attract more students
with st.beta_expander("How attract more students"):
    st.write('''D'après les données de notre étude pour attirer plus d'étudiants, nous devons organiser plus de salon,plus de porte ouvertes,
    faire des partenariats avec des entreprises , faire des enquêtes de satisfaction auprès des étudiants''')


