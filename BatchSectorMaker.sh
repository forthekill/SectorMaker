#!/bin/sh

function worldroller() 
{
     while read LINE
    do
SYSTEMS=$(( $RANDOM % 25 + 22 ))
#echo $SYSTEMS
./SectorMaker.sh $LINE $SYSTEMS $2 $3 $4
wait
    done < /tmp/$1
    }


#Create Sector Names

#run the name generator
echo " "
perl /Library/WebServer/CGI-Executables/trav/lc -$1 /Library/WebServer/CGI-Executables/trav/namesmaster.txt > /tmp/sectornamesA
sed 's/$/_Sector/g' /tmp/sectornamesA > /tmp/sectornamesB
sed 's/ _Sector/_Sector/g' /tmp/sectornamesB > /tmp/sectornames
worldroller sectornames $2 $3 $4

#echo "  o . . . . . . . . . . . . . . . . . . . . . . . . ."
echo " "
#echo "  o . . . . . . . . . . . . . . . . . . . . . . . . ."
#echo "  ."
echo "  .  Master sector generation process complete. "
echo "  .  Generation of "$1" sectors took" $SECONDS "seconds."
#echo "  ."
#echo "  o . . . . . . . . . . . . . . . . . . . . . . . . ."
echo " "


