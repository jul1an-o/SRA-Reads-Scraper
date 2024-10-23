import requests
from bs4 import BeautifulSoup

# Function to get the number of spots from the SRA page
def get_number_of_spots(sra_link):
    response = requests.get(sra_link)
    if response.status_code != 200:
        print(f"Failed to retrieve {sra_link} - Status Code: {response.status_code}")
        return None

    # Parse the SRA page
    sra_soup = BeautifulSoup(response.text, 'html.parser')

    # Look for all tables on the page
    tables = sra_soup.find_all('table')
    print(f"Found {len(tables)} tables on the page.")
    
    # Loop through each table to find the one with the run information
    for table in tables:
        # Get all the rows from the table
        rows = table.find_all('tr')
        
        for row in rows:
            # Get all the cells in the row
            cells = row.find_all('td')
            if cells and len(cells) > 1:  # Ensure there's enough data
                # Check if the first cell contains 'Run'
                if 'SRR' in cells[0].text:  # Adjust to look for the run name
                    # The number of spots is typically in the second cell
                    number_of_spots = cells[1].text.strip()
                    return number_of_spots

    return None

# Function to scrape the GSE page for samples
def scrape_gse_samples(gse_id):
    gse_url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={gse_id}"
    response = requests.get(gse_url)
    if response.status_code != 200:
        print(f"Failed to retrieve {gse_url} - Status Code: {response.status_code}")
        return
    
    # Parse the GSE page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all sample links
    sample_links = soup.find_all('a', href=True, text=lambda x: x and 'GSM' in x)
    
    for sample_link in sample_links:
        sample_url = f"https://www.ncbi.nlm.nih.gov{sample_link['href']}"
        print(f"Fetching sample page: {sample_url}")
        sample_response = requests.get(sample_url)
        
        if sample_response.status_code != 200:
            print(f"Failed to retrieve {sample_url} - Status Code: {sample_response.status_code}")
            continue

        sample_soup = BeautifulSoup(sample_response.text, 'html.parser')
        sra_link_tag = sample_soup.find('a', href=True, text=lambda x: x and 'SRX' in x)
        
        if sra_link_tag:
            sra_link = sra_link_tag['href']
            print(f"Identified SRA link: {sra_link}")

            # Get the number of spots from the SRA page
            number_of_spots = get_number_of_spots(sra_link)
            if number_of_spots:
                print(f"Number of spots for {sample_link.text}: {number_of_spots}")
            else:
                print(f"Number of spots not found for {sample_link.text}.")
        else:
            print(f"No SRA link found for {sample_link.text}.")

if __name__ == "__main__":
    gse_id = input("Please enter the GSE ID (e.g., GSE234205): ")
    scrape_gse_samples(gse_id)