"""Driver file for scraping IRS Prior Year Products website & downloading site's PDFs"""

from bs4 import BeautifulSoup
import logging
import requests
import os


logging.basicConfig(filename='scrape_downloads_activity.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

BASE_URL = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"


def get_form_name():
    """Prompt user for desired forms' names"""

    print("Please type the desired form's name.")
    print("E.g. '> Form W-2' or '> Form 1095-C'")

    return input("> ").title()


def get_desired_yrs():
    """Prompt user for desired range of years"""

    print("Please type the desired inclusive range of years.")
    print("E.g. '> 2018-2020'")

    year_range = input("> ").title().split("-")

    # Account for input, where user only inputs one year:
    if len(year_range) == 1:
        year_range = [year_range[0], year_range[0]]

    return year_range


def get_all_search_results(desired_form):
    """Query IRS Prior Year Products page for user's desired forms / search params & return results"""
    
    logging.info(f"Executing search for: {desired_form}")
    
    # Create container for all results:
    all_search_results = []

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


def download_forms(desired_form, desired_yrs, all_search_results):
    """Filter all_search_results for forms that are an exact match to user's search params & download"""

    # Create subdirectory if it does not already exist:
    file_path = f'{desired_form}/example.pdf'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Successful created subdirectory {directory}.")

    # Move into subdirectory:
    os.chdir(desired_form)

    for result in all_search_results:
        # If the user's search params matche the current search result, download form to subdirectory:
        if desired_form == result['product_num'] and desired_yrs[0] <= result['year'] and desired_yrs[1] >= result['year']:
            response = requests.get(result['pdf_link'])
            logging.info(response)

            # Check for unsuccessful response:
            if response.status_code != 200:
                return "HTTP Error Code"

            # Save file with formatted name to curr subdirectory:
            file_name = "{} - {}.pdf".format(result['product_num'], result['year'])
            with open(file_name, "wb") as file:
                file.write(response.content)
                file.close()

    logging.info(f"Query successful! PDFs saved to '/{desired_form}.")
    print(f"Query successful! View PDFs in '/{desired_form}.")


if __name__ == "__main__":
    desired_form = get_form_name()
    desired_yrs = get_desired_yrs()
    all_search_results = get_all_search_results(desired_form)

    if len(all_search_results) == 0:
        logging.info("False query for search params: {desired_form}, {desired_yrs}")
        print("ERROR: FALSE QUERY")
        print("Please check your input!")

    elif all_search_results == "HTTP Error Code":
        print("HTTP Error. Please try again.")

    else:
        download_forms(desired_form, desired_yrs, all_search_results)