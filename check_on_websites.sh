#!/bin/bash
# Add a cd to path where the script is if calling this with cron:
# cd ""
export DISPLAY=":0"
arr=( "https://perso.telecom-paristech.fr/rvogel/")
site_no=0
for site in ${arr[@]}
do
    # Do the new screenshot and put them in monitor_${site_no}
    dirname="monitor_"${site_no}"/"
    if ! [[ -d $dirname ]]
    then
	echo "Making the "${dirname}" directory."
	mkdir ${dirname}
    fi

    if [ ! "$(ls -A ${dirname})" ];
    then
	echo "No version before."
	name_old="$(ls -A ${dirname})"
	/usr/local/bin/webscreenshot -o "monitor_"${site_no} ${site}
	name_new="$(ls -A ${dirname})"
	mv ${dirname}${name_new} ${dirname}"new.png"
    else
	echo "Comparing two versions."
	name_old="$(ls -A ${dirname})"
	mv ${dirname}${name_old} "old.png"
	/usr/local/bin/webscreenshot -o "monitor_"${site_no} ${site} 
	name_new="$(ls -A ${dirname})"
	mv ${dirname}${name_new} ${dirname}"new.png"
	mv "old.png" ${dirname}"old.png"
	echo "python check-diff-image-and-email.py "${site_no} ${site}
	python3 check-diff-image-and-email.py ${site_no} ${site}
        rm ${dirname}"old.png"
    fi
    site_no=$((site_no + 1))
    date > "log.txt"
done
