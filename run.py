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
				#POST comment to pull request using pull request number
				print(repo.get_pull(pull_request.number).create_issue_comment("Hello from a program for a pull request"))
				break
				#DELETE comment using it's ID
				#print(pull_request.get_issue_comment(482981943).delete())
				#PUT (EDIT) a pull request comment
				print(pull_request.get_issue_comment(482736272).edit("Here we go again from program"))
				#print(type(pull_request.get_issue_comment(482981943)))
				break
				print(type(pull_request))
				print("Pull Request: ",pull_request.title)
				print("Pull Request Comment: ",pull_request.body)
				ID = pull_request.number
				print(pull_request.html_url)
				print("User: ",pull_request.user)
				print("User: ",pull_request.user.login)
				print("Number: ",ID)
				pull = repo.get_pull(ID)
				print(pull)
				print("Date: ",repo.get_pull(ID).created_at)
				#pull.create_comment("Hello from a program")
				for comments in pull_request.get_issue_comments():
					print("Comment: ",comments.body)
					print(type(comments))
					print("Commentor_name", comments.user.login)
					print("Timestamp ",comments.created_at)
					#Comment ID
					print("ID",comments.id)
					
				#print(pull_request)
				print(type(pull_request))
				break
		
username = ("kmn5409")
password = getpass()
g = Github(username,password)
#g = Github()
print(Github)
print(g)
#g = Github('c5c1fb044b46cde5a102ae0f507309e01f68d593')
'''
try:
	print(g.get_user().login)
except:
	print(None)

print(g)
print(g.get_user().login)
'''
'''
print(g.get_user())
print(g.get_user().created_at)
print(g.get_user().get_key)
print(g.get_user().create_key('key'))
print(g.get_user().get_keys())
#print(g.get_user().get_key().key)
id1 = g.get_user().id
print(id1)
#print(g.get_user().ge))
commits = 0
#postCommit(g)
'''
#print(g.get_user().login)
#print(g.RateLimit().rate.remaining)
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

