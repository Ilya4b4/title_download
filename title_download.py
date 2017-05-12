#!/usr/bin/python
from urllib2 import urlopen
import json, unicodedata
import os

# setting workding directories
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'wiiu_tickets')
try:
        os.makedirs(dest_dir)
except OSError:
        pass # already exists

#download URLs
url_wiiu='http://wiiu.titlekeys.gq/json'
url_3ds='http://3ds.titlekeys.gq/json'

# download JSON files from wiiu and 3ds from webserver and save it to "$CONSOLE.json"
response = urlopen(url_wiiu)
with open('wiiu.json', 'w') as json_file:
    for item in response:
          json_file.write("%s\n" % item)
json_file.close()
print "Saved raw JSON Output to", script_dir, "wiiu.json"
# read Content of wiiu.json file and parse it from JSON syntax
with open('wiiu.json') as json_file:
    parsed = json.load(json_file)
json_file.close()

#open formatted output key.file
key_file = open("keys_wiiu.txt",'w') 
key_file.write("""#Common Keys#
D7B00402659BA2ABD2CB0DB27FA2B656 # Wii U Common Key:
805E6285CD487DE0FAFFAA65A6985E17 # Wii U Espresso Ancast Key
B5D8AB06ED7F6CFC529F2CE1B4EA32FD # Wii U Starbuck Ancast Key
############################################################

TitleID # TitleKey # Title Name (REGION) # Ticket Type
""")
#go over parsed file content
for i in xrange(len(parsed)):
# check if the content of Titlekey or Name is empty
    if parsed[i]['titleKey'] == None or parsed[i]['name'] == None:
        pass
    else:
# set variables
        key = parsed[i]['titleKey']
        titleid = parsed[i]['titleID']
# Check if title is application, dlc, etc...
        if titleid[:8] == "00050000":
            tiktype = "eShop/Application";
            pass
        elif titleid[:8] == "00050002":
            tiktype = "Demo"
            pass
        elif titleid[:8] == "0005000E":
            tiktype = "Patch"
            pass
        elif titleid[:8] == "0005000C":
            tiktype = "DLC"
            pass
        else:
            tiktype = "Unknown"
            pass
# Check if a Ticket is available and download it, if it doesn't exit
        if parsed[i]['ticket'] == "1":
            filename = "%s.tik" % titleid
            path = os.path.join(dest_dir, filename)
            url_tik = "http://wiiu.titlekeys.gq/ticket/%s" % filename
            if os.path.isfile(path):
                print "File", path, "already exists."
            else:
                print "Downloading:", path
                ticketfile = urlopen(url_tik)
                with open(path,'wb') as output:
                      output.write(ticketfile.read())
                ticketfile.close()
# format name variable for plaintext
        name = parsed[i]['name']
        name = name.replace('\n','').replace('\t','')
        name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
        region = parsed[i]['region']
# set line per line with the variables declared
        line_data = str(titleid),' # ', str(key),' # ',str(name),' (',str(region),')',' # ',str(tiktype)
        normalized_data = "".join(line_data)
# write lines to file 
        key_file.write("%s\n" %normalized_data)
print "Saved WiiU Title Information to:", script_dir, "keys_wiiu.txt"
key_file.close()

############
# 3ds part #
############

response = urlopen(url_3ds)
with open('3ds.json', 'w') as json_file:
    for item in response:
          json_file.write("%s\n" % item)
json_file.close()
print "Saved raw JSON Output to", script_dir, "3ds.json"

# read Content of wiiu.json file and parse it from JSON syntax
with open('3ds.json') as json_file:
    parsed = json.load(json_file)
json_file.close()

key_file = open("keys_3ds.txt",'w') 
key_file.write("""TitleID # TitleKey # encTitleKey # Title Name (REGION) # Serial # Ticket Type
""")
#go over parsed file content
for i in xrange(len(parsed)):
# check if the content of Titlekey or Name is empty
    if parsed[i]['titleKey'] == None or parsed[i]['name'] == None:
        pass
    else:
# set variables
        key = parsed[i]['titleKey']
        titleid = parsed[i]['titleID']
        if titleid[:8] == "00040010" or "0004001b" or "0004009b" or "000400db" or "00040030" or "00040130" or "00040138":
            tiktype = "System";
            pass
        elif titleid[:8] == "00040000":
            tiktype = "eShop/Application"
            pass
        elif titleid[:8] == "00040001":
            tiktype = "DlpChild"
            pass
        elif titleid[:8] == "00040002":
            tiktype = "Demo"
            pass
        elif titleid[:8] == "0004000e":
            tiktype = "Patch"
            pass
        elif titleid[:8] == "0004008c":
            tiktype = "DLC"
            pass
        elif titleid[:8] == "00048004":
            tiktype = "DSiWare"
            pass
        elif titleid[:8] == "00048005" or "0004800f":
            tiktype = "DSi System"
            pass
        else:
            tiktype = "Unknown"
            pass
# format name variable for plaintext
        serial = parsed[i]['serial']
        enckey = parsed[i]['encTitleKey']
        name = parsed[i]['name']
        name = name.replace('\n','').replace('\t','')
        name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
        region = parsed[i]['region']
# set line per line with the variables declared
        line_data = str(titleid),' # ', str(key),' # ', str(enckey),' # ',str(name),' (',region,')',' # ',str(serial),' # ', str(tiktype)
        normalized_data = "".join(line_data)
# write lines to file 
        key_file.write("%s\n" %normalized_data)
print "Saved 3DS Title Information to:", script_dir, "keys_3ds.txt"
key_file.close()
