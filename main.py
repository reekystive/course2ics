from course import Config, EAMS

username = input('请输入学号: ').strip()
password = input('请输入密码: ')
print()

config = Config(username, password)
e = EAMS(config)
e.login()
e.login_eams()

print()
sems = e.get_all_semesters()
e.display_semesters()
sem = input('请选择学期 ID (默认为最后一个学期): ').strip()
print()

if sem == '':
    sem = sems[-1]['id']
else:
    sem = int(sem)

rev_sems = sems
rev_sems.reverse()
sem_name = ''
for item in rev_sems:
    if item['id'] == sem:
        sem_name = item['year'] + ' ' + item['name'] + '学期'
        break

print(f'正在获取 {sem_name} 课程信息')
courses = e.get_courses(sem)

first_date = input('请输入第一周的第一天对应的日期 (e.g. 2021-08-02): ').strip()
print('正在生成 ICS 文件')
e.generate_ics(courses, first_date)

print('完成')
