import folium
import pandas as pd
import urllib.request
def exportStations(url):
    page = urllib.request.urlopen(url)
    text =  str(page.read().decode(page.headers.get_content_charset()))
    text=text[text.index("stations"):text.index("    $(document)")]
    #print(text[text.index("stations"):text.index("    $(document)")])
    with open("Stations.txt","r",encoding="utf-8") as file:
        stationLocations=eval(file.read())
    temp=text.split(",\"other\":")


    for st in temp:
        if st.find("lat")!=-1:
            latPos = st.find("lat") + len("lat\":\"")
            lat = float(st[latPos:st.find("\"", latPos)])

            lngPos=st.find("lng")+len("lng\":\"")
            lng=float(st[lngPos:st.find("\"",lngPos)])

            namePos=st.rfind("name")+len("name\": \"")
            name=st[namePos:st.find("\"",namePos)]
            pos=[lat,lng]
            stationLocations[name]=pos


    with open('Stations.txt', 'w', encoding='utf-8') as file:
        file.write(str(stationLocations))
    file.close()
def encodeUrl(str):
    lib = {"ē": "%c4%93",
           "ŗ": "%c5%97",
           "ū": "%c5%ab",
           "ī": "%c4%ab",
           "ō": "%c5%8d",
           "ļ": "%c4%ba",
           "ķ": "%c4%b6",
           "ģ": "%c4%9f",
           "š": "%c5%a1",
           "ā": "%c4%81",
           "ņ": "%c5%86",
           "č": "%c4%8d",
           "ž": "%c5%be ",
           "Ō": "%c5%8c",
           "Ī": "%c4%aa",
           "Ū": "%c5%aa",
           "Ŗ": "%c5%96",
           "Ē": "%c4%93",
           "Ļ": "%c4%b9",
           "Ķ": "%c4%b6",
           "Ģ": "%c4%9e",
           "Š": "%c5%a0",
           "Ā": "%c4%80",
           "Ņ": "%c5%85",
           "Č": "%c4%8c",
           "Ž": "%c5%bd"}
    for let in str:
        if let in lib.keys():
            str = str.replace(let, lib[let])

    return str
def getLinkList():
    sites=["/autobusu-kustibu-saraksts","/tramvaju-kustibu-saraksts"]
    linkList = []
    for site in sites:
        page = urllib.request.urlopen('https://satiksme.daugavpils.lv' + site)
        text = str(page.read().decode(page.headers.get_content_charset()))
        timetableURLs = text[text.find("class=\"odd\""):text.find("</table>", text.find("class=\"odd\""))]
        timetableURLs = timetableURLs.split("href=\"")
        timetableURLs.pop(0)

        for st in timetableURLs:
            tempUrl = st[0:st.find("\"")]
            tempUrl = encodeUrl(tempUrl)
            linkList.append("https://satiksme.daugavpils.lv" + tempUrl)
    return linkList

def updateStations():
    linkList=getLinkList()
    for link in linkList:
        exportStations(link)
# Create a map centered at a specific location
#def CreateMap(workdayTimetable,holydayTimetable):
m = folium.Map(location=[55.872, 26.5356], zoom_start=15,zoom_control=False)  # Daugavpils coordinates
updateStations()
stations={}
stationNames=[]
stationCoords=[]
with open('Stations.txt', 'r', encoding='utf-8') as file:
    stations=eval(file.read())
    stationNames=stations.keys()
    stationCoords=stations.values()
#data=pd.DataFrame(workdayTimetable.values(),workdayTimetable.keys())
#table = data.to_html(
#   classes="table table-striped table-hover table-condensed table-responsive"
#)
h="""
<style>
.button {
  background-color: #04AA6D; /* Green */
  border: 1px solid green;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  font-size: 14px;
  cursor: pointer;
  width: 100px;
  display: block;
}

.button:not(:last-child) {
  border-bottom: none; /* Prevent double borders */
}

.button:hover {
  background-color: #3e8e41;
}
</style>
<body>

<div >
  <button class="button">Button</button>
  <button class="button">Button</button>
</div>

</body>
"""
if len(stationNames)==len(stationCoords):
    for cor,name in zip(stationCoords,stationNames):
        html = f"""
            <div style="font-family: 'Arial'; font-size: 14px; color: black;">
                <b>{name}</b>
            </div>
        """
        # Create a popup with the custom HTML
        popup = folium.Popup(h)
        tooltip=folium.Tooltip(html)
        # Add marker with the custom popup
        marker=folium.Marker(location=cor,tooltip=tooltip, popup=popup).add_to(m)

# Save the map to an HTML file
m.save('nyc_map.html')
