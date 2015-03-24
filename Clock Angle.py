import time as time2
def clock_angle(time):
    hour, minute = [int(x) for x in time.split(':')]
    minute_angle = minute * 6
    hour_angle = ((hour % 12) + minute / 60) / 12 * 360
    result = round(abs(minute_angle - hour_angle), 1)
    print()
    print('time', time)
    print(hour_angle, minute_angle, 'result', result)
    time2.sleep(0.1)
    return min(result, 360 - result)

print(clock_angle("02:30"))


if __name__ == '__main__':
    #These "asserts" using only for self-checking and not necessary for auto-testing
    assert clock_angle("02:30") == 105, "02:30"
    assert clock_angle("13:42") == 159, "13:42"
    assert clock_angle("01:42") == 159, "01:42"
    assert clock_angle("01:43") == 153.5, "01:43"
    assert clock_angle("00:00") == 0, "Zero"
    assert clock_angle("12:01") == 5.5, "Little later"
    assert clock_angle("18:00") == 180, "Opposite"