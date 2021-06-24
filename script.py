import queue


try:
    import sys
    import requests
    import threading
    from queue import Queue
    from time import sleep
    import random
    import uuid
    import secrets
except Exception as e:
    print(e)
    input("Enter To Exit")
    sys.exit()


instagram_email = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
snapchat_get = "https://accounts.snapchat.com/accounts/merlin/login#/enter-user-email"
snapchat_post = "https://accounts.snapchat.com/accounts/merlin/login"

try:
    with open("email.txt","r") as text:
        s = text.read().strip().splitlines()

    with open("proxies.txt","r") as pro:
        my_proxies = pro.read().strip().splitlines()

except Exception as e:
    print(f"{e}")
    input("Enter To exit")
    sys.exit()
class Email_reset():
    def __init__(self):
        self.q = Queue()
        self.req = requests.Session()
        self.lock = threading.Lock()
        self.error, self.counter, self.banned ,self.attempts = 0,0,0,0

        for i in s:
            self.q.put(i)
        print(""" 
            [+] 1 - for all ( twitter , instagram , snapchat )[+]
            [===================================================]
            [+] 2 - twitter email check [+]
            [===================================================]
            [+] 3 - Instagram email check [+]
            [===================================================]
            [+] 4 - Snapchat email check [+]

            Multpi Chice for Example: 2 3 or 4 3 like that :) 

            ./ Create by Hatim Alotebi 
                @31421.bye | hatim_arab

        """)
        self.choice =str(input("Enter Number Please:"))
        self.threads = int(input("[+] Enter Threads [+]:"))
        type_pro = int(input("[1] Http/Https ---- [2] socks4 ------ [3] socks5 [only number]:"))
        if type_pro == 1:
            for i in range(self.threads):
                threading.Thread(target=self.send,args=(self.proxies,)).start()
                sleep(0)
        elif type_pro == 2:

            for i in range(self.threads):
                threading.Thread(target=self.send,args=(self.proxies_socks4,)).start()
                sleep(0)
        else:
            for i in range(self.threads):
                threading.Thread(target=self.send,args=(self.proxies_socks5,)).start()
                sleep(0)

    def send(self,proxies):
        try:
            if "1" in self.choice:

                while 1:
                    try:
                        email = str(self.q.get(timeout=3))
                        print(f"Targeting:{email}")
                    except:
                        print("Empty Queue")
                        break
                    try:
                        self.instagram(email,proxies)
                    except Exception as e:
                        print(f"Error Instagram {e}")
                        self.error+=1
                        self.q.put(email)
                    try:
                        self.twitter(email,proxies)
                    except Exception as e:
                        print("Error Twitter:",e)
                        self.error+=1
                        self.q.put(email)

                    try:
                        self.snapchat(email,proxies)
                    except Exception as e:
                        print("Error Snapchat:",e)
                        self.error+=1 
                        self.q.put(email)

                    with self.lock:
                        print(f"Attempts:{self.attempts} | success:{self.counter} | error:{self.error}",end="\r",flush=True)
            else:

                while 1:
                    try:

                        email = str(self.q.get(timeout=3))
                        print(f"Targeting:{email}")
                    except:
                        break
                    if "3" in self.choice:

                        try:
                            self.instagram(email,proxies)
                        except Exception as e:
                            print(f"Error Instagram {e}")
                            self.error+=1
                            self.q.put(email)

                    if "2" in self.choice:

                        try:
                            self.twitter(email,proxies)
                        except Exception as e:
                            print("Error Twitter:",e)
                            self.error+=1
                    else:
                        try:
                            self.snapchat(email,proxies)
                        except Exception as e:
                            print("Error Snapchat:",e)
                            self.error+=1 
                            self.q.put(email)

                    print(f"success:{self.counter} | Attempts:{self.attempts} | error:{self.error}",end="\r",flush=True)
        except Exception as e:
            print(e)
    def proxies(self):
        pro = random.choice(my_proxies)
        return {"http":f"http://{pro}","https":f"https://{pro}"}
        
    def proxies_socks4(self):
        pro = random.choice(my_proxies)
        return {"http":f"socks4://{pro}","https":f"socks4://{pro}"}



    def proxies_socks5(self):
        pro = random.choice(my_proxies)
        return {"http":f"socks5://{pro}","https":f"socks5://{pro}"}
        
        

    def instagram(self,email,pro_func):
        data= {

            "email_or_username":email,
            "recaptcha_challenge_field":"",
            "flow":"",
            "app_id":"" 

        }
        head = {"method": "POST", "X-CSRFToken":"missing",
        "Referer": "https://www.instagram.com/accounts/account_recovery_send_ajax/",
        "X-Requested-With":"XMLHttpRequest",
        "path":"/accounts/account_recovery_send_ajax/",
        "accept": "*/*", "ContentType": "application/x-www-form-urlencoded",
        "mid":secrets.token_hex(8)*2,"csrftoken":"missing","rur":"FTW","user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"}
        try:

            c = self.req.post(instagram_email,headers=head,data=data,proxies=pro_func(),timeout=5)
        except Exception as e:
            if ("timeout") in str(e):
                self.instagram(email=email,pro_func=pro_func)
        else:
                
            if 200 == c.status_code:
                with open("Instagram.txt","a") as wr:
                    wr.write(email+"\n")
                
                with open("social_media.txt","a") as wr:
                    wr.write("instagram:"+email+"\n")
                self.counter+=1
                print(f"[+] LINKED : {email}  | PLATFORM:INSTAGRAM")
            elif c.status_code == 429:
                self.q.put(email)
                self.banned+=1


    def twitter(self,em,pro_func):
        try:
                
            email = em.split("@")
            url = f"https://api.twitter.com/i/users/email_available.json?email={email[0]}%40{email[1]}"
        except:
            print("BAD EMAIL FORMATING")
        try:

            r = self.req.get(url,headers={"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"},proxies=pro_func(),timeout=5)
        except Exception as e:
            if ("timeout") in str(e):
                self.twitter(em=em,pro_func=pro_func)
            print("error:",str(e))
        else:
                
            if ('{"valid":false,"msg":"Email has already been taken.","taken":true}') in r.text:
                with open("twitter.txt","a") as wr:
                    wr.write(em+"\n")
                
                with open("social_media.txt","a") as wr:
                    wr.write("twitter:"+em+"\n")
                self.counter+=1
                print(f"[+] LINKED : {em}  | PLATFORM:TWITTER")

            elif r.status_code == 429:
                self.q.put(em)
                self.banned+=1

            elif not ('{"valid":true,"msg":"Available!","taken":false}') in r.text:
                with open('logs_error',"a") as wr:
                    wr.write("Logs of email:"+em+"\n message:"+r.text+"\n")
                self.error+=1

    def snapchat(self,email,pro_func):
        data = {"email":email,"app":"BITMOJI_APP"}
        head = {
             "method":"GET",
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
            "path":"/accounts/merlin/login",
            "scheme":"https",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer":"https://accounts.snapchat.com/accounts/merlin/login",
            "Origin":"https://accounts.snapchat.com"

            }
        try:
                
            get_cookies = self.req.get(snapchat_get,headers=head,proxies=pro_func(),timeout=5)
            
            cookie = {
                "xsrf_token":get_cookies.cookies["xsrf_token"],
                "web_client_id":get_cookies.cookies["web_client_id"],

            }
            heads = {
                "method":"POST",
                "x-xsrf-token":get_cookies.cookies["xsrf_token"],
                "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0",
                "path":"/accounts/merlin/login",
                "scheme":"https",
                "Accept":"application/json, text/plain, */*",
                "Referer":"https://accounts.snapchat.com/accounts/merlin/login",
                "Origin":"https://accounts.snapchat.com"
                }
        except:
            self.snapchat(email,pro_func)
        try:

            req = self.req.post(snapchat_post,json=data,headers=heads,cookies=cookie,proxies=pro_func(),timeout=5)
        except Exception as e:
            if ("timeout") in str(e):
                self.snapchat(email=email,pro_func=pro_func)
            else:
                raise Exception(f"{str(e)}")
        else:
                
            if 200 == req.status_code:
                with open("snapchat.txt","a") as wr:
                    wr.write(email+"\n")
                print(f"[+] LINKED : {email}  | PLATFORM:SNAPCHAT")

                with open("social_media.txt","a") as wr:
                    wr.write("snapchat:"+email+"\n")
                self.counter+=1
            elif req.status_code == 429:
                self.q.put(email)
                self.banned+=1
    
Email_reset()


