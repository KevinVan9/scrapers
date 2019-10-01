'''
Downloads all links as files from a specified page and saves them to the
folder of this program.
'''


from bs4 import BeautifulSoup
import requests, time, os


DELETE = True #Reset $html.txt file
FILE_TYPES = [".txt", ".csv", ".pdf", ".jpg", ".png"] #file types wanted
TARGET_SPECS = "" #link similarities
url = "" #URL of page to download from

def findnth(substr, string, n):
    index = 0
    curr = string.find(substr)
    index += curr
    string = string[curr + 1::]
    for _ in range (n-1):
        curr = string.find(substr)
        index += curr + 1
        string = string[curr + 1::]
    return index

if os.stat("$html.txt").st_size:
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
        url = input("Enter url: ")
    response = requests.get(url)
    source = response.text
    html = BeautifulSoup(source, 'lxml')


'''Note: This is specific to scraping off github...'''


'''Grabbing all the a tags with hrefs with specs and using innermost directory as file name'''
for a in html.find_all("a", href=True):
    link = a["href"]
    if link and link[0] == "/": #Stitching child directory to the url to form valid link
        index = findnth("/", url, 3) #Index of first directory assuming there are two '/' in the domain. // in https://
        link = url[:index] + link
    print("Link: " + link)

    link.replace("blob", "raw") #github blob directory is preview. raw is download
    
    if (not TARGET_SPECS and link.find("/") != -1) or (TARGET_SPECS and TARGET_SPECS in link): 
        name = ''
        i=-1
        while link[i] != "/":
            name = link[i] + name
            i-=1
        if name and name[len(name)-4::] in FILE_TYPES: 
            print("Downloading from: {} as '{}'".format(link, name))
            response = requests.get(url)
            with open("{}".format(name), "wb") as f:
                f.write(response.content)
                print("SUCCESS!\n")
        else:
            print("Link not valid\n")          
    else:
        print("Link not valid\n")

'''_____'''
        
                

