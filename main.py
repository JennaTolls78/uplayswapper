import requests, random, time, os, json, base64, threading
from colorama import Fore, init, Style
from requests_ip_rotator import ApiGateway
init()

lock = threading.Lock()

#random variables
r = requests.session()
r.put("https://public-ubiservices.ubi.com/v1/profiles/")

#login url
login_url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"

#big colors :D
print(f"""{Style.BRIGHT}{Fore.RED}                                                                    
                                                                    
    ___                   ___      ___      ___      ___      __    
  ((   ) ) //  / /  / / //   ) ) //   ) ) //   ) ) //___) ) //  ) ) 
   \ \    //  / /  / / //   / / //___/ / //___/ / //       //       
//   ) ) ((__( (__/ / ((___( ( //       //       ((____   //        
\n\n{Fore.RESET}""")

##AWS
##Only uncomment these 3 lines if u REALLY need to avoid getting rate limited
##And you can't turn a vpn on/off for some reason. Note you need an AWS account and key
##p.s U can also use this to avoid getting rate limited on a turbo glhf
#gateway = ApiGateway("https://public-ubiservices.ubi.com", access_key_id = '', access_key_secret = '')
#gateway.start()
#r.mount("https://public-ubiservices.ubi.com", gateway)

#getting the logins to the accounts and config
with open('./config.json') as f:
    config = json.load(f)

name_email = config.get('name_email')
name_password = config.get('name_password')

swap_email = config.get('swap_email')
swap_password = config.get('swap_password')
swap_method = config.get('method')
#backup claim
def backup_create(name):
    claim_headers = {
        'Ubi-AppId':'2c2d31af-4ee4-4049-85dc-00dc74aef88f',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Ubi-RequestedPlatformType':'uplay'
        }

    random_int = random.randint(100,999999)

    email = f""
    password = f"{name}A{random_int}!?"
    claim_payload = {
        "email":email,
        "confirmedEmail":email,
        "firstName":"bob",
        "lastName":"loblaw",
        "nameOnPlatform":name,
        "legalOptinsKey":"eyJ2dG91IjoiNC4wIiwidnBwIjoiNC4wIiwidnRvcyI6IjIuMSIsImx0b3UiOiJlbi1VUyIsImxwcCI6ImVuLVVTIiwibHRvcyI6ImVuLVVTIn0",
        "isDateOfBirthApprox":False,
        "age":"",
        "dateOfBirth":"2000-06-21T00:00:00.00000Z",
        "password":f"{name}{random_int}!?",
        "country":"US",
        "preferredLanguage":"en"
        }

    backup_result = r.post("https://public-ubiservices.ubi.com/v3/users", headers=claim_headers, json=claim_payload)

    if backup_result.status_code == 200:
        print(f"\nBackup: {email}:{password}")
    else:
        print(f"\nBackup: Backup Claim Failed")

#logging in to account with name
name_account = name_email + ':' + name_password
name_user = ((name_account).encode('ascii'))
name_auth = (base64.b64encode(name_user)).decode('ascii')

name_headers = {
    'Authorization': 'Basic ' + name_auth,
    'Ubi-AppId': '2c2d31af-4ee4-4049-85dc-00dc74aef88f',
    'Ubi-RequestedPlatformType': 'uplay',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Referer': 'https://connect.ubisoft.com/'
    }

name_payload = {
    'rememberMe': 'false'
    }

name_r = r.post(login_url, headers=name_headers, json=name_payload)

if name_r.status_code == 200:
    name_res = name_r.json()

    name_name = name_res['nameOnPlatform']
    name_auth_token = name_res['ticket']
    name_userid = name_res['userId']
    name_sessionid = name_res['sessionId']
    print(f"Target: {Fore.GREEN}{name_name}{Fore.RESET}")

