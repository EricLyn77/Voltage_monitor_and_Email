import psutil
from psutil._common import bytes2human

usage=psutil.disk_usage('/media/pi/A0A29269A2924426')
print(bytes2human(usage.free))
