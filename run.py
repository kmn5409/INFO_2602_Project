from github import Github



def getCommit(g):
	for repo in g.get_user("kmn5409").get_repos():
		if(repo.name == "Test"):
			#print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").message)
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96"))
			print(type(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").parents))
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").sha)
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").author)
			print(type(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96")))
			repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").create_comment(body="Hello World from program",line=4,path="test.py",position=0)
		

g = Github("c5c1fb044b46cde5a102ae0f507309e01f68d593")
commits = 0
getCommit(g)


'''
for repo in g.get_user("chaoss").get_repos():
	#print(repo.name," ",repo.get_commits())
	print(repo.name)
	if(repo.name == "whitepaper"):
		for i in repo.get_commits():
			print("Message: ",i.commit.message[:])
			print(i.commit.committer.date)
			print(i.commit.author.name)
			commits+=1
print("Commits: ",commits)
'''
