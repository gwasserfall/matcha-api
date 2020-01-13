l = ["asd", "ass", "asdd", "ddasd", "adfsa"]

def matches(val):
	if "as" in val:
		return True
	return False

print(list(filter(matches, l)))

"""
select
    match.id
    IFNULL((select 1
        from matches 
			where matchee_id = my.id
        and matcher_id = match.id), 0)
        as matched
	from matches
	right join users my on matches.matcher_id = my.id
	right join users match on matches.matchee_id = match.id
	where my.id=4;
"""