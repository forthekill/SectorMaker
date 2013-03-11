#!/bin/sh

# SectorMaker.cgi
# by Micki Kaufman micki001@concentric.net
# 
#   I was looking at my LBB collection, and got an idea, so voila!
# Presenting the Traveller Sector Guidebook .cgi script. Creates and returns 
# a high-resolution (vector-art) pdf containing the sector data and hexmaps, 
# listed subsector by subsector.
#

# BASIC INSTRUCTIONS

# INSTALLATION
# 
# # STEP ONE
# ## install Apple's "Xcode Tools" from http://developer.apple.com/macosx/
# 
# # STEP TWO
# ## install the Mac OSX version of /usr/local/bin/pdftk (used for splitting, joining, compressing and overlaying 
# ## pdf pages) from http://www.pdfhacks.com//usr/local/bin/pdftk/
# 
# # STEP THREE
# ## install pdf-API2 (a perl resource for handling pdfs and fonts) 
# ## from http://search.cpan.org/~areibens/PDF-API2-0.55/lib/PDF/API2.pm
# 
# # STEP FOUR
# ## unzip the SectorMaker archive from http://micki001.cnc.net/trav/SectorMakerScripts.zip 
# ## and place all the files in the computer's cgi folder. Also, create the output folder.
# mkdir /sectors/autogen
# unzip SectorMakerScripts.zip -d /Library/WebServer/CGI-Executables/
# 
# # STEP FIVE
# ## move to the install directory and set the script permissions properly.
# cd /Library/WebServer/CGI-Executables/install
# chmod ugo+x SectorMaker.cgi SectorMaker.sh BatchSectorMaker.sh
# 
# # STEP SIX
# ## move the custom CoreFont main file into the newly-installed pdf-api2 CoreFont folder.
# cp pdf-api2/corefont.pm /Library/Perl/5.8.6/PDF/API2/Resource/Font/
# 
# # STEP SEVEN
# ## install the custom CoreFont fonts into the newly-installed pdf-api2 CoreFont folder.
# cp pdf-api2/universbold.pm pdf-api2/univers.pm pdf-api2/optima.pm /Library/Perl/5.8.6/PDF/API2/Resource/Font/CoreFont/
# 
# # STEP EIGHT
# ## install the required TrueType fonts (a few styles of Univers and Optima) into your computer's '/Library/Fonts/' folder.
# cp ttf/Univers_Bold_Italic.ttf ttf/Univers.ttf ttf/Univers_Bold.ttf ttf/Optima.ttf ttf/Univers_Italic.ttf /Library/Fonts/
# 
# # STEP NINE
# ## install the custom SW4 Traveller binaries into your computer's '/usr/bin/' folder.
# cp bin//usr/local/bin/full-upp bin//usr/local/bin/mapsub3 bin//usr/local/bin/subsec2 bin//usr/local/bin/gensec3 /usr/bin/
# 
# # STEP TEN
# ## install enscript files
# cp enscript/enscript.cfg enscript/travellerpagenums.hdr enscript/travellerpagenums2.hdr /usr/share/enscript/
#  
# 
# # USING THE SCRIPTS
# 
# ## To use the script from the command line, navigate to the /Library/WebServer/CGI-Executables folder and use the following syntax:
# ./SectorMaker.sh {sectorname} {density} {tech} {desc} {{secfile}} {{regen}}
# 
# ## To use the script from a web browser, use the following URL syntax (you must already have 
# ## turned on 'Web Sharing', using the 'Sharing' Preference Pane of 'System Preferences'):
# http://[servername]/cgi-bin/SectorMaker.cgi?{sectorname}+{density}+{tech}+{desc}+{{secfile}}+{{regen}}
# 
# ## To use the batch sector maker, navigate to the /Library/WebServer/CGI-Executables folder and use the following syntax:
# ./BatchSectorMaker.sh {number of sectors} {tech} {desc}
#
# ./SectorMaker.cgi parameters:
# 
#  {sectorname} 
# 
#  {density|rift/sparse/scattered/dense or Xx} 
# 
#  {tech|backwater,frontier,mature,cluster} 
# 
#  {desc: Description|1=UPP and Animal,2=just UPP,3=none} 
# 
#  {secfile: Pre-existing sector file name (used if an existing set of .sec, route and alliance 
#     files is available in trav/sectorfiles)}
# 
#  {regen: Pre-existing regeneration options|1=use existing file's pre-existing borders and routes,
#     2=only use pre-existing routes,3=only use pre-existing borders and routes}
# 
# REQUIRES:
#   - Apple's XCode Tools
#       http://developer.apple.com/macosx/
#   - /usr/bin/pstopdf 
#       (built in on Mac OSX)
#   - enscript 
#       (built in on Mac OSX)
#   - /usr/local/bin/pdftk
#       http://www.pdfhacks.com//usr/local/bin/pdftk/   
# 
#   Using sector tools, the sector data and individual subsector data is 
# created, and the PostScript hexmap is generated. Using /usr/bin/pstopdf, the PostScript 
# hexmap is converted to a pdf. Using enscript, the text sector data is 
# converted to a  PostScript file. Still working on page size. using /usr/local/bin/pdftk, the 
# pdf's are overlaid and concatenated together. And then we serve it up!
#
# Far Future Enterprises Fair Use Notice:
# The Traveller game in all forms is owned by Far Future Enterprises. Copyright 
# 1977 - 1998 Far Future Enterprises. Traveller is a registered trademark of Far 
# Future Enterprises.  Far Future permits web sites and fanzines for this game, 
# provided it contains this notice, that Far Future is notified, and subject to 
# a withdrawal of permission on 90 days notice.  The contents of this site are 
# for personal, non-commercial use only. Any use of Far Future  EnterprisesÕs 
# copyrighted material or trademarks anywhere on this web site and its files  
# should not be viewed as a challenge to those copyrights or trademarks. In 
# addition, any  program/articles/file on this site cannot be republished or 
# distributed without the consent  of the author who contributed it. 
#  


#### First, here are the get_UPP, ?(random_Quote)? and parse_SectorDescription functions.

SCORING=1



### get_UPP (requires '/usr/local/bin/full-upp', installed in bin folder)

