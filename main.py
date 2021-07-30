from course import Config, EAMS
from configparser import ConfigParser
from getpass import getpass
import sys

cfg = ConfigParser()
cfg.read('config.ini')
pause_cfg = cfg.get('on-exit', 'pause-on-exit').strip().lower()
pause_on_exit = False
if pause_cfg == 'true':
    pause_on_exit = True


def pause() -> None:
    if not pause_on_exit:
        return
    sys.stdin.flush()
    input('按回车键退出...')


print('==== CourseTable2ICS for SSPU by ReekyStive ====')
username = input('请输入学号: ').strip()
password = getpass('请输入密码 (输入时不可见): ')
print()

config = Config(username, password)
e = EAMS(config)
try:
    print('正在登录统一认证...', end=' ')
    sys.stdout.flush()
    e.login()
    if e.is_logged_in == False:
        sys.exit(1)
    print('成功')

    print('正在登录教务系统...', end=' ')
    sys.stdout.flush()
    e.login_eams()
    if e.is_logged_in == False:
        sys.exit(1)
    print('成功')
except:
    print('失败')
    pause()
    sys.exit(1)
print()

sems = e.get_all_semesters()
e.display_semesters()
sem = input('请输入学期 ID (默认为最后一个学期): ').strip()

if sem == '':
    sem = sems[-1]['id']
else:
    sem = int(sem)

rev_sems = sems
rev_sems.reverse()

while True:
    sem_name = None
    for item in rev_sems:
        if item['id'] == sem:
            sem_name = item['year'] + ' ' + item['name'] + '学期'
            break

    if sem_name == None:
        while True:
            try:
                sem = input('学期 ID 有误, 请重新输入: ').strip()
                sem = int(sem)
                break
            except:
                continue
    else:
        print()
        print(f'正在获取 {sem_name} 课程信息')
        courses = e.get_courses(sem)
        break

if len(courses) == 0:
    print('未找到任何课程')
    pause()
    sys.exit(1)

print('找到课程:')
for item in courses:
    print(f'[{str(item["code"])}] {str(item["name"])}')
print()

date = input('请输入第一周的第一天对应的日期 (e.g. 2021-09-13): ').strip()

while True:
    if len(date.split('-')) == 3:
        temp = date.split('-')
        try:
            temp[0] = str(int(temp[0])).zfill(4)
            temp[1] = str(int(temp[1])).zfill(2)
            temp[2] = str(int(temp[2])).zfill(2)
            if len(temp[0]) == 4 and len(temp[1]) == 2 and len(temp[2]) == 2:
                date = temp[0] + '-' + temp[1] + '-' + temp[2]
                break
        except:
            pass
    date = input('日期格式有误, 请重新输入: ').strip()

print('正在生成 ICS 文件')
try:
    e.generate_ics(courses, date)
except:
    print('失败')
    pause()
    sys.exit(1)
print('已保存: courses.ics')
pause()
