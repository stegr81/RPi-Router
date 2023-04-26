import requests,re
def login():
        r=requests.get('https://somewifi.com/login/')
        # If the service uses CSRF authentication tokens, I find this using regex. It's unique and one time use.
        p=re.compile(r'("csrfmiddlewaretoken".value="([^"]*))') 
        csrfmiddlewaretoken=p.search(r.text)[2]
        url='https://somewifi.com/login/'
        payload={
                'csrfmiddlewaretoken':csrfmiddlewaretoken,
                'next':'/',
                'username':'xxxxxxxx',
                'password':'xxxxxxxx',
                }
        requests.post(url,data=payload)
login()