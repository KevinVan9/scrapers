'''
Downloads all links as files from a specified page and saves them to the
folder of this program
'''

from bs4 import BeautifulSoup
import requests, time, os, csv


DELETE = True #Reset $html.txt file
FILE_TYPES = [".txt", ".csv", ".pdf", ".jpg", ".png"] #file types wanted
TARGET_SPECS = "" #similarities
url = "https://www.olgame.tw/sds/robot_inq.php?inq=-1&ip2=1" #URL of page to download from

def findnth(substr, string, n):
    index = 0
    curr = string.find(substr)
    index += curr
    string = string[curr + 1::]
    for i in range (n-1):
        curr = string.find(substr)
        index += curr + 1
        string = string[curr + 1::]
    return index

if os.path.isfile("$html.txt") and os.stat("$html.txt").st_size:
    '''
    Rig html straight from browser and paste it in $links.txt in the same directory.
    For sites that block scripts.
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

#print(html) 

'''Running through Gundam series and scraping units from each one into a csv'''
root = "https://www.olgame.tw/sds/"
series_table = html.find("table", {"width":"192", "border":"0", "cellspacing":"0", "cellpadding":"0"})
#new_csv = open("unit_list.csv", 'w')
#writer = csv.writer(new_csv)
#writer.writerow(['series', 'name', 'unit_id', 'img_link'])
print('series, unit_id, swapped hexadecimal(WXYZ->YZ WX), name , img_link')
i=0

for a in series_table.findAll("a", href=True):
    i+=1
    select = html.find('select', {'name':"inp2", 'class':"inp"})
    series = select.find("option", {"value":"{}".format(i)}).text.strip()
    url = root + a["href"]
    response = requests.get(url)
    source = response.text.strip()
    html = BeautifulSoup(source, 'lxml')
    for td in html.findAll("td", {'valign':"top", 'class':"edit"}):
        img_link = root + td.a.img["src"]
        name = td.text.strip()
        j = td.a["href"].find("id=")
        unit_id = td.a["href"][j+3:j+8]
        hexadecimal = str(hex(int(unit_id)))[2:]
        paste = hexadecimal[2:] + " " + hexadecimal[:2]
        print(series +', '+ unit_id+', '+ paste + ', '+ name+','+ img_link)
        #writer.writerow([series, unit_id, name, img_link])
#new_csv.close()






        
                

