class Employee:

    def __init__(self,id,name,code):
        self.id = id
        self.name = name
        self.code = code

LOCK_RECORD = dict()
EMPLOYEES = list()
MAX_ID = 0
WORK_LEN = 6
CODE_LEN = 6
WORK_TIME = '8:00-17:00'
CLOSING_TIME = '17:00'
USERS = dict()

def add(e:Employee):
        EMPLOYEES.append(e)

def remove(id):
    for emp in EMPLOYEES:
        if str(id) == str(emp.id):
            EMPLOYEES.remove(emp)
            if emp.name in LOCK_RECORD.keys():
                del LOCK_RECORD[emp.name]
                break

def get_new_id():
    global MAX_ID
    MAX_ID += 1
    return MAX_ID