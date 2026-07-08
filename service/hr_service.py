from entity import organizations as o
from util import public_tools as tool
from util import io_tools as io
import datetime
import calendar


# 加载数据
def load_emp_data():
    io.checking_data_file()      # 文件自检
    io.load_users()               # 载入管理员账号
    io.load_lock_record()         # 载入打卡记录
    io.load_employee_info()       # 载入员工信息
    io.load_employee_pic()        # 载入员工照片



# 添加新员工
def add_new_employee(name):
    code = tool.randomCode()                       # 生成随机特征码
    newEmp = o.Employee(o.get_new_id(), name, code) # 创建员工对象
    o.add(newEmp)                                  # 组织结构中添加新员工
    io.save_employee_all()                         # 保存最新的员工信息
    return code                                    # 返回新员工的特征码


# 删除某个员工
def remove_employee(id):
    tool.remove_pics(id)       # 删除该员工所有图片
    o.remove(id)               # 从组织结构中删除
    io.save_employee_all()     # 保存最新的员工信息
    io.save_lock_record()      # 保存最新的打卡记录


# 为指定员工添加打卡记录
def add_lock_record(name):
    record = o.LOCK_RECORD
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 当前时间

    if name in record.keys():          # 如果这个人有打卡记录
        r_list = record[name]          # 取出他的记录

        if len(r_list) == 0:           # 如果记录为空
            r_list = list()            # 创建新列表

        r_list.append(now_time)        # 记录当前时间

    else:                              # 如果这个人从未打过卡
        r_list = list()                # 创建新列表
        r_list.append(now_time)        # 记录当前时间
        record[name] = r_list          # 将记录保存在字典中

    io.save_lock_record()              # 保存所有打卡记录


# 所有员工信息报表
def get_employee_report():
    report = "########################################\n"
    report += "员工名单如下所示：\n"
    i = 0

    for emp in o.EMPLOYEES:
        report += "(" + str(emp.id) + ")" + emp.name + "\t"
        i += 1

        if i == 4:
            report += "\n"
            i = 0

    report = report.strip()
    report += "\n########################################"
    return report


# 检查 id 是否存在
def check_id(id):
    for emp in o.EMPLOYEES:
        if str(id) == str(emp.id):
            return True

    return False


# 通过特征码获取员工姓名
def get_name_with_code(code):
    for emp in o.EMPLOYEES:
        if str(code) == str(emp.code):
            return emp.name


# 通过 id 获取员工特征码
def get_code_with_id(id):
    for emp in o.EMPLOYEES:
        if str(id) == str(emp.id):
            return emp.code


# 验证管理员账号和密码
def valid_user(username, password):
    if username in o.USERS.keys():
        if o.USERS.get(username) == password:
            return True

    return False


# 保存上下班时间
def save_work_time(work_time, close_time):
    o.WORK_TIME = work_time
    o.CLOSING_TIME = close_time
    io.save_work_time_config()


# 打印指定日期的打卡日报
def get_day_report(date):
    io.load_work_time_config()  # 读取上下班时间

    # 今天 0 点
    earliest_time = datetime.datetime.strptime(
        date + " 00:00:00", "%Y-%m-%d %H:%M:%S"
    )

    # 今天中午 12 点
    noon_time = datetime.datetime.strptime(
        date + " 12:00:00", "%Y-%m-%d %H:%M:%S"
    )

    # 今晚 0 点之前
    latest_time = datetime.datetime.strptime(
        date + " 23:59:59", "%Y-%m-%d %H:%M:%S"
    )

    # 上班时间
    work_time = datetime.datetime.strptime(
        date + " " + o.WORK_TIME, "%Y-%m-%d %H:%M:%S"
    )

    # 下班时间
    closing_time = datetime.datetime.strptime(
        date + " " + o.CLOSING_TIME, "%Y-%m-%d %H:%M:%S"
    )

    late_list = []        # 迟到名单
    left_early = []       # 早退名单
    absent_list = []      # 缺席名单

    for emp in o.EMPLOYEES:
        if emp.name in o.LOCK_RECORD.keys():
            emp_lock_list = o.LOCK_RECORD.get(emp.name)
            is_absent = True

            for lock_time_str in emp_lock_list:
                lock_time = datetime.datetime.strptime(
                    lock_time_str, "%Y-%m-%d %H:%M:%S"
                )

                # 如果当天有打卡记录
                if earliest_time < lock_time < latest_time:
                    is_absent = False

                    # 上班时间后，中午之前打卡，算迟到
                    if work_time < lock_time <= noon_time:
                        late_list.append(emp.name)

                    # 中午之后，下班之前打卡，算早退
                    if noon_time < lock_time < closing_time:
                        left_early.append(emp.name)

            if is_absent:
                absent_list.append(emp.name)

        else:
            absent_list.append(emp.name)

    emp_count = len(o.EMPLOYEES)

    print("--------" + date + "--------")
    print("应到人数：" + str(emp_count))
    print("缺席人数：" + str(len(absent_list)))

    absent_name = ""
    if len(absent_list) == 0:
        absent_name = "（空）"
    else:
        for name in absent_list:
            absent_name += name + " "
    print("缺席名单：" + absent_name)

    print("迟到人数：" + str(len(late_list)))

    late_name = ""
    if len(late_list) == 0:
        late_name = "（空）"
    else:
        for name in late_list:
            late_name += name + " "
    print("迟到名单：" + late_name)

    print("早退人数：" + str(len(left_early)))

    early_name = ""
    if len(left_early) == 0:
        early_name = "（空）"
    else:
        for name in left_early:
            early_name += name + " "
    print("早退名单：" + early_name)