function get_UPP() 
{
/usr/local/bin/full-upp $2 > /tmp/$1uppo.txt
cat /tmp/$1uppo.txt /Library/WebServer/CGI-Executables/trav/ret.txt > /tmp/$1upp.txt
chmod ugo+w /tmp/$1upp.txt /tmp/$1uppo.txt
#echo "Content-Type: application/text" 
#echo " Filename: "$1upp.txt
echo ""
echo $1
echo "Name: "$4 > /tmp/$1name1.txt
sed '/_/ s/_/ /g' /tmp/$1name1.txt > /tmp/$1name.txt
cat < /tmp/$1name.txt
sed -n '/ '$3' /p' /tmp/*_polities.txt > /tmp/$1polityinter.txt
cat /Library/WebServer/CGI-Executables/trav/Affiliation.txt /tmp/$1polityinter.txt > /tmp/$1polity.txt
cat < /tmp/$1polity.txt
#echo ""
echo "UPP: "$2
echo ""
cat < /tmp/$1upp.txt
rm -rf /tmp/$1upp.txt
rm -rf /tmp/$1polityinter.txt
rm -rf /tmp/$1polity.txt
rm -rf /tmp/*uppo.txt
rm -rf /tmp/$1name1.txt
rm -rf /tmp/$1name.txt
     return
     }




### get_More (grabs cargo and animal encounters)

function get_More() 
{
cd /Library/WebServer/CGI-Executables/trav
perl shell.pl --tool=animal --extended --profile=$2 > /tmp/$1animo.txt
perl shell.pl --tool=bk7.trade.cargo --profile=$2 > /tmp/$1cargo.txt
cat /tmp/$1animo.txt /Library/WebServer/CGI-Executables/trav/ret.txt > /tmp/$1anim.txt
chmod ugo+w /tmp/$1anim.txt /tmp/$1animo.txt
#echo "Content-Type: application/text" 
#echo " Filename: "$1anim.txt
#echo ""
echo "Generic Cargo:"
#echo ""
cat < /tmp/$1cargo.txt
#echo $1
echo ""
echo "Animal Encounters:"
#echo ""
cat < /tmp/$1anim.txt
rm -rf /tmp/$1anim.txt
rm -rf /tmp/$1animo.txt
cd /Library/WebServer/CGI-Executables/
     return
     }





### get_SectorDescriptions grabs each of the planet's descriptions (using the get_UPP function on each) and then serves the whole thing up as a text file and pdf.

function get_SectorDescriptions()
{
needforanim=2


## Main Loop
if [ "$needforanim" -lt "$desc" ]; then 	# -n tests to see if the argument is non empty
     while read LINE
    do
          get_UPP $LINE $2 > /tmp/$1det$LINE-a.txt 
#               echo "  .  $1 World debug - UPP description render complete @" $SECONDS "seconds.   "
               done < /tmp/$1
else
     while read LINE
    do
          get_UPP $LINE $2 > /tmp/$1det$LINE-a.txt 
#               echo "  .  $1 World debug - UPP description render complete @" $SECONDS "seconds.   "
          get_More $LINE > /tmp/$1det$LINE-banim.txt
#                echo "  .  $1 World debug - cargo and animal encounters description render complete @" $SECONDS "seconds.   "
              done < /tmp/$1
          fi


# Combine all the descriptions into one text file.
cat /Library/WebServer/CGI-Executables/trav/pageblanker.txt /tmp/$2title.txt /Library/WebServer/CGI-Executables/trav/descinfo.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1det*.txt > /tmp/$1finaldet.txt
wait

## Assemble the pages into a description section pdf

# Create .ps files from each datafile
enscript --word-wrap --margins=35:35:0:40 --fancy-header='travellerpagenums2' --header='|- $% -|' --header-font=Univers9 /tmp/$1finaldet.txt -f Courier6.5 --media=Traveller -q -p /tmp/$1out.ps
wait

# Create .pdf files from each datafile .ps
/usr/bin/pstopdf /tmp/$1out.ps -o /tmp/$1piecetemp.pdf
wait

# Grab the pages, starting #36 (the prior 35 are blank to set up the numbering, since the /usr/local/bin/pdftk program can't start the numbering at 36.
/usr/local/bin/pdftk /tmp/$1piecetemp.pdf cat 38-end output /tmp/$1piecetempText.pdf
wait

# Grab the first page of the descriptions
/usr/local/bin/pdftk /tmp/$1piecetempText.pdf cat 1-1 output /tmp/$1piecetempIntro.pdf
wait

# Place the 'World Descriptions' header on the first page, in keeping with the document's section headings.
/usr/local/bin/pdftk /tmp/$1piecetempIntro.pdf background /Library/WebServer/CGI-Executables/trav/Desc_Background.pdf output /tmp/$1pieceDescIntroWithBack.pdf
wait

# Grab the rest of the descriptions
/usr/local/bin/pdftk /tmp/$1piecetempText.pdf cat 2-end output /tmp/$1pieceEnd.pdf
wait

# Join the first page of descriptions (now with header) and the rest of the descriptions
/usr/local/bin/pdftk /tmp/$1pieceDescIntroWithBack.pdf /tmp/$1pieceEnd.pdf cat output /tmp/$1piece.pdf
wait

return
}




### get_Sectormap makes a one-page sector map, including borders.

function get_Sectormap()
{

# Wipe pesky underscores
sed '/_/ s/_/ /g' /tmp/$1secdata > /tmp/$1secdataZ
ditto /tmp/$1secdataZ /tmp/$1_secdatapre

# Remove the first line so it doesn't get chunked
sed '1d' /tmp/$1_secdatapre > /tmp/$1_secdata

# Cut new chunks for sec2pdf-friendly format
cut -b20-23 /tmp/$1_secdata > /tmp/$1_secdataID
cut -b19-19 /tmp/$1_secdata > /tmp/$1_secdataSpace
cut -b1-14 /tmp/$1_secdata > /tmp/$1_secdataName
cut -b25-34 /tmp/$1_secdata > /tmp/$1_secdataUPP
cut -b35-52 /tmp/$1_secdata > /tmp/$1_secdataTrade
cut -b53-55 /tmp/$1_secdata > /tmp/$1_secdataPBG
cut -b56-58 /tmp/$1_secdata > /tmp/$1_secdataEmpire
cut -b60-60 /tmp/$1_secdata > /tmp/$1_secdataTAS

# Combine chunks in sec2pdf-friendly format, with new heading for sec2pdf
paste -d '\0' /tmp/$1_secdataName /tmp/$1_secdataID /tmp/$1_secdataSpace /tmp/$1_secdataUPP /tmp/$1_secdataSpace /tmp/$1_secdataTrade /tmp/$1_secdataTAS /tmp/$1_secdataSpace /tmp/$1_secdataSpace /tmp/$1_secdataPBG /tmp/$1_secdataEmpire /tmp/$1_secdataSpace > /tmp/$1_newsecdata1
cat trav/SectorTop.txt /tmp/$1_newsecdata1 > /tmp/$1_newsecdata

# Grab pre-existing alliances
if [ $2 > 0 ]; then 	# -n tests to see if the argument is non empty
perl allygen2.pl -f 2 -r -o /tmp/$1_automsec2 /tmp/$1_newsecdata
#echo "  .  $1 Sector debug - Allygen generation complete @" $SECONDS "seconds.   "

# Strip various allygen items, based on param $6 ($3 here)


## Loop
if [ $3 = 3 ]; then
sed '/# Alliance:/d' /tmp/$1_automsec2.msec > /tmp/$1_automsec2a.msec
sed '/border/d' /tmp/$1_automsec2a.msec > /tmp/$1_automsec2b.msec
sed '/route/d' /tmp/$1_automsec2b.msec > /tmp/$1_automsec3.msec
cat /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_route.txt /tmp/$1_automsec3.msec > /tmp/$1_automsec.msec
fi

if [ $3 = 2 ]; then
sed '/# Alliance:/d' /tmp/$1_automsec2.msec > /tmp/$1_automsec2a.msec
sed '/route/d' /tmp/$1_automsec2a.msec > /tmp/$1_automsec3.msec
cat /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_route.txt /tmp/$1_automsec3.msec > /tmp/$1_automsec.msec
fi

if [ $3 = 1 ]; then
cat /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_route.txt /tmp/$1_automsec2.msec > /tmp/$1_automsec.msec
fi

if [ $3 = 0 ]; then
cat /tmp/$1_automsec2.msec > /tmp/$1_automsec.msec
fi


# Generate Sector Map
perl sec2pdf.pl -s $1 -f 2 -b -a -h -B -pTraveller -t sector -m /tmp/$1_automsec.msec -d /tmp/$1_newsecdata -o /tmp/$1_sectormap1.pdf
#echo "  .  $1 Sector debug - Small Sectormap generation complete @" $SECONDS "seconds.   "

# Generate Subsector Maps (borders, routes and regions)
perl sec2pdf_borders.pl -f 2 -s $1 -a -B -pTraveller -m /tmp/$1_automsec.msec -d /tmp/$1_newsecdata -o /tmp/$1_subsectorborders.pdf
#echo "  .  $1 Sector debug - Subsector routes generation complete @" $SECONDS "seconds.   "

else
# Generate New Allegiances
perl allygen2.pl -f 2 -i -r -o /tmp/$1_automsec /tmp/$1_newsecdata
#echo "  .  $1 Sector debug - Allygen generation complete @" $SECONDS "seconds.   "

# Generate Sector Map
perl sec2pdf.pl -s $1 -f 2 -b -a -B -h -pTraveller -t sector -m /tmp/$1_automsec.msec -d /tmp/$1_newsecdata -o /tmp/$1_sectormap1.pdf
#echo "  .  $1 Sector debug - Small Sectormap generation complete @" $SECONDS "seconds.   "

# Generate Sector Map
perl sec2pdf_borders.pl -f 2 -s $1 -a -B -pTraveller -m /tmp/$1_automsec.msec -d /tmp/$1_newsecdata -o /tmp/$1_subsectorborders.pdf
#echo "  .  $1 Sector debug - Subsector routes generation complete @" $SECONDS "seconds.   "
fi

# Combine the map with canon Classic Traveller background
/usr/local/bin/pdftk /Library/WebServer/CGI-Executables/trav/backgrounds/SectorMap_Background.pdf background /tmp/$1_sectormap1.pdf output /tmp/$1_sectormap2.pdf compress
wait

return
}




### get_Polity randomly generates names for each of the polities generated by allygen.pl

function get_Polity {
case $((RANDOM%211+1)) in
1)echo $1 "Accomodation (" $2 ")"
;;
2)echo $1 "Accord (" $2 ")"
;;
3)echo $1 "Accordate (" $2 ")"
;;
4)echo $1 "Accordment (" $2 ")"
;;
5)echo $1 "Affiliation (" $2 ")"
;;
6)echo $1 "Affiliate (" $2 ")"
;;
7)echo $1 "Affinity (" $2 ")"
;;
8)echo $1 "Aggregate (" $2 ")"
;;
9)echo $1 "Alliance (" $2 ")"
;;
10)echo $1 "Amalgam (" $2 ")"
;;
11)echo $1 "Amalgamate (" $2 ")"
;;
12)echo $1 "Amalgamation (" $2 ")"
;;
13)echo $1 "Arbitration (" $2 ")"
;;
14)echo $1 "Ascendancy (" $2 ")"
;;
15)echo $1 "Assemblage (" $2 ")"
;;
16)echo $1 "Assembly (" $2 ")"
;;
17)echo $1 "Association (" $2 ")"
;;
18)echo $1 "Authority (" $2 ")"
;;
19)echo $1 "Autocracy (" $2 ")"
;;
20)echo $1 "Birthright (" $2 ")"
;;
21)echo $1 "Biumvirate (" $2 ")"
;;
22)echo $1 "Brotherhood (" $2 ")"
;;
23)echo $1 "Cabal (" $2 ")"
;;
24)echo $1 "Cartel (" $2 ")"
;;
25)echo $1 "Circle (" $2 ")"
;;
26)echo $1 "Circuit (" $2 ")"
;;
27)echo $1 "Clanholds (" $2 ")"
;;
28)echo $1 "Clanworlds (" $2 ")"
;;
29)echo $1 "Coalition (" $2 ")"
;;
30)echo $1 "Colonies (" $2 ")"
;;
31)echo $1 "Combine (" $2 ")"
;;
32)echo $1 "Command (" $2 ")"
;;
33)echo $1 "Commission (" $2 ")"
;;
34)echo $1 "Commonality (" $2 ")"
;;
35)echo $1 "Commonwealth (" $2 ")"
;;
36)echo $1 "Commune (" $2 ")"
;;
37)echo $1 "Communion (" $2 ")"
;;
38)echo $1 "Compact (" $2 ")"
;;
39)echo $1 "Compromise (" $2 ")"
;;
40)echo $1 "Concord (" $2 ")"
;;
41)echo $1 "Concordate (" $2 ")"
;;
42)echo $1 "Concourse (" $2 ")"
;;
43)echo $1 "Concurrence (" $2 ")"
;;
44)echo $1 "Confed (" $2 ")"
;;
45)echo $1 "Confederacy (" $2 ")"
;;
46)echo $1 "Confederation (" $2 ")"
;;
47)echo $1 "Confines (" $2 ")"
;;
48)echo $1 "Conglomerate (" $2 ")"
;;
49)echo $1 "Congress (" $2 ")"
;;
50)echo $1 "Congruity (" $2 ")"
;;
51)echo $1 "Conjunction (" $2 ")"
;;
52)echo $1 "Consanguinity (" $2 ")"
;;
53)echo $1 "Consolidation (" $2 ")"
;;
54)echo $1 "Consortium (" $2 ")"
;;
55)echo $1 "Conspiracy (" $2 ")"
;;
56)echo $1 "Constellation (" $2 ")"
;;
57)echo $1 "Consulate (" $2 ")"
;;
58)echo $1 "Control (" $2 ")"
;;
59)echo $1 "Cooperate (" $2 ")"
;;
60)echo $1 "Cooperative (" $2 ")"
;;
61)echo $1 "Coordinate (" $2 ")"
;;
62)echo $1 "Corporate (" $2 ")"
;;
63)echo $1 "Council (" $2 ")"
;;
64)echo $1 "County (" $2 ")"
;;
65)echo $1 "Covenant (" $2 ")"
;;
66)echo $1 "Crusade (" $2 ")"
;;
67)echo $1 "Delegation (" $2 ")"
;;
68)echo $1 "Democracy (" $2 ")"
;;
69)echo $1 "Demos (" $2 ")"
;;
70)echo $1 "Dependency (" $2 ")"
;;
71)echo $1 "Desmense (" $2 ")"
;;
72)echo $1 "Dictatorship (" $2 ")"
;;
73)echo $1 "Directorship (" $2 ")"
;;
74)echo $1 "Disjuncture (" $2 ")"
;;
75)echo $1 "District (" $2 ")"
;;
76)echo $1 "Domain (" $2 ")"
;;
77)echo $1 "Dominance (" $2 ")"
;;
78)echo $1 "Dominate (" $2 ")"
;;
79)echo $1 "Dominion (" $2 ")"
;;
80)echo $1 "Duchy (" $2 ")"
;;
81)echo $1 "Dynasty (" $2 ")"
;;
82)echo $1 "Ecclesiasty (" $2 ")"
;;
83)echo $1 "Empire (" $2 ")"
;;
84)echo $1 "Enclave (" $2 ")"
;;
85)echo $1 "Exchange (" $2 ")"
;;
86)echo $1 "Expanse (" $2 ")"
;;
87)echo $1 "Extent (" $2 ")"
;;
88)echo $1 "Faction (" $2 ")"
;;
89)echo $1 "Factors (" $2 ")"
;;
90)echo $1 "Federacy (" $2 ")"
;;
91)echo $1 "Federate (" $2 ")"
;;
92)echo $1 "Federation (" $2 ")"
;;
93)echo $1 "Fraternity (" $2 ")"
;;
94)echo $1 "Free Worlds (" $2 ")"
;;
95)echo $1 "Fusion (" $2 ")"
;;
96)echo $1 "Group (" $2 ")"
;;
97)echo $1 "Guild (" $2 ")"
;;
98)echo $1 "Harmony (" $2 ")"
;;
99)echo $1 "Hegemony (" $2 ")"
;;
100)echo $1 "Hierate (" $2 ")"
;;
101)echo $1 "Indentureship (" $2 ")"
;;
102)echo $1 "Integration (" $2 ")"
;;
103)echo $1 "Interacterate (" $2 ")"
;;
104)echo $1 "Inquisition (" $2 ")"
;;
105)echo $1 "Judicature (" $2 ")"
;;
106)echo $1 "Judiciary (" $2 ")"
;;
107)echo $1 "Judiciate (" $2 ")"
;;
108)echo $1 "Junction (" $2 ")"
;;
109)echo $1 "Juncture (" $2 ")"
;;
110)echo $1 "Jurisdiction (" $2 ")"
;;
111)echo $1 "Kinship (" $2 ")"
;;
112)echo $1 "Kinworlds (" $2 ")"
;;
113)echo $1 "Kithworlds (" $2 ")"
;;
114)echo $1 "League (" $2 ")"
;;
115)echo $1 "Legacy (" $2 ")"
;;
116)echo $1 "Legate (" $2 ")"
;;
117)echo $1 "Legion (" $2 ")"
;;
118)echo $1 "Magistracy (" $2 ")"
;;
119)echo $1 "Magistrate (" $2 ")"
;;
120)echo $1 "Mandate (" $2 ")"
;;
121)echo $1 "Manifest (" $2 ")"
;;
122)echo $1 "Merger (" $2 ")"
;;
123)echo $1 "Ministry (" $2 ")"
;;
124)echo $1 "Monarchy (" $2 ")"
;;
125)echo $1 "Monopoly (" $2 ")"
;;
126)echo $1 "Mutuality (" $2 ")"
;;
127)echo $1 "Network (" $2 ")"
;;
128)echo $1 "Occupation (" $2 ")"
;;
129)echo $1 "Order (" $2 ")"
;;
130)echo $1 "Organization (" $2 ")"
;;
131)echo $1 "Outlands (" $2 ")"
;;
132)echo $1 "Outworlds (" $2 ")"
;;
133)echo $1 "Pact (" $2 ")"
;;
134)echo $1 "Partnership (" $2 ")"
;;
135)echo $1 "Patronage (" $2 ")"
;;
136)echo $1 "Polity (" $2 ")"
;;
137)echo $1 "Possessions (" $2 ")"
;;
138)echo $1 "Power (" $2 ")"
;;
139)echo $1 "Predominance (" $2 ")"
;;
140)echo $1 "Preeminence (" $2 ")"
;;
141)echo $1 "Prepotency (" $2 ")"
;;
142)echo $1 "Prerogative (" $2 ")"
;;
143)echo $1 "Presidency (" $2 ")"
;;
144)echo $1 "Primacy (" $2 ")"
;;
145)echo $1 "Principality (" $2 ")"
;;
146)echo $1 "Proletariat (" $2 ")"
;;
147)echo $1 "Protectorate (" $2 ")"
;;
148)echo $1 "Province (" $2 ")"
;;
149)echo $1 "Radius (" $2 ")"
;;
150)echo $1 "Range (" $2 ")"
;;
151)echo $1 "Reaches (" $2 ")"
;;
152)echo $1 "Realm (" $2 ")"
;;
153)echo $1 "Reconciliation (" $2 ")"
;;
154)echo $1 "Regency (" $2 ")"
;;
155)echo $1 "Regime (" $2 ")"
;;
156)echo $1 "Region (" $2 ")"
;;
157)echo $1 "Regnum (" $2 ")"
;;
158)echo $1 "Reign (" $2 ")"
;;
159)echo $1 "Republic (" $2 ")"
;;
160)echo $1 "Rimworlds (" $2 ")"
;;
161)echo $1 "Ring (" $2 ")"
;;
162)echo $1 "Scope (" $2 ")"
;;
163)echo $1 "Settlements (" $2 ")"
;;
164)echo $1 "Signatorate (" $2 ")"
;;
165)echo $1 "Signatory (" $2 ")"
;;
166)echo $1 "Society (" $2 ")"
;;
167)echo $1 "Sodality (" $2 ")"
;;
168)echo $1 "Sovereignty (" $2 ")"
;;
169)echo $1 "Sphere (" $2 ")"
;;
170)echo $1 "States (" $2 ")"
;;
171)echo $1 "Stronghold (" $2 ")"
;;
172)echo $1 "Subjugacy (" $2 ")"
;;
173)echo $1 "Subjugate (" $2 ")"
;;
174)echo $1 "Superiority (" $2 ")"
;;
175)echo $1 "Supremacy (" $2 ")"
;;
176)echo $1 "Suzerainty (" $2 ")"
;;
177)echo $1 "Syndicate (" $2 ")"
;;
178)echo $1 "Synthesis (" $2 ")"
;;
179)echo $1 "Sweep (" $2 ")"
;;
180)echo $1 "Technocracy (" $2 ")"
;;
181)echo $1 "Territories (" $2 ")"
;;
182)echo $1 "Theocracy (" $2 ")"
;;
183)echo $1 "Throne Worlds (" $2 ")"
;;
184)echo $1 "Trade Association (" $2 ")"
;;
185)echo $1 "Trade Coalition (" $2 ")"
;;
186)echo $1 "Trade Confederation (" $2 ")"
;;
187)echo $1 "Trade Federation (" $2 ")"
;;
188)echo $1 "Trade Union (" $2 ")"
;;
189)echo $1 "Transcendancy (" $2 ")"
;;
190)echo $1 "Treaty (" $2 ")"
;;
191)echo $1 "Tripartite (" $2 ")"
;;
192)echo $1 "Triumvirate (" $2 ")"
;;
193)echo $1 "Trust (" $2 ")"
;;
194)echo $1 "Tyranny (" $2 ")"
;;
195)echo $1 "Unanimity (" $2 ")"
;;
196)echo $1 "Unification (" $2 ")"
;;
197)echo $1 "Union (" $2 ")"
;;
198)echo $1 "Unity (" $2 ")"
;;
199)echo $1 "Worlds (" $2 ")"
;;
200)echo $1 "Zone (" $2 ")"
;;
201)echo "Grand Duchy of "$1 "(" $2 ")"
;;
202)echo "Great "$1 "(" $2 ")"
;;
203)echo "League of "$1 "Worlds (" $2 ")"
;;
204)echo "Lords of "$1 "(" $2 ")"
;;
205)echo "New Worlds of "$1 "(" $2 ")"
;;
206)echo "Stellar Kingdom of "$1 "(" $2 ")"
;;
207)echo "Unified Systems of "$1 "(" $2 ")"
;;
208)echo "Concordance of "$1 "Worlds (" $2 ")"
;;
209)echo "League of "$1 "Worlds (" $2 ")"
;;
210)echo "Glory of "$1 "(" $2 ")"
;;
211)echo "Planetary Alliance of "$1 "(" $2 ")"
;;
212)echo "Entreaty of "$1 "(" $2 ")"
;;
*)echo $1
;;
esac
return
}



### get_Polities: Grabs each polity

function get_Polities {
     while read LINE
    do
          get_Polity $LINE > /tmp/$1polity$LINE.txt 
               done < /tmp/$1
}





#### Now the main body of the script.


### 1. GENERATE THE COVERS


## Generate the custom cover 

# Generate the text of the sector name
echo $1 > /tmp/$1seccoverA.txt
sed '/_/ s/_/ /g' /tmp/$1seccoverA.txt > /tmp/$1seccover.txt

# Add a line to the sectorname for processing
cat /Library/WebServer/CGI-Executables/trav/covercat.txt /tmp/$1seccover.txt > /tmp/$1seccover2.txt

# LBB cover
enscript --word-wrap /tmp/$1seccover2.txt -r --margins=266:-300:-400:407 -B -f OptimaItalic32 --media=Letter -q -p /tmp/$1seccover1.ps

# Turn the generated text white for the cover
sed '/5 578 M/ s/5 578 M/5 578 M 1 setgray/g' /tmp/$1seccover1.ps > /tmp/$1seccover.ps 

# Make the generated text of the cover a pdf
/usr/bin/pstopdf /tmp/$1seccover.ps -o /tmp/$1seccover1.pdf

# Combine the generated name and the background front cover pdf into the new sector front cover.
/usr/local/bin/pdftk /tmp/$1seccover1.pdf background /Library/WebServer/CGI-Executables/trav/SectorData_Cover.pdf output /tmp/$1CoverInt.pdf
wait

#echo "  .  $1 Sector debug - cover complete @" $SECONDS "seconds.   "

## Generate the back page

# Random Quote Grabber
./trav/randomquote.sh > /tmp/$1backquote.txt

# LBB Back
enscript /tmp/$1backquote.txt -r --word-wrap --margins=122:-100:364:40 -B -f OptimaItalic20 --media=Letter -q -p /tmp/$1Back1.ps

# Make the generated text of the back cover a pdf
sed '/5 567 M/ s/5 567 M/5 567 M 1 setgray/g' /tmp/$1Back1.ps > /tmp/$1CoverBack.ps 

# Make the generated text of the back cover a pdf
/usr/bin/pstopdf /tmp/$1CoverBack.ps -o /tmp/$1BackCovertemp.pdf

# Combine the generated text and the background back cover pdf into the new sector back cover.
/usr/local/bin/pdftk /tmp/$1BackCovertemp.pdf background /tmp/$1CoverInt.pdf output /tmp/$1Cover.pdf
wait

#echo "  .  $1 Sector debug - back cover complete @" $SECONDS "seconds.   "


### 2. GENERATE OR GRAB THE SECTOR'S DATA


## Generate the raw subsector data or import it

if [ $5 > 0 ]; then 
cp /Library/WebServer/CGI-Executables/trav/sectorfiles/$5 /tmp/$1secdata
sed q /tmp/$1secdata > /tmp/$1secdataorighead
sed '1d' /tmp/$1secdata > /tmp/$1secdataorig
NUM_WORLDS=`wc -l /tmp/$1secdataorig | awk '{ print $1 }'`

else 
/usr/local/bin/gensec3 $2 $3 > /tmp/$1secdataorig2

# Save the first line of the sector file ('Version' tag)
sed q /tmp/$1secdataorig2 > /tmp/$1secdataorighead

# Remove the first line for the text processing
sed '1d' /tmp/$1secdataorig2 > /tmp/$1secdataorig

#echo "  .  $1 Sector debug - data generation complete @" $SECONDS "seconds.   "

## Generate the sector's system names

# Count the number of worlds generated
NUM_WORLDS=`wc -l /tmp/$1secdataorig | awk '{ print $1 }'`

# Grab the generated datafile's contents preceding and following the name
cut -b20-80 /tmp/$1secdataorig > /tmp/$1secdataorigBack

# Run the random word generator
perl /Library/WebServer/CGI-Executables/trav/lc -$NUM_WORLDS /Library/WebServer/CGI-Executables/trav/namesmaster.txt > /tmp/$1namegrab1

# Grab the names from the file
sed -e :a -e 's/^.\{1,18\}$/& /;ta' /tmp/$1namegrab1 > /tmp/$1namegrab2

# Combine the three files into a new secdata file with the names inside
paste -d '\0' /tmp/$1namegrab2 /tmp/$1secdataorigBack > /tmp/$1secdatainterim

# paste the header back onto the sector data
cat /tmp/$1secdataorighead /tmp/$1secdatainterim > /tmp/$1secdata

fi

#echo "  .  $1 Sector debug - word generation complete @" $SECONDS "seconds.   "


### 4. GENERATE THE SECTOR MAP

## If we're using a pre-existing sector file, don't change the alliances.

if [ $5 > 0 ]; then 

# Run the map with old alliances retained
get_Sectormap $1 2 $6
wait
sed -n '/route/p' /tmp/$1_automsec.msec > /tmp/$1_route.txt

else
# Run the map with new alliances
get_Sectormap $1
wait

#echo "  .  $1 Sector debug - sector map generation complete @" $SECONDS "seconds.   "


## If it's a fresh sector, go ahead and generate the names of the Alliances

# Grab a version of the msec file without 'border'
sed '/# Alliance: / s/# Alliance: / /g' /tmp/$1_automsec.msec > /tmp/$1_before.msec

#sed '/# Alliance: /d' /tmp/$1_automsec.msec > /tmp/$1_beforeZ.msec
sed '/border/d' /tmp/$1_automsec.msec > /tmp/$1_before1a.msec
sed -n '/route/p' /tmp/$1_before1a.msec > /tmp/$1_route.txt

sed '/route/d' /tmp/$1_before.msec > /tmp/$1_before1.msec
sed '/border/d' /tmp/$1_before1.msec > /tmp/$1_after1.msec

sed -n 'G; s/\n/&&/; /^\([ -~]*\n\).*\n\1/d; s/\n//; h; P' /tmp/$1_after1.msec > /tmp/$1_after.msec
# Count the alliances in the file
NUM_POLS=`wc -l /tmp/$1_after.msec | awk '{ print $1 }'`

# Generate the right number of random names
perl /Library/WebServer/CGI-Executables/trav/lc -$NUM_POLS /Library/WebServer/CGI-Executables/trav/namesmaster.txt > /tmp/politynames

# Put the codes with the random names and run the polity combiner
paste -d '\0' /tmp/politynames /tmp/$1_after.msec > /tmp/$1_combo1.msec
sed '/  / s/  / /g' /tmp/$1_combo1.msec > /tmp/$1_combo.msec
get_Polities $1_combo.msec

# Put all the polity names together as the final 'alliances' text
cat /tmp/$1_combo.msecpolity*.txt > /tmp/$1_polities.txt
ditto /tmp/$1_polities.txt /tmp/$1_alliances.txt
wait

#echo "  .  $1 Sector debug - alliance generation complete @" $SECONDS "seconds.   "
fi


# NOTE: Need to add code to grab any spaces INSIDE the names and turn them into underscores. Right now it's manual.


## Grab the alliances (pre-existing or not) and parse them into the secdata file

# Save the first line of the sector file ('Version' tag)
sed q /tmp/$1secdata > /tmp/$1secdataorighead2

# Remove the first line for the text processing
if [ $5 > 0 ]; then 
ditto /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_alliances.txt /tmp/$1secdatadesc_alliances.txt
wait
ditto /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_alliances.txt /tmp/$1_alliances.txt
wait
ditto /Library/WebServer/CGI-Executables/trav/sectorfiles/$1_alliances.txt /tmp/$1_polities.txt
wait
ditto /tmp/$1secdata /tmp/$1_automsec.sec
wait
else
sed '1,15d' /tmp/$1_automsec.sec > /tmp/$1_newsecdataProc
sed '1d' /tmp/$1secdata > /tmp/$1secdataProc

# Splice the new secdata file
cut -b1-56 /tmp/$1secdataProc > /tmp/$1_secdataEmpirePre
cut -b60-64 /tmp/$1secdataProc > /tmp/$1_secdataEmpirePost
cut -b56-58 /tmp/$1_newsecdataProc > /tmp/$1_secdataNewEmpire

# Put it all together
paste -d '\0' /tmp/$1_secdataEmpirePre /tmp/$1_secdataNewEmpire /tmp/$1_secdataEmpirePost > /tmp/$1secdatainterim2
cat /tmp/$1secdataorighead2 /tmp/$1secdatainterim2 > /tmp/$1secdata

# safety kludge for literal problem
ditto /tmp/$1_alliances.txt /tmp/$1secdatadesc_alliances.txt
wait

#echo "  .  $1 Sector debug - alliance parsing complete @" $SECONDS "seconds.   "
fi


### GENERATE THE SUBSECTOR MAPS AND DATA PAGES

#Create Title Text for Listings and Descriptions
echo ""$1"""" > /tmp/$1titleA.txt
sed '/_/ s/_/ /g' /tmp/$1titleA.txt > /tmp/$1title.txt

# Create Title Text for Sector Map
echo "Contains" $NUM_WORLDS" systems." > /tmp/$1Sectormapsubtitle.txt
#echo ""$1""" Sector (containing" $NUM_WORLDS" systems)" > /tmp/$1SectorMaptitleA.txt
#sed '/_/ s/_/ /g' /tmp/$1SectorMaptitleA.txt > /tmp/$1SectorMaptitle.txt

#cat /tmp/$1title.txt /tmp/$1Sectormapsubtitle.txt > /tmp/$1SectorMaptitle.txt
cat /tmp/$1title.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1Sectormapsubtitle.txt > /tmp/$1SectorMaptitle.txt

## Big Per-Subsector Loop Starts
whichborderpage=0
for x in A B C D E F G H I J K L M N O P; do

let "whichborderpage = whichborderpage +1"
# Generate this subsector's data file

/usr/local/bin/subsec2 S=$x < /tmp/$1secdata > /tmp/$1subsec1$x
NUM_SUBSECWORLDS=`wc -l /tmp/$1subsec1$x | awk '{ print $1 }'`

sed '/_/ s/_/ /g' /tmp/$1subsec1$x > /tmp/$1subsec$x
wait

# Create a duplicate
sed '' /tmp/$1subsec$x > /tmp/$1subsecdata$x

# Reorder the ID on the datafile for output only
cut -b20-24 /tmp/$1subsecdata$x > /tmp/$1secdatareorderID
cut -b1-19 /tmp/$1subsecdata$x > /tmp/$1secdatareorderName1
sed '/_/ s/_/ /g' /tmp/$1secdatareorderName1 > /tmp/$1secdatareorderName
cut -b25-81 /tmp/$1subsecdata$x > /tmp/$1subsecend$x



## ============= HERE'S THE SCORING ================= ##




## EXPERIMENTAL: Find the capital



function totalize() {

echo `expr "$1" "+" "$2" "+" "$3" "+" "$4" "+" "$5" "+" "$6" "+" "$7" "+" "$8" + "$9" | awk '{ print $1 }'`
#echo $TOTAL
return
}







function tally() {
tallyline=10
filler="_"
while read LINE
do
let "tallyline = tallyline +1"
totalize $LINE > /tmp/$2subsecdataItemTally$1_$tallyline
done < /tmp/$3

cat /tmp/$2subsecdataItemTally$1* > /tmp/$2subsecdataFinalTally$1
return
}









function scorer() {
ditto /tmp/$1subsecdata$x /tmp/$1subsecdataInit$x
cut -b1-19 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreName$x
cut -b24-24 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreSpace$x
cut -b25-25 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreStarport$x
cut -b29-29 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScorePop$x
cut -b32-33 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreTech1$x
sed '/-/ s/-/_/g' /tmp/$1subsecdataScoreTech1$x > /tmp/$1subsecdataScoreTech$x
cut -b36-52 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreTrade$x
cut -b59-61 /tmp/$1subsecdataInit$x > /tmp/$1subsecdataScoreBases$x

paste -d '\0' /tmp/$1subsecdataScoreSpace$x /tmp/$1subsecdataScoreStarport$x /tmp/$1subsecdataScoreSpace$x /tmp/$1subsecdataScorePop$x /tmp/$1subsecdataScoreSpace$x /tmp/$1subsecdataScoreTech$x /tmp/$1subsecdataScoreSpace$x /tmp/$1subsecdataScoreTrade$x /tmp/$1subsecdataScoreBases$x > /tmp/$1subsecdataScore$x

#Tradeclass:
#Ri: +1
#Po: -2
#Hi: +5
#Ni: -1
#Lo: -2
#Ba: -5
#Fl: -1

sed '/Ri/ s/Ri/1/g' /tmp/$1subsecdataScore$x > /tmp/$1subsecdataScore1$x
sed '/Po/ s/Po/-2/g' /tmp/$1subsecdataScore1$x > /tmp/$1subsecdataScore2$x
sed '/Hi/ s/Hi/5/g' /tmp/$1subsecdataScore2$x > /tmp/$1subsecdataScore3$x
sed '/Ni/ s/Ni/-1/g' /tmp/$1subsecdataScore3$x > /tmp/$1subsecdataScore4$x
sed '/Lo/ s/Lo/-2/g' /tmp/$1subsecdataScore4$x > /tmp/$1subsecdataScore5$x
sed '/Ba/ s/Ba/-5/g' /tmp/$1subsecdataScore5$x > /tmp/$1subsecdataScore6$x
sed '/Fl/ s/Fl/-1/g' /tmp/$1subsecdataScore6$x > /tmp/$1subsecdataScore7$x

#Zones:
#Amber: -5
#Red: -20
#U: -20

sed '/R$/ s/R$/-20/g' /tmp/$1subsecdataScore7$x > /tmp/$1subsecdataScore8$x
sed '/A$/ s/A$/-5/g' /tmp/$1subsecdataScore8$x > /tmp/$1subsecdataScore9$x

#StarPort:
#A: +10
#B: +5
#C: +2
#D: +1

sed '/^ A/ s/^ A/10/g' /tmp/$1subsecdataScore9$x > /tmp/$1subsecdataScore10$x
sed '/^ B/ s/^ B/5/g' /tmp/$1subsecdataScore10$x > /tmp/$1subsecdataScore11$x
sed '/^ C/ s/^ C/2/g' /tmp/$1subsecdataScore11$x > /tmp/$1subsecdataScore12$x
sed '/^ D/ s/^ D/1/g' /tmp/$1subsecdataScore12$x > /tmp/$1subsecdataScore13$x
sed '/^ E/ s/^ E/0/g' /tmp/$1subsecdataScore13$x > /tmp/$1subsecdataScore13a$x
sed '/^ X/ s/^ X/0/g' /tmp/$1subsecdataScore13a$x > /tmp/$1subsecdataScore13b$x

#Population:
#Add population number

sed '/ A / s/ A / 10 /g' /tmp/$1subsecdataScore13b$x > /tmp/$1subsecdataScore14$x
sed '/ B / s/ B / 11 /g' /tmp/$1subsecdataScore14$x > /tmp/$1subsecdataScore15$x
sed '/ C / s/ C / 12 /g' /tmp/$1subsecdataScore15$x > /tmp/$1subsecdataScore16$x
sed '/ D / s/ D / 13 /g' /tmp/$1subsecdataScore16$x > /tmp/$1subsecdataScore17$x
sed '/ E / s/ E / 14 /g' /tmp/$1subsecdataScore17$x > /tmp/$1subsecdataScore18$x
sed '/ F / s/ F / 15 /g' /tmp/$1subsecdataScore18$x > /tmp/$1subsecdataScore19$x
sed '/ G / s/ G / 16 /g' /tmp/$1subsecdataScore19$x > /tmp/$1subsecdataScore20$x
sed '/ H / s/ H / 17 /g' /tmp/$1subsecdataScore20$x > /tmp/$1subsecdataScore21$x
sed '/ I / s/ I / 18 /g' /tmp/$1subsecdataScore21$x > /tmp/$1subsecdataScore22$x

#TechLevel:
#Add 2*techlevel

sed '/_0 / s/_0 / 0 /g' /tmp/$1subsecdataScore22$x > /tmp/$1subsecdataScore22a$x
sed '/_1 / s/_1 / 2 /g' /tmp/$1subsecdataScore22a$x > /tmp/$1subsecdataScore22b$x
sed '/_2 / s/_2 / 4 /g' /tmp/$1subsecdataScore22b$x > /tmp/$1subsecdataScore22c$x
sed '/_3 / s/_3 / 6 /g' /tmp/$1subsecdataScore22c$x > /tmp/$1subsecdataScore22d$x
sed '/_4 / s/_4 / 8 /g' /tmp/$1subsecdataScore22d$x > /tmp/$1subsecdataScore22e$x
sed '/_5 / s/_5 / 10 /g' /tmp/$1subsecdataScore22e$x > /tmp/$1subsecdataScore22f$x
sed '/_6 / s/_6 / 12 /g' /tmp/$1subsecdataScore22f$x > /tmp/$1subsecdataScore22g$x
sed '/_7 / s/_7 / 14 /g' /tmp/$1subsecdataScore22g$x > /tmp/$1subsecdataScore22h$x
sed '/_8 / s/_8 / 16 /g' /tmp/$1subsecdataScore22h$x > /tmp/$1subsecdataScore22i$x
sed '/_9 / s/_9 / 18 /g' /tmp/$1subsecdataScore22i$x > /tmp/$1subsecdataScore22j$x
sed '/_A / s/_A / 20 /g' /tmp/$1subsecdataScore22j$x > /tmp/$1subsecdataScore22k$x
sed '/_B / s/_B / 22 /g' /tmp/$1subsecdataScore22k$x > /tmp/$1subsecdataScore22l$x
sed '/_C / s/_C / 24 /g' /tmp/$1subsecdataScore22l$x > /tmp/$1subsecdataScore22m$x
sed '/_D / s/_D / 26 /g' /tmp/$1subsecdataScore22m$x > /tmp/$1subsecdataScore22n$x
sed '/_E / s/_E / 28 /g' /tmp/$1subsecdataScore22n$x > /tmp/$1subsecdataScore22o$x
sed '/_F / s/_F / 30 /g' /tmp/$1subsecdataScore22o$x > /tmp/$1subsecdataScore22p$x
sed '/_G / s/_G / 32 /g' /tmp/$1subsecdataScore22p$x > /tmp/$1subsecdataScore22q$x
sed '/_H / s/_H / 34 /g' /tmp/$1subsecdataScore22q$x > /tmp/$1subsecdataScore22r$x
sed '/_I / s/_I / 36 /g' /tmp/$1subsecdataScore22r$x > /tmp/$1subsecdataScore23$x

#Bases:
#Z, Y, G, N, 2, H: +4
#
#Planet names:
#Provincial name: -100 (To avoid that a planet with a name that sounds like a small place becomes the capital)

sed '/[A-z]/ s/[A-z]/ /g' /tmp/$1subsecdataScore23$x > /tmp/$1subsecdataScoreFinal1$x
sed '/  */ s/  */ /g' /tmp/$1subsecdataScoreFinal1$x > /tmp/$1subsecdataScoreFinal$x

return
}






