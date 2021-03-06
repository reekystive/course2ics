import requests
import re
from typing import List
from configparser import ConfigParser
from calender import Calender, Event
import datetime

# For build
import os
prefix = './'
if not os.path.exists('main.py'):
    prefix = '../'


class Config:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password


class EAMS:
    semesters = None

    def __init__(self, config: Config) -> None:
        self.config = config
        self.s = requests.Session()
        self.is_logged_in = False
        self.is_logged_in_eams = False
        # print('Init for user', self.config.username)
        ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0)' + \
            ' Gecko/20100101 Firefox/88.0'
        self.s.headers.update({'User-Agent': ua})

    def login(self) -> None:
        "执行用户登录"

        # print('Logging in')
        url = 'https://id.sspu.edu.cn/cas/login'
        r = self.s.get(url)

        # 登录
        txt = re.sub(r'\s*', '', r.text)
        lt = re.match(r'.*?name="lt"\s*value="(.*?)".*', txt) \
            .group(1).strip()
        data = {
            'username': self.config.username,
            'password': self.config.password,
            # 'imageCodeName': '',
            'errors': '0',
            'lt': lt,
            '_eventId': 'submit'
        }
        r = self.s.post(url=url, data=data)

        # 检查是否登录成功
        if r.text.find('class="success"') != -1:
            # print('Login success')
            self.is_logged_in = True
        else:
            # print('Login failed')
            self.is_logged_in = False

    def login_eams(self) -> None:
        "登录教务系统"

        # print('Logging in EAMS')
        self.s.get('https://jx.sspu.edu.cn/eams/login.action')
        cookies = self.s.cookies.items()
        success = False
        for item in cookies:
            if item[0] == 'JSESSIONID' and '.-worker' in item[1]:
                success = True
                break
        if not success:
            # print('Login EAMS failed')
            self.is_logged_in_eams = False
            return
        # print('Login EAMS success')
        self.is_logged_in_eams = True

    def get_all_semesters(self) -> List:
        "获得所有学期编号"

        url = 'https://jx.sspu.edu.cn/eams/dataQuery.action'
        r = self.s.post(url=url, data={'dataType': 'semesterCalendar'})

        conf = r.text.strip()
        conf = re.sub(r'^{.*,semesters:', '', conf, count=1)
        conf = re.sub(r',yearIndex:.*}$', '', conf, count=1)
        conf = re.sub(r'^{y0:\[{', '', conf, count=1)
        conf = re.sub(r'}\]}$', '', conf, count=1)
        conf = re.sub(r'],\w+:\[', ',', conf)

        confs = re.split(r'},{', conf)
        res = []
        for item in confs:
            cur = re.match(r'id:(\d+),schoolYear:"(.+)",name:"(.+)"', item)
            id = cur.group(1)
            year = cur.group(2)
            name = cur.group(3)
            res.append({'id': int(id), 'year': year, 'name': name})

        self.semesters = res
        return res

    def display_semesters(self) -> None:
        "显示最近 6 个学期"

        if self.semesters == None:
            self.get_all_semesters()
        sems = self.semesters
        sems = sems[-6:]
        for it in sems:
            print(f'id: {it["id"]}, semester: {it["year"]} {it["name"]}学期')

    def get_courses(self, semester: int) -> List:
        "获取指定学期的课程信息"

        ids_url = 'https://jx.sspu.edu.cn/eams/courseTableForStd.action'
        r = self.s.get(ids_url)
        txt = re.sub(r'\s*', '', r.text)
        grp = re.match(
            r'.*?function\s*refreshTable\(.*?\).*?"std".*?"ids","(\d+)".*', txt)
        ids = grp.group(1)

        url = 'https://jx.sspu.edu.cn/eams/courseTableForStd!courseTable.action'
        data = {
            'ignoreHead': '1',
            'setting.kind': 'std',
            'startWeek': '1',
            'semester.id': str(semester),
            'ids': ids
        }
        r = self.s.post(url=url, data=data)

        txt = r.text.strip().replace('\n', '')
        txt = re.sub(r'^.*var index=\d+;\s*var activity=\w+;',
                     '', txt, count=1)
        txt = re.sub(r'table\d*.marshalTable\(\d+,\d+,\d+\);.*$',
                     '', txt, count=1)
        txt = txt.strip().replace('\t', '')

        courses = []
        txts = re.split(r'activity = new TaskActivity', txt)[1:]
        for item in txts:
            temp = re.split(r';', item)[:-1]

            start = re.match(
                r'^index\s*=(\d+)\*unitCount\+(\d+)$', temp[1].strip())
            end = re.match(
                r'^index\s*=(\d+)\*unitCount\+(\d+)$', temp[-2].strip())
            start_time = (int(start.group(1)) + 1, int(start.group(2)) + 1)
            end_time = (int(end.group(1)) + 1, int(end.group(2)) + 1)

            inf_txt = re.match(r'^\s*\((.*)\)\s*$', temp[0].strip()).group(1)
            inf = re.match(
                r'^".*","(.*)",".*","(.*)",".*","(.*)","(.*)",".*",".*"$', inf_txt)
            teacher = inf.group(1).strip()
            course_name_raw = inf.group(2).strip()
            location = inf.group(3).strip()
            weeks_txt = inf.group(4).strip()

            name_group = re.match(r'^(.*)\((\d+)\)$', course_name_raw)
            course_name = name_group.group(1).strip()
            course_code = name_group.group(2).strip()

            weeks = []
            for i in range(len(weeks_txt)):
                if weeks_txt[i] == '1':
                    weeks.append(i)

            course = {
                'start': start_time,
                'end': end_time,
                'weeks': weeks,
                'name': course_name,
                'code': course_code,
                'teacher': teacher,
                'location': location
            }
            courses.append(course)
        return courses

    def generate_ics(self, courses: List, first_date: str) -> None:
        "生成 ICS 文件. first_date: 第一周的周一对应的日期"

        c = Calender()
        for course in courses:
            for week in course['weeks']:
                delta_days = 7 * (week - 1) + (course['start'][0] - 1)
                first = datetime.datetime.strptime(first_date, '%Y-%m-%d')
                delta = datetime.timedelta(days=delta_days)
                day = first + delta
                day_str = day.strftime('%Y-%m-%d')

                cfg = ConfigParser()
                cfg.read(prefix + 'config.ini')
                temp = cfg.get('time-table', str(course['start'][1])).strip()
                begin_time = temp.split('-')[0].strip()
                temp = cfg.get('time-table', str(course['end'][1])).strip()
                end_time = temp.split('-')[1].strip()
                begin_str = day_str + ' ' + begin_time.strip()
                end_str = day_str + ' ' + end_time.strip()

                e = Event()
                e.name = course['name']
                e.begin = begin_str
                e.end = end_str

                disc = ''
                disc += '授课地点: ' + course['location'] + '\n'
                disc += '课程序号: ' + course['code'] + '\n'
                disc += '授课老师: ' + course['teacher']
                e.description = disc

                e.identifier = begin_str + ' ' + course['code']
                # used to generate uid

                c.add(e)

        with open(prefix + 'courses.ics', 'w', encoding='utf-8', newline='\n') as ics_file:
            ics_file.write(c.get_str())