# 打印今天的打卡日报
def get_today_report():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    get_day_report(str(date))


# 创建指定月份的打卡记录月报
def get_month_report(month):
    io.load_work_time_config()  # 读取上下班时间

    date = datetime.datetime.strptime(month, "%Y-%m")
    monthRange = calendar.monthrange(date.year, date.month)[1]

    month_first_day = datetime.date(date.year, date.month, 1)
    month_last_day = datetime.date(date.year, date.month, monthRange)

    clock_in = "I"       # 正常上班打卡标志
    clock_out = "O"      # 正常下班打卡标志
    late = "L"           # 迟到标志
    left_early = "E"     # 早退标志
    absent = "A"         # 缺席标志

    lock_report = dict()  # 键为员工名，值为员工打卡情况列表

    for emp in o.EMPLOYEES:
        emp_lock_data = []  # 员工打卡情况列表

        if emp.name in o.LOCK_RECORD.keys():
            emp_lock_list = o.LOCK_RECORD.get(emp.name)
            index_day = month_first_day

            while index_day <= month_last_day:
                is_absent = True

                earliest_time = datetime.datetime.strptime(
                    str(index_day) + " 00:00:00",
                    "%Y-%m-%d %H:%M:%S"
                )

                noon_time = datetime.datetime.strptime(
                    str(index_day) + " 12:00:00",
                    "%Y-%m-%d %H:%M:%S"
                )

                latest_time = datetime.datetime.strptime(
                    str(index_day) + " 23:59:59",
                    "%Y-%m-%d %H:%M:%S"
                )

                work_time = datetime.datetime.strptime(
                    str(index_day) + " " + o.WORK_TIME,
                    "%Y-%m-%d %H:%M:%S"
                )

                closing_time = datetime.datetime.strptime(
                    str(index_day) + " " + o.CLOSING_TIME,
                    "%Y-%m-%d %H:%M:%S"
                )

                emp_today_data = ""

                for lock_time_str in emp_lock_list:
                    lock_time = datetime.datetime.strptime(
                        lock_time_str,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    # 如果当前日期有打卡记录
                    if earliest_time < lock_time < latest_time:
                        is_absent = False

                        # 上班时间前打卡
                        if lock_time <= work_time:
                            emp_today_data += clock_in

                        # 下班时间后打卡
                        elif lock_time >= closing_time:
                            emp_today_data += clock_out

                        # 上班时间后，中午之前打卡
                        elif work_time < lock_time <= noon_time:
                            emp_today_data += late

                        # 中午之后，下班之前打卡
                        elif noon_time < lock_time < closing_time:
                            emp_today_data += left_early

                if is_absent:
                    emp_today_data = absent

                emp_lock_data.append(emp_today_data)
                index_day = index_day + datetime.timedelta(days=1)

        else:
            index_day = month_first_day

            while index_day <= month_last_day:
                emp_lock_data.append(absent)
                index_day = index_day + datetime.timedelta(days=1)

        lock_report[emp.name] = emp_lock_data

    report = "\\姓名 / 日期\\"
    index_day = month_first_day

    while index_day <= month_last_day:
        report += "," + str(index_day.day)
        index_day = index_day + datetime.timedelta(days=1)

    report += "\n"

    for emp in lock_report.keys():
        report += emp + ","
        data_list = lock_report.get(emp)

        for data in data_list:
            report += data + ","

        report += "\n"

    # CSV 文件标题日期
    title_date = month_first_day.strftime("%Y年%m月")
    file_name = title_date + "考勤月报"

    # 生成 CSV 文件
    io.create_CSV(file_name, report)


# 创建上个月打卡记录月报
def get_pre_month_report():
    today = datetime.date.today()
    pre_month = today + datetime.timedelta(days=-1)
    pre_month = pre_month.strftime("%Y-%m")
    get_month_report(pre_month)

def get_record_all():
    """
    获取所有打卡记录
    """
    return o.LOCK_RECORD