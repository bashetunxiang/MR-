from datetime import datetime
from entity import organizations as o


# ==========================
# 人员进入体育馆
# ==========================
def person_enter(person):
    """
    person:
    {
        "id":1,
        "name":"张三"
    }
    """

    # 已经在馆，不允许重复进入
    if is_online(person["id"]):
        return None

    # 今日进入顺序+1
    o.ARRIVAL_ORDER += 1

    now = datetime.now()

    record = {
        "person_id": person["id"],
        "name": person["name"],
        "arrival_order": o.ARRIVAL_ORDER,
        "enter_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        "leave_time": "",
        "stay_time": "",
        "status": "在馆"
    }

    o.LOCK_RECORD[person["id"]] = record

    return record


# ==========================
# 人员离馆
# ==========================
def person_leave(person_id):

    if person_id not in o.LOCK_RECORD:
        return None

    record = o.LOCK_RECORD[person_id]

    # 已经离馆
    if record["status"] == "已离馆":
        return record

    leave_time = datetime.now()

    enter_time = datetime.strptime(
        record["enter_time"],
        "%Y-%m-%d %H:%M:%S"
    )

    stay = leave_time - enter_time

    record["leave_time"] = leave_time.strftime("%Y-%m-%d %H:%M:%S")
    record["stay_time"] = str(stay).split(".")[0]
    record["status"] = "已离馆"

    o.LOCK_RECORD[person_id] = record

    return record


# ==========================
# 判断是否已经在馆
# ==========================
def is_online(person_id):

    if person_id not in o.LOCK_RECORD:
        return False

    return o.LOCK_RECORD[person_id]["status"] == "在馆"


# ==========================
# 获取所有在馆人员
# ==========================
def get_online_people():

    people = []

    for record in o.LOCK_RECORD.values():

        if record["status"] == "在馆":

            people.append(record)

    return people


# ==========================
# 当前在馆人数
# ==========================
def get_online_count():

    return len(get_online_people())


# ==========================
# 获取所有打卡记录
# ==========================
def get_all_record():

    return list(o.LOCK_RECORD.values())


# ==========================
# 根据人员ID获取记录
# ==========================
def get_record(person_id):

    return o.LOCK_RECORD.get(person_id)


# ==========================
# 删除记录
# ==========================
def remove_record(person_id):

    if person_id in o.LOCK_RECORD:

        del o.LOCK_RECORD[person_id]

        return True

    return False


# ==========================
# 今日到馆人数
# ==========================
def today_total():

    today = datetime.now().strftime("%Y-%m-%d")

    count = 0

    for record in o.LOCK_RECORD.values():

        if record["enter_time"].startswith(today):

            count += 1

    return count


# ==========================
# 今日离馆人数
# ==========================
def today_leave():

    today = datetime.now().strftime("%Y-%m-%d")

    count = 0

    for record in o.LOCK_RECORD.values():

        if record["leave_time"] != "" and record["leave_time"].startswith(today):

            count += 1

    return count


# ==========================
# 重置今日进入顺序
# （每天凌晨调用一次）
# ==========================
def reset_arrival_order():

    o.ARRIVAL_ORDER = 0


# ==========================
# 清空所有打卡记录
# ==========================
def clear_record():

    o.LOCK_RECORD.clear()