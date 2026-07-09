from entity import organizations as o
from util import public_tools as tool
from util import io_tools as io
from service import attendance_service as ats
from service import record_service as rds
from service import statistics_service as sts


# ==========================
# 数据初始化
# ==========================
def load_emp_data():

    io.checking_data_file()

    io.load_users()

    io.load_lock_record()

    io.load_employee_info()

    io.load_employee_pic()


# ==========================
# 添加新人员
# ==========================
def add_new_employee(name):

    code = tool.randomCode()

    emp = o.Employee(

        o.get_new_id(),

        name,

        code

    )

    o.add(emp)

    io.save_employee_all()

    return code


# ==========================
# 删除人员
# ==========================
def remove_employee(id):

    io.remove_pics(id)

    o.remove(id)

    io.save_employee_all()

    io.save_lock_record()


# ==========================
# 判断ID是否存在
# ==========================
def check_id(id):

    for emp in o.EMPLOYEES:

        if int(emp.id) == int(id):

            return True

    return False


# ==========================
# 根据特征码获取姓名
# ==========================
def get_name_with_code(code):

    for emp in o.EMPLOYEES:

        if str(emp.code) == str(code):

            return emp.name

    return None


# ==========================
# 根据ID获取特征码
# ==========================
def get_code_with_id(id):

    for emp in o.EMPLOYEES:

        if int(emp.id) == int(id):

            return emp.code

    return None


# ==========================
# 获取人员对象
# ==========================
def get_employee(id):

    for emp in o.EMPLOYEES:

        if int(emp.id) == int(id):

            return emp

    return None


# ==========================
# 获取所有人员
# ==========================
def get_all_employee():

    return o.EMPLOYEES


# ==========================
# 人员总数
# ==========================
def employee_count():

    return len(o.EMPLOYEES)


# ==========================
# 人员列表
# ==========================
def get_employee_report():

    report = ""

    report += "==============================\n"

    report += "      体育馆人员列表\n"

    report += "==============================\n"

    report += "编号\t姓名\n"

    for emp in o.EMPLOYEES:

        report += "{}\t{}\n".format(

            emp.id,

            emp.name

        )

    report += "=============================="

    return report


# ==========================
# 管理员登录
# ==========================
def valid_user(username, password):

    if username not in o.USERS:

        return False

    return o.USERS[username] == password


# ==========================
# 获取全部打卡记录
# ==========================
def get_record_all():

    return rds.get_all_records()


# ==========================
# 获取当前在馆人员
# ==========================
def get_online_people():

    return rds.get_online_people()


# ==========================
# 当前在馆人数
# ==========================
def get_online_count():

    return rds.get_online_count()
# ==========================
# 今日到馆人数
# ==========================
def get_today_total():

    return sts.today_total()


# ==========================
# 今日离馆人数
# ==========================
def get_leave_total():

    return sts.leave_total()


# ==========================
# 平均停留时间
# ==========================
def get_average_stay():

    return sts.average_stay_time()


# ==========================
# 最近进入体育馆人员
# ==========================
def get_latest_people(number=10):

    return sts.latest_people(number)


# ==========================
# 人流高峰
# ==========================
def get_peak_hour():

    return sts.peak_hour()


# ==========================
# 今日趋势
# ==========================
def get_today_trend():

    return sts.today_trend()


# ==========================
# 首页统计数据
# ==========================
def get_dashboard():

    return sts.dashboard()


# ==========================
# 获取折线图数据
# ==========================
def get_line_chart():

    return sts.line_chart()


# ==========================
# 获取饼图数据
# ==========================
def get_pie_chart():

    return sts.pie_chart()


# ==========================
# 根据姓名查询人员
# ==========================
def get_employee_by_name(name):

    for emp in o.EMPLOYEES:

        if emp.name == name:

            return emp

    return None


# ==========================
# 根据编号查询人员
# ==========================
def get_employee_by_id(person_id):

    for emp in o.EMPLOYEES:

        if int(emp.id) == int(person_id):

            return emp

    return None


# ==========================
# 查询打卡记录
# ==========================
def get_record(person_id):

    return rds.get_record(person_id)


# ==========================
# 删除打卡记录
# ==========================
def delete_record(person_id):

    return rds.delete_record(person_id)


# ==========================
# 清空打卡记录
# ==========================
def clear_record():

    return rds.clear_records()


# ==========================
# 判断人员是否在馆
# ==========================
def is_online(person_id):

    return rds.is_online(person_id)


# ==========================
# 人员进入体育馆
# ==========================
def person_enter(person):

    record = ats.person_enter(person)

    if record is not None:

        rds.save_record(record)

    return record


# ==========================
# 人员离馆
# ==========================
def person_leave(person_id):

    record = ats.person_leave(person_id)

    if record is not None:

        rds.update_record(record)

    return record


# ==========================
# 系统首页信息
# ==========================
def system_info():

    data = {

        "employee_count": employee_count(),

        "today_total": get_today_total(),

        "online_total": get_online_count(),

        "leave_total": get_leave_total(),

        "average_stay": get_average_stay()

    }

    return data