elif name_r.status_code == 401:

    print(f"Target: {Fore.RED}Invalid Login{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

elif name_r.status_code == 409:

    print(f"Target: {Fore.RED}Recieved Captcha{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

elif name_r.status_code == 429:

    print(f"Target: {Fore.RED}Rate Limited From Logins{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

else:

    print(f"Target: {Fore.RED}Unkown Error, Check Config{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

#login to account we want name on
swap_account = swap_email + ':' + swap_password
swap_user = ((swap_account).encode('ascii'))
swap_auth = (base64.b64encode(swap_user)).decode('ascii')

swap_headers = {
    'Authorization': 'Basic ' + swap_auth,
    'Ubi-AppId': '2c2d31af-4ee4-4049-85dc-00dc74aef88f',
    'Ubi-RequestedPlatformType': 'uplay',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Referer': 'https://connect.ubisoft.com/'
    }

swap_payload = {
    'rememberMe': 'false'
    }

swap_r = r.post(login_url, headers=swap_headers, json=swap_payload)

if swap_r.status_code == 200:
    swap_res = swap_r.json()

    swap_name = swap_res['nameOnPlatform']
    swap_auth_token = swap_res['ticket']
    swap_userid = swap_res['userId']
    swap_sessionid = swap_res['sessionId']
    print(f"Fresh: {Fore.GREEN}{swap_name}{Fore.RESET}")

elif swap_r.status_code == 401:

    print(f"Fresh: {Fore.RED}Invalid Login{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

elif swap_r.status_code == 409:

    print(f"Fresh: {Fore.RED}Recieved Captcha{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

elif swap_r.status_code == 429:

    print(f"Fresh: {Fore.RED}Rate Limited From Logins{Fore.RESET}")
    time.sleep(5)
    os._exit(0)

else:

    print(f"Fresh: {Fore.RED}Unkown Error, Check Config{Fore.RESET}")
    time.sleep(5)
    os._exit(0)


print(f"\nHow do you want caps: ", end="")
name_name = input()

print(f"Change {name_name} to: ", end="")
release_name = input()

#confirming the swap
print(f"Press enter to swap {name_name} onto {swap_name}\n", end="")
input()

#defining headers
name_headers = {
    'Ubi-AppId':'c7f6bc1a-5464-4469-abf5-7bbb3126b5e2',
    'Authorization':"Ubi_v1 t=" + name_auth_token,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'ubi-sessionid':name_sessionid
    }

name_payload = {'nameOnPlatform': release_name}

swap_headers = {
    'Ubi-AppId':'c7f6bc1a-5464-4469-abf5-7bbb3126b5e2',
    'Authorization':"Ubi_v1 t=" + swap_auth_token,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'ubi-sessionid':swap_sessionid
    }

swap_payload = {"nameOnPlatform":name_name}

#defining urls
name_url = f"https://public-ubiservices.ubi.com/v1/profiles/{name_userid}"
swap_url = f"https://public-ubiservices.ubi.com/v1/profiles/{swap_userid}"

#auto swap
if swap_method == 'main':
    success = 0

    def release():
        name_result = r.put(name_url, headers=name_headers, json=name_payload)
        if name_result.status_code == 200:
            with lock: print(f"Released {name_name}")
        elif name_result.status_code == 429:
            with lock: print("Error Releasing: Rate Limited")
        elif name_result.status_code == 403:
            with lock: print("Error Releasing: No Name Change")
        elif name_result.status_code == 400:
            with lock: print("Error Releasing: Not Available or Vulgar")
        else:
            with lock: print(f"Error Releasing: Unkown Code: {name_result.status_code}")

    def claim():
        global success
        swap_result = r.put(swap_url, headers=swap_headers, json=swap_payload)
        if swap_result.status_code == 200:
            if success == 0:
                success = success + 1
                with lock: print(f"Successfully swapped {Fore.GREEN}{name_name}{Fore.RESET}")
        elif swap_result.status_code == 429:
            with lock: print(f"Error Swapping: {Fore.RED}Rate Limited{Fore.RESET}")
        elif swap_result.status_code == 403:
            with lock: print(f"Error Swapping: {Fore.RED}No Name Change{Fore.RESET}")
        elif swap_result.status_code == 400:
            with lock: print(f"Error Swapping: {Fore.RED}Not Available or Vulgar{Fore.RESET}")
        else:
            with lock: print(f"Error Swapping: {Fore.RED}Unkown{Fore.RESET}")
        
#threads
    threading.Thread(target=release).start()
    threading.Timer(0.0001, claim).start()
    threading.Timer(0.001, claim).start()
    threading.Timer(0.1, claim).start()
    threading.Timer(0.2, claim).start()
    threading.Timer(0.4, claim).start()
    time.sleep(.7)
    if success == 0:
        backup_create(name_name)
    

#closing program
input() 

##[Hook 1: Baba Stilz]
"""I don't feel no pain
I don't care cause I don't feel no pain
I don't really care
I don't feel no pain
I don't care cause I don't feel no pain

[Verse: Yung Lean]
Hate, love, driving foreign
Drop top, rockin' Ralph Lauren
Had to upgrade, we love soup pourin'
Milk and cereal like every mornin'
No lies in my mouth, I don't speak corny
Stockholm ridin' for lean, don't we?
Tell your friends that I'm dead, homie
No soul, no life, just blood on me
Keep my boys around, all you others bore me
Don't talk to no one, don't steal my glory
Fuck, fuck my glory, the whole world ignores me
And I'm stuck in my room till that snorts it
G-shock, G-shock round my wrist, wearing Gucci boots
Looking at myself like "why you wearin' that stupid human suit?"
I relive for recruit, I survive and I shoot
Magic powers, I use, you hate me, I assume
Don't give a fucks about you, being myself's kind of cool
Alien Face on the news, Lean's always on the move
I can't handle no booze, livin' my dreams, I need you
If you talk that's on you, I brought Sweden back on the moon
[Hook 2: Baba Stilz]
[?]
Life is so worthless
Heavy [?]
Feeling so worthless
I don't feel ok
I don't care cause I don't feel no pain
I don't really care
I don't feel no pain
I don't care cause I don't feel no pain"""