import time
import threading


class TwitterSnowFlakeIdGenerator(object):
    def __init__(self):
        self.center_id = 0  # 数据中心ID
        self.node_id = 0  # 机器ID
        self.start_millisecond = 1611458635000  # 2021-01-24 11:23:55
        self.last_millisecond = self.start_millisecond  # 起点时间戳
        self.sequence = 0
        self.sequence_mask = 4096
        self.lock = threading.Lock()  # 互斥锁

    def __timestamp_compare__(self, now_millisecond):
        if now_millisecond > self.last_millisecond:
            self.sequence = 0
        elif now_millisecond == self.last_millisecond:
            self.sequence += 1
            if self.sequence == self.sequence_mask:
                self.sequence = 0
        else:
            pass
        # 此时同处一毫秒内，应自增sequence

    def next_id(self):
        now_millisecond = int(time.time() * 1000)  # 毫秒级别
        self.lock.acquire()
        self.__timestamp_compare__(now_millisecond)
        # 0(1) 000....000(41) 0000000000(10) 000000000000(12)
        # 高1位：固定0
        # 随后41位: 时间戳
        # 随后10位: 高5位是数据中心ID，低5位是机器ID
        # 低12位: 自增序列，如果1ms内有一个机器多次请求，要求自增序列自增
        # 转换成10进制总共20位
        result = '%(number)020d' % {
            'number': (((now_millisecond - self.start_millisecond) << 22) | (self.center_id << 17) | (
                        self.node_id << 12) | self.sequence)}
        self.last_millisecond = now_millisecond
        self.lock.release()
        return result


media_id_generator = TwitterSnowFlakeIdGenerator()
