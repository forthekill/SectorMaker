<span class="s1">**SectorMaker Installation - Mac OSX
(10.x)**</span><span class="s2">  
</span>Original version by Micki Kaufman (micki001@concentric.net)

Note: there is a Ubuntu version available by Chris Moynihan (forthekill
at gmail.com, forthekill.com)

**I. Installation**

**STEP ONE - Install Perl**<span class="s2">  
</span><span class="s3">Install Perl 5.</span>

sudo apt-get install perl

<span class="s4">**STEP TWO - Install PDFTK
1.44**</span><span class="s2">  
</span>Install the Mac version of PDFTK, used for splitting, joining,
compressing and overlaying PDF pages.

http://www.pdflabs.com/docs/install-pdftk/

<span class="s4">**STEP THREE - Install
FONT-TTF**</span><span class="s2">  
</span>Install PDF-API2, a Perl resource for handling PDFs and fonts.

perl -MCPAN -e 'install Font::TTF'<span class="Apple-converted-space">
</span>

<span class="s4">**STEP FOUR - Install
PDF-API2**</span><span class="s2">  
</span>Install PDF-API2, a Perl resource for handling PDFs and fonts.

perl -MCPAN -e 'install PDF::API2'<span class="Apple-converted-space">
</span>

<span class="s4">**STEP FIVE - Create The Output and Temp
Folders**</span><span class="s2">  
</span>Create folders for the script to use, one for the final output
and one for temporary files.

sudo mkdir /sectors

sudo mkdir /sectors/autogen

sudo chmod 777 /sectors/autogen

<span class="s4">**STEP SIX - Download and Unzip the SectorMaker
Archive**</span><span class="s2">  
</span>Unzip the SectorMaker files from the archive. This will create a
folder called SectorMakerScripts in that location.

unzip SectorMakerScripts.zip

cd SectorMakerScripts

**STEP SEVEN - Copy all files into the CGI Executables
Folder**<span class="s2">  
</span><span class="s3">Copy them to the apache directory.</span>

sudo cp \* /Library/WebServer/CGI-Executables

<span class="s4">**STEP EIGHT - Copy Custom
Corefonts**</span><span class="s2">  
</span>Install the custom CoreFont fonts.

cd install/pdf-api2

sudo cp universbold.pm univers.pm optima.pm
/opt/local/lib/perl5/site_perl/5.12.3/PDF/API2/Resource/Font/CoreFont/

sudo cp CoreFont.pm
/opt/local/lib/perl5/site_perl/5.12.3/PDF/API2/Resource/Font/

**STEP NINE - Modify CoreFont.pm**<span class="s2">  
</span>Add the following line to line 224 of CoreFont.pm
(/opt/local/lib/perl5/site_perl/5.12.3/PDF/API2/Resource/Font/CoreFont.pm)

univers universbold

**STEP TEN - Install the New Fonts**<span class="s5">**  
**</span>Install the required TrueType fonts (a few styles of Univers
and Optima) into the fonts folder.

sudo cp Univers\* Optima\* /Library/Fonts/

<span class="s4">**STEP ELEVEN - Copy the Custom
Binaries**</span><span class="s2">  
</span>Install the custom SW4 Traveller binaries into your computer's
<span class="s6">/usr/local/bin/</span> folder.

cd ./install/bin

sudo cp full-upp mapsub3 subsec2 gensec3 /usr/local/bin/

<span class="s4">**STEP TWELVE - Set the Script
Permissions**</span><span class="s2">  
</span>Move to the <span class="s6">cgi-bin</span> directory and set the
script permissions properly.

cd /Library/WebServer/CGI-Executables

sudo chmod ugo+x SectorMaker.cgi SectorMaker.sh BatchSectorMaker.sh

**STEP THIRTEEN - Copy the Enscript Config Files**<span class="s2">  
</span><span class="s3">Copy the custom enscript files.</span>

cd install/enscript

sudo cp enscript.cfg /usr/share/enscript/

sudo cp traveller\*.hdr /usr/share/enscript/

**II. Using the Scripts**

<span class="s4">**Using the Scripts Via Command
Line**</span><span class="s2">  
</span><span class="s3">To use the script from the command line,
navigate to the
</span>/Library/WebServer/CGI-Executables<span class="s3"> folder and
use the following syntax:</span><span class="s2">  
</span>./SectorMaker.sh {sectorname} {density} {tech} {desc} {{secfile}}
{{regen}}<span class="s7">  
</span><span class="s2">  
</span><span class="s3">To use the batch sector maker, navigate to
the</span> /var/www/cgi-bin<span class="s3"> folder and use the
following syntax:</span><span class="s2">  
</span>./BatchSectorMaker.sh {number of sectors} {tech} {desc}

