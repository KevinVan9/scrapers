'''html attributes into search criteria of find function'''
a=input("here: ")
b="{"
a = a.replace("=", "':")
x = a.split()
b = "'"+x[0]+"', {"
for attr in a.split()[1:]:
    b += ("'" + attr + ", ")   
b = b[0:len(b)-2]
b += "}" 
print(b)
    

