import requests
import urllib3

import constants as c


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def operation_a(x):
    ret = requests.get(f'{c.BASE_URL}/A/{x}/0', verify=False).content
    print('a', ret)
    return ret


def operation_b(x):
    ret = requests.get(f'{c.BASE_URL}/B/{len(x)}/0', verify=False).content
    print('b', ret)
    return ret


def operation_c(x):
    ret = requests.get(f'{c.BASE_URL}/C/{len(x)}/0', verify=False).content
    print('c', ret)
    return ret
