import math
import random
from os import remove
import folium
import pandas as pd
import urllib.request
from branca.element import Template, MacroElement, JavascriptLink



def checkForSimilarCords(cords,currentsid, stations):
    for sid in stations:
        if stations[sid]['pos'] == cords and sid != currentsid:
            return False
    return True


def exportStations(url):
    page = urllib.request.urlopen(url)
    text = str(page.read().decode(page.headers.get_content_charset()))
    text = text[text.index("{\"routes"):text.index("    $(document)")]
    data = eval(text)
    with open("Stations.txt", "r", encoding="utf-8") as file:
        stationLocations = eval(file.read())
    for station in data["stations"]:
        sid = station["sid"]
        name = station["name"].strip()
        transportName = busORtrain(url) + " " + station["number"]
        pos = [float(station["geo"]['lat']), float(station["geo"]['lng'])]
        if "\"" in name:
            name = name.replace("\"", "*")
        """
        {sid:{'name':name, 'pos':pos},sid:{'name':name, 'pos':pos}} 
        {sid:{'name':name, 'pos':pos, 'transport':transport},sid:{'name':name, 'pos':pos, 'transport':transport}}
        transport = {transportName:[wtime,htime],transportName:[wtime,htime]}
        wtime,htime = ["time","time"]
        """
        if sid in stationLocations.keys():
            if transportName not in stationLocations[sid]['transport'].keys():
                stationLocations[sid]['transport'][transportName] = [station["wtlist"],station["htlist"]]
        if sid not in stationLocations.keys() and checkForSimilarCords(pos,sid,stationLocations):
            stationLocations[sid]={'name':name,'pos':pos,'transport':{transportName:[station["wtlist"],station["htlist"]]}}

    remove('Stations.txt')
    with open('Stations.txt', 'w', encoding='utf-8') as file:
        file.write(str(stationLocations))
    file.close()

def encodeUrl(url):
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
    for let in url:
        if let in lib.keys():
            url = url.replace(let, lib[let])
    return url
def checkForExtraLink(url):
    extraLink="None"
    page = urllib.request.urlopen(url)
    text = str(page.read().decode(page.headers.get_content_charset()))
    text= text[text.index("<span class=\"change-derection\"></span>"):text.index("<div class=\"streets\">")-5]
    if len(text)>40:
        extraLink=text[text.index("<a href=\'")+len("<a href=\'"):text.index("\' class=\'back-link\'>")]
    return extraLink
def busORtrain(url):
    if url.find("tramvajs") != -1:
        return "Tramvajs"
    elif url.find("autobus") != -1:
        return "Autobuss"
    return "Transports"

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

