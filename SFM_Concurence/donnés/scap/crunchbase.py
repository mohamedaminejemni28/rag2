import donnés.scap.transfor_markdown as transfor_markdown

# 1-trouver la page crunchbase d'une entreprise 2-acceder au page finaniciere ,3-scraper le contenu ,4-convertir en marldown , extraire une partie utile



def scrape_and_transform_crunchbase_financials(nom_entreprise:str,mots_cles:str=None):
    search_terms=nom_entreprise + "crunchbase"
    if mots_cles :
        search_terms+=" " + mots_cles
    results=transfor_markdown.search_urls_and_preview(search_terms,3)
    url =None 
    for result in results:
        if "crunchbase.com" in result['href']:
            url=result['href']
            break 
    if url is None:
        return "Aucune page Crunchbase trouvée."
    url = url.split("/organization/")[0] + "/organization/" + url.split("/organization/")[1].split("/")[0]
    url += "/company_financials"
    result=transfor_markdown.scrape_and_convert_to_markdown(url)
    with open("scrape_company.md", "w", encoding="utf-8") as f:
        f.write(result)
    return result

s=scrape_and_transform_crunchbase_financials("sfm technologies","SFM technologies" )
print("ssssssssssssssssssssssssssssssssssssssssssssssss/n",s)