import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import requests
import json

#url = "https://projet-7-backend-ef69878bbc3f.herokuapp.com/"
url = "http://127.0.0.1:5000/"

################################################
# Fonctions d'affichage & récolte informations #
################################################

def txt_accueil():
    st.title("Page d'accueil")
    st.header("Objectif de l'application")
    st.write("""Cette application a pour but d'être un prototype "front-end" dans une démarche 
            de mise en place d'un projet MLOps. Elle se présente en 3 parties distinctes.""")
    st.subheader("La page d'accueil")
    st.write("""Cette première partie sert à rappeler le but et le fonctionnement de l'application.""")
    st.subheader("Obtention de prêt")
    st.write("""Cette deuxième partie est la principale raison d'exister de cette application.
             C'est dans cet onglet que le client peut renseigner son numéro de demande de prêt
             si celle-ci a déjà été formulée auprès de l'établissement bancaire. Si ce n'est pas
             le cas, quelques informations essentielles à l'obtention d'un prêt ainsi que quelques informations
             subsidiaires peuvent également être communiquées afin d'obtenir une première simulation.""")
    st.subheader("L'onglet de comparaison")
    st.write("""Enfin, cette dernière extension n'est pas un passage obligé de l'application. Elle sert
             seulement au client à comparer sa situation et/ou sa demande de prêt avec d'autres
             demandes déjà formulées. Elle peut notamment être utile si le prêt est refusé afin
             de comprendre les raisons du refus.""")

def txt_loan():
    st.title("Simulation d'une demande de crédit")
    st.write("""C'est dans ce pan de l'application que vous allez pouvoir suivre votre demande
             de crédit si vous l'avez formulé au préalable (auquel cas vous possédez déjà un numéro
             de demande prêt) ou sinon rentrer les informations nécessaires au calcul de votre situation.
             Dans les deux cas, cette application reste une :red[simulation] et n'a pas pour but de délivrer
             un résultat officiel.""")
    st.write("""Vous obtiendrez à l'issue de cette simulation un score noté sur 100. Il représente votre
             aptitude à pouvoir rembourser un prêt selon les informations que vous nous communiquez. Le score
             à dépasser pour obtenir un prêt de notre part est **:red[49/100]**.""")
    st.write("""Si votre simulation est négative, nous vous encourageons fortement à vous diriger sur l'onglet
             de comparaison qui a été développé pour que vous puissez comprendre les raisons qui font
             votre refus.""")
    st.subheader("Calculateur")

def txt_loan_noID():
    st.warning("""A noter que certaines des informations sont facultatives. Un remplissage plus poussée
               vous fournira une réponse plus précise.""")
    gender = st.selectbox("Civilité", ["-","Monsieur","Madame"])
    age = st.number_input("Age", min_value=0, step=1)
    cnt_children = st.number_input("Nombre d'enfants à charge", step=1)
    time_employment = st.number_input("Temps en activité (en années)", min_value=0, step=1)
    income = st.number_input("Revenu mensuel total :red[(requis)]", min_value=0, step=1)
    own_car = st.selectbox("Possédez-vous une voiture ?", ["-","Oui","Non"])
    own_realty = st.selectbox("Êtes-vous propriétaire immobilier ?", ["-","Oui","Non"])
    if own_realty == "-":
        own_realty = np.nan
    amt_goods_price = st.number_input("Montant du/des bien(s) à acheter :red[(requis)]", min_value=0, step=1)
    if amt_goods_price == 0:
        amt_goods_price = np.nan
    amt_credit = st.number_input("Montant total envisagé du crédit :red[(requis)]", min_value=0, step=1)
    reimbursement_method = st.radio("Quelle méthode choisissez-vous pour le remboursement :red[(requis)] :",
                                    ["Renseigner un montant souhaité à rembourser par mois",
                                    "Renseigner le nombre d'années sur lesquelles étaler le remboursement"])
    if reimbursement_method == "Renseigner un montant souhaité à rembourser par mois":
        amt_annuity = st.number_input("Montant mensuel à rembourser :", min_value=0, step=1)
    elif reimbursement_method == "Renseigner le nombre d'années sur lesquelles étaler le remboursement":
        reimbursement_period = st.number_input("Renseigner en nombre d'années la période de remboursement:",
                                               min_value=0,
                                               step=1)
        if reimbursement_period >= 1 :
            amt_annuity = amt_credit / (reimbursement_period * 12)
        else :
            amt_annuity = 0
    return gender, age, cnt_children, time_employment, income, own_car, own_realty, amt_goods_price, amt_credit, amt_annuity

