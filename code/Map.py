from os import remove
from offline_folium import offline
import folium
import pandas as pd
import urllib.request
from branca.element import Template, MacroElement, JavascriptLink


def averageCoords(coords):  # [[lat1,lng1],[lat2,lng2]]
    avlat = (coords[0][0] + coords[1][0]) / 2
    avlng = (coords[0][1] + coords[1][1]) / 2
    return [avlat, avlng]
def exportStations(url):
    page = urllib.request.urlopen(url)
    text = str(page.read().decode(page.headers.get_content_charset()))
    text = text[text.index("{\"routes"):text.index("    $(document)")]
    data = eval(text)
    with open("Stations.txt", "r", encoding="utf-8") as file:
        stationLocations = eval(file.read())
    for station in data["stations"]:
        name = station["name"]
        if "\\\"" in name:
            name = name.replace("\\\"", "*")
        pos = [float(station["geo"]['lat']), float(station["geo"]['lng'])]
        if name in stationLocations.keys():
            pos = averageCoords([pos, stationLocations[name]])
        stationLocations[name] = pos
    remove('Stations.txt')
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
           "ž": "%c5%be",
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
def checkForExtraLink(url):
    extraLink="None"
    page = urllib.request.urlopen(url)
    text = str(page.read().decode(page.headers.get_content_charset()))
    text= text[text.index("<span class=\"change-derection\"></span>"):text.index("<div class=\"streets\">")-5]
    if len(text)>40:
        extraLink=text[text.index("<a href=\'")+len("<a href=\'"):text.index("\' class=\'back-link\'>")]
    return extraLink
def getLinkList():
    saite="/daugavpils-kustibu-saraksts"
    linkList = []
    page = urllib.request.urlopen('https://satiksme.daugavpils.lv' + saite)
    text = str(page.read().decode(page.headers.get_content_charset()))
    timetableURLs = text[text.find("class=\"odd\""):text.find("</table>", text.find("class=\"odd\""))]
    timetableURLs = timetableURLs.split("href=\"")
    timetableURLs.pop(0)

    for st in timetableURLs:
        tempUrl = st[0:st.find("\"")]
        tempUrl = encodeUrl(tempUrl)
        linkList.append("https://satiksme.daugavpils.lv" + tempUrl)
        extraLink=checkForExtraLink(linkList[-1])
        if extraLink != "None":
            extraLink = encodeUrl(extraLink)
            linkList.append("https://satiksme.daugavpils.lv" + extraLink)
    return linkList

def upddateMap():
    """ In last build uncomment this!!!
    linkList = getLinkList()
    for link in linkList:
        exportStations(link)
    """
    m = folium.Map(location=[55.872, 26.5356], zoom_start=15,zoom_control=False)  # Daugavpils coordinate
    with open('Stations.txt', 'r', encoding='utf-8') as file:
        stations = eval(file.read())
        stationNames = stations.keys()
        stationCoords = stations.values()
    if len(stationNames) == len(stationCoords):
        for cor, name in zip(stationCoords, stationNames):
            if "*" in name:
                name = name.replace("*","\\\"")
            htmlTooltip = f"""
                <div style = "font-family: 'Arial'; font-size: 14px; color: black;">
                    <b>{name}</b>
                </div>
            """
            if "\\\"" in name:
                name=name.replace("\\\"","*")
            htmlIcon = """<style>
                         button {
                         border: none;
                         background-color: inherit;
                         }
                         .icon{
                         position: absolute;
                         top: -31px;
                         left: -11px;
                         }
                        </style>
                        """+f"""
                        <button onmouseup = "openNav('{name}')">"""

            if "*" in name:
                name = name.replace("*","\"")
            htmlIcon+=f"""
                         <img class = "icon"  src = "icons/marker-shadow.png">
                         <img class = "icon" id = '{name}' src = "icons/marker-icon.png" >
                        </button>
                        """
            tooltip = folium.Tooltip(htmlTooltip)
            icon = folium.DivIcon(htmlIcon)
            marker = folium.Marker(location = cor,
                                 tooltip = tooltip,
                                 icon = icon
                                 ).add_to(m)
    menu = """
    {% macro html(this, kwargs) %}
        <style>
            /* Боковая панель */
            .sidebar {
                max-height: 30%;
                width: 300px;
                position: fixed;
                z-index: 1000;
                top: 10px;
                left: 10px;
                background-color: #f8f9fa;
                transition: 0.5s;
            }

            /* Стили элементов бокового меню */
            #stationName{                
                width: 260px;
                padding: 4px 4px 4px 4px;
                text-align: center;
                left: 0px;
                font-size: 20px;
                color: #333;
                display: inline;
                border: none;
            }            
            #searchImg{
                height: 90%;
                top: 5%;
                right: 5%;
            }
            #searchButton{
                height: 100%;
                width: 40px;
                position: absolute;
                right: 0px;
                border: none;
                background-color: #64c8fb;
            }

            
        </style>

        <div id = "sidebar" class = "sidebar">
                <input type = "text" id = "stationName" name = "stationName">
                <button type = "button" id = "searchButton" onclick = "searchStation()"><img id = "searchImg" src = "icons/search.png">
        </div>
        <script>            
             document.addEventListener("DOMContentLoaded", function() {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.station_finder = channel.objects.station_finder;
                });
            });
            function searchStation(){
            """+f"""      
                var map = window.{m.get_name()};"""+"""
                let name = document.getElementById("stationName").value
                station_finder.findStation(name,
                    function(coords){     
                        if (coords.length == 2){
                            var center = map.getCenter();
                            let xDif = center.lat - coords[0];
                            let yDif = center.lng - coords[1];
                            let distance = Math.sqrt(xDif*xDif+yDif*yDif);
                            if (distance>0.012){
                            
                                let zoom;
                                if (map.getZoom() < 16) zoom = 16;
                                else zoom = map.getZoom();    
                                map.setView(coords, zoom);
                            }
                            if(document.getElementsByClassName("current").length > 0){             
                                document.getElementsByClassName("current")[0].src = "icons/marker-icon.png";                    
                                document.getElementsByClassName("current")[0].classList.remove("current");
                            }      
                            document.getElementById(name).classList.add("current");  
                            document.getElementById(name).src = "icons/current-marker-icon.png";
                        }
                    }
                ); 
            }
            
            function openNav(name) {
                while(name.includes("*") == true){
                    name = name.replace("*","\\\"");          
                }
                document.getElementById("stationName").value=name;  
                searchStation();
                
                
            }
    
            /* Закрыть боковое меню */
            function closeNav() {
                document.getElementById("sidebar").style.height = "0";
            }
    </script>
    {% endmacro %}
    """
    menu_element = MacroElement()
    menu_element._template = Template(menu)
    m.get_root().header.add_child(JavascriptLink('qrc:///qtwebchannel/qwebchannel.js'))
    m.get_root().add_child(menu_element)
    return m
    # Save the map to an HTML file
if __name__ == "__main__":
    m=upddateMap()
    m.save('nyc_map.html')