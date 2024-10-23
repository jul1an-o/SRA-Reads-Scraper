import requests
from bs4 import BeautifulSoup

# Function to get the number of spots and the run information from the SRA page
def get_run_and_spots(sra_link):
    response = requests.get(sra_link)
    if response.status_code != 200:
        print(f"Failed to retrieve {sra_link} - Status Code: {response.status_code}")
        return None, None

    # Parse the SRA page
    sra_soup = BeautifulSoup(response.text, 'html.parser')

    # Look for all tables on the page
    tables = sra_soup.find_all('table')
    
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
                    run_name = cells[0].text.strip()
                    number_of_spots = cells[1].text.strip()
                    return run_name, number_of_spots

    return None, None

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
    sample_links = soup.find_all('a', href=True, string=lambda x: x and 'GSM' in x)

    # Print header for tab-delimited output
    print("Sample\tRun\t# of Spots")
    
    for sample_link in sample_links:
        sample_url = f"https://www.ncbi.nlm.nih.gov{sample_link['href']}"
        sample_response = requests.get(sample_url)
        
        if sample_response.status_code != 200:
            print(f"Failed to retrieve {sample_url} - Status Code: {sample_response.status_code}")
            continue

        sample_soup = BeautifulSoup(sample_response.text, 'html.parser')
        sra_link_tag = sample_soup.find('a', href=True, string=lambda x: x and 'SRX' in x)
        
        if sra_link_tag:
            sra_link = sra_link_tag['href']

            # Get the run and the number of spots from the SRA page
            run_name, number_of_spots = get_run_and_spots(sra_link)
            if run_name and number_of_spots:
                print(f"{sample_link.text}\t{run_name}\t{number_of_spots}")
            else:
                print(f"{sample_link.text}\tNo run found or spots not found.")
        else:
            print(f"{sample_link.text}\tNo SRA link found.")

if __name__ == "__main__":
    gse_id = input("Please enter the GSE ID (e.g., GSE234205): ")
    scrape_gse_samples(gse_id)