from entity import organizations as o
from util import io_tools as io


# ==========================
# 保存进入记录
# ==========================
def save_record(record):
    """
    保存进入体育馆记录
    """

    if record is None:
        return False

    o.LOCK_RECORD[record["person_id"]] = record

    io.save_lock_record()

    return True


# ==========================
# 更新离馆记录
# ==========================
def update_record(record):
    """
    更新离馆记录
    """

    if record is None:
        return False

    if record["person_id"] in o.LOCK_RECORD:

        o.LOCK_RECORD[record["person_id"]] = record

        io.save_lock_record()

        return True

    return False


# ==========================
# 获取所有记录
# ==========================
def get_all_records():

    return list(o.LOCK_RECORD.values())


# ==========================
# 根据人员ID查询记录
# ==========================
def get_record(person_id):

    if person_id in o.LOCK_RECORD:

        return o.LOCK_RECORD[person_id]

    return None


# ==========================
# 根据姓名查询记录
# ==========================
def get_record_by_name(name):

    for record in o.LOCK_RECORD.values():

        if record["name"] == name:

            return record

    return None


# ==========================
# 删除记录
# ==========================
def delete_record(person_id):

    if person_id in o.LOCK_RECORD:

        del o.LOCK_RECORD[person_id]

        io.save_lock_record()

        return True

    return False


# ==========================
# 清空记录
# ==========================
def clear_records():

    o.LOCK_RECORD.clear()

    io.save_lock_record()


# ==========================
# 当前在馆人员
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
# 已离馆人员
# ==========================
def get_leave_people():

    people = []

    for record in o.LOCK_RECORD.values():

        if record["status"] == "已离馆":

            people.append(record)

    return people


# ==========================
# 今日到馆人数
# ==========================
def today_total():

    return len(o.LOCK_RECORD)


# ==========================
# 今日离馆人数
# ==========================
def today_leave():

    return len(get_leave_people())


# ==========================
# 判断是否已在馆
# ==========================
def is_online(person_id):

    if person_id not in o.LOCK_RECORD:

        return False

    return o.LOCK_RECORD[person_id]["status"] == "在馆"


# ==========================
# 获取最新进入记录
# ==========================
def latest_records(number=10):

    records = sorted(

        o.LOCK_RECORD.values(),

        key=lambda x: x["enter_time"],

        reverse=True

    )

    return records[:number]


# ==========================
# 获取平均停留时间（秒）
# ==========================
def average_stay_time():

    total = 0

    count = 0

    for record in o.LOCK_RECORD.values():

        if record["stay_time"] == "":

            continue

        h, m, s = map(int, record["stay_time"].split(":"))

        total += h * 3600 + m * 60 + s

        count += 1

    if count == 0:

        return "00:00:00"

    avg = total // count

    h = avg // 3600

    m = (avg % 3600) // 60

    s = avg % 60

    return "{:02}:{:02}:{:02}".format(h, m, s)