from util import public_tools as tool
from util import camera
from service import hr_service as hr


ADMIN_LOGIN = False


# ==========================
# 管理员登录
# ==========================
def login():
    global ADMIN_LOGIN

    while True:
        username = input("请输入管理员账号（输入0取消操作）：").strip()

        if username == "0":
            return False

        password = input("请输入管理员密码：").strip()

        if hr.valid_user(username, password):
            ADMIN_LOGIN = True
            print(username + " 登录成功！")
            return True
        else:
            print("账号或密码错误，请重新输入！")
            print("-----------------------------")


# ==========================
# 检查管理员是否登录
# ==========================
def check_login():
    if ADMIN_LOGIN:
        return True

    print("该功能需要管理员登录！")
    return login()


# ==========================
# 系统启动
# ==========================
def start():
    finish = False

    menu = """
+------------------------------------------------+
|              体育馆视频打卡系统                |
+------------------------------------------------+
① 人员进入场馆
② 人员离开场馆
③ 人员管理
④ 查看在馆人员
⑤ 数据统计
⑥ 查看全部记录
⑦ 摄像头预览
⑧ 退出系统
--------------------------------------------------
"""

    while not finish:
        print(menu)
        option = input("请输入菜单序号：").strip()

        if option == "1":
            person_enter()

        elif option == "2":
            if check_login():
                person_leave()

        elif option == "3":
            if check_login():
                employee_management()

        elif option == "4":
            if check_login():
                show_online_people()

        elif option == "5":
            if check_login():
                show_statistics()

        elif option == "6":
            if check_login():
                show_all_records()

        elif option == "7":
            camera.preview()

        elif option == "8":
            finish = True

        else:
            print("输入的指令有误，请重新输入！")

    print("Bye Bye!")


# ==========================
# 人员进入场馆
# ==========================
def person_enter():
    print("请正面对准摄像头，系统正在识别...")

    record = camera.clock_in()

    if record is not None:
        print("\n进入场馆成功！")
        print_record(record)
    else:
        print("未识别到有效人员，进入失败。")


# ==========================
# 人员离开场馆
# ==========================
def person_leave():
    print(hr.get_employee_report())

    try:
        person_id = int(input("请输入离馆人员编号（输入0取消）：").strip())
    except ValueError:
        print("输入格式错误，请输入数字编号！")
        return

    if person_id == 0:
        return

    if not hr.check_id(person_id):
        print("无此人员，操作取消！")
        return

    record = camera.clock_out(person_id)

    if record is not None:
        print("\n离馆成功！")
        print_record(record)
    else:
        print("该人员当前不在馆，无法离馆。")


# ==========================
# 人员管理
# ==========================
def employee_management():
    menu = """
+------------------------------------------------+
|                人员管理功能菜单                |
+------------------------------------------------+
① 录入新人员
② 删除人员
③ 查看人员列表
④ 返回上级菜单
--------------------------------------------------
"""

    while True:
        print(menu)
        option = input("请输入菜单序号：").strip()

        if option == "1":
            add_employee()

        elif option == "2":
            delete_employee()

        elif option == "3":
            print(hr.get_employee_report())

        elif option == "4":
            return

        else:
            print("输入的指令有误，请重新输入！")


# ==========================
# 新增人员
# ==========================
def add_employee():
    name = input("请输入新人员姓名（输入0取消）：").strip()

    if name == "0":
        return

    if name == "":
        print("姓名不能为空！")
        return

    code = hr.add_new_employee(name)

    print("请面对摄像头，按三次回车键完成拍照！")

    camera.register(code)

    print(name + " 录入成功！")


# ==========================
# 删除人员
# ==========================
def delete_employee():
    print(hr.get_employee_report())

    try:
        person_id = int(input("请输入要删除的人员编号（输入0取消）：").strip())
    except ValueError:
        print("输入格式错误，请输入数字编号！")
        return

    if person_id == 0:
        return

    if not hr.check_id(person_id):
        print("无此人员，操作取消！")
        return

    verification = tool.randomNumber(4)

    input_ver = input("[" + str(verification) + "] 请输入验证码：").strip()

    if str(verification) == input_ver:
        hr.remove_employee(person_id)
        print(str(person_id) + "号人员已删除！")
    else:
        print("验证码错误，操作取消！")


# ==========================
# 查看当前在馆人员
# ==========================
def show_online_people():
    people = hr.get_online_people()

    print("\n================ 当前在馆人员 ================")

    if people is None or len(people) == 0:
        print("当前暂无人员在馆。")
        print("============================================")
        return

    for record in people:
        print_record(record)

    print("============================================")


# ==========================
# 查看全部记录
# ==========================
def show_all_records():
    records = hr.get_record_all()

    print("\n================ 全部到馆记录 ================")

    if records is None or len(records) == 0:
        print("暂无到馆记录。")
        print("============================================")
        return

    for record in records:
        print_record(record)

    print("============================================")


# ==========================
# 数据统计
# ==========================
def show_statistics():
    data = hr.system_info()

    print("\n================ 体育馆数据统计 ================")
    print("人员总数：", data.get("employee_count", 0))
    print("今日到馆人数：", data.get("today_total", 0))
    print("当前在馆人数：", data.get("online_total", 0))
    print("今日离馆人数：", data.get("leave_total", 0))
    print("平均停留时间：", data.get("average_stay", "00:00:00"))

    peak = hr.get_peak_hour()

    if peak is not None:
        print("人流高峰时段：{}点，人数：{}".format(
            peak.get("hour"),
            peak.get("count")
        ))
    else:
        print("人流高峰时段：暂无数据")

    print("===============================================")


# ==========================
# 打印单条记录
# ==========================
def print_record(record):
    if record is None:
        return

    print("--------------------------------")
    print("人员编号：", record.get("person_id", ""))
    print("姓名：", record.get("name", ""))
    print("第几个进入场馆：第{}位".format(record.get("arrival_order", "")))
    print("进入时间：", record.get("enter_time", ""))
    print("离馆时间：", record.get("leave_time", ""))
    print("停留时间：", record.get("stay_time", ""))
    print("状态：", record.get("status", ""))
    print("--------------------------------")


# ==========================
# 程序入口
# ==========================
if __name__ == "__main__":
    hr.load_emp_data()

    title = """
************************************************************
*                  体育馆视频打卡管理系统                  *
************************************************************
"""

    print(title)

    start()