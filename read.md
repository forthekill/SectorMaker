  SectorMaker Installation - Ubuntu   p.p1 {margin: 0.0px 0.0px 12.0px 0.0px; font: 12.0px Verdana} p.p2 {margin: 0.0px 0.0px 16.0px 0.0px; font: 16.0px Verdana} p.p3 {margin: 0.0px 0.0px 12.0px 0.0px; font: 14.0px Verdana} p.p4 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px 'Courier New'; background-color: #84bdce} p.p5 {margin: 0.0px 0.0px 12.0px 0.0px; font: 12.0px 'Courier New'; background-color: #84bdce} p.p6 {margin: 0.0px 0.0px 12.0px 0.0px; font: 12.0px 'Courier New'} span.s1 {font: 24.0px Arial} span.s2 {font: 12.0px 'Lucida Grande'} span.s3 {font: 12.0px Verdana} span.s4 {font: 14.0px Verdana} span.s5 {font: 14.0px 'Lucida Grande'} span.s6 {font: 12.0px 'Courier New'} span.s7 {font: 12.0px Monaco}

**SectorMaker Installation - Mac OSX (10.x)**  
Original version by Micki Kaufman (micki001@concentric.net)

Note: there is a Ubuntu version available by Chris Moynihan (forthekill at gmail.com, forthekill.com)

**I. Installation**

**STEP ONE - Install Perl**  
Install Perl 5.

sudo apt-get install perl

**STEP TWO - Install PDFTK 1.44**  
Install the Mac version of PDFTK, used for splitting, joining, compressing and overlaying PDF pages.

http://www.pdflabs.com/docs/install-pdftk/

**STEP THREE - Install FONT-TTF**  
Install PDF-API2, a Perl resource for handling PDFs and fonts.

perl -MCPAN -e 'install Font::TTF'

**STEP FOUR - Install PDF-API2**  
Install PDF-API2, a Perl resource for handling PDFs and fonts.

perl -MCPAN -e 'install PDF::API2'

**STEP FIVE - Create The Output and Temp Folders**  
Create folders for the script to use, one for the final output and one for temporary files.

sudo mkdir /sectors

sudo mkdir /sectors/autogen

sudo chmod 777 /sectors/autogen

**STEP SIX - Download and Unzip the SectorMaker Archive**  
Unzip the SectorMaker files from the archive. This will create a folder called SectorMakerScripts in that location.

unzip SectorMakerScripts.zip

cd SectorMakerScripts

**STEP SEVEN - Copy all files into the CGI Executables Folder**  
Copy them to the apache directory.

sudo cp \* /Library/WebServer/CGI-Executables

**STEP EIGHT - Copy Custom Corefonts**  
Install the custom CoreFont fonts.

cd install/pdf-api2

sudo cp universbold.pm univers.pm optima.pm /opt/local/lib/perl5/site\_perl/5.12.3/PDF/API2/Resource/Font/CoreFont/

sudo cp CoreFont.pm /opt/local/lib/perl5/site\_perl/5.12.3/PDF/API2/Resource/Font/

**STEP NINE - Modify CoreFont.pm**  
Add the following line to line 224 of CoreFont.pm (/opt/local/lib/perl5/site\_perl/5.12.3/PDF/API2/Resource/Font/CoreFont.pm)

univers universbold

**STEP TEN - Install the New Fonts**Install the required TrueType fonts (a few styles of Univers and Optima) into the fonts folder.

sudo cp Univers\* Optima\* /Library/Fonts/

**STEP ELEVEN - Copy the Custom Binaries**  
Install the custom SW4 Traveller binaries into your computer's /usr/local/bin/ folder.

cd ./install/bin

sudo cp full-upp mapsub3 subsec2 gensec3 /usr/local/bin/

**STEP TWELVE - Set the Script Permissions**  
Move to the cgi-bin directory and set the script permissions properly.

