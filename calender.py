from typing import List
import uuid


class Event:
    name = ''
    begin = ''
    end = ''
    description = ''
    identifier = ''  # used to generate uid

    def __init__(self) -> None:
        pass

    def get_str(self) -> None:
        begin_str = self.begin.strip() \
            .replace(' ', 'T').replace('-', '').replace(':', '') + '00'
        end_str = self.end.strip() \
            .replace(' ', 'T').replace('-', '').replace(':', '') + '00'
        disc_str = self.description.strip() \
            .replace('\n', '\\n')
        name_str = self.name.strip() \
            .replace('\n', '\\n')

        namespace = uuid.UUID('7e6ec0dd-0d77-41d1-82b4-4469894007dd')
        uid_str = str(uuid.uuid3(namespace, self.identifier))
        uid_str = uid_str + '@' + uid_str[:4] + '.org'

        s = ''
        s += 'BEGIN:VEVENT\n'
        s += 'DTSTART;TZID=Asia/Shanghai:' + begin_str + '\n'
        s += 'DTEND;TZID=Asia/Shanghai:' + end_str + '\n'
        s += 'UID:' + uid_str + '\n'
        s += 'DESCRIPTION:' + disc_str + '\n'
        s += 'SUMMARY:' + name_str + '\n'
        s += 'END:VEVENT'
        return s


class Calender:
    events = []

    def __init__(self, events: List = []) -> None:
        self.events = events

    def get_str(self) -> str:
        time_zone = """
        BEGIN:VTIMEZONE
        TZID:Asia/Shanghai
        BEGIN:STANDARD
        TZOFFSETFROM:+0800
        TZOFFSETTO:+0800
        TZNAME:CST
        DTSTART:19700101T000000
        END:STANDARD
        END:VTIMEZONE
        """.strip().replace(' ', '')

        s = ''
        s += 'BEGIN:VCALENDAR\n'
        s += 'PRODID:CourseTable2ICS by ReekyStive\n'
        s += 'VERSION:2.0\n'
        s += time_zone + '\n'

        for event in self.events:
            s += event.get_str()
            s += '\n'

        s += 'END:VCALENDAR\n'
        return s

    def add(self, event: Event):
        self.events.append(event)