function grabCapital() {

# get the lowercase version of the subsector letter
LOWERSUB=`echo $x |tr "[A-Z]" "[a-z]" `
#echo $LOWERSUB

# find the line in the 'routes' file containing the subsector name, if it exists.
SUBSECNAMEFOUND=`sed -n "/^$LOWERSUB /p" /tmp/$1_automsec.msec | awk '{ print $2 " " $3 " " $4 " " $5 }'`
#echo $SUBSECNAMEFOUND

# if so, grab the name's contents and put it into 'CAPITALNAME'.
if [ "$SUBSECNAMEFOUND" > 0 ]; then
echo $SUBSECNAMEFOUND > /tmp/$1_subsecname$x.txt
CAPITALNAME=`cat < /tmp/$1_subsecname$x.txt | awk '{ print $0 }'`

# If not, combine a new file with 'Ca' autogenerated.
else

cut -b1-19 /tmp/$1subsecdata$x > /tmp/$1subsecdataName$x
cut -b36-51 /tmp/$1subsecdata$x > /tmp/$1subsecdataTrade$x
paste -d '\0' /tmp/$1subsecdataTrade$x /tmp/$1subsecdataName$x > /tmp/$1subsecdataSum1$x
sed -n -e '/ Ca /{1!p;g;$!N;}' -e h /tmp/$1subsecdataSum1$x > /tmp/$1subsecdataSum2$x
cut -b17-60 /tmp/$1subsecdataSum2$x > /tmp/$1subsecdataSum3$x
sed 's/[ \t]*$//' /tmp/$1subsecdataSum3$x > /tmp/$1subsecdataSum4$x 
PRIORCAPITAL=`cat < /tmp/$1subsecdataSum4$x | awk '{ print $0 }'`

# If no line contains 'Ca'
if [ $PRIORCAPITAL > 0 ]; then
CAPITALNAME=`cat < /tmp/$1subsecdataSum4$x | awk '{ print $1 }'`
else
CAPITALNAME=`cat < /tmp/$1subsecdataScorerSheetCapital$x | awk '{ print $2 }'`
WORLDLINE=`cat < /tmp/$1subsecdataScorerSheetCapital$x | awk '{ print $1 }'`

# Revise subsector data to include 'Capital'

#remove prior lines
#remove subsequent lines
#grab trade chunk
#replace chunk's last two digits with 'Ca'
#reduce chunk's white space to 1 space only
#recombine chunk into line
#recombine subsector data into new secfile

fi

fi

echo "The "$CAPITALNAME" subsector contains "$NUM_SUBSECWORLDS" worlds."  > /tmp/$1subsecdataSum$x
#, with a population of "$SUBSECPOP". The highest population is "$HIGHPOP", at "$HIGHPOPWORLD". The highest tech level is "$HIGHTEK", at "$HIGHTEK_WORLD"."
return
}