cd /Library/WebServer/CGI-Executables

sudo chmod ugo+x SectorMaker.cgi SectorMaker.sh BatchSectorMaker.sh

**STEP THIRTEEN - Copy the Enscript Config Files**  
Copy the custom enscript files.

cd install/enscript

sudo cp enscript.cfg /usr/share/enscript/

sudo cp traveller\*.hdr /usr/share/enscript/

**II. Using the Scripts**

**Using the Scripts Via Command Line**  
To use the script from the command line, navigate to the /Library/WebServer/CGI-Executables folder and use the following syntax:  
./SectorMaker.sh {sectorname} {density} {tech} {desc} {{secfile}} {{regen}}  
  
To use the batch sector maker, navigate to the /var/www/cgi-bin folder and use the following syntax:  
./BatchSectorMaker.sh {number of sectors} {tech} {desc}

**Using the Scripts Via Web Browser**  
To use the script from a web browser, use the syntax for either of the two following URLs:  
  
http://\[servername\]/cgi-bin/SectorMaker.cgi/_sectorName_.pdf?{sectorname}+{density}+{tech}+{desc}+{{secfile}}+{{regen}}  
http://\[servername\]/cgi-bin/SectorMaker.cgi?{sectorname}+{density}+{tech}+{desc}+{{secfile}}+{{regen}}  
  
The first URL will return a file called _sectorName_.pdf to the browser.  
The second URL will return a file called SectorMaker.cgi to the browser, which is actually a PDF.

**Parameters**  
{sectorname}  
What you would like the name of the sector to be.  
  
{density|zero,rift,sparse,scattered,dense, or Xx}  
Determines the stellar density of the sector (avg. of worlds per subsector)  
zero = 0% (No random worlds will be generated. A _sectorName_\_names.txt file in /sectors/autogen must be present, which will be used for the world names and locations)  
rift = 4% (~1-10)  
sparse = 16% (~5-20)  
scattered = 33% (~19-35)  
dense = 66% (~40-62)  
Xx = Xx% (Specify a number, from 0 to 100)  
  
{tech|backwater,frontier,mature,cluster}  
The general technology level of the sector, how well travelled it is  
  
{desc|1,2,3}  
Level of description for generated worlds  
1 = UPP and Animal  
2 = UPP only  
3 = None  
  
{secfile|_sectorName_.sec}  
Pre-existing sector file name. Used if an existing set of files is available in /sectors/autogen (_sectorName_.sec, _sectorName_\_route.txt, _sectorName_\_alliances.txt)  
Using this parameter renders the density and tech parameters irrelevant, although with the command line you need to put something for those as placeholders.  
  
{regen|1,2,3}  
Pre-existing regeneration options. Used only if a secfile is specified.  
1 = Use pre-existing routes and borders (May generate additional routes and borders)  
2 = Use pre-existing routes only (Will not generate additional routes, but it will generate new borders)  
3 = Use pre-existing routes and borders only (Will not generate any new routes or borders)

**Examples**

./SectorMaker.sh Orion sparse mature 1  
This will create Orion.pdf with 16% world density in the sector, at a mature tech level, and include UPP and Animal descriptions for each world.

./SectorMaker.sh Orion 20 mature 2  
This will create Orion.pdf with 20% world density in the sector, at a mature tech level, and include UPP descriptions for each world.

./SectorMaker.sh Orion dense mature 3 Orion.sec 3  
This will create Orion.pdf, ignoring the world density and tech level, and use the existing Orion.sec, Orion\_route.txt, and Orion\_alliances.txt files instead. The borders and routes will be used, and new ones may be added. The worlds will have no descriptions.

./SectorMaker.sh Orion zero mature 2  
This will create Orion.pdf, but no randomly generated worlds will be created. If Orion\_names.txt is present in /sectors/autogen it will use those worlds, and randomly generate routes borders and world descriptions. If it is not present, you will get an empty sector.
