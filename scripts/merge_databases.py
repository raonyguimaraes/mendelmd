import json

# unify 3 models
# "model": "auth.user",
# "model": "account.emailaddress",
# "model": "account.emailconfirmation",

auth_user = []
usernames = []
emails = []
duplicated_emails = []
duplicated_usernames = []
empty_usernames = []
email_username = []

db1 = json.load(open('../fixtures/mendelmdorg/fixtures/users.json'))
db2 = json.load(open('../fixtures/ufmg/fixtures/users.json'))

# print(db1[0].keys())
# print(len(db1))
# print(len(db2))

users = {}

n_auth = 0

dbs = [db1,db2]
for db in dbs:
	# n_auth +=1
	# n_emailaddress +=1
	# n_emailconfirmation +=1
	for item in db:
		#print(item['model'])#, item['fields'], item, 
		if item['model'] == 'auth.user':
			# n_auth += 1
			# print(item)
			email = item['fields']['email']
			username = item['fields']['username']

			#this ignores the user the it's already found in the previous model
			if (username not in usernames) and (email not in emails):
				users[username] = {}
				# users[username]['auth'] = item
				users[username]['model'] = item

			emails.append(email)	
			usernames.append(username)
		# elif item['model'] == 'account.emailaddress':

		# 	email = item['fields']['email']
		# 	username = item['fields']['user'][0]
		# 	users[username]['emailaddress'] = item

		# elif item['model'] == 'account.emailconfirmation':

print(len(users))

# users_output = open('../fixtures/merged_users.json', 'w')
# users_output.writelines('[\n')
user_list = []
emailaddress_list = []
emailaddress_count = 1

for user in users:
	user_list.append(users[user]['model'])
	email = users[user]['model']["fields"]['email']
	username = users[user]['model']["fields"]['username']
	if email != '':
		#
		email_object = {
		    "pk": emailaddress_count,
		    "model": "account.emailaddress",
		    "fields": {
		        "primary": True,
		        "email": "{}".format(email),
		        "user": [
		            "{}".format(username)
		        ],
		        "verified": True
		    }
		}
		user_list.append(email_object)
		emailaddress_count+=1


obj = open('../fixtures/merged_users.json', 'w')
json.dump(user_list, obj, indent=4)
# json.dump(emailaddress_list, obj, indent=4)
obj.close


# output = open('merged_import.json')
#this needs to be a list

# for key in users:
# 	print(key,users[key])
	# print()

			# t = email,username
			# if t not in email_username:
			# 	email_username.append(t)
			# if email != '':
			# 	if email not in emails:
			# 		emails.append(email)
			# 	else:
			# 		duplicated_emails.append(email)
			# if username != '':
			# 	if username not in usernames:
			# 		usernames.append(username)
			# 	else:
			# 		duplicated_usernames.append(username)
			# else:
			# 	empty_usernames.append(item)

			# if username in dup_usernames:
			# 	print(item)

# print()
# for item in email_username:
# 	print(item)
# print(emails)
# print(len(emails))
# print(len(duplicated_emails))
# print(duplicated_emails)

# print(usernames)
# print(len(usernames))
# print(len(duplicated_usernames))
# print(duplicated_usernames)

# print(empty_usernames)

# # for item in db2:
# # 	print(item['model'])#, item['fields'], item, 