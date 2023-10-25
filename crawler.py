import requests
from bs4 import BeautifulSoup

def is_ip_logger(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Check if the page contains any suspicious keywords indicating an IP logger
    suspicious_keywords = ['iplogger', 'iplogger.org', 'iplogger.com']
    
    for keyword in suspicious_keywords:
        if keyword in response.text:
            # Check if the page specifically mentions IP loggers
            if "explain" in response.text.lower() and "what" in response.text.lower():
                return False
            return True
    
    return False
    
def crawl(start_url):
    visited = set()
    queue = [(start_url, 0)]
    
    while queue:
        url, depth = queue.pop(0)
        visited.add(url)
        
        if is_ip_logger(url):
            crawl_data = open('crawl_data.txt', 'a')
            crawl_data.write(url + '\n')
        
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.startswith('http') and href not in visited:
                        queue.append((href, depth + 1))
            except:
                continue

def main():
    crawl('https://www.iplogger.org/')

if __name__ == '__main__':
    main()