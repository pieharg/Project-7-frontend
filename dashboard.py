import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import requests

url = "https://project-7-40e812473cc8.herokuapp.com/"

#####################
# Obtention de prêt #
#####################

def minimum_salary(amt_income):
    """
    Return True or False depending if the income inputed is enough for simulation or comparison
    """
    minimum_salary = requests.get(url+"minimum_income", params={"amt_income":amt_income}).json()
    return minimum_salary

def maximum_salary(amt_income):
    """
    Return True or False depending if the income inputed is too much for simulation or comparison
    """
    maximum_salary = requests.get(url+"maximum_income", params={"amt_income":amt_income}).json()
    return maximum_salary

def result(score):
    """
    Takes in the score and display the simulation result
    """
    if score < 48 : # le seuil obtenu était 0.52 (> =mauvais payeur) avec la proba donc 48(< =mauvais payeur) avec le score 
        st.error(f"""Vous obtenez un score de **{round(score,1)}/100** . Cela est malheureusement trop faible pour être
                 en mesure de se voir offrir un prêt de notre part.""")
    else :
        st.success(f"""Vous obtenez un score de **{round(score,1)}/100** . Vous êtes éligible à un prêt de notre part. 
                   Félicitations !""")

def got_loan_number_simulation():
    """
    Display text and return the simulation result for an already-made request
    """
    col1, col2 = st.columns(2)
    with col1 :
        client_ID = st.number_input("Numéro d'identification de la demande de prêt", step=1)
        client_info = requests.get(url+"client_info", params={"client_ID":client_ID})
    if client_info.json():
        if st.button("Simuler :"):
            score = requests.get(url+"predict/ID", params={"client_ID":client_ID}).json()
            result(score)
    else :
        st.error("L'identifiant fourni n'est pas reconnu dans notre base de données.")

