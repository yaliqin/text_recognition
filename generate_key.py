import requests
import json




def gen_key(app_id, api_key):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    params = {"grant_type":"client_credentials","client_id":app_id,"client_secret":api_key}
    r=requests.post(host,data=params)
    if r.status_code == 200: #Get the right response
        content= json.loads(r.content)
        secret_key = content["access_token"]
        return secret_key
