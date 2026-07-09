"""
全局数据管理
"""

# ==========================
# 人员实体
# ==========================
class Employee:

    def __init__(self, id, name, code):
        self.id = int(id)
        self.name = name
        self.code = code

    def __str__(self):
        return f"{self.id}\t{self.name}\t{self.code}"


# ==========================
# 全局变量
# ==========================

# 人员列表
EMPLOYEES = []

# 打卡记录
"""
LOCK_RECORD 示例：

{
    1:{
        "person_id":1,
        "name":"张三",
        "arrival_order":1,
        "enter_time":"2026-07-09 09:00:00",
        "leave_time":"",
        "stay_time":"",
        "status":"在馆"
    }
}
"""
LOCK_RECORD = {}

# 最大ID
MAX_ID = 0

# 人脸特征码长度
CODE_LEN = 6

# 摄像头照片大小
IMG_WIDTH = 640
IMG_HEIGHT = 480

# 今日到馆顺序
ARRIVAL_ORDER = 0

# 工作时间（保留，方便以后扩展）
WORK_TIME = "08:00:00"

# 闭馆时间
CLOSING_TIME = "22:00:00"

# 管理员账号
USERS = {}


# ==========================
# 人员管理
# ==========================

def add(employee: Employee):
    EMPLOYEES.append(employee)


def remove(id):

    for emp in EMPLOYEES:

        if int(emp.id) == int(id):

            EMPLOYEES.remove(emp)

            if emp.id in LOCK_RECORD:
                del LOCK_RECORD[emp.id]

            return True

    return False


def get_new_id():

    global MAX_ID

    MAX_ID += 1

    return MAX_ID


# ==========================
# 查询
# ==========================

def get_employee(id):

    for emp in EMPLOYEES:

        if int(emp.id) == int(id):
            return emp

    return None


def get_employee_by_code(code):

    for emp in EMPLOYEES:

        if str(emp.code) == str(code):
            return emp

    return None


def get_employee_by_name(name):

    for emp in EMPLOYEES:

        if emp.name == name:
            return emp

    return None


# ==========================
# 人数统计
# ==========================

def employee_count():
    return len(EMPLOYEES)


def online_count():

    count = 0

    for record in LOCK_RECORD.values():

        if record["status"] == "在馆":
            count += 1

    return count


# ==========================
# 到馆顺序
# ==========================

def next_arrival_order():

    global ARRIVAL_ORDER

    ARRIVAL_ORDER += 1

    return ARRIVAL_ORDER


def reset_arrival_order():

    global ARRIVAL_ORDER

    ARRIVAL_ORDER = 0