## Scoring loop

## Process:
# 1. see if there is a line in the msec file with a lowercase version of the subsector letter and a space at the beginning.




# 2. if so, use that line.
# 3. if not, enable the scoring loop.
# 4. In the scoring loop, if there is a world in the subsector with 'Ca', that's the subsector capital and therefore the name.
# 5. If not, determine the capital and modify the world's line in the .sec file.
#
# If the msec file has a line containing the lowercase variant of the subsector letter, followed by a space, use the rest of the line as the subsector name.
#
#
#
#




if [ $SCORING ]; then

if [ $NUM_SUBSECWORLDS -gt 0 ]; then
#echo "This subsector ( "$x" ) has "$NUM_SUBSECWORLDS" worlds."

scorer $1
wait

# Tally up the scores
tally $x $1 $1subsecdataScoreFinal$x > /tmp/$1subsecdataTally$x

# Include the names
paste -d '\0' /tmp/$1subsecdataFinalTally$x /tmp/$1subsecdataScoreSpace$x /tmp/$1subsecdataScoreName$x > /tmp/$1subsecdataScorerSheet$x
wait

# Sort subsector worlds by tally
sort -n -r /tmp/$1subsecdataScorerSheet$x > /tmp/$1subsecdataScorerSheetSorted$x
sed q /tmp/$1subsecdataScorerSheetSorted$x > /tmp/$1subsecdataScorerSheetCapital$x

