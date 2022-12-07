import json
import numpy as np
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from pip._vendor import requests


def get_ip(host):
    url = f"https://www.ipaddress.com/site/{host}"
    ip_list = np.empty(shape=(0, 2), dtype=object)
    html_doc = requests.get(url).text
    bs = BeautifulSoup(html_doc, "html.parser")
    scripts = bs.find_all("script", {"type": "application/ld+json"})
    for script in scripts:
        json_loads = json.loads(script.string)
        if "mainEntity" in json_loads:
            # print(json_loads)
            main_entity_ = json_loads["mainEntity"]
            # print(main_entity_)
            for i in main_entity_:
                if str(i["name"]).__contains__("IP address?"):

                    text_ = i["acceptedAnswer"]["text"]
                    bs = BeautifulSoup(text_, "html.parser")
                    ip_ul = bs.find_all("strong")
                    ul = len(ip_ul)
                    ip_list = np.empty(shape=(ul, 2), dtype=object)
                    for li in range(ul):
                        ip_list[li][0] = ip_ul[li].text
                        ip_list[li][1] = host
    return ip_list


def get_start(host_list: list):
    records = []

    with ThreadPoolExecutor(max_workers=cpu_count() + 1) as pool:
        task_list = []

        for host in host_list:
            obj = pool.submit(get_ip, host.strip().replace("\n", ""))
            task_list.append(obj)

        for task in as_completed(task_list):
            records.append(task.result())

    return records


with open(r"host_list.txt") as fr:
    hosts = fr.readlines()
    ret = get_start(hosts)

    with open("hosts", "w") as fw:
        fw.truncate()
        for j in ret:
            res = np.array(j, str)
            print(res)
            np.savetxt(fw, res, ["%-20s", "%s"])
        fw.close()

    fr.close()