def txt_comp():
    st.title("Comparaison de situation")
    st.markdown("""Comment énoncé sur la page d'accueil, cette extension de l'application sert
                à venir comparer sa situation avec d'autres personnes :red[ayant obtenu leur prêt]. Elle
                est recommandée aux personnes se voyant refuser leur demande de prêt.
                \n C'est purement dans un but de pédagogie et de transparence que cette ressource est
                mise à disposition. Elle peut aider le client à comprendre précisément quelles sont les
                raisons qui font que la demande est refusée en venant confronter quelques éléments de 
                sa situation à celles d'autres usagers.""")
    st.subheader("Décryptage des informations")

def txt_comp_noID():
    income = st.number_input("Revenu mensuel total :red[(requis)]", min_value=0, step=1)
    amt_credit = st.number_input("Montant total envisagé du crédit :red[(requis)]", min_value=0, step=1)
    reimbursement_method = st.radio("Quelle méthode choisissez-vous pour le remboursement :red[(requis)] :",
                                    ["Renseigner un montant souhaité à rembourser par mois",
                                     "Renseigner le nombre d'années sur lesquelles étaler le remboursement"])
    if reimbursement_method == "Renseigner un montant souhaité à rembourser par mois":
        amt_annuity = st.number_input("Montant mensuel à rembourser :", min_value=0, step=1)
    elif reimbursement_method == "Renseigner le nombre d'années sur lesquelles étaler le remboursement":
        reimbursement_period = st.number_input("Renseigner en nombre d'années la période de remboursement:",
                                               min_value=0,
                                               step=1)
        if reimbursement_period != 0 :
            amt_annuity = amt_credit / (reimbursement_period * 12)
    return income, amt_credit, amt_annuity

########################################
# Fonctions d'affichage des graphiques #
########################################

