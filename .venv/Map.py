import folium
import pandas as pd
import urllib.request
from branca.element import Template, MacroElement
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

def upddateMap():
    """ In last build uncomment this!!!
    linkList = getLinkList()
    for link in linkList:
        exportStations(link)
    """
    m = folium.Map(location=[55.872, 26.5356], zoom_start=15,zoom_control=False)  # Daugavpils coordinate
    stations={}
    stationNames=[]
    stationCoords=[]
    with open('Stations.txt', 'r', encoding='utf-8') as file:
        stations=eval(file.read())
        stationNames=stations.keys()
        stationCoords=stations.values()
    if len(stationNames)==len(stationCoords):
        for cor,name in zip(stationCoords,stationNames):
            htmlTooltip = f"""
                <div style="font-family: 'Arial'; font-size: 14px; color: black;">
                    <b>{name}</b>
                </div>
            """
            htmlIcon="""
                        <style>
                         button {border: none;
                            background-color: inherit;}
                         img{position:absolute}
                        </style>
                        """+f"""
                        <button onclick="openNav('{name}')">
                         <img src="icons\marker-shadow.png">
                         <img src="icons\marker-icon.png" >
                        </button>
                        """
            tooltip=folium.Tooltip(htmlTooltip)
            icon=folium.DivIcon(htmlIcon)
            marker=folium.Marker(location=cor,
                                 tooltip=tooltip,
                                 icon=icon).add_to(m)
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
                padding: 8px 8px 8px 8px;
                text-align: center;
                left: 0px;
                font-size: 16px;
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

        <div id="sidebar" class="sidebar">
            <form id="search">
                <input type="text" id="stationName" name="stationName">
                <button type="button" id="searchButton" onclick="searchStation()"><img id="searchImg" src="icons\search.png">
                </form>
        </div>

        <script>
            function searchStation(){
            }
            
            function openNav(name) {
                document.getElementById("sidebar").style.height = "auto";   
                document.getElementById("stationName").value=name;
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
    m.get_root().add_child(menu_element)
    return m
    # Save the map to an HTML file
