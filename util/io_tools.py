from service import hr_service as hr
from entity import organizations as o
from service import recognize_service as rs
import os
import cv2
import numpy as np
import json
from clock.entity.organizations import WORK_TIME

PATH = os.getcwd() + '\\data\\'
PIC_PATH = PATH + 'faces\\'
DATA_FILE = PATH + 'employee.txt'
WORK_TIME = PATH +'work_time.txt'
USER_PASSWORD = PATH + 'user_password.txt'
RECORD_FILE = PATH + 'lock_record.txt'
IMG_WIDTH = 640
IMG_HEIGHT = 480

def checking_data_file():
    if not os.path.exists(PATH):
        os.makedirs(PATH, exist_ok=True)
        print('数据文件夹丢失，已重新创建：' + PATH)
    if not os.path.exists(PIC_PATH):
        os.makedirs(PIC_PATH, exist_ok=True)
        print('人脸图片文件夹丢失，已重新创建：' + PIC_PATH)
    sample1 = PIC_PATH + '1000000000.png'     #样本1路径
    if not os.path.exists(sample1):
        #创建一个空内容的图像
        sample1_img_1 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)
        sample1_img_1[:, :,0] = 255
        cv2.imwrite(sample1, sample1_img_1)
        print('默认样本1已补充')
    sample2 = PIC_PATH + '2000000000.png'
    if not os.path.exists(sample2):
        #创建一个空内容的图像
        sample2_img_2 = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)
        sample2_img_2[:, :,1] = 255
        cv2.imwrite(sample2, sample2_img_2)
        print('默认样本2已补充')
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, 'a+')
        print('员工信息文件丢失，已重新创建：' + DATA_FILE)
    if not os.path.exists(RECORD_FILE):
        open(RECORD_FILE, 'a+')
        print('打卡记录文件丢失，已重新创建：' + RECORD_FILE)
    if not os.path.exists(USER_PASSWORD):
        file = open(USER_PASSWORD, 'a+',encoding='utf-8')
        user = dict()
        user['dhl'] = '541610'
        json.dump(
            user,
            file,
            ensure_ascii=False
        )
        file.close()
        print('管理员账号密码文件丢失，已重新创建：' + RECORD_FILE)
    if not os.path.exists(WORK_TIME):
        file = open(WORK_TIME, 'a+',encoding='utf-8')
        file.write('9:00:00/17:00:00')
        file.close()
        print('上下班时间配置文件丢失，已重新创建：' + RECORD_FILE)



#载入所有员工信息
def load_employee_info():
    max_id = 1;
    file = open(DATA_FILE, 'r',encoding='utf-8')
    for line in file.readlines():
        id,name,code = line.rstrip('\n').split('\t')
        o.add(o.Employee(id,name,code))
        if int(id) > max_id:
            max_id = int(id)
    o.MAX_ID = max_id
    file.close()
#载入所有打卡记录
def load_lock_record():

    if not os.path.exists(RECORD_FILE):
        return

    with open(RECORD_FILE, "r", encoding="utf-8") as file:

        text = file.read().strip()

        if text == "":
            o.LOCK_RECORD = {}

        else:
            o.LOCK_RECORD = json.loads(text)

# 加载员工图像
def load_employee_pic():
    photos = list()                    # 样本图像列表
    labels = list()                    # 标签列表
    pics = os.listdir(PIC_PATH)        # 读取所有照片

    if len(pics) != 0:                 # 如果照片文件夹不是空的
        for file_name in pics:         # 遍历所有图像文件
            code = file_name[0:o.CODE_LEN]   # 截取文件名开头的特征码

            # 以灰度图像的方式读取样本
            photos.append(cv2.imread(PIC_PATH + file_name, 0))

            # 样本的特征码作为训练标签
            labels.append(int(code))

        rs.train(photos, labels)       # 识别器训练样本

    else:
        print("Error >> 员工照片文件丢失，请重新启动程序并录入员工信息")
# 加载上下班时间数据
def load_work_time_config():
    file = open(WORK_TIME, "r", encoding="utf-8")  # 打开上下班时间记录文件，只读
    text = file.read().rstrip()                    # 读取所有文本
    times = text.split("/")                        # 分割字符串
    o.WORK_TIME = times[0]                         # 第一个值是上班时间
    o.CLOSING_TIME = times[1]                      # 第二个值是下班时间
    file.close()                                   # 关闭文件
# 加载管理员账号和密码
def load_users():
    file = open(USER_PASSWORD, "r", encoding="utf-8")  # 打开管理员账号文件，只读
    text = file.read()                                 # 读取所有文本

    if len(text) > 0:                                  # 如果存在文本
        o.USERS = json.loads(text)                           # 将文本转换成打卡记录字典

    file.close()

def save_employee_all():
    """
    保存所有员工信息
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        for emp in o.EMPLOYEES:
            file.write(str(emp.id) + '\t' + emp.name + '\t' + str(emp.code) + '\n')

    file.close()

# 将打卡记录持久化
def save_lock_record():

    with open(RECORD_FILE, "w", encoding="utf-8") as file:

        json.dump(
            o.LOCK_RECORD,
            file,
            ensure_ascii=False,
            indent=4
        )


# 将上下班时间写到文件中
def save_work_time_config():
    file = open(WORK_TIME, "w", encoding="utf-8")  # 打开上下班时间配置文件，只写，覆盖
    times = str(o.WORK_TIME) + "/" + str(o.CLOSING_TIME)
    file.write(times)  # 将字符串内容写入到文件中
    file.close()  # 关闭文件
# 删除指定员工的所有照片
def remove_pics(id):
    code = str(hr.get_code_with_id(id))      # 获取该员工的特征码
    pics = os.listdir(PIC_PATH)              # 读取所有照片文件

    for file_name in pics:                   # 遍历文件
        if file_name.startswith(code):       # 如果文件名以特征码开头
            os.remove(PIC_PATH + file_name)  # 删除此文件
            print("删除照片：" + file_name)
# 生成CSV文件，采用Windows默认的GBK编码
def create_CSV(file_name, text):
    file = open(PATH + file_name + ".csv", "w", encoding="gbk")  # 打开文件，只写，覆盖
    file.write(text)                                            # 将文本写入文件中
    file.close()                                                # 关闭文件
    print("已生成文件，请注意查看：" + PATH + file_name + ".csv")

def remove_pics(id):

    code = str(hr.get_code_with_id(id))

    pics = os.listdir(PIC_PATH)

    for file_name in pics:

        if file_name.startswith(code):

            try:

                os.remove(PIC_PATH + file_name)

                print("删除照片：" + file_name)

            except Exception as e:

                print(e)