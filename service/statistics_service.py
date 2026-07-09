from entity import organizations as o
from datetime import datetime
from collections import defaultdict


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
# 当前在馆人数
# ==========================
def online_total():

    count = 0

    for record in o.LOCK_RECORD.values():

        if record["status"] == "在馆":
            count += 1

    return count


# ==========================
# 今日离馆人数
# ==========================
def leave_total():

    today = datetime.now().strftime("%Y-%m-%d")

    count = 0

    for record in o.LOCK_RECORD.values():

        if record["leave_time"] != "":

            if record["leave_time"].startswith(today):
                count += 1

    return count


# ==========================
# 平均停留时间
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


# ==========================
# 每小时进入人数
# ==========================
def hourly_statistics():

    result = defaultdict(int)

    for record in o.LOCK_RECORD.values():

        hour = record["enter_time"][11:13]

        result[hour] += 1

    return dict(result)


# ==========================
# 今日趋势
# ==========================
def today_trend():

    data = []

    hours = []

    stat = hourly_statistics()

    for i in range(24):

        h = "{:02}".format(i)

        hours.append(h)

        data.append(stat.get(h, 0))

    return {

        "hours": hours,

        "count": data

    }


# ==========================
# 最近进入人员
# ==========================
def latest_people(number=10):

    records = sorted(

        o.LOCK_RECORD.values(),

        key=lambda x: x["enter_time"],

        reverse=True

    )

    return records[:number]


# ==========================
# 停留时间分布
# ==========================
def stay_distribution():

    data = {

        "30分钟以内": 0,

        "30~60分钟": 0,

        "1~2小时": 0,

        "2小时以上": 0

    }

    for record in o.LOCK_RECORD.values():

        if record["stay_time"] == "":
            continue

        h, m, s = map(int, record["stay_time"].split(":"))

        minute = h * 60 + m

        if minute < 30:

            data["30分钟以内"] += 1

        elif minute < 60:

            data["30~60分钟"] += 1

        elif minute < 120:

            data["1~2小时"] += 1

        else:

            data["2小时以上"] += 1

    return data


# ==========================
# 人流高峰
# ==========================
def peak_hour():

    stat = hourly_statistics()

    if len(stat) == 0:

        return None

    hour = max(stat, key=stat.get)

    return {

        "hour": hour,

        "count": stat[hour]

    }


# ==========================
# 首页统计数据
# ==========================
def dashboard():

    return {

        "today_total": today_total(),

        "online_total": online_total(),

        "leave_total": leave_total(),

        "average_stay": average_stay_time(),

        "peak_hour": peak_hour()

    }


# ==========================
# ECharts折线图数据
# ==========================
def line_chart():

    trend = today_trend()

    return {

        "x": trend["hours"],

        "y": trend["count"]

    }


# ==========================
# ECharts饼图数据
# ==========================
def pie_chart():

    dist = stay_distribution()

    return [

        {

            "name": key,

            "value": value

        }

        for key, value in dist.items()

    ]