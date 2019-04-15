from github import Github
from getpass import getpass



def postCommit(g):
	for repo in g.get_user("kmn5409").get_repos():
		if(repo.name == "Test"):
			#print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").message)
			#GET
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96"))
			print(type(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").parents))
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").sha)
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").author)
			#POST
			'''print(type(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96")))
			repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").create_comment('Hello from a program!')'''
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").get_comments()[2])
			print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").get_comments()[2].body)
			#DELETE
			#print(repo.get_commit("856870f91562680d0a097a037df15290cdb49b96").get_comments()[4].delete())	


def postPullRequest(g):
	for repo in g.get_user("kmn5409").get_repos():
		if(repo.name == "Test"):
			for pull_request in repo.get_pulls():
				print(type(pull_request))
				print("Pull Request: ",pull_request.title)
				print("Pull Request Comment: ",pull_request.body)
				ID = pull_request.number
				print(pull_request.html_url)
				print(ID)
				pull = repo.get_pull(ID)
				print(pull)
				print("Date: ",repo.get_pull(ID).created_at)
				#pull.create_comment("Hello from a program")
				for comments in pull_request.get_issue_comments():
					print("Comment: ",comments.body)
				#print(pull_request)
		
username = ("kmn5409")
password = getpass()
g = Github(username,password)
#g = Github('c5c1fb044b46cde5a102ae0f507309e01f68d593')
commits = 0
#postCommit(g)
postPullRequest(g)

#c5c1fb044b46cde5a102ae0f507309e01f68d593

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

'''
Potentially a manager for someone's repository
POST reminders about what things they need to do

Utilization of session within the developed API, what does this mean?
'''

