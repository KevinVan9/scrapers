'''
Downloads all links as files from a specified page and saves them to the
folder of this program, assuming all links are valid
'''
from sys import argv
from bs4 import BeautifulSoup
from urllib.parse import unquote
from getpass import getpass
import requests, time, os


def find_nth(substr, string, n):
    index = 0
    curr = string.find(substr)
    index += curr
    string = string[curr + 1::]
    for _ in range (n-1):
        curr = string.find(substr)
        index += curr + 1
        string = string[curr + 1::]
    return index

def find_attr(session, url, tag, attributes):
    html = BeautifulSoup(session.get(url).text, 'lxml')
    val = html.find(tag, attributes)
    return val

def href_downloader(html, session=None, match=None, block=None):
    for a in html.find_all("a", href=True, target="_blank"):
        link = root + a["href"]
        if (not match and link.find("/") != -1) or (match and match in link): 
            if session:
                response = session.get(link)
            else:
                response = requests.get(link)
            url = unquote(response.url)
            name = url[len(url)-url[::-1].find("/")::]
            print("Downloading from: {} as '{}'".format(link, name))
            if block in name:
                print("Blocked link")
                pass
            with open("{}".format(name), "wb") as f:
                f.write(response.content)
                print("SUCCESS!\n")  
        else:
            print("Link not valid\n")
        
#Reset $html.txt file
DELETE = False
#file types wanted
FILE_TYPES = [".txt", ".csv", ".pdf", ".jpg", ".png"]
#link similarities
MATCH_KEYWORD = "content"
#block
BLOCK_KEYWORD = "pres"
#contains the nonce we needed to login
nonce_name = "blackboard.platform.security.NonceUtil.nonce"
#URL of login page
login_url = "https://app.lms.unimelb.edu.au/webapps/login/"
#url of page with all the content to download
url = None
#root url to stitch directories onto
root = login_url[0: find_nth("/", login_url, 3)]


os.chdir(os.path.dirname(argv[0]))
         
if os.path.exists("$html.txt") and os.stat("$html.txt").st_size and not url:
    '''
    Rig html straight from browser and paste it in $links.txt in the same directory.
    For sites that block scripts/non browser access.
    '''
    with open("$html.txt", "r") as f:
        source = f.read()
    if DELETE:    
        open('$html.txt', 'w').close()
    html = BeautifulSoup(source, 'lxml')
    
else:
    #Sites that don't block/redirect
    if not url:
        url = input("Enter url at which all links to download are on: ")
        username = input("Enter username: ")
        password = input("Enter password: ")

    #Stuff we send to server
    payload = {
        'user_id': username,
        'password': password,
        'action': 'login',
        'new_loc': ''
    }
    #Start new session with lms
    with requests.Session() as s:
        #Find nonce from session and add it to the payload so we can post it back in login form
        p = s.get(login_url)
        nonce = find_attr(s, login_url, 'input', {'name':nonce_name})
        payload[nonce_name] = nonce['value']
        p = s.post(login_url, data=payload)
        #Now we are logged in for our session
        #Now we make authorised request for page with files to download
        response = s.get(url)
        source = response.text
        html = BeautifulSoup(source, 'lxml')
        print(html)
        '''Grabbing all the a tags with hrefs and onclicks that have specification and using innermost directory as file name'''
        href_downloader(html, session=s, match=MATCH_KEYWORD, block=BLOCK_KEYWORD)
        


    




