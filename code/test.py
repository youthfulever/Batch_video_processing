from datetime import datetime


def calculate_time_difference(time1, time2):
    format_str = '%H:%M:%S.%f'
    dt1 = datetime.strptime(time1, format_str)
    dt2 = datetime.strptime(time2, format_str)
    time_diff = dt2 - dt1

    return time_diff.total_seconds()*1000


print(calculate_time_difference('00:00:00.000','00:01:50.010'))