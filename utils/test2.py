import requests
import json
from os.path import expanduser
from requests.auth import HTTPBasicAuth

username = "wanghanlin917@gmail.com"
password = "19970917wjwhl"
sess = requests.Session()
sess.auth = HTTPBasicAuth(username, password)
response = sess.post("https://api.worldquantbrain.com/authentication")
# print(response.status_code)
# print(response.json())
# simulation_data = {
#     'type': 'REGULAR',
#     'settings': {
#         'instrumentType': 'EQUITY',
#         'region': 'USA',
#         'universe': 'TOP3000',
#         'delay': 1,
#         'decay': 5,
#         'neutralization': 'SUBINDUSTRY',
#         'truncation': 0.08,
#         'unitHandling': 'VERIFY',
#         'nanHandling': 'ON',
#         'language': 'FASTEXPR',
#         'pasteurization': 'ON',
#         'visualization': 'false'
#     },
#     'regular': 'liabilities/assets'  # 表达式
# }
simulation_data = {"type": "REGULAR",
                   "settings": {"nanHandling": "ON", "instrumentType": "EQUITY", "delay": 1, "universe": "TOP3000",
                                "truncation": 0.08, "unitHandling": "VERIFY", "testPeriod": "P0D",
                                "pasteurization": "ON", "region": "USA", "language": "FASTEXPR", "decay": 0,
                                "neutralization": "None", "visualization": False},
                   "regular": "liabilities/assets"}
from time import sleep

# https://api.worldquantbrain.com/simulations
sim_resp = sess.post("https://api.worldquantbrain.com/simulations", json=simulation_data)
print("dddd", sim_resp.headers)
sim_progress_url = sim_resp.headers['Location']
while True:
    sim_progress_resp = sess.get(sim_progress_url)
    retry_after_sec = float(sim_progress_resp.headers.get('Retry-After', 0))
    if retry_after_sec == 0:
        break
    sleep(retry_after_sec)

alpha_id = sim_progress_resp.json()
print(alpha_id)
