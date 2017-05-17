#!/usr/bin/python
from urllib2 import urlopen
import json, unicodedata
import os

# setting workding directories
script_dir = os.path.dirname(os.path.abspath(__file__))
ticket_dir = os.path.join(script_dir, 'wiiu_tickets')
bin_dir = os.path.join(script_dir, '3ds_files')
try:
        os.makedirs(ticket_dir)
except OSError:
        pass # already exists
try:
        os.makedirs(bin_dir)
except OSError:
        pass # already exists

#download URLs

url_wiiu='http://wiiu.titlekeys.gq'
url_3ds='http://3ds.titlekeys.gq'

# download JSON files from wiiu and 3ds from webserver and save it to "$CONSOLE.json"
response = urlopen("%s/json" % url_wiiu)
with open('wiiu.json', 'w') as json_file:
    for item in response:
          json_file.write("%s\n" % item)
json_file.close()
response = urlopen("%s/json" % url_3ds)
with open('3ds.json', 'w') as json_file:
    for item in response:
          json_file.write("%s\n" % item)
json_file.close()
# read Content of $CONSOLE.json file and parse it from JSON syntax
with open('wiiu.json') as json_file:
    parsed_wiiu = json.load(json_file)
json_file.close()
with open('3ds.json') as json_file:
    parsed_3ds = json.load(json_file)
json_file.close()

#open formatted output key.file
def generate_keyfile(input,type):
    if type == "wiiu":
        key_file = open("keys_%s.txt" % type,'w')
        key_file.write("""#Common Keys#
D7B00402659BA2ABD2CB0DB27FA2B656 # Wii U Common Key:
805E6285CD487DE0FAFFAA65A6985E17 # Wii U Espresso Ancast Key
B5D8AB06ED7F6CFC529F2CE1B4EA32FD # Wii U Starbuck Ancast Key
############################################################

TitleID # TitleKey # Title Name (REGION) # Ticket Type
""")
    elif type == "3ds":
        key_file = open("keys_%s.txt" % type,'w')
        key_file.write("""TitleID # TitleKey # encTitleKey # Title Name (REGION) # Serial # Ticket Type
""")
        remote_file_list = ["download","downloadenc","seeddb","downloadmissingforencryption"]
        filename = ["decTitleKeys.bin","encTitleKeys.bin","seeddb.bin","decTitleKeys_missing.bin"]
        count = 0
        for i in remote_file_list:
            url = "%s/%s" % (url_3ds, i)
            file = urlopen(url)
            path = os.path.join(bin_dir, filename[count])
            print "Downloading:", path, ""
            with open(path,'wb') as output:
                  output.write(file.read())
            file.close()
            count = count + 1
    for i in xrange(len(input)):
        if input[i]['titleKey'] == None or input[i]['name'] == None:
            pass
        else:
            key = input[i]['titleKey']
            titleid = input[i]['titleID']
            name = input[i]['name']
            name = name.replace('\n','').replace('\t','')
            name = unicodedata.normalize('NFKD', name).encode('ascii','ignore')
            region = input[i]['region']
# set line per line with the variables declared
            if not 'encTitleKey' in input[i]:
                pass
            else:
                enckey = input[i]['encTitleKey']
#                print input[i]['encTitleKey']
            if not 'serial' in input[i]:
                pass
            else:
                serial = input[i]['serial']
            if type == "wiiu":
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
                if input[i]['ticket'] == "1":
                    filename = "%s.tik" % input[i]['titleID']
                    path = os.path.join(ticket_dir, filename)
                    url = "%s/ticket/%s" % (url_wiiu, filename)
                    if not os.path.isfile(path):
                        print "Downloading:", path
                        ticketfile = urlopen(url)
                        with open(path,'wb') as output:
                              output.write(ticketfile.read())
                        ticketfile.close()
            elif type == "3ds":
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
            line_data = "%s # %s" % (str(titleid), str(key))
            if 'enckey' in locals():
                line_data = "%s # %s" % (str(line_data), str(enckey))
            line_data = "%s # %s # %s" % (line_data, str(name), str(region))
            if 'serial' in locals():
                line_data = "%s # %s" % (str(line_data), str(serial))
            line_data = "%s # %s" % (line_data, str(tiktype))
            normalized_data = "".join(line_data)
            key_file.write("%s\n" %normalized_data)

generate_keyfile(parsed_wiiu, "wiiu")
generate_keyfile(parsed_3ds, "3ds")
