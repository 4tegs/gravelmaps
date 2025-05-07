# gravelmaps.de
Documentation of the Garmin Maps for Offroad Adventures published on https://gravelmaps.de . <br/>
The maps have a focus for motorcycle / enduro / off-road purpose.<br/>
<p>This maps have developed over several years, based on my personal experience in offroad riding. The maps have been downloaded many thousands of times. They are obviously well used by the off-road community.</p>


## Prerequisites

Before you start, you should be aware of some prerequistes. So what do YOU need to know?
* You must understand Openstreetmap and its tagging features as this îs your the main knowledge when defining the style.
* Its a good idea to have some basic programming skills in Python.

## Overview

The diagram shows how the maps are created. The following sections will tell you what tools are used and what supporting files are needed to create the map. Some files you will need to download, others you will need to create yourself.

![Workflow in creating  Garmin map. <br/>Find the original yEd Graph file in ./images/](./images/workflow.jpg)

### Tools
The numbers relate to the numbers in the diagram. All links refer to windows programs.

| Number | Tool | Link to origin |
| --- | --- | --- |
| 1 | wget | https://sourceforge.net/projects/gnuwin32/files/wget/ |
| 2 | OSMconvert | https://wiki.openstreetmap.org/wiki/Osmconvert |
| 3 | OSMconvert | see 2  |
| 4 | Splitter | https://www.mkgmap.org.uk/download/splitter.html |
| 5 | MkGMAP | https://www.mkgmap.org.uk/download/mkgmap.html |
| 6 | gmt.exe | https://www.gmaptool.eu/ |
| 7 | NSISbi (must be 64bit Version due to the size of the output files) | https://sourceforge.net/projects/nsisbi/ |
| 8 | 7Z | https://www.7-zip.org/ |
| 9 | gmt.exe | see 6  |
|  |  |  |


Additional Tools for preparation before you start compiling:

| What for? | Tool | Link to origin |
| --- | --- | --- |
| In case you want to make contour lines | hgt2osm | hgt2osm (https://github.com/FSofTlpz/Hgt2Osm2) |
|  | srtm2osm | https://wiki.openstreetmap.org/wiki/Srtm2Osm |
|  | phyghtmap | http://katze.tfiu.de/projects/phyghtmap/ |
| To prepare your TYP files | TYPWiz | https://www.pinns.co.uk |
| In order to run the compilation in an automated way, use  |  00_Make_Maps.py<br/>00_Make_Maps.json<br/>00_Make_Maps.cmd | this github repository | 


### Supporting files needed 
The numbers relate to the numbers in the diagram.

| Number  | what's done | Supporting file | where to get |
| ---  | --- | --- | --- |
| In advance of compile | Prepare DEM data | My favourite and best available free elevation data for Europe: Sonny' LiDAR Digital terrain models of Europe<br/>(Digital Terrain Model DTM based on precise LiDAR height sources) |  https://sonny.4lima.de/ |
|  |  |30-Meter SRTM Tile Downloader (Nasa Earth Data)  |  https://dwtkns.com/srtm30m/ |
|  |  | If you search for areas not handled by the two sites above | https://viewfinderpanoramas.org/dem3.html |
|  |  | A resource to find other resources | https://www.imagico.de/map/demsearch.php |
| 1 | Download Geodata.<br/> Has pbf format.  |  | https://download.geofabrik.de/ |
| 2 | Convert every "country.pbf" to "country.o5m" for use in next step. |  |  |
| 3 | Merge all country.o5m into a geo.o5m |  |  |
| 4 | Split the "geo.o5m" to be used for compile. | CITIES  | https://download.geonames.org/export/dump/  |
|  |  | sea-latest  | https://www.thkukuk.de/osm/data/sea-latest.zip |
| 5 | Compile the map | sea-latest | see above |
|  |  | bounds-latest | https://www.thkukuk.de/osm/data/bounds-latest.zip |
|  |  | The style. The master logic of **what** the map will display and **when**. | this github repository | 
|  |  | Your Copyright definition text file | this github repository |
|  |  | Your Licence file | this github repository |
|  |  | Your Options File.<br/>Tells the MKGMap compiler what to do. | You prepare.<br/>or<br/>00_Make_Maps.py will create one for you. |
|  |  | roadNameConfig.txt<br/>Tells MKGMap how to handle roadnames. | An example is provided with the MKGMap compiler. |
| 6 | replace TYP files to match map Family number.<br/>(Needed as well in 7,8,9) | The Typ files describe **how the map looks like**. | this github repository |
| 7  | Pack the former compiled data to a windows installer   | no special files |  |
| 8 | Pack the former compiled data to a GMAPI (New Garmin Map format) | no special files |  |
| 9 | Rework the gmapsupp.img and inject the right "Garmin map name" and "Family number". | no special files |  |
|  |  |  |  |

## STYLE and TYP
So while the STYLE describes what is displayed (roads, points, polygons) and when (depending on the zoom level), the TYP file decides how it looks. 
Whatever you choose to display via STYLE must have an equivalent in the TYP file.

### TYP Files

You find 5 different TYP files in the following design:
| TYP file | description |
| --- | --- |
| grvl_p.typ | This is the standard Garmin image to be used with your Garmin device = gmapsupp.img<br/> This version uses wider roads so that they can be seen more quickly on the Garmin display. |
| grvl_pB.typ | Same layout as grvl_p.typ, but with borders highlighted. A spin-off from Covid times. Sometimes helpful. |
| grvl_pn.typ | Same layout as grvl_p.typ, but uses smaller lines for roads. This is the default for the installer to use with Basecamp. This layout gives good visibility on your screen. |
| grvl_pnb.typ | Narrow lines for computer display with highlighted borders. |
| orux.typ | Special map layout for use with Android devices running OruxMaps. |
|  |  |

### STYLE

Each style is made of a variety definition files that describe what is displayed (roads, points, polygons) and when (depending on the zoom level). You can learn how the definition is done by using the mkgmap style manual: https://www.mkgmap.org.uk/doc/pdf/style-manual.pdf

These styles are available:

| Style | description |
| --- | --- |
| offroad | This is the standard style for the gravelmaps.de |
| orux | This style is a child from the standard offroad style, made for use with Android devices running Oruxmaps. <br/> The layout has been changed significantly: The way of how areas appear / disappear, small tracks like single trails are missing.  |
| street | Based on the standard style, all offroad tracks have been discarded. Due to a lack of interest I removed them from the website 01.2022 |
| rad | This is my personal adaption of the standard style for use with my road-bicycle. It has a reduced layout, missing "not so good" tracks. |

## Special

ReplaceTyp.cmd is made for changing the layout of gravelmaps images. To run it, you need
<ol> 
<li>the TYP Files </li>
<li>gmt.exe </li>
<li>be_invisible.cmd </li>
<li>be_visible.cmd </li>
</ol>
Simply drag & drop the img file onto replace_typ.cmd.

## Licence
© Gravelmaps cartography is licensed under CC-BY-NC-SA,   
https://creativecommons.org/licenses/by-nc-sa/4.0/  

Website: https://gravelmaps.de or https://motorradtouren.de<br/>
E-mail: info@motorradtouren.de<br/>
Owner: Hans Straßgütl 

Disclaimer:  
This gravelmaps code can be used freely for any personal use.  
Further distribution or commercial use is not allowed without attribution and permission from Hans Straßgütl.  
Please note that the software is experimental and provided "as is" and you use the software at your own risk.

..........................................................................  
For all other software used, please refer to the relevant licence descriptions.