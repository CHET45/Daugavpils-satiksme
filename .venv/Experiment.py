from PyQtApp import StationFinder
station_finder = StationFinder()
coords=station_finder.findStation('Butļerova iela')
print(str(coords))