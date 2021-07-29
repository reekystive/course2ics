# CourseTable2ICS

Convert course table to ICS for SSPU

如果你是上海第二工业大学的学生，你可以用这个工具来生成你的课程表对应的 [ICS 文件](https://zh.wikipedia.org/wiki/ICalendar)来导入导入各种日历软件中。

## 快速开始

下载 [Releases](https://github.com/ReekyStive/CourseTable2ICS/releases/latest) 中打包好的版本即可开始使用（仅限 Windows）。

## 从源代码运行

你需要有 Python3。

### 安装依赖

本工具仅使用了 `requests` 第三方包。

``` bash
$ pip install -r requirements.txt
# maybe pip3
```

### 运行

``` bash
$ python main.py
# maybe python3
```

根据提示即可生成 ICS 文件。

## Screenshot

### 运行截图

<img width="682" alt="Screen Shot 2021-07-29 at 04 52 04" src="https://user-images.githubusercontent.com/26853900/127394283-db33a8f4-25d7-4031-9753-4f709c107595.png">

### 效果截图 (Google Calendar)

<img width="766" alt="Screen Shot 2021-07-29 at 05 32 43" src="https://user-images.githubusercontent.com/26853900/127399661-8f2a5b17-928e-4fc0-97d3-de3d910615f9.png">

## TODO

- [ ] 将同一课程的事件合并为一个 (利用 repeat)
