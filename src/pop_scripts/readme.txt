#####
USE FLASK CLI COMMANDS NOW:

flask populate
#####


#!/bin/bash

cat clean_db.sql | mysql draftdodger

python get_conferences.py
python get_divisions.py
python get_teams.py

mysql -BN -e "select id from team" | \
	awk '{print "python get_team_roster.py",$1}'

mysql -BN -e "select id from team" | \
	awk '{print "python get_roster_stats.py",$1}'