<span class="s4">**Using the Scripts Via Web
Browser**</span><span class="s2">  
</span><span class="s3">To use the script from a web browser, use the
syntax for either of the two following URLs:</span><span class="s2">  
  
</span>http://\[servername\]/cgi-bin/SectorMaker.cgi/*sectorName*.pdf?{sectorname}+{density}+{tech}+{desc}+{{secfile}}+{{regen}}<span class="s7">  
</span>http://\[servername\]/cgi-bin/SectorMaker.cgi?{sectorname}+{density}+{tech}+{desc}+{{secfile}}+{{regen}}<span class="s2">  
  
</span><span class="s3">The first URL will return a file called
</span>*sectorName*.pdf<span class="s3"> to the
browser.</span><span class="s2">  
</span><span class="s3">The second URL will return a file called
</span>SectorMaker.cgi<span class="s3"> to the browser, which is
actually a PDF.</span>

<span class="s4">**Parameters**</span><span class="s2">  
</span>{sectorname}<span class="s2">  
</span><span class="s3">What you would like the name of the sector to
be.</span><span class="s2">  
  
</span>{density\|zero,rift,sparse,scattered,dense, or
Xx}<span class="s2">  
</span><span class="s3">Determines the stellar density of the sector
(avg. of worlds per subsector)</span><span class="s2">  
</span>zero = 0% (No random worlds will be generated. A
*sectorName*\_names.txt file in /sectors/autogen must be present, which
will be used for the world names and locations)<span class="s7">  
</span>rift = 4% (~1-10)<span class="s7">  
</span>sparse = 16% (~5-20)<span class="s7">  
</span>scattered = 33% (~19-35)<span class="s7">  
</span>dense = 66% (~40-62)<span class="s7">  
</span>Xx = Xx% (Specify a number, from 0 to 100)<span class="s2">  
  
</span>{tech\|backwater,frontier,mature,cluster}<span class="s2">  
</span><span class="s3">The general technology level of the sector, how
well travelled it is</span><span class="s2">  
  
</span>{desc\|1,2,3}<span class="s2">  
</span><span class="s3">Level of description for generated
worlds</span><span class="s2">  
</span>1 = UPP and Animal<span class="s7">  
</span>2 = UPP only<span class="s7">  
</span>3 = None<span class="s2">  
  
</span>{secfile\|*sectorName*.sec}<span class="s2">  
</span><span class="s3">Pre-existing sector file name. Used if an
existing set of files is available in
</span>/sectors/autogen<span class="s3">
</span>(*sectorName*.sec<span class="s3">,
</span>*sectorName*\_route.txt<span class="s3">,
</span>*sectorName*\_alliances.txt<span class="s3">)</span><span class="s2">  
</span><span class="s3">Using this parameter renders the density and
tech parameters irrelevant, although with the command line you need to
put something for those as placeholders.</span><span class="s2">  
  
</span>{regen\|1,2,3}<span class="s7">  
</span><span class="s3">Pre-existing regeneration options. Used only if
a </span>secfile<span class="s3"> is
specified.</span><span class="s2">  
</span>1 = Use pre-existing routes and borders (May generate additional
routes and borders)<span class="s7">  
</span>2 = Use pre-existing routes only (Will not generate additional
routes, but it will generate new borders)<span class="s7">  
</span>3 = Use pre-existing routes and borders only (Will not generate
any new routes or borders)

**Examples**

<span class="s6">./SectorMaker.sh Orion sparse mature
1</span><span class="s2">  
</span>This will create Orion.pdf with 16% world density in the sector,
at a mature tech level, and include UPP and Animal descriptions for each
world.

<span class="s6">./SectorMaker.sh Orion 20 mature
2</span><span class="s2">  
</span>This will create Orion.pdf with 20% world density in the sector,
at a mature tech level, and include UPP descriptions for each world.

<span class="s6">./SectorMaker.sh Orion dense mature 3 Orion.sec
3</span><span class="s2">  
</span>This will create Orion.pdf, ignoring the world density and tech
level, and use the existing <span class="s6">Orion.sec</span>,
<span class="s6">Orion_route.txt</span>, and
<span class="s6">Orion_alliances.txt</span> files instead. The borders
and routes will be used, and new ones may be added. The worlds will have
no descriptions.

<span class="s6">./SectorMaker.sh Orion zero mature
2</span><span class="s2">  
</span>This will create Orion.pdf, but no randomly generated worlds will
be created. If <span class="s6">Orion_names.txt</span> is present in
<span class="s6">/sectors/autogen</span> it will use those worlds, and
randomly generate routes borders and world descriptions. If it is not
present, you will get an empty sector.
