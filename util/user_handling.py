# We used this script to delete 450 users that had registered before we
# disallowed registering through the web form


import os
import json
import requests
from dotenv import load_dotenv

CKAN_API_URL="https://ckan.madiphs.org/api/3/action"

# This is needed to load any ENV settings from a .env (dotenv) file
# on your path
load_dotenv()
api_key=os.getenv("CKAN_API_KEY")

def get_user_list():
    with open("tmp/user_list.json") as user_list_file:
        return json.load(user_list_file)
    
def delete_users(id_list:list):
    for id in id_list:
        r = requests.post(
            f"{CKAN_API_URL}/user_delete",
            data={"id":id},
            headers={'Authorization':api_key}
        )
        if r.status_code == 200:
            print("Successfully deleted user with id=%s" % id)
        else:
            print("Error: %s" % r.text)
            exit(0)

def create_user(
        name:str,
        email:str,
        fullname:str,
        password:str
):
    r=requests.post(
        f"{CKAN_API_URL}/user_create",
            data={
                "name": name,
                "email": email,
                "fullname": fullname,
                "password": password
            },
            headers={'Authorization':api_key}
    )
    if r.status_code == 200:
        print("Successfully created user %s" % name)
    else:
        print("Error: %s" % r.text)
    
user_list = get_user_list()
print("Number of users: %s" % len(user_list["result"]))
user_ids_to_delete=[]
for user in user_list["result"]:
    if user["number_created_packages"] == 0 and user["id"] not in ["55b8de6e-279b-4e90-9f37-6b8cde68e4be:"]:
        user_ids_to_delete.append(user["id"])

#delete_users(user_ids_to_delete)

#create_user("foobar","foo@bar.com","ACME Foobar","123PassXXX")


    

