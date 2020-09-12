import requests
import urllib3

import constants as c

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def operation_a(x):
    ret = requests.get(f'{c.BASE_URL}/A/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('a', ret)
    return ret


def operation_b(x):
    ret = requests.get(f'{c.BASE_URL}/B/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('b', ret)
    return ret


def operation_c(x):
    ret = requests.get(f'{c.BASE_URL}/C/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('c', ret)
    return ret


def operation_0(x):
    ret = requests.get(f'{c.BASE_URL}/0/{x}/0', verify=False).content
    if c.PRINT_RESPONSES:
        print('0', ret)
    return ret
