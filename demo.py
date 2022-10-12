"""Sample code and test for adafruit_in219"""

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
import os

import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header

import schedule
import psutil
from psutil._common import bytes2human

def getDiscDir():
    cmd = 'df -h'
    data = os.popen(cmd)
    res = data.read()
    res = res.splitlines()
    ssd_info = res[-1].strip().split(' ')
    ssd_info = [s for s in ssd_info if s != '']
    flag = True
    if ssd_info[0] != '/dev/sda1':
        flag = False
    storage = int(ssd_info[4][0])
    ssd_dir = []
    ssd_dir = ssd_info[-2] + ' ' + ssd_info[-1]
    return ssd_dir
 
def voltage():
    i2c_bus = board.I2C()

    ina1 = INA219(i2c_bus,addr=0x40)
    ina2 = INA219(i2c_bus,addr=0x41)
    ina3 = INA219(i2c_bus,addr=0x42)

    print("ina219 test")

    ina1.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina1.bus_voltage_range = BusVoltageRange.RANGE_16V

    ina2.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina2.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina2.bus_voltage_range = BusVoltageRange.RANGE_16V

    ina3.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina3.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina3.bus_voltage_range = BusVoltageRange.RANGE_16V


    # measure and display loop
    bus_voltage1 = ina1.bus_voltage        # voltage on V- (load side)
    shunt_voltage1 = ina1.shunt_voltage    # voltage between V+ and V- across the shunt
    power1 = ina1.power
    current1 = ina1.current                # current in mA

    bus_voltage2 = ina2.bus_voltage        # voltage on V- (load side)
    shunt_voltage2 = ina2.shunt_voltage    # voltage between V+ and V- across the shunt
    power2 = ina2.power
    current2 = ina2.current                # current in mA
    
    bus_voltage3 = ina3.bus_voltage        # voltage on V- (load side)
    shunt_voltage3 = ina3.shunt_voltage    # voltage between V+ and V- across the shunt
    power3 = ina3.power
    current3 = ina3.current                # current in mA
    

    
    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage1 + shunt_voltage1),(shunt_voltage1),(bus_voltage1),(power1),(current1/1000)))
    print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage2 + shunt_voltage2),(shunt_voltage2),(bus_voltage2),(power2),(current2/1000)))
    print("PSU Voltage:{:6.3f}V    Shunt Voltage:{:9.6f}V    Load Voltage:{:6.3f}V    Power:{:9.6f}W    Current:{:9.6f}A".format((bus_voltage3 + shunt_voltage3),(shunt_voltage3),(bus_voltage3),(power3),(current3/1000)))
    print("")
    print("")
    
    try:
        usage=psutil.disk_usage(getDiscDir())    
        sendContent = 'battery voltage is: ' + str(bus_voltage2 + shunt_voltage2)+'\n' + 'rest space for hard drive: ' + str(usage.free) + 'kb'
    except:
        sendContent = 'battery voltage is: ' + str(bus_voltage2 + shunt_voltage2)+'\n' + 'rest space for hard drive: ' + str(-1)
    sender = 'lidarunr@gmail.com'
    receivers = ['lidarunr@gmail.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
    
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(sendContent, 'plain', 'utf-8')
    message['From'] = Header("voltage", 'utf-8')   # 发送者
    message['To'] =  Header("voltage", 'utf-8')        # 接收者
 
    subject = 'voltage test'
    message['Subject'] = Header(subject, 'utf-8')
 
 
    user = 'lidarunr@gmail.com'
    password = 'extsiyrrohtwgtuz'
 
    smtpserver = 'smtp.gmail.com'
    try: 
        smtp = smtplib.SMTP_SSL(smtpserver,465)
        smtp.login(user,password)
        smtp.sendmail(sender, receivers, message.as_string())
    except:
        pass
    


time.sleep(30)
voltage()

schedule.every(45).minutes.do(voltage)


while True:
    schedule.run_pending()
    time.sleep(1)
    
    





