import urllib.request

def encodeUrl(str):
    lib={"ē":"%c4%93",
         "ŗ":"%c5%97",
         "ū":"%c5%ab",
         "ī":"%c4%ab",
         "ō":"%c5%8d",
         "ļ":"%c4%ba",
         "ķ":"%c4%b6",
         "ģ":"%c4%9f",
         "š":"%c5%a1",
         "ā":"%c4%81",
         "ņ":"%c5%86",
         "č":"%c4%8d",
         "ž":"%c5%be ",
         "Ō":"%c5%8c",
         "Ī":"%c4%aa",
         "Ū":"%c5%aa",
         "Ŗ":"%c5%96",
         "Ē":"%c4%93",
         "Ļ":"%c4%b9",
         "Ķ":"%c4%b6",
         "Ģ":"%c4%9e",
         "Š":"%c5%a0",
         "Ā":"%c4%80",
         "Ņ":"%c5%85",
         "Č":"%c4%8c",
         "Ž":"%c5%bd"}
    for let in str:
        if let in lib.keys():
            str=str.replace(let,lib[let])

    return str

url='https://satiksme.daugavpils.lv'
page = urllib.request.urlopen(url+'/autobusu-kustibu-saraksts')
text =  str(page.read().decode(page.headers.get_content_charset()))


timetableURLs=text[text.find("class=\"odd\""):text.find("</table>",text.find("class=\"odd\""))]
timetableURLs=timetableURLs.split("href=\"")
timetableURLs.pop(0)
linkList=[]
for st in timetableURLs:
    tempUrl=st[0:st.find("\"")]
    tempUrl=encodeUrl(tempUrl)
    linkList.append("https://satiksme.daugavpils.lv"+tempUrl)
