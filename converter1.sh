#!/bin/sh
#clear
#Convert DAT files to usable format

cut -b1-14 /tmp/$1.sec > /tmp/$1_names1

#remove trailing spaces in names
sed 's/[ \t]*$//' /tmp/$1_names1 > /tmp/$1_names2

#convert spaces to underscores
sed 's/ /_/g' /tmp/$1_names2 > /tmp/$1_names3

#return names to proper width
sed -e :a -e 's/^.\{1,14\}$/& /;ta' /tmp/$1_names3 > /tmp/$1_names

cut -b15-18 /tmp/$1.sec > /tmp/$1_ID
cut -b19-19 /tmp/$1.sec > /tmp/$1_space
cut -b20-29 /tmp/$1.sec > /tmp/$1_Upp
cut -b31-32 /tmp/$1.sec > /tmp/$1_Base
cut -b33-46 /tmp/$1.sec > /tmp/$1_Trade
cut -b52-57 /tmp/$1.sec > /tmp/$1_PBG
cut -b49-49 /tmp/$1.sec > /tmp/$1_Zone
cut -b52-58 /tmp/$1.sec > /tmp/$1_End
paste -d '\0' /tmp/$1_names /tmp/$1_space /tmp/$1_space /tmp/$1_space /tmp/$1_space /tmp/$1_ID /tmp/$1_space /tmp/$1_Upp /tmp/$1_Base /tmp/$1_Trade /tmp/$1_space /tmp/$1_space /tmp/$1_PBG /tmp/$1_space /tmp/$1_Zone > /tmp/$1paste.sec
open /tmp/$1paste.sec 

#
#FarFrontiers
#
#cut -b61-61 FarFrontiersINTER.sec > FarFrontiers_space
#cut -b1-48 FarFrontiersINTER.sec > FarFrontiers_front
#cut -b74-75 FarFrontiersINTER.sec > FarFrontiers_tas
#cut -b76-81 FarFrontiersINTER.sec > FarFrontiers_back
#
#paste -d '\0' FarFrontiers_front FarFrontiers_tas FarFrontiers_space FarFrontiers_back > FarFrontiers_new
#