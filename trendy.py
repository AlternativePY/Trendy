import pandas as pd
from colorama import Fore, Style, init
import logging
import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import os

# Set up logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Set default values for parameters
months = 6
trend = 75
remove_keywords = ["kelime 1", "kelime-2", "kelime3"]

# Function to remove data based on specified keywords
def remove_data(keywords_to_remove):
    df = pd.read_csv('semrush.csv')

    # Filtering out rows containing specified keywords in the 'URL' column
    mask = df['URL'].str.contains('|'.join(keywords_to_remove), case=False, na=False)
    df = df[~mask]

    df.to_csv('semrush.csv', index=False)

# Function to keep only unique URLs in the dataset
def unique_urls():
    df = pd.read_csv('semrush.csv')

    unique_df = df.drop_duplicates(subset='URL', keep='first')
    
    unique_df.to_csv('semrush.csv', index=False)

# Function to query data based on specified criteria
def query_data(months, trend):
    df = pd.read_csv('semrush.csv')

    # Filtering data based on trends criteria
    def trend_check(trends_str):
        trends = eval(trends_str)
        min_count = months
        min_value = trend
        count = sum(1 for t in trends if t > min_value)
        return count >= min_count

    df = df[df['Trends'].apply(trend_check)]
    
    df.to_csv('Data/data.csv', index=False)
    df.to_excel('Data/data.xlsx', index=False)
    print(Fore.GREEN + Style.BRIGHT + "\nData analysis completed!")

# Function to fetch the title of a given URL
def run_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.text.strip() if soup.title else "Title Not Found"
        return title
    except requests.exceptions.RequestException as e:
        error_message = f"URL: {url} - Connection error: {e}"
        logging.error(Fore.RED + Style.BRIGHT + error_message)
        return None
    except Exception as e:
        error_message = f"URL: {url} - An error occurred: {e}"
        logging.error(Fore.RED + Style.BRIGHT + error_message)
        return None

# Function to fetch titles for URLs in the dataset
def fetch_titles():
    csv_file = 'Data/data.csv'
    output_file = 'Data/title.txt'
    
    try:
        df = pd.read_csv(csv_file)
        urls = df["URL"]
        
        with open(output_file, 'a', encoding='utf-8') as f:
            for url in urls:
                title = run_url(url)
                if title:
                    f.write(f"{title}\n")
                else:
                    f.write(Fore.RED + Style.BRIGHT + "\nTitle Not Found")
        
        print(Fore.RED + Style.BRIGHT + f"\nTitle data successfully written to {output_file}.")
    except Exception as e:
        logging.error(f"CSV File: {csv_file} - An error occurred: {e}")
        print(Fore.RED + Style.BRIGHT + "\nAn error occurred. Details are in the 'error.log' file.")

# Function to clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main loop for user interaction
while True:
    clear_console()
    text = """
    ┌────────────────────────────────────────────────────┐
    │████████╗██████╗ ███████╗███╗   ██╗██████╗ ██╗   ██╗│
    │╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔══██╗╚██╗ ██╔╝│
    │   ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ██║ ╚████╔╝ │
    │   ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║  ╚██╔╝  │
    │   ██║   ██║  ██║███████╗██║ ╚████║██████╔╝   ██║   │
    │   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝    ╚═╝   │
    └────────────────────────────────────────────────────┘
    """

    print(Fore.WHITE + Style.BRIGHT + f"{text}")
    
    print(Fore.WHITE + Style.BRIGHT + "\n[1] Query Data""\n""\n[2] Fetch Titles""\n")

    choice = input(Fore.WHITE + Style.BRIGHT + "\nMake your choice: ")

    if choice == '1':
        unique_urls()
        remove_data(remove_keywords)
        query_data(months, trend)
        input("\nPress any key to continue: ") 
    elif choice == '2':
        fetch_titles()
        input("\nPress any key to continue: ")                         
    elif choice.lower() == 'q':
        print(Fore.WHITE + Style.BRIGHT + "\nExiting the program..")
        break
    else:
        print(Fore.WHITE + Style.BRIGHT + "\nInvalid choice!")
        input("\nPress any key to continue: ")