def mandatory_info():
    """
    Display and return MANDATORY informations for simulation
    """
    st.subheader("""_:red[Informations nécessaires à la simulation]_""")
    col1, col2 = st.columns(2)
    with col1 :
        income = st.number_input("Revenu mensuel total", min_value=0, step=1)
        amt_goods_price = st.number_input("Montant du/des bien(s) à acheter", min_value=0, step=1)
        amt_credit = st.number_input("Montant total envisagé du crédit", min_value=0, step=1)
        reimbursement_method = st.radio("Quelle méthode choisissez-vous pour le remboursement :",
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
        return income, amt_goods_price, amt_credit, amt_annuity

def optional_info():
    """
    Display and return OPTIONAL information for simulation
    """
    st.subheader("""_:orange[Informations optionnelles à la simulation]_""")
    col1, col2 = st.columns(2)
    with col1 :
        gender = st.selectbox("Civilité", ["Monsieur","Madame"], index=None, placeholder="Veuillez choisir une option.")
        age = st.number_input("Age", min_value=0, step=1)
        cnt_children = st.number_input("Nombre d'enfants à charge", step=1)
        time_employment = st.number_input("Temps en activité (en années)", min_value=0, step=1) 
        own_car = st.selectbox("Possédez-vous une voiture ?", ["Oui","Non"], index=None, placeholder="Veuillez choisir une option.")
        own_realty = st.selectbox("Êtes-vous propriétaire immobilier ?", ["Oui","Non"], index=None, placeholder="Veuillez choisir une option.")
    return gender, age, cnt_children, time_employment, own_car, own_realty

def retrieve_score_mandatory(amt_income, amt_goods_price, amt_credit, amt_annuity):
    """
    Retrieve score from backend and return simulation result for mandatory part only
    """
    score = requests.get(url+"predict/mandatory", params={"amt_income":amt_income,
                                                          "amt_goods_price":amt_goods_price,
                                                          "amt_credit":amt_credit,
                                                          "amt_annuity":amt_annuity}).json()
    result(score)

def retrieve_score_optional(amt_income, amt_goods_price, amt_credit, amt_annuity, gender, age, cnt_children, time_employment, own_car, own_realty):
    """
    Retrieve score from backend and return simulation result for (mandatory + optional) part
    """
    score = requests.get(url+"predict/optional", params={"amt_income":amt_income,
                                                         "amt_goods_price":amt_goods_price,
                                                         "amt_credit":amt_credit,
                                                         "amt_annuity":amt_annuity,
                                                         "gender":gender,
                                                         "age":age,
                                                         "cnt_children":cnt_children,
                                                         "time_employment":time_employment,
                                                         "own_car":own_car,
                                                         "own_realty":own_realty}).json()
    result(score)

###############
# Comparaison #
###############

def tab1_comparison(amt_income):
    """
    Return a few metrics relative to the database to compare situations
    """
    m1 = requests.get(url+"compare/metric_1", params={"amt_income":amt_income}).json()
    m2 = requests.get(url+"compare/metric_2", params={"amt_income":amt_income}).json()
    m3 = requests.get(url+"compare/metric_3", params={"amt_income":amt_income}).json()
    st.header("Comparaison avec des personnes proches de votre situation")
    st.subheader("Salaire")
    st.write(f"Votre salaire est plus grand que :violet[{int(round(m1,0))}%] de notre échantillon.")
    st.subheader("Crédit")
    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
             fait une demande de crédit d'une valeur de :violet[{int(round(m2,0))}].""")
    st.subheader("Annuités")
    st.write(f"""Les personnes avec un salaire proche du votre (plus ou moins 5%) ont en moyenne
             choisi des annuités d'une valeur de :violet[{int(round(m3,0))}].""")
    
def tab2_comparison(amt_income):
    """
    Return graph to compare client income relative to the database income distribution
    """
    distrib_income = requests.get(url+"compare/distribution_income").json()
    st.header("Comparaison avec la distribution de salaire")
    fig = plt.figure()
    if amt_income <= 400000:
        distrib_income = [x for x in distrib_income if x <= 400000]
        sns.histplot(distrib_income, bins=18, log_scale=False)
        plt.axvline(amt_income, color='red', linestyle='dashed', label='Salaire personnel')
        plt.xlabel("Salaire")
        plt.xticks([5e4,1e5,1.5e5,2e5,2.5e5,3e5,3.5e5,4e5],['50k','100k','150k','200k','250k','300k','350k','400k'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    else:
        sns.histplot(distrib_income, bins=35, log_scale=True)
        plt.axvline(amt_income, color='red', linestyle='dashed', label='Salaire personnel')
        plt.xlabel("Salaire")
        plt.xticks([1e5,1e6,1e7],['100k','1M','10M'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    st.write("""Ce graphique compare votre salaire à la distribution de salaire
             des personnes ayant obtenu un prêt chez nous. Il peut vous donner une/des
             information(s) quant à votre capacité à effectuer un prêt.""")

def tab3_comparison(amt_credit) :
    """
    Return graph to compare client credit amount relative to the database credit amount distribution
    """
    distrib_credit = requests.get(url+"compare/distribution_credit").json()
    st.header("Comparaison avec la distribution du montant du crédit")
    fig = plt.figure()
    sns.histplot(distrib_credit, bins=50, log_scale=False)
    plt.axvline(amt_credit, color='red', linestyle='dashed', label='Montant de crédit demandé')
    plt.xlabel("Montant du crédit")
    plt.xticks([0,1e6,2e6,3e6,4e6],['0','1M','2M','3M','4M'])
    plt.ylabel("Distribution")
    plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
    plt.legend(loc='upper right')
    st.pyplot(fig)
    st.write("""Ce graphique compare le montant de votre crédit demandé face à la distribution
             des crédits que nous avons accepté. Il peut vous donner une/des
             information(s) quant à votre capacité à effectuer un prêt.""")

def tab4_comparison(amt_annuity):
    """
    Return graph to compare client annuity amount relative to the database annuity amount distribution
    """
    distrib_annuity = requests.get(url+"compare/distribution_annuity").json()
    st.header("Comparaison avec la distribution du montant des annuités")
    fig = plt.figure()
    if amt_annuity <= 100000:
        distrib_annuity = [x for x in distrib_annuity if x <= 100000]
        sns.histplot(distrib_annuity, bins=50, log_scale=False)
        plt.axvline(amt_annuity, color='red', linestyle='dashed', label='Montant des annuités choisies')
        plt.xlabel("Montant des annuités")
        plt.xticks([0,2e4,4e4,6e4,8e4,1e5],['0','20k','40k','60k','80k','100k'])
        plt.ylabel("Distribution")
        plt.yticks([5e3,1e4,1.5e4,2e4],['5,000','10,000','15,000','20,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    else:
        sns.histplot(distrib_annuity, bins=50, log_scale=False)
        plt.axvline(amt_annuity, color='red', linestyle='dashed', label='Montant des annuités choisies')
        plt.xlabel("Montant des annuités")
        plt.xticks([0,5e4,1e5,1.5e5,2e5,2.5e5],['0','50k','100k','150k','200k','250k'])
        plt.ylabel("Distribution")
        plt.yticks([1e4,2e4,3e4,4e4],['10,000','20,000','30,000','40,000'])
        plt.legend(loc='upper right')
        st.pyplot(fig)
    st.write("""Ce graphique compare le montant des annuités choisies face à la distribution
             des autres montants d'annuités que nous avons accepté. Il peut vous donner une/des
             information(s) quant à votre capacité à effectuer un prêt.""")

def got_loan_number_comparison() :
    """
    Display text and return the comparison result for an already-made request
    """
    col1, col2 = st.columns(2)
    with col1 :
        client_ID = st.number_input("Numéro d'identification de la demande de prêt", step=1)
    client_info = requests.get(url+"client_info", params={"client_ID":client_ID})
    if client_info.json() :
        if st.button("Résultats") :
            tab1, tab2, tab3, tab4 = st.tabs(["Quelques métriques","Salaire","Crédit","Annuités"])
            with tab1 :
                client_income = requests.get(url+"compare/ID/client_income", params={"client_ID":client_ID}).json()
                tab1_comparison(client_income)
            with tab2 :
                tab2_comparison(client_income)
            with tab3 :
                client_credit = requests.get(url+"compare/ID/client_credit", params={"client_ID":client_ID}).json()
                tab3_comparison(client_credit)
            with tab4 :
                client_annuity = requests.get(url+"compare/ID/client_annuity", params={"client_ID":client_ID}).json()
                tab4_comparison(client_annuity)
    else :
        st.error("L'identifiant fourni n'est pas reconnu dans notre base de données.")

def compare_mandatory(amt_income, amt_credit, amt_annuity) :
    """
    Display text and return the comparison result
    """
    if st.button("Résulats") :
        tab1, tab2, tab3, tab4 = st.tabs(["Quelques métriques","Salaire","Crédit","Annuités"])
        with tab1 :
            tab1_comparison(amt_income)
        with tab2 :
            tab2_comparison(amt_income)
        with tab3 :
            tab3_comparison(amt_credit)
        with tab4 :
            tab4_comparison(amt_annuity)

#######################
# Page d'informations #
#######################

def txt_info_page():
    st.title("Page d'informations")
    st.header("Objectif de l'application")
    st.write("""Cette application a pour but d'être un prototype front-end dans une démarche 
            de mise en place d'un projet MLOps. Elle se présente en 2 parties distinctes.""")
    st.subheader("Obtention de prêt")
    st.write("""Cette première partie est la principale raison d'exister de cette application.
             C'est dans cet onglet que le client peut renseigner son numéro de demande de prêt
             si celle-ci a déjà été formulée auprès de l'établissement bancaire. Si ce n'est pas
             le cas, quelques informations essentielles à l'obtention d'un prêt ainsi que quelques informations
             complémentaires peuvent également être communiquées afin d'obtenir une première simulation.""")
    st.subheader("L'onglet de comparaison")
    st.write("""Cette deuxième extension n'est pas un passage obligé de l'application. Elle sert
             seulement au client à comparer sa situation et/ou sa demande de prêt avec d'autres
             demandes déjà formulées :red[et acceptées]. Elle peut notamment être utile si le prêt est refusé afin
             de comprendre les raisons du refus.""")
    
#####################
# Wrapper Front-End #
#####################

page = st.sidebar.selectbox('Select Page', ['Obtention de prêt','Comparaison',"Page d'informations"])

# Obtention de prêt
if page =='Obtention de prêt':
    st.title("Simulation d'une demande de crédit")
    st.write("""Pour plus d'informations sur le critère d'obtention et sur le fonctionnement du
             simulateur, se référer à la page d'informations accessible via les différents onglets.""")
    st.subheader("Calculateur")
    col1, col2 = st.columns(2)
    with col1 :
        method_simulation = st.selectbox("Possédez-vous déjà un numéro de demande de prêt ?",
                                        ("Oui","Non"),
                                        index=None,
                                        placeholder="Veuillez choisir une option.")
    st.divider()
    if method_simulation == "Oui" : # si demande pré-faite
        got_loan_number_simulation()
    elif method_simulation == "Non": # si pas de demande pré-faite
        amt_income, amt_goods_price, amt_credit, amt_annuity = mandatory_info()
        if st.checkbox("Je souhaite également remplir les informations optionnelles (recommandé)"):
            st.divider()
            gender, age, cnt_children, time_employment, own_car, own_realty = optional_info()
            if amt_goods_price >= 1 and amt_credit >= 1 and amt_annuity >= 1 and gender != None and age >=1 and own_car != None and own_realty != None :
                if minimum_salary(amt_income) :
                    if maximum_salary(amt_income) :
                        if st.button("Simuler"):
                            retrieve_score_optional(amt_income, amt_goods_price, amt_credit, amt_annuity, gender, age, cnt_children, time_employment, own_car, own_realty)
                    else :
                        st.error("Votre revenu mensuel est trop élevé pour prétendre à un crédit dans notre établissement.")
                else :
                    st.error("Votre revenu mensuel est trop faible pour prétendre à un crédit dans notre établissement.")
            else :
                st.error("Veuillez saisir toutes les informations affichées pour le calcul de vote profil.")
        else :
            if amt_goods_price >= 1 and amt_credit >= 1 and amt_annuity >= 1 :
                if minimum_salary(amt_income) :
                    if maximum_salary(amt_income) :
                        if st.button("Simuler") :
                            retrieve_score_mandatory(amt_income, amt_goods_price, amt_credit, amt_annuity)
                    else :
                        st.error("Votre revenu mensuel est trop élevé pour prétendre à un crédit dans notre établissement.")
                else :
                    st.error("Votre revenu mensuel est trop faible pour prétendre à un crédit dans notre établissement.")
            else :
                st.error("Veuillez saisir les informations requises pour le calcul de vote profil.")

# Comparaison
if page == 'Comparaison' :
    st.title("Comparaison de situation")
    st.write("""Pour plus d'informations sur le critère d'obtention et sur le fonctionnement du 
             simulateur, se référer à la page d'informations accessible via les différents onglets.""")
    st.subheader("Comparateur")
    col1, col2 = st.columns(2)
    with col1 :
        method_comparison = st.selectbox("Possédez-vous déjà un numéro de demande de prêt ?",
                                         ("Oui","Non"),
                                         index=None,
                                         placeholder="Veuillez choisir une option.")
    st.divider()
    if method_comparison == "Oui" :
        got_loan_number_comparison()
    elif method_comparison == "Non" :
        amt_income, amt_goods_price, amt_credit, amt_annuity = mandatory_info()
        if amt_goods_price >= 1 and amt_credit >= 1 and amt_annuity >= 1 :
            if minimum_salary(amt_income) :
                if maximum_salary(amt_income) :
                    compare_mandatory(amt_income, amt_credit, amt_annuity)
                else :
                    st.error("""Votre salaire est trop élevé pour obtenir un crédit dans notre établissement.
                             Une comparaison n'est pas envisageable.""")
            else :
                st.error("""Votre salaire est trop faible pour obtenir un crédit dans notre établissement. 
                         Une comparaison n'est pas envisageable.""")
        else :
            st.error("Veuillez saisir les informations requises pour la comparaison de votre situation.")

# Page d'informations
if page == "Page d'informations":
    txt_info_page()