# Run the main loop
grabCapital $1

# Create Subsector subtitle
echo $CAPITALNAME "Subsector" > /tmp/$1subsectitle$x.txt

# Put the heading on top of this subsector's data file (for printing)
paste -d '\0' /tmp/$1secdatareorderID /tmp/$1secdatareorderName /tmp/$1subsecend$x > /tmp/$1subsecReorder$x
cat -u /Library/WebServer/CGI-Executables/trav/introspace.txt /tmp/$1title.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1subsectitle$x.txt /Library/WebServer/CGI-Executables/trav/subtitles/subtitle$x.txt /Library/WebServer/CGI-Executables/trav/beginfile.txt /tmp/$1subsecReorder$x /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1subsecdataSum$x > /tmp/$1subsecOut$x

else


# Compile 'em without subsector scoring
paste -d '\0' /tmp/$1secdatareorderID /tmp/$1secdatareorderName /tmp/$1subsecend$x > /tmp/$1subsecReorder$x
cat -u /Library/WebServer/CGI-Executables/trav/introspace.txt /tmp/$1title.txt /Library/WebServer/CGI-Executables/trav/subtitles/subtitle$x.txt /Library/WebServer/CGI-Executables/trav/beginfile.txt /tmp/$1subsecReorder$x /Library/WebServer/CGI-Executables/trav/ret.txt > /tmp/$1subsecOut$x
wait
fi

