import requests
from bs4 import BeautifulSoup

# Convert from ticker to CIK
# Used when first searching for a company form
def getCompanyNameAndCIK(input):
    # Form URL to search for ticker
    url = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + input + "&owner=exclude&action=getcompany"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    # Get results
    try:
        results = soup.find("span", {"class": "companyName"}).text.split(" CIK#: ")
        company_name = results[0]
        CIK = results[1][:10]
        # I believe all CIK numbers are 10 long
    except IndexError:
        return None

    return company_name, CIK


# Convert from CIK to the most recently filed 13F document as an XML
# Having a date included as an input and then checking it with any matching "documentsbutton"
# filing dates would allow for fetching specific 13F forms that aren't the most recent
def get13F_Form(CIK):
    # Search for 13F forms associated with the given CIK
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" \
          + CIK + "&type=&dateb=&count=100&scd=filings"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    # "documentsbutton" is the id for each possible link for each UI button that has a link
    # Keep the first link that has a 13F as a formName - Will be most recent in order
    try:
        links = soup.findAll("a", id="documentsbutton")
        for link in links:
            form_name = link.previous_element.previous_element.previous_sibling.text
            if form_name[:3] == "13F":
                # soup of the page containing links holing the xml information
                soup = BeautifulSoup(requests.get("https://www.sec.gov" + link["href"]).text, "html.parser")

                # date of form - done after finding the right form so it only needs to be given a value once
                form_date = soup.find("div", string="Filing Date").next_sibling.next_sibling.text

                # link used to get "INFORMATION TABLE" xml form file
                link_href = soup.findAll("td", string="INFORMATION TABLE")[2].next_sibling.next_sibling.next_element[
                    "href"]
                # xml form page
                xml = requests.get("https://www.sec.gov" + link_href).text
                return xml, form_name, form_date
    except IndexError:
        return [None, None, None]

    return [None, None, None]
