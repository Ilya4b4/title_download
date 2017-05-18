# WiiU/3DS Title ID,Keys and Ticket Downloader
Download pretty much all content from both wiiu.titlekeys.gq
and 3ds.titlekys.gq
* JSON file to setup a mirror from the original site
* plain text key.txt for daily usage
* $TITLEID.tik files for all availble wiiu ticket files
* decrypted and encrypted 3ds ticket files for use with freeshop etc

## Arguments
* -w, --wiiu     download everything from wiiu site"
* -3, --3ds      download everything from 3ds site"
* --wurl URL     specify url for the wiiu titlekey site with http[s] prefix"
* --3url URL     specify url for the 3ds titlekey site with http[s] prefix"
* -l, --local    generate key file only. Do not attempt for network connection"

## Usage
```bash
python title:download.py -w -d
```
Downloads everything from both 3ds and wiiu titlekey site

```bash
python title_download.py -3 --3url "http://example.site"
```
Downloads everything from 3ds titlekey site with a custom url

```bash
python title_download.py -w -3 --wurl "http://example.site" --3url "http://3ds.example.site"
```
Downloads everything from bot 3ds and wiiu titlkey site with custom urls
for both arguments

```bash
python title_download.py -3 -w --local
```
Only converts the local "wiiu.json" and "3ds.json" file into human
readable format

## ToDos
* none at the moment
