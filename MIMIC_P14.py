#!/usr/bin/python3

'''
MIMIC_P14.py
14-11-2020
MIMIC Panel TV RasPI control Terminal
'''

#Peripheral related
import smbus
from gpiozero import LED, Button
import serial
import os
from os import path
from os import system
from os import listdir
from time import sleep, time_ns
from datetime import datetime
import threading
import sys
from sys import argv
import logging
from subprocess import call

spp = serial.Serial('/dev/ttyS0', baudrate = 115200) #or /dev/ttyS0
spp.timeout = 0.3
global Fault_flag , debounce

Fault_flag = 0
debounce = 0
Fault_list =[]
Fault_list = ['0']*616    #created a list with 616 0s
LM3_flag = 0
LM4_flag = 0
LM5_flag = 0
LM6_flag = 0


def listtostring(s):
    str1 = ""
    return(str1.join(s))

def getStatus(logFile, txEnable):
    global spp,cnt
    cnt = 0
    sensorStatus = 0
    scan_result = []
    logFile.seek(0) #For overwriting to the same line for every scan
    for i in range(1,12):
        cmd=[60,7,i,255,1,165,62]
        cmdBytes=bytes(cmd)
        try:
            txEnable.on()
            spp.write(cmdBytes)
            spp.flush()
            txEnable.off()
            sleep(0.1)
            sensorStatus=spp.read(16)
            Payload = sensorStatus[5:12] #Extract the payload
        except serial.SerialTimeoutException:
            pass
        except:
            print('Unkown serial exception occured')
        for eb in Payload:
            data_byte = '{0:08b}'.format(eb)
            for i in range(8):
                scan_result.append(data_byte[i])           
    #print(len(scan_result), ' Status bits received')
    for line in scan_result:
            logFile.write(line)
            logFile.write('\n')
            logFile.flush()
    if LM3.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        RLY4.on()
        #if(LM3_flag == 0):
            #LM3_flag = 1
            #RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM3_flag = 0
        

    if LM4.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        RLY4.on()
        #if(LM4_flag == 0):
            #LM4_flag = 1
            #RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM4_flag = 0
        
    if LM5.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        RLY4.on()
        #if(LM5_flag == 0):
            #LM5_flag = 1
            #RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM5_flag = 0
        
    if LM6.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        RLY4.on()
        #if(LM6_flag == 0):
            #LM6_flag = 1
            #RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM6_flag = 0

    
         
         



    for count in range(len(scan_result)):
        if(scan_result[count] == '1'):
            cnt = cnt+1
            #print(f"switch triggered at {count}")
            #print(cnt)
        

        if((scan_result[count] == '1') and (Fault_list[count] == '0')) :
            Fault_list[count] = '1'
            RLY3.on()   #Hooter on 
        if(scan_result[count] == '0'):
            Fault_list[count] = '0'
        

    if (cnt >= 1):
        Fault_flag = 1
    if (cnt == 0):
        Fault_flag = 0
        
    if((Fault_flag == 0)and (LM3_flag == 0) and (LM4_flag == 0) and (LM5_flag == 0 )and (LM6_flag == 0)):
        RLY3.off()                   #RLY4 - Bulb
        RLY4.off()                   #RLY3 - Hooter
       
    
    if(Fault_flag == 1):
        #RLY3.on()
        RLY4.on()
    
    scan_result.clear()      
    print('\n---------------------scan completed-----------------------\n')    

if __name__ == '__main__':
    fileforlog = open('/var/www/html/MIMIC_TV_Log.txt', "w")
    #Init all Outputs
    RLY1 = LED(21)
    RLY2 = LED(20)
    RLY3 = LED(26)
    RLY4 = LED(16)
    RLY5 = LED(19)
    RLY6 = LED(13)
    RLY7 = LED(12)
    D5L = LED(23)
    Q2B = LED(4)
    TRE = LED(18)

    RLY1.off()
    RLY2.off()
    RLY3.off()
    RLY4.off()
    RLY5.off()
    RLY6.off()
    RLY7.off()
    D5L.off()
    Q2B.on()
    TRE.off()
    
    #Init all Inputs
    LM1 = Button(10)
    LM2 = Button(9)
    LM3 = Button(25)
    LM4 = Button(11)
    LM5 = Button(8)
    LM6 = Button(7)
    #LM7 = Button(5)
    LM8 = Button(6)

    #Enable Required Threads
    
    while True:
        if LM1.is_pressed:      #scan switch
            D5L.on()
            getStatus(fileforlog, TRE)
            D5L.off()
            getStatus(fileforlog, TRE)
        
        else:
            RLY3.off()
            RLY4.off()
        if LM2.is_pressed:
            sleep(0.1)
            debounce = debounce+1
            RLY3.off()

        else :
            debounce = 0
        if(debounce > 20):
            os.system("shutdown now -h")
        #print(debounce)
                      
    print('Exiting')

    