def graph_income(income, data):
    fig = plt.figure()
    if income <= 400000:
        data = [x for x in data if x <= 400000]
        sns.histplot(data, bins=18, log_scale=False)
        plt.axvline(income, color='red', linestyle='dashed', label='Salaire personnel')
        plt.xlabel("Salaire")
        plt.xticks([5e4,1e5,1.5e5,2e5,2.5e5,3e5,3.5e5,4e5],['50k','100k','150k','200k','250k','300k','350k','400k'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    else:
        sns.histplot(data, bins=35, log_scale=True)
        plt.axvline(income, color='red', linestyle='dashed', label='Salaire personnel')
        plt.xlabel("Salaire")
        plt.xticks([1e5,1e6,1e7],['100k','1M','10M'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)

def graph_credit(amt_credit, data):
    fig = plt.figure()
    sns.histplot(data, bins=50, log_scale=False)
    plt.axvline(amt_credit, color='red', linestyle='dashed', label='Montant de crédit demandé')
    plt.xlabel("Montant du crédit")
    plt.xticks([0,1e6,2e6,3e6,4e6],['0','1M','2M','3M','4M'])
    plt.ylabel("Distribution")
    plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
    plt.legend(loc='upper right')
    st.pyplot(fig)

def graph_annuity(amt_annuity, data):
    fig = plt.figure()
    if amt_annuity <= 100000:
        data = [x for x in data if x <= 100000]
        sns.histplot(data, bins=50, log_scale=False)
        plt.axvline(amt_annuity, color='red', linestyle='dashed', label='Montant des annuités choisies')
        plt.xlabel("Montant des annuités")
        plt.xticks([0,2e4,4e4,6e4,8e4,1e5],['0','20k','40k','60k','80k','100k'])
        plt.ylabel("Distribution")
        plt.yticks([5e3,1e4,1.5e4,2e4],['5,000','10,000','15,000','20,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    else:
        sns.histplot(data, bins=50, log_scale=False)
        plt.axvline(amt_annuity, color='red', linestyle='dashed', label='Montant des annuités choisies')
        plt.xlabel("Montant des annuités")
        plt.xticks([0,5e4,1e5,1.5e5,2e5,2.5e5],['0','50k','100k','150k','200k','250k'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)

#############
# Front-End #
#############

page = st.sidebar.selectbox('Select Page', ['Accueil','Obtention de prêt','Comparaison'])

# Accueil
if page == 'Accueil':
    txt_accueil()

# Obtention de prêt
if page =='Obtention de prêt':
    txt_loan()
    if st.checkbox("Je possède un numéro de demande de prêt"):
        client_ID = st.number_input("Numéro d'identification de la demande de prêt", step=1)
        client_info = requests.get(url+"client_info", params={"client_ID":client_ID})
        if client_info.json():
            if st.button("Simuler :"):
                score = requests.get(url+"predict/ID", params={"client_ID":client_ID}).json()
                if score < 49 : # le seuil obtenu était 0.51 (> =mauvais payeur) avec la proba donc 49(< =mauvais payeur) avec le score 
                    st.error(f"""Vous obtenez un score de **{round(score,1)}/100** . Cela est malheureusement trop faible pour être
                             en mesure de se voir offrir un prêt de notre part.""")
                else :
                    st.success(f"""Vous obtenez un score de **{round(score,1)}/100** . Vous êtes éligible à un prêt de notre part.
                                   Félicitations !""")
        else :
            st.error("L'identifiant fourni n'est pas reconnu dans notre base de données.")
    else :
        gender, age, cnt_children, time_employment, income, own_car, own_realty, amt_goods_price, amt_credit, amt_annuity = txt_loan_noID()
        if income >= 1 and amt_goods_price >= 1 and amt_credit >= 1 and amt_annuity >= 1 :
            if st.button("Simuler :"):
                score = requests.get(url+"predict/noID", params={"gender":gender,
                                                                "age":age,
                                                                "cnt_children":cnt_children,
                                                                "time_employment":time_employment,
                                                                "income":income,
                                                                "own_car":own_car,
                                                                "own_realty":own_realty,
                                                                "amt_goods_price":amt_goods_price,
                                                                "amt_credit":amt_credit,
                                                                "amt_annuity":amt_annuity}).json()
                if score < 49 : # le seuil obtenu était 0.51 (> =mauvais payeur) avec la proba donc 49(< =mauvais payeur) avec le score 
                    st.error(f"""Vous obtenez un score de **{round(score,1)}/100** . Cela est malheureusement trop faible pour être
                             en mesure de se voir offrir un prêt de notre part.""")
                else :
                    st.success(f"""Vous obtenez un score de **{round(score,1)}/100** . Vous êtes éligible à un prêt de notre part.
                                   Félicitations !""")
                st.warning("A noter que ce score est à caractère indicatif seulement.")
        else :
            st.error("Veuillez saisir les informations requises pour le calcul de vote profil.")

#Comparaison
if page == 'Comparaison':
    txt_comp()
    if st.checkbox("Je possède un numéro de demande de prêt"):
        client_ID = st.number_input("Numéro d'identification de la demande de prêt", step=1)
        client_info = requests.get(url+"client_info", params={"client_ID":client_ID})
        if client_info.json():
            if st.button("Résultats"):
                tab1, tab2, tab3, tab4 = st.tabs(["Salaire","Crédit","Annuités","Quelques métriques"])
                with tab1:
                    data_income = requests.get(url+"comparison/ID/graph_income",params={"client_ID":client_ID}).json()
                    income = data_income["income"]
                    data = data_income["data"]
                    st.header("Comparaion avec la distribution de salaire")
                    graph_income(income, data)
                    st.write("""Ce graphique compare votre salaire à la distribution de salaire
                             des personnes ayant obtenu un prêt chez nous. Il peut vous donner une/des
                             information(s) quant à votre capacité à effectuer un prêt.""")
                with tab2:
                    data_credit = requests.get(url+"comparison/ID/graph_credit",params={"client_ID":client_ID}).json()
                    amt_credit = data_credit["credit"]
                    data = data_credit["data"]
                    st.header("Comparaion avec la distribution des montants d'emprunts")
                    graph_credit(amt_credit, data)
                    st.write("""Ce graphique compare le montant de votre crédit demandé face à la distribution
                            des crédits que nous avons accepté. Il peut vous donner une/des
                            information(s) quant à votre capacité à effectuer un prêt.""")
                with tab3:
                    data_annuity = requests.get(url+"comparison/ID/graph_annuity",params={"client_ID":client_ID}).json()
                    amt_annuity = data_annuity["annuity"]
                    data = data_annuity["data"]
                    st.header("Comparaion avec la distribution des annuités remboursées")
                    graph_annuity(amt_annuity, data)
                    st.write("""Ce graphique compare le montant des annuités choisies face à la distribution
                     des autres montants d'annuités que nous avons accepté. Il peut vous donner une/des
                     information(s) quant à votre capacité à effectuer un prêt.""")
                with tab4:
                    data_metrics = requests.get(url+"comparison/ID/metrics",params={"client_ID":client_ID}).json()
                    m1 = data_metrics["metrics"][0]
                    m2 = data_metrics["metrics"][1]
                    m3 = data_metrics["metrics"][2]
                    st.header("Comparaison avec des personnes proches de votre situation")
                    st.subheader("Salaire")
                    st.write(f"Votre salaire est plus grand que :violet[{int(round(m1,0))}%] de notre échantillon.")
                    st.subheader("Crédit")
                    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
                             fait une demande de crédit d'une valeur de :violet[{int(round(m2,0))}].""")
                    st.subheader("Annuités")
                    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
                             choisi des annuités d'une valeur de :violet[{int(round(m3,0))}].""")
        else:
            st.error("L'identifiant fourni n'est pas reconnu dans notre base de données.")
    else :
        income, amt_credit, amt_annuity = txt_comp_noID()
        if income >= 1 and amt_credit >= 1 and amt_annuity >= 1 :
            if st.button("Résultats"):
                tab1, tab2, tab3, tab4 = st.tabs(["Salaire","Crédit","Annuités","Quelques métriques"])
                with tab1:
                    data_income = requests.get(url+"comparison/noID/graph_income").json()
                    data = data_income["data"]
                    st.header("Comparaion avec la distribution de salaire")
                    graph_income(income, data)
                    st.write("""Ce graphique compare votre salaire à la distribution de salaire
                             des personnes ayant obtenu un prêt chez nous. Il peut vous donner une/des
                             information(s) quant à votre capacité à effectuer un prêt.""")
                with tab2:
                    data_credit = requests.get(url+"comparison/noID/graph_credit").json()
                    data = data_credit["data"]
                    st.header("Comparaion avec la distribution des montants d'emprunts")
                    graph_credit(amt_credit, data)
                    st.write("""Ce graphique compare le montant de votre crédit demandé face à la distribution
                            des crédits que nous avons accepté. Il peut vous donner une/des
                            information(s) quant à votre capacité à effectuer un prêt.""")
                with tab3:
                    data_annuity = requests.get(url+"comparison/noID/graph_annuity").json()
                    data = data_annuity["data"]
                    st.header("Comparaion avec la distribution des annuités remboursées")
                    graph_annuity(amt_annuity, data)
                    st.write("""Ce graphique compare le montant des annuités choisies face à la distribution
                     des autres montants d'annuités que nous avons accepté. Il peut vous donner une/des
                     information(s) quant à votre capacité à effectuer un prêt.""")
                with tab4:
                    data_metrics = requests.get(url+"comparison/noID/metrics", params={"income":income}).json()
                    m1 = data_metrics["metrics"][0]
                    m2 = data_metrics["metrics"][1]
                    m3 = data_metrics["metrics"][2]
                    st.header("Comparaison avec des personnes proches de votre situation")
                    st.subheader("Salaire")
                    st.write(f"Votre salaire est plus grand que :violet[{int(round(m1,0))}%] de notre échantillon.")
                    st.subheader("Crédit")
                    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
                             fait une demande de crédit d'une valeur de :violet[{int(round(m2,0))}].""")
                    st.subheader("Annuités")
                    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
                             choisi des annuités d'une valeur de :violet[{int(round(m3,0))}].""")
        else :
            st.error("Veuillez saisir les informations requises.")
