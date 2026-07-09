import cv2
from util import public_tools as tool
from util import io_tools as io
from service import recognize_service as rs
from service import hr_service as hr
from service import attendance_service as ats
from service import record_service as rds

ESC_KEY = 27
ENTER_KEY = 13


# ==========================
# 注册人员（采集3张人脸照片）
# ==========================
def register(code):

    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    success, frame = cameraCapture.read()

    shooting_time = 0

    while success:

        cv2.imshow("Register", frame)

        success, frame = cameraCapture.read()

        key = cv2.waitKey(1)

        if key == ESC_KEY:
            break

        if key == ENTER_KEY:

            photo = cv2.resize(
                frame,
                (io.IMG_WIDTH, io.IMG_HEIGHT)
            )

            img_name = (
                    io.PIC_PATH
                    + str(code)
                    + str(tool.randomNumber(8))
                    + ".png"
            )

            cv2.imwrite(img_name, photo)

            shooting_time += 1

            print("成功采集第{}张照片".format(shooting_time))

            if shooting_time >= 3:
                break

    cv2.destroyAllWindows()

    cameraCapture.release()

    io.load_employee_pic()


# ==========================
# 人员进入体育馆
# ==========================
def clock_in():

    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    success, frame = cameraCapture.read()

    while success:

        cv2.imshow("Gym Check In", frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if rs.found_face(gray):

            gray = cv2.resize(
                gray,
                (io.IMG_WIDTH, io.IMG_HEIGHT)
            )

            code = rs.recognise_face(gray)

            if code != -1:

                name = hr.get_name_with_code(code)

                if name is not None:

                    emp = hr.get_employee_by_name(name)

                    person = {

                        "id": emp.id,

                        "name": emp.name

                    }

                    # 已经在馆
                    if ats.is_online(code):

                        print("{} 已经在馆".format(name))

                    else:

                        record = ats.person_enter(person)

                        if record is not None:

                            rds.save_record(record)

                            print("--------------------------------")

                            print("识别成功")

                            print("姓名：", record["name"])

                            print("第{}位进入体育馆".format(
                                record["arrival_order"]
                            ))

                            print("进入时间：", record["enter_time"])

                            print("--------------------------------")

                            cv2.destroyAllWindows()

                            cameraCapture.release()

                            return record

        success, frame = cameraCapture.read()

        if cv2.waitKey(1) == ESC_KEY:
            break

    cv2.destroyAllWindows()

    cameraCapture.release()

    return None


# ==========================
# 人员离馆
# ==========================
def clock_out(person_id):

    record = ats.person_leave(person_id)

    if record is None:

        print("未找到该人员")

        return None

    rds.update_record(record)

    print("--------------------------------")

    print("姓名：", record["name"])

    print("离馆时间：", record["leave_time"])

    print("停留时间：", record["stay_time"])

    print("--------------------------------")

    return record


# ==========================
# 摄像头实时预览
# ==========================
def preview():

    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    success, frame = cameraCapture.read()

    while success:

        cv2.imshow("Camera Preview", frame)

        success, frame = cameraCapture.read()

        if cv2.waitKey(1) == ESC_KEY:
            break

    cv2.destroyAllWindows()

    cameraCapture.release()


# ==========================
# 摄像头实时识别（不打卡）
# ==========================
def recognize():

    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    success, frame = cameraCapture.read()

    while success:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if rs.found_face(gray):

            gray = cv2.resize(
                gray,
                (io.IMG_WIDTH, io.IMG_HEIGHT)
            )

            code = rs.recognise_face(gray)

            if code != -1:

                name = hr.get_name_with_code(code)

                cv2.putText(

                    frame,

                    name,

                    (20, 40),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    1,

                    (0, 255, 0),

                    2

                )

        cv2.imshow("Recognition", frame)

        success, frame = cameraCapture.read()

        if cv2.waitKey(1) == ESC_KEY:
            break

    cv2.destroyAllWindows()

    cameraCapture.release()