fi


## ======================= END SCORING ======================= ##






# Change the version number to trip the logic of the mapper
sed '/3/ s/3/2/g' /tmp/$1secdataorighead > /tmp/$1secdataorighead2
wait

# Put the header on each subsector file
cat /tmp/$1secdataorighead2 /tmp/$1subsec$x > /tmp/$1subsecCalc$x
wait

# Map each subsector's data
/usr/local/bin/mapsub3 -p < /tmp/$1subsecCalc$x > /tmp/$1subsec$x.ps

# Create .pdf file from this subsectors map's .ps file
/usr/bin/pstopdf /tmp/$1subsec$x.ps -o /tmp/$1subsecinter$x.pdf
wait

# Create .ps file from this subsectors data's file
enscript /tmp/$1subsecOut$x --word-wrap --margins=40:20:40:40 -B -f Courier7.5 --media=Traveller -q -p /tmp/$1subsecdata$x.ps
wait

# Create .pdf file from this subsector data's .ps file
/usr/bin/pstopdf /tmp/$1subsecdata$x.ps -o /tmp/$1subsecdatainter$x.pdf
wait

# Place the generated data on a background with header and page number
/usr/local/bin/pdftk /tmp/$1subsecdatainter$x.pdf background /Library/WebServer/CGI-Executables/trav/backgrounds/Data_Background$x.pdf output /tmp/$1subsecdata$x.pdf
wait

