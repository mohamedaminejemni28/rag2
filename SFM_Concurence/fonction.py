import pandas as pd
from ftfy import fix_text
import seaborn as sns
import matplotlib.pyplot as plt



def read_file(file_excel: str, sheet_name: str) -> pd.DataFrame:
    df=pd.read_excel(file_excel, sheet_name)
    return df

def nettoyer_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.applymap(lambda x: fix_text(str(x)) if isinstance(x, str) else x)




def formation_filtré(df:pd.DataFrame,service:str )-> pd.DataFrame:

    df_filtré = df[df["Produit/Service"].str.lower().str.strip() == service.lower().strip()]
    return df_filtré


def concurent_triéee_partarif(df:pd.DataFrame):
        df_triée = df.sort_values(by="Nouveau_Tarif (€)", ascending=True).reset_index(drop=True)
        return df_triée


def concurant_actif_ou_pas(df:pd.DataFrame,offre:str):
    df_offres = df[df["Offre_Spéciale"].str.strip().str.lower() == offre]
    return df_offres


def static_tarif(df:pd.DataFrame):
        stats = df.groupby("Produit/Service")["Nouveau_Tarif (€)"].agg(
        Tarif_Minimum="min",
        Tarif_Maximum="max",
        Tarif_Moyen="mean"
        ).reset_index()

        return stats    


def generer_resume_concurrentiel(df: pd.DataFrame):



    resume = "Résumé du marché concurrentiel \n"
    services = df["Produit/Service"].unique()

    for service in services:
    
        df_service = df[df["Produit/Service"] == service]
        min_tarif = df_service["Nouveau_Tarif (€)"].min()
        max_tarif = df_service["Nouveau_Tarif (€)"].max()
        moy_tarif = df_service["Nouveau_Tarif (€)"].mean()
        nb_offres = df_service[df_service["Offre_Spéciale"].str.lower() == "oui"].shape[0]

        resume += (
                f"{service} : de {min_tarif} à {max_tarif}€, "
                f"moyenne {round(moy_tarif, 2)}€, "
                f"{nb_offres} offre(s) spéciale(s)."
                "\n"
            )

    return resume



def plot_tarifs(df: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    sns.boxplot(x="Produit/Service", y="Nouveau_Tarif (€)", data=df)
    plt.title("Distribution des tarifs par service")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_offres_speciales(df: pd.DataFrame):
    df_offres = df[df["Offre_Spéciale"].str.lower().str.strip() == "oui"]
    offres_par_service = df_offres["Produit/Service"].value_counts().sort_values(ascending=False)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=offres_par_service.index, y=offres_par_service.values)
    plt.title("Nombre d’offres spéciales par service")
    plt.ylabel("Nombre d’offres spéciales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def exporter_vers_excel(df: pd.DataFrame, 
                        df_filtré: pd.DataFrame, 
                        df_triée: pd.DataFrame, 
                        df_stats: pd.DataFrame, 
                        filename: str = "analyse_concurrentielle.xlsx"):

    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name="Données Nettoyées", index=False)
        df_filtré.to_excel(writer, sheet_name="Filtrage Service", index=False)
        df_triée.to_excel(writer, sheet_name="Tri Par Tarif", index=False)
        df_stats.to_excel(writer, sheet_name="Statistiques", index=False)


def exporter_resume_txt(resume: str, filename: str = "resume_concurrentiel.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(resume)









df=read_file("Agent_Commercial_IA_SFM_Gigantic_Dataset.xlsx","Veille_Concurrents")
print(df.head())
df=nettoyer_df(df)
df_form=formation_filtré(df,"Formation Cloud")
print("dfform",df_form.head())
df_triée=concurent_triéee_partarif(df)
print(df_triée.head())

df_off=concurant_actif_ou_pas(df,"non")
print("df_off",df_off.head())

stats=static_tarif(df)
print(stats)


resume=generer_resume_concurrentiel(df)
print("resume********************",resume)


     
#plot_tarifs(df)
#plot_offres_speciales(df)

exporter_vers_excel(df, df_form, df_triée, stats)
exporter_resume_txt(resume)
