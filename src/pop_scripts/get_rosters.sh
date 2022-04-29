mysql -BN -e "select id from team" | \
	awk '{print "python get_team_roster.py",$1}' 