# Extract the proper subsector borders page
/usr/local/bin/pdftk /tmp/$1_subsectorborders.pdf cat $whichborderpage output /tmp/$1subsecborders$x.pdf
wait

# Combine the borders and the previous pdf
/usr/local/bin/pdftk /tmp/$1subsecinter$x.pdf background /tmp/$1subsecborders$x.pdf output /tmp/$1subsecinter2$x.pdf
wait

# Place the generated map on a background with header and page number
/usr/local/bin/pdftk /Library/WebServer/CGI-Executables/trav/backgrounds/Map_Background$x.pdf background /tmp/$1subsecinter2$x.pdf output /tmp/$1subsec$x.pdf
wait



#echo "  .  $1 Sector debug - " $x "subsector data / map parsing complete @" $SECONDS "seconds.   "

# Each subsector's loop ends here
done

# Then recombine subsectors into new secdatafile


### Assemble final .pdf containing cover and each subsector's map and data

# Sectormap Page

# Combine text for Sectormap
cat /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1SectorMaptitle.txt > /tmp/$1Maptitle.txt 

# Grab the Sector's title for the map page
enscript --word-wrap --margins=35:-100:0:40 --fancy-header='travellerpagenums' --header='' --header-font=Univers9 /tmp/$1Maptitle.txt -f Univers8 --media=Traveller -q -p /tmp/$1_SectorMapSectorTitle.ps
wait

# Make the generated text of the back cover a pdf
/usr/bin/pstopdf /tmp/$1_SectorMapSectorTitle.ps -o /tmp/$1_SectorMapSectorTitle.pdf

#place the map on a Classic Traveller background
/usr/local/bin/pdftk /tmp/$1_SectorMapSectorTitle.pdf background /tmp/$1_sectormap2.pdf output /tmp/$1_sectormap.pdf
wait


# DEBUG - echo "  .  $1 Sector debug - sector map generation complete @" $SECONDS "seconds.   "



# Polities Page

# combine text
cat /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1title.txt /Library/WebServer/CGI-Executables/trav/ret.txt /tmp/$1_alliances.txt > /tmp/$1_politiespage.txt
wait

#turn to ps file
enscript --word-wrap --margins=35:-100:0:40 --fancy-header='travellerpagenums' --header='' --header-font=Univers9 /tmp/$1_politiespage.txt -f Univers8 --media=Traveller -q -p /tmp/$1_politiespageout.ps
wait

# turn to pdf
/usr/bin/pstopdf /tmp/$1_politiespageout.ps -o /tmp/$1_politiespage1.pdf
wait

# join with background (header, page nums)
/usr/local/bin/pdftk /tmp/$1_politiespage1.pdf background /Library/WebServer/CGI-Executables/trav/backgrounds/SectorPolities_Background.pdf output /tmp/$1_politiespage.pdf
wait

#echo "  .  $1 Sector debug - polities generation complete @" $SECONDS "seconds.   "



## Decide - descriptions or no?
# Evaluate whether the fourth argument is higher than 1 (to bypass descriptions)

needfordesc=3
desc=$4

let "desc = desc + 1"

if [ "$needfordesc" -lt "$desc" ]; then 	# -n tests to see if the argument is non empty


## BRING IT TOGETHER WITHOUT DESCRIPTIONS

