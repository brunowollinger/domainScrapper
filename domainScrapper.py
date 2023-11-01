from bs4 import BeautifulSoup
import Levenshtein
import requests
import zipfile
import os
import sys
import re

def setup():
    if not os.path.isdir('reports'):
        os.mkdir('reports')
    if not os.path.exists('reports/rankedDomains.csv'):
        with open('reports/rankedDomains.csv', 'w'):
            pass
    return

def download():
    response = requests.get('https://www.whoisds.com/newly-registered-domains')
    if response.status_code != 200:
        print(f'Error accessing the URL: {response.status_code}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    tableRow = table.find_all('tr')[2]
    linkCell = tableRow.find_all('td')[-1]
    downloadLink = linkCell.find('a')['href']

    fileRequest = requests.get(downloadLink)
    filename = re.search(r'filename="(.*)"', fileRequest.headers['Content-Disposition']).group(1)
    fullPath = f'reports/{filename}'
    with open(fullPath, 'wb') as file:
        file.write(fileRequest.content)
    return fullPath

def extractDomains(fullPath):
    with zipfile.ZipFile(fullPath, 'r') as file:
        extractedFilename = file.namelist()[0]
        file.extractall('reports')
    os.remove(fullPath)
    return f'reports/{extractedFilename}'

def rankDomains(targetDomain, fullPath):
    with open(fullPath, 'r') as domainList:
        with open('reports/rankedDomains.csv', 'a') as rankedDomains:
            for line in domainList:
                line = line.rstrip()
                csvString = f"{line},{Levenshtein.distance(targetDomain, line)}\n"
                rankedDomains.write(csvString)

def main():
    setup()
    try:
        targetDomain = sys.argv[1]
    except IndexError:
        print('Target domain missing!')
        return
    zipFullPath = download()
    txtFullPath = extractDomains(zipFullPath)
    rankDomains(targetDomain, txtFullPath)

if __name__ == '__main__':
    main()
