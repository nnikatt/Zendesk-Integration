from urllib import response
import requests


def fetch_api(url,method,payload={},params={}):
    headers = {
    "Accept": "application/json",
    "content-type": "application/json"
    }
    auth = ("api_keys","api_keys")

    if method in ['POST','PUT']:
        response = requests.request(method=method,url=url,headers=headers,json=payload,auth=auth).json()
    else:
        response = requests.request(method=method,url=url,headers=headers,params=params,auth=auth).json()

    return response

#This function would check if the phone number retrieved from Dubber exists in Zendesk
def check_phone_number(phone):
    phone = phone.get('phone')
    create_user = True
    params = {
    'query': phone,
    }
    search_url = 'https://d3v-(yourinstance).zendesk.com/api/v2/users/search'
    response = fetch_api(search_url,'GET',params=params)

    if len(response['users']) > 0:
        for item in response['users']:
            name = item['name']
            email = item['email']
            if item['phone'] == phone:
                print('User already exist \n')
                create_user = False
                break

    if create_user:
        print(f'New contact with phone number: {phone} created \n')
        url = "https://d3v-(yourinstance).zendesk.com/api/v2/users"
        payload = {"user": {
            "phone":phone,
        }}
        fetch_api(url,"POST",payload=payload)      

    end_customer = {"name":name,"email":email}
    return end_customer
    
def generate_ticket(requester='test user',subject='Help my problem',comment='my print is not working'):
    end_customer = check_phone_number(requester)
    user_name =end_customer.get('name')
    ticket_url = "https://d3v-(yourinstance).zendesk.com/api/v2/requests"
    subject = f"Auto generated ticket by Dubber for customer: {user_name}"
    payload = {"request": {
        "requester": end_customer,
        "subject":subject,
        "assignee_id":903996268726,
        "comment": {"body": comment}
    }}
    
    ticket = fetch_api(ticket_url,"POST",payload=payload)

    assigne_payload = {"ticket":{
        "assignee_id":903996268726
    }}

    url = f"https://d3v-(yourinstance).zendesk.com/api/v2/tickets/{ticket['request']['id']}.json"

    response = fetch_api(url,"PUT",payload=assigne_payload)

    return response


print(generate_ticket(requester={'phone':"04501234"}))