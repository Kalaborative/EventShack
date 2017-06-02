def grabber(query):
	addwords = ["add", "new", "put", "insert", "on", "give"]
	removewords = ["remove", "subtract", "take", "off", "delete"]
	quantitywords = ["much", "many", "number"]
	orgs = ["alice", "dylan symm", "natsu", "destyn", "esm", "smol bunny", "rope bunny", "panda", "helix", "nitro", "bailey", "fumucat"]
	addattempt = False
	removeattempt = False
	orgattempt = False
	quantattempt = False
	orgid = []
	queryL = query.lower()
	words = queryL.split()
	for w in words:
		if len(w) <= 2:
			words.remove(w)
		elif len(w) == 3 and w == "the":
			words.remove(w)
	for word in words:
		if word in addwords and word in removewords:
			return "You have requested a confusing action. You can only add or remove."
		elif word in addwords:
			addattempt = True
		elif word in removewords:
			removeattempt = True
		elif word in quantitywords:
			quantattempt = True
		else:
			for o in orgs:
				if word in o:
					orgattempt = True
					orgid.append(o)
	if addattempt and not orgattempt:
		return ["It looks like you're trying to add a strike, but I cannot identify that organizer."]
	elif addattempt and orgattempt and len(orgid) == 1:
		return ["It looks like you want to add a strike to %s. Is this correct?" % orgid[0].capitalize(), orgid[0]]
	elif addattempt and orgattempt and len(orgid) > 1:
		return ["It looks like you want to add a strike to more than one person. Is this correct?", [o for o in orgid]]
	elif removeattempt and not orgattempt:
		return ["It looks like you're trying to remove a strike, but I cannot identify that organizer."]
	elif removeattempt and orgattempt and len(orgid) == 1:
		return ["It looks like you want to remove a strike from %s. Is this correct?" % orgid[0].capitalize(), orgid[0]]
	elif removeattempt and orgattempt and len(orgid) > 1:
		return ["It looks like you want to remove a strike to more than one person. Is this correct?", [o for o in orgid]]
	elif orgattempt and not addattempt and not removeattempt and not quantattempt:
		return ["It looks like you're trying to edit info for %s but the action could not be understood." % orgid[0].capitalize()]
	elif quantattempt and not orgattempt:
		return ["It looks like you're trying to see how many strikes someone has, but I cannot identify that organizer."]
	elif quantattempt and orgattempt:
		return ["It looks like you want to see how many strikes %s has. Is this correct?" % orgid[0].capitalize(), orgid[0]]
	else:
		return ["I could not understand you."]
