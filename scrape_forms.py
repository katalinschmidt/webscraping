"""Driver file for scraping IRS Prior Year Products website & returning site's query as JSON"""

from bs4 import BeautifulSoup
import logging
import requests
import json


logging.basicConfig(filename='scrape_forms_activity.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

BASE_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"


def get_search_params():
    """Prompt user for desired forms' names"""

    print("Please type the desired forms' names.")
    print("E.g. '> Form W-2', or '> Form W-2, Form 1095-C'")

    return input("> ").title().split(", ")


def get_all_search_results(search_params):
    """Query IRS Prior Year Products page for user's desired forms / search params & return results"""
        
    logging.info(f"Executing search for: {search_params}")

    # Create container for all results:
    all_search_results = []

    # Search for each form in user's list of desired forms:
    for desired_form in search_params:
        # Initialize var for pagination:
        idx_first_row = 0

        # Execute GET request until pagination complete:
        while True:
            # Modify BASE_URL for desired search:
            search_url = (BASE_URL + "?" + 
                        "indexOfFirstRow={}" + 
                        "&sortColumn=sortOrder" +
                        "&value={}" +
                        "&criteria=formNumber" + 
                        "&resultsPerPage=200" +
                        "&isDescending=false"
                        ).format(idx_first_row, desired_form)

            # Request raw HTML:
            response = requests.get(search_url)
            logging.info(response)


            # Check for unsuccessful response:
            if response.status_code != 200:
                return "HTTP Error Code"

            # If successful response, use BeautifulSoup to parse HTML:
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.findAll(True, {'class':['even','odd']})
            
            # Check for completed pagination:
            if search_results == []:
                logging.info(f"No data found for given criteria: {search_url}")
                break
            # If pagination inccomplete, pull data from table:
            else:
                for row in search_results:
                    product_num = row.find('td', class_='LeftCellSpacer').text.strip()
                    title = row.find('td', class_='MiddleCellSpacer').text.strip()
                    year = row.find('td', class_='EndCellSpacer').text.strip()
                    pdf_link = row.find('a')['href']

                    # Add current result to all results list:
                    all_search_results.append(
                        {
                        'product_num': product_num,
                        'title': title,
                        'year': year,
                        'pdf_link': pdf_link
                        }            
                    )
                
                # Paginate table:
                logging.info("Paginating table...")
                idx_first_row += 200 # +=200 because resultsPerPage=200
    
    return all_search_results


def return_user_query(search_params, all_search_results):
    """Filter all_search_results for forms that are an exact match to user's search_params & return as JSON incl. max/min years"""

    all_form_years = {} 
    form_num_to_title = {}
    for result in all_search_results:
        # Calc max/min year by collecting all years of a given form:
        if result['product_num'] in all_form_years:
            all_form_years[result['product_num']].append(result['year'])
        else:
            all_form_years[result['product_num']] = [result['year']]
        # Track title for each product num (for next for loop):
        form_num_to_title[result['product_num']] = result['title']


    exact_matches = []
    for desired_form in search_params:
        for key, value in all_form_years.items():
            # Since all_form_years already has unique keys repr each product_num (i.e. no duplicates), 
            # we will pull the final search result from there:
            if desired_form == key:
                exact_matches.append(
                    {
                    'form_number': key,
                    'form_title': form_num_to_title[key],
                    'min_year': min(value),
                    'max_year': max(value)
                    }
                )
    
    exact_matches = json.dumps(exact_matches)
    
    # Write JSON data to file:
    with open("query_results.json", "w") as file:
        file.write(json.dumps(json.loads(exact_matches), indent=4, sort_keys=True))
        file.close()
        
    logging.info("Query successful! Results stored in '/query_results.json'.")
    print("Query successful! View results in '/query_results.json'.")


if __name__ == "__main__":
    search_params = get_search_params()
    all_search_results = get_all_search_results(search_params)

    if len(all_search_results) == 0:
        logging.info(f"False query for search params: {search_params}")
        print("ERROR: FALSE QUERY")
        print("Please check your input!")

    elif all_search_results == "HTTP Error Code":
        print("HTTP Error. Please try again.")

    else:
        return_user_query(search_params, all_search_results)