# Bring it together with the right TOC (no 'world descriptions' line)
/usr/local/bin/pdftk /tmp/$1Cover.pdf /Library/WebServer/CGI-Executables/trav/SectorData_IntNoDesc.pdf /tmp/$1subsecdataA.pdf /tmp/$1subsecA.pdf /tmp/$1subsecdataB.pdf /tmp/$1subsecB.pdf /tmp/$1subsecdataC.pdf /tmp/$1subsecC.pdf /tmp/$1subsecdataD.pdf /tmp/$1subsecD.pdf /tmp/$1subsecdataE.pdf /tmp/$1subsecE.pdf /tmp/$1subsecdataF.pdf /tmp/$1subsecF.pdf /tmp/$1subsecdataG.pdf /tmp/$1subsecG.pdf /tmp/$1subsecdataH.pdf /tmp/$1subsecH.pdf /tmp/$1subsecdataI.pdf /tmp/$1subsecI.pdf /tmp/$1subsecdataJ.pdf /tmp/$1subsecJ.pdf /tmp/$1subsecdataK.pdf /tmp/$1subsecK.pdf /tmp/$1subsecdataL.pdf /tmp/$1subsecL.pdf /tmp/$1subsecdataM.pdf /tmp/$1subsecM.pdf /tmp/$1subsecdataN.pdf /tmp/$1subsecN.pdf /tmp/$1subsecdataO.pdf /tmp/$1subsecO.pdf /tmp/$1subsecdataP.pdf /tmp/$1subsecP.pdf cat output /tmp/$1pre.pdf
wait
#echo "  .  $1 Sector debug - initial pdf document combination (without descs) complete @" $SECONDS "seconds.   "

# Combine the subsector pages into the final pdf and compress
#/usr/local/bin/pdftk /tmp/$1pre.pdf /tmp/$1Back.pdf cat output /tmp/$1.pdf compress
/usr/local/bin/pdftk /tmp/$1pre.pdf /tmp/$1_sectormap.pdf /tmp/$1_politiespage.pdf cat output /tmp/$1.pdf compress
wait

# Back up the relevant files in the survey archives
cp /tmp/$1.pdf /sectors/autogen/$1.pdf
cp /tmp/$1secdata /sectors/autogen/$1.sec
wait

#echo "  .  $1 Sector debug - final document combination (without descs) complete @" $SECONDS "seconds.   "
else 


## PARSE THE UPP'S OF EACH WORLD INTO TEXTUAL DESCRIPTIONS

# Cut and recombine the ID, UPP, NAME and Polity fields into a new list
cut -b20-24 /tmp/$1secdata > /tmp/$1secdatadescreformID
cut -b25-34 /tmp/$1secdata > /tmp/$1secdatadescreformSpaceUPP
cut -b1-18 /tmp/$1secdata > /tmp/$1secdatadescreformName
cut -b57-59 /tmp/$1secdata > /tmp/$1secdatadescreformEmpire

paste -d '\0' /tmp/$1secdatadescreformID /tmp/$1secdatadescreformSpaceUPP /tmp/$1secdatadescreformEmpire /tmp/$1secdatadescreformName > /tmp/$1secdatareform
#sed -e 's/ /\+/' /tmp/$1secdatareform > /tmp/$1secdatareform2
#sed -e 's/-//' /tmp/$1secdatareform2 > /tmp/$1secdatareform3
#sed -e 's/-//' /tmp/$1secdatareform > /tmp/$1secdatareform4
#sed -e 's/ /\+/' /tmp/$1secdatareform3 > /tmp/$1secdataform4
#sed '1d' /tmp/$1secdataform4 > /tmp/$1secdatadesc
sed '1d' /tmp/$1secdatareform > /tmp/$1secdatadesc

# Run the Descriptions generator
get_SectorDescriptions $1secdatadesc $1
wait

## BRING IT TOGETHER WITH TEXTUAL DESCRIPTIONS

# Bring it together with the right TOC (w/ 'world descriptions' line)
/usr/local/bin/pdftk /tmp/$1Cover.pdf /Library/WebServer/CGI-Executables/trav/SectorData_IntDesc.pdf /tmp/$1subsecdataA.pdf /tmp/$1subsecA.pdf /tmp/$1subsecdataB.pdf /tmp/$1subsecB.pdf /tmp/$1subsecdataC.pdf /tmp/$1subsecC.pdf /tmp/$1subsecdataD.pdf /tmp/$1subsecD.pdf /tmp/$1subsecdataE.pdf /tmp/$1subsecE.pdf /tmp/$1subsecdataF.pdf /tmp/$1subsecF.pdf /tmp/$1subsecdataG.pdf /tmp/$1subsecG.pdf /tmp/$1subsecdataH.pdf /tmp/$1subsecH.pdf /tmp/$1subsecdataI.pdf /tmp/$1subsecI.pdf /tmp/$1subsecdataJ.pdf /tmp/$1subsecJ.pdf /tmp/$1subsecdataK.pdf /tmp/$1subsecK.pdf /tmp/$1subsecdataL.pdf /tmp/$1subsecL.pdf /tmp/$1subsecdataM.pdf /tmp/$1subsecM.pdf /tmp/$1subsecdataN.pdf /tmp/$1subsecN.pdf /tmp/$1subsecdataO.pdf /tmp/$1subsecO.pdf /tmp/$1subsecdataP.pdf /tmp/$1subsecP.pdf cat output /tmp/$1pre.pdf
wait
#echo "  .  $1 Sector debug - initial pdf document combination (with descs) complete @" $SECONDS "seconds.   "

# Combine the subsector pages and descriptions pages, plus covers into the final pdf and compress
#/usr/local/bin/pdftk /tmp/$1pre.pdf /tmp/$1secdatadescpiece.pdf /tmp/$1Back.pdf cat output /tmp/$1.pdf compress
/usr/local/bin/pdftk /tmp/$1pre.pdf /tmp/$1_sectormap.pdf /tmp/$1_politiespage.pdf /tmp/$1secdatadescpiece.pdf cat output /tmp/$1.pdf compress
wait

# Trim the description file's beginning section
sed '1,2596d' /tmp/$1secdatadescfinaldet.txt > /tmp/$1secdatadescfinaldet1.txt
cat /tmp/$1title.txt /tmp/$1secdatadescfinaldet1.txt > /tmp/$1_desc.txt
# Back up the relevant files in the survey archives
cp /tmp/$1.pdf /sectors/autogen/$1.pdf
cp /tmp/$1secdata /sectors/autogen/$1.sec
cp /tmp/$1_desc.txt /sectors/autogen/$1_desc.txt
wait

#echo "  .  $1 Sector debug - document combination (with descs) complete @" $SECONDS "seconds.   "
fi

### BACK THE REST UP

# Obsolete backups
#cp /tmp/$1_sectormap.pdf /sectors/autogen/$1_sectormap.pdf
#cp /tmp/$1_subsectorborders.pdf /sectors/autogen/$1_subsectorborders.pdf
#/usr/local/bin/pdftk /tmp/$1.pdf cat 2-end output /tmp/$1nocover.pdf

# Optional (?): Save file versions for 'sec2pdf' backwards compatibility
cp /tmp/$1_polities.txt /sectors/autogen/$1_alliances.txt
#sed '/# Alliance: /d' /tmp/$1_automsec.msec > /tmp/$1route1.txt
#sed '/border/d' /tmp/$1route1.txt > /sectors/autogen/$1_route.txt
cp /tmp/$1_automsec.msec /sectors/autogen/$1_route.txt
#cp /tmp/$1_automsec.sec /sectors/autogen/$1_automsec.sec


#Clean up all traces
#rm -rf /tmp/*$1*
#rm -rf /tmp/*.txt
#rm -rf /tmp/*anim*
#rm -rf /tmp/*cargo*
#rm -rf /tmp/*polity*

#echo "  .  $1 Sector debug - backups and cleanups complete @" $SECONDS "seconds.   "

# Provide statistics
#echo "  .  $1 containing" $NUM_WORLDS" worlds ("$2"%) took" $SECONDS "seconds to generate.   "

### And Serve (temporarily disabled till I fix the web server perms)

# CGI for presenting a pdf
echo "Content-Type: application/pdf" 
echo " Filename: "$1.pdf
echo "" 
cat < /tmp/$1.pdf


#Clean up all traces
rm -rf /tmp/*$1*
rm -rf /tmp/*.txt
rm -rf /tmp/*anim*
rm -rf /tmp/*cargo*
rm -rf /tmp/*polity*

