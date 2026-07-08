import random
import datetime
from entity import organizations as o
def randomNumber(len):
    first = str(random.randint(1, 9))
    last = "".join(random.sample('1234567890', len - 1))
    return first + last
def randomCode():
    return randomNumber(o.CODE_LEN)
def valid_time(str):
    try:
        datetime.datetime.strptime(str, '%H:%M')
        return True
    except ValueError:
        return False
def valid_year_month(str):
    try:
        datetime.datetime.strptime(str, '%Y-%m')
        return True
    except ValueError:
        return False
def valid_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False





import os
from entity import organizations as o


def remove_pics(id):
    """
    删除指定员工的所有人脸图片
    """
    # 员工照片文件夹
    pic_path = os.getcwd() + "\\data\\faces\\"

    if not os.path.exists(pic_path):
        return

    code = None

    for emp in o.EMPLOYEES:
        if str(emp.id) == str(id):
            code = str(emp.code)
            break

    if code is None:
        return

    for file_name in os.listdir(pic_path):
        if file_name.startswith(code):
            os.remove(pic_path + file_name)