def updateMap():
    """ In last build uncomment this!!!
    linkList = getLinkList()
    for link in linkList:
        exportStations(link)
    """

    m = folium.Map(location=[55.872, 26.5356], zoom_start=15,zoom_control=False)  # Daugavpils coordinate
    with open('Stations.txt', 'r', encoding='utf-8') as file:
        stations = eval(file.read())
    for sid in stations.keys():
        name = stations[sid]['name']
        cords = stations[sid]['pos']
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
                    <button onmouseup = "openNav('{name}','{sid}')">
                     <img class = "icon"  src = "icons/marker-shadow.png">
                     <img class = "icon" id = '{sid}' src = "icons/marker-icon.png" >
                    </button>
                    """
        tooltip = folium.Tooltip(htmlTooltip)
        icon = folium.DivIcon(htmlIcon)
        marker = folium.Marker(location = cords,
                             tooltip = tooltip,
                             icon = icon
                             ).add_to(m)
    menu = """
    {% macro html(this, kwargs) %}
        <style>
            #sidebar {
                position: fixed;
                z-index: 1000;
                top: 10px;
                left: 10px;
                transition: 0.5s;        
            }
            #transports {     
                width: 260px;
                position: fixed;           
                max-height: 40%;
                overflow: auto;
                background-color: #f8f9fa;
            }
            #stationName{                
                width: 260px;
                padding: 4px 4px 4px 4px;
                text-align: left;
                left: 0px;
                font-size: 18px;
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
            
            .collapsible {
              background-color: #777;
              color: white;
              cursor: pointer;
              padding: 8px;
              width: 100%;
              border: none;
              text-align: left;
              outline: none;
              font-size: 15px;
            }
            .active, .collapsible:hover {
              background-color: #555;
            }
            .column {
              box-sizing: border-box;
              float: left;
              width: 50%;
              padding: 5px;
            }
            
            .content {
              padding: 0 18px;
              max-height: 0;
              overflow: hidden;
              transition: max-height 0.2s ease-out;
              background-color: #f1f1f1;
            }
            .timetable{
                border-collapse: collapse;
                width: 100%;
            }
            .timetable td, .timetable th{
            border: 1px solid #ddd;
            padding: 8px;
            }
            .timetable tr:hover {background-color: #ddd;}
            
            

            
        </style>

        <div id = "sidebar">
                <input type = "text" id = "stationName" name = "stationName">
                <button type = "button" id = "searchButton" onclick = "searchStationByName()"><img id = "searchImg" src = "icons/search.png"></button>
                <div id = "transports">
                </div>
        </div>
        <script>            
             document.addEventListener("DOMContentLoaded", function() {
                new QWebChannel(qt.webChannelTransport, function(channel) {
                    window.station_finder = channel.objects.station_finder;
                });
            });
            
            function searchStationByName(){
            """+f"""      
                var map = window.{m.get_name()};"""+"""
                let name = document.getElementById("stationName").value
                document.getElementById("transports").innerHTML = "";                
                document.getElementById("transports").style.border = "";
                station_finder.findStation(name,
                    function(cordsAndID){
                        let cords = cordsAndID[0]; 
                        if (cords.length == 2){
                            var center = map.getCenter();
                            let xDif = center.lat - cords[0];
                            let yDif = center.lng - cords[1];
                            let distance = Math.sqrt(xDif*xDif+yDif*yDif);                          
                            let zoom;
                            if (map.getZoom() < 17) zoom = 17;
                            else zoom = map.getZoom();    
                            map.setView(cords, zoom);
                            
                        }      
                        const len = document.getElementsByClassName("current").length;
                        for (let i = 0 ;  i < len; i++){               
                            document.getElementsByClassName("current")[0].src = "icons/marker-icon.png";                    
                            document.getElementsByClassName("current")[0].classList.remove("current");        
                        }
                               
                        if (cordsAndID[1].length >= 1){
                            for(let i = 0 ; i < cordsAndID[1].length ; i++){
                            if (!document.getElementById(cordsAndID[1][i]).classList.contains("current")){
                                document.getElementById(cordsAndID[1][i]).classList.add("current");  
                                document.getElementById(cordsAndID[1][i]).src = "icons/current-marker-icon.png";
                            }
                            }
                        }                        
                    }
                ); 
            }
            function searchStationByID(ID){
            """+f"""      
                var map = window.{m.get_name()};"""+"""
                station_finder.findStation(ID,
                    function(cords){     
                        if (cords.length == 2){
                            var center = map.getCenter();
                            let xDif = center.lat - cords[0];
                            let yDif = center.lng - cords[1];
                            let distance = Math.sqrt(xDif*xDif+yDif*yDif);
                            if (distance>0.012 || map.getZoom() < 16){                            
                                let zoom;
                                if (map.getZoom() < 16) zoom = 16;
                                else zoom = map.getZoom();    
                                map.setView(cords, zoom);
                            }   
                            const len = document.getElementsByClassName("current").length;
                            for (let i = 0 ;  i < len; i++){
                                document.getElementsByClassName("current")[0].src = "icons/marker-icon.png";                    
                                document.getElementsByClassName("current")[0].classList.remove("current");
                            }                            
                            if (!document.getElementById(ID).classList.contains("current")){                           
                                document.getElementById(ID).classList.add("current");  
                                document.getElementById(ID).src = "icons/current-marker-icon.png";
                            }
                        }
                    }
                ); 
            }
            function searchTransport(ID){
                station_finder.findTransport(ID,
                    function(transport){
                        document.getElementById("transports").style.border = "2px solid #ddd";
                        document.getElementById("transports").innerHTML = "";
                        for(let i = 0; i < transport.length; i++){
                            html = `<button class="collapsible">${transport[i][0]}</button>
                            <div class="content">
                                `;   
                                                          
                                for(let d = 0; d<transport[i][1].length;d++){
                                
                                    html+='<div class="column"><table class="timetable">';
                                    if(d==0){
                                    html += "<tr><th>Darba dienas</th><tr>";
                                    }
                                    else{
                                    html += "<tr><th>Brīvdienas</th><tr>";
                                    }
                                    
                                    for(let t = 0; t<transport[i][1][d].length; t++){
                                        html+=`
                                            <tr>
                                                <td>${transport[i][1][d][t]}</td>
                                            </tr>`;
                                    }
                                    html+="</table></div>";
                                }                            
                            html+="</div>";
                            document.getElementById("transports").innerHTML +=html ;
                        }
                        var coll = document.getElementsByClassName("collapsible");
                        var i;
                        
                        for (i = 0; i < coll.length; i++) {
                          coll[i].addEventListener("click", function() {
                            this.classList.toggle("active");
                            var content = this.nextElementSibling;
                            if (content.style.maxHeight){
                              content.style.maxHeight = null;
                            } else {
                              content.style.maxHeight = content.scrollHeight + "px";
                            } 
                          });
                        }
                    }
                );
                
            }
            function openNav(name, ID) {
                while(name.includes("*") == true){
                    name = name.replace("*","\\\"");          
                }
                searchTransport(ID);
                document.getElementById("stationName").value=name;  
                searchStationByID(ID);
                
                
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
    m=updateMap()
    m.save('nyc_map.html')