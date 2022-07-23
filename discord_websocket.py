from websocket import WebSocket
from json import dumps, loads
from threading import Thread
from time import sleep
from re import match
from httpx import Client


phone = "0"
token = ""
class sockets(WebSocket):
    def __init__(self, tokens):
        super().__init__()
        self.tokens = tokens

    def send_hb(self, heartbeat_interval : float):
        while True:
            sleep(heartbeat_interval)
            self.send(dumps({"op":1,"d":None}))

    def on_message(self):
        with Client() as client:
            self.connect("wss://gateway.discord.gg/?encoding=json&v=9&compress=json")
            heartbeat_interval = loads(self.recv())['d']['heartbeat_interval'] / 1000
            self.send(dumps({"op":2,"d":{"token": self.tokens,"capabilities": 253,"properties":{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-US","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.113 Safari/537.36","browser_version":"96.0.4664.113","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":109190,"client_event_source":None},"compress":False}}))
            Thread(target=gateway.send_hb,args=(heartbeat_interval,)).start()
            while True:
                data = loads(self.recv())
                if (data['t'] == 'MESSAGE_CREATE'): 
                    message = data['d']['content']
                    if match(
                        r"https:\/\/gift\.truemoney\.com\/campaign\/\?v=+[a-zA-Z0-9]{18}", message
                    ):  
                        print("FOUND VOUCHER")
                        code = message.split("?v=")[1]
                        response = client.post(f"https://gift.truemoney.com/campaign/{code}",json={"mobile": phone, "voucher_hash": code}, headers={"Accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36","Content-Type": "application/json","Origin": "https://gift.truemoney.com","Accept-Language": "en-US,en;q=0.9","Connection": "keep-alive"})
                        if (
                            response.status_code == 200
                            and response.json()["status"]["code"] == "SUCCESS"
                        ):
                            Amount_receive = float(response.json()["data"]["my_ticket"]["amount_baht"])
                            print(f"RECEIVED {Amount_receive}B")

                    else:

                        print(message)

gateway = sockets(token)
Thread(target=gateway.on_message).start()
