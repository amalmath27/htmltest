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
    global LM3_flag,LM4_flag,LM5_flag,LM6_flag
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
    print(len(scan_result), ' Status bits received')
    for line in scan_result:
            logFile.write(line)
            logFile.write('\n')
            logFile.flush()
    if LM3.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        #RLY4.on()  #commented on 29th
        if(LM3_flag == 0):
            LM3_flag = 1
            RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM3_flag = 0
        

    if LM4.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        #RLY4.on()  #commented on 29th
        if(LM4_flag == 0):
            LM4_flag = 1
            RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM4_flag = 0
        
    if LM5.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        #RLY4.on()  #commented on 29th
        if(LM5_flag == 0):
            LM5_flag = 1
            RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM5_flag = 0
        
    if LM6.is_pressed:
        logFile.write('0')
        logFile.write('\n')
        logFile.flush()
        #RLY4.on()  #commented on 29th
        if(LM6_flag == 0):
            LM6_flag = 1
            RLY3.on() 
    else:
        logFile.write('1')
        logFile.write('\n')
        logFile.flush()
        LM6_flag = 0

    
         
         



    for count in range(len(scan_result)):
        if(scan_result[count] == '0'):    #changed this for debugging , change it later to 1 , also comment debug message
            cnt = cnt+1
            print(f"switch triggered at {count}")
            #print(cnt)  #uncoment it later
        

        if((scan_result[count] == '1') and (Fault_list[count] == '0')) :
            Fault_list[count] = '1'
            RLY3.on()   #Hooter on 
        if(scan_result[count] == '0'):
            Fault_list[count] = '0'

    if((scan_result[131] == '1')  or(scan_result[130] == '1') or (scan_result[129] == '1') or (scan_result[128] == '1') or
        (scan_result[127] == '1') or(scan_result[126] == '1') or(scan_result[125] == '1') or(scan_result[123] == '1') or
        (scan_result[122] == '1') or(scan_result[121] == '1') or(scan_result[120] == '1') or(scan_result[119] == '1') or
        (scan_result[118] == '1') or(scan_result[117] == '1') or(scan_result[116] == '1') or(scan_result[115] == '1') or
        (scan_result[114] == '1') or(scan_result[147] == '1') or(scan_result[148] == '1') or(scan_result[149] == '1') or
        (scan_result[150] == '1') or(scan_result[151] == '1') or(scan_result[152] == '1') or(scan_result[153] == '1') or
        (scan_result[155] == '1') or(scan_result[156] == '1') or(scan_result[157] == '1') or(scan_result[158] == '1') or
        (scan_result[159] == '1') or(scan_result[160] == '1') or(scan_result[161] == '1') or(scan_result[162] == '1') or
        (scan_result[163] == '1') or(scan_result[164] == '1') or(scan_result[113] == '1') or(scan_result[112] == '1') or
        (scan_result[195] == '1') or(scan_result[194] == '1') or(scan_result[193] == '1') or(scan_result[191] == '1') or
        (scan_result[190] == '1') or(scan_result[189] == '1') or(scan_result[188] == '1') or(scan_result[187] == '1') or
        (scan_result[186] == '1') or(scan_result[185] == '1') or(scan_result[184] == '1') or(scan_result[183] == '1') or
        (scan_result[182] == '1') or(scan_result[165] == '1') or(scan_result[166] == '1') or(scan_result[167] == '1') or
        (scan_result[196] == '1') or(scan_result[197] == '1') or(scan_result[199] == '1') or(scan_result[200] == '1') or
        (scan_result[201] == '1') or(scan_result[202] == '1') or(scan_result[203] == '1') or(scan_result[204] == '1') or
        (scan_result[205] == '1') or(scan_result[206] == '1') or(scan_result[207] == '1') or(scan_result[208] == '1') or
        (scan_result[181] == '1') or(scan_result[180] == '1') or(scan_result[179] == '1') or(scan_result[178] == '1') or
        (scan_result[177] == '1') or(scan_result[176] == '1') or(scan_result[173] == '1') or(scan_result[172] == '1') or
        (scan_result[171] == '1') or(scan_result[170] == '1') or(scan_result[169] == '1') or(scan_result[168] == '1') or
        (scan_result[251] == '1') or(scan_result[250] == '1') or(scan_result[249] == '1') or(scan_result[248] == '1') or
        (scan_result[209] == '1') or(scan_result[210] == '1') or(scan_result[211] == '1') or(scan_result[212] == '1') or
        (scan_result[213] == '1') or(scan_result[214] == '1') or(scan_result[217] == '1') or(scan_result[218] == '1') or
        (scan_result[219] == '1') or(scan_result[220] == '1') or(scan_result[221] == '1') or(scan_result[222] == '1') or
        (scan_result[223] == '1') or(scan_result[252] == '1') or(scan_result[253] == '1') or(scan_result[254] == '1') or
        (scan_result[247] == '1') or(scan_result[246] == '1') or(scan_result[245] == '1') or(scan_result[244] == '1') or
        (scan_result[243] == '1') or(scan_result[242] == '1') or(scan_result[241] == '1') or(scan_result[240] == '1') or
        (scan_result[239] == '1') or(scan_result[238] == '1') or(scan_result[237] == '1') or(scan_result[236] == '1') or
        (scan_result[235] == '1') or(scan_result[234] == '1') or(scan_result[233] == '1') or(scan_result[232] == '1') or
        (scan_result[231] == '1') or(scan_result[255] == '1') or(scan_result[256] == '1') or(scan_result[257] == '1') or
        (scan_result[258] == '1') or(scan_result[259] == '1') or(scan_result[260] == '1') or(scan_result[261] == '1') or
        (scan_result[262] == '1') or(scan_result[263] == '1') or(scan_result[264] == '1') or(scan_result[265] == '1') or
        (scan_result[266] == '1') or(scan_result[267] == '1') or(scan_result[268] == '1') or(scan_result[269] == '1') or
        (scan_result[270] == '1') or(scan_result[271] == '1') or(scan_result[229] == '1') or(scan_result[228] == '1') or
        (scan_result[227] == '1') or(scan_result[226] == '1') or(scan_result[225] == '1') or(scan_result[224] == '1') or
        (scan_result[305] == '1') or(scan_result[304] == '1') or(scan_result[303] == '1') or(scan_result[302] == '1') or
        (scan_result[301] == '1') or(scan_result[300] == '1') or(scan_result[299] == '1') or(scan_result[298] == '1') or
        (scan_result[297] == '1') or(scan_result[296] == '1') or(scan_result[273] == '1') or(scan_result[274] == '1') or
        (scan_result[275] == '1') or(scan_result[276] == '1') or(scan_result[277] == '1') or(scan_result[278] == '1') or
        (scan_result[309] == '1') or(scan_result[310] == '1') or(scan_result[311] == '1') or(scan_result[312] == '1') or
        (scan_result[313] == '1') or(scan_result[314] == '1') or(scan_result[315] == '1') or(scan_result[316] == '1') or
        (scan_result[317] == '1') or(scan_result[318] == '1') or(scan_result[295] == '1') or(scan_result[294] == '1') or
        (scan_result[293] == '1') or(scan_result[292] == '1') or(scan_result[291] == '1') or(scan_result[290] == '1') or
        (scan_result[289] == '1') or(scan_result[288] == '1') or(scan_result[287] == '1') or(scan_result[286] == '1') or
        (scan_result[285] == '1') or(scan_result[284] == '1') or(scan_result[283] == '1') or(scan_result[282] == '1') or
        (scan_result[281] == '1') or(scan_result[280] == '1') or(scan_result[363] == '1') or(scan_result[319] == '1') or
        (scan_result[320] == '1') or(scan_result[321] == '1') or(scan_result[322] == '1') or(scan_result[323] == '1') or
        (scan_result[324] == '1') or(scan_result[325] == '1') or(scan_result[326] == '1') or(scan_result[327] == '1') or
        (scan_result[328] == '1') or(scan_result[329] == '1') or(scan_result[330] == '1') or(scan_result[331] == '1') or
        (scan_result[332] == '1') or(scan_result[333] == '1') or(scan_result[334] == '1') or(scan_result[335] == '1')):

        RLY4.on()   # R3 ON

    if((scan_result[131] == '0')  and  (scan_result[130] == '0') and (scan_result[129] == '0') and (scan_result[128] == '0') and
        (scan_result[127] == '0') and(scan_result[126] == '0') and(scan_result[125] == '0') and(scan_result[123] == '0') and
        (scan_result[122] == '0') and (scan_result[121] == '0')and(scan_result[120] == '0') and(scan_result[119] == '0') and
        (scan_result[118] == '0') and(scan_result[117] == '0') and(scan_result[116] == '0') and(scan_result[115] == '0') and
        (scan_result[114] == '0') and(scan_result[147] == '0') and(scan_result[148] == '0') and(scan_result[149] == '0') and
        (scan_result[150] == '0') and(scan_result[151] == '0') and(scan_result[152] == '0') and(scan_result[153] == '0') and
        (scan_result[155] == '0') and(scan_result[156] == '0') and(scan_result[157] == '0') and(scan_result[158] == '0') and
        (scan_result[159] == '0') and(scan_result[160] == '0') and(scan_result[161] == '0') and(scan_result[162] == '0') and
        (scan_result[163] == '0') and(scan_result[164] == '0') and(scan_result[113] == '0') and(scan_result[112] == '0') and
        (scan_result[195] == '0') and(scan_result[194] == '0') and(scan_result[193] == '0') and(scan_result[191] == '0') and
        (scan_result[190] == '0') and(scan_result[189] == '0') and(scan_result[188] == '0') and(scan_result[187] == '0') and
        (scan_result[186] == '0') and(scan_result[185] == '0') and(scan_result[184] == '0') and(scan_result[183] == '0') and
        (scan_result[182] == '0') and(scan_result[165] == '0') and(scan_result[166] == '0') and(scan_result[167] == '0') and
        (scan_result[196] == '0') and(scan_result[197] == '0') and(scan_result[199] == '0') and(scan_result[200] == '0') and
        (scan_result[201] == '0') and(scan_result[202] == '0') and(scan_result[203] == '0') and(scan_result[204] == '0') and
        (scan_result[205] == '0') and(scan_result[206] == '0') and(scan_result[207] == '0') and(scan_result[208] == '0') and
        (scan_result[181] == '0') and(scan_result[180] == '0') and(scan_result[179] == '0') and(scan_result[178] == '0') and
        (scan_result[177] == '0') and(scan_result[176] == '0') and(scan_result[173] == '0') and(scan_result[172] == '0') and
        (scan_result[171] == '0') and(scan_result[170] == '0') and(scan_result[169] == '0') and(scan_result[168] == '0') and
        (scan_result[251] == '0') and(scan_result[250] == '0') and(scan_result[249] == '0') and(scan_result[248] == '0') and
        (scan_result[209] == '0') and(scan_result[210] == '0') and(scan_result[211] == '0') and(scan_result[212] == '0') and
        (scan_result[213] == '0') and(scan_result[214] == '0') and(scan_result[217] == '0') and(scan_result[218] == '0') and
        (scan_result[219] == '0') and(scan_result[220] == '0') and(scan_result[221] == '0') and(scan_result[222] == '0') and
        (scan_result[223] == '0') and(scan_result[252] == '0') and(scan_result[253] == '0') and(scan_result[254] == '0') and
        (scan_result[247] == '0') and(scan_result[246] == '0') and(scan_result[245] == '0') and(scan_result[244] == '0') and
        (scan_result[243] == '0') and(scan_result[242] == '0') and(scan_result[241] == '0') and(scan_result[240] == '0') and
        (scan_result[239] == '0') and(scan_result[238] == '0') and(scan_result[237] == '0') and(scan_result[236] == '0') and
        (scan_result[235] == '0') and(scan_result[234] == '0') and(scan_result[233] == '0') and(scan_result[232] == '0') and
        (scan_result[231] == '0') and(scan_result[255] == '0') and(scan_result[256] == '0') and(scan_result[257] == '0') and
        (scan_result[258] == '0') and(scan_result[259] == '0') and(scan_result[260] == '0') and(scan_result[261] == '0') and
        (scan_result[262] == '0') and(scan_result[263] == '0') and(scan_result[264] == '0') and(scan_result[265] == '0') and
        (scan_result[266] == '0') and(scan_result[267] == '0') and(scan_result[268] == '0') and(scan_result[269] == '0') and
        (scan_result[270] == '0') and(scan_result[271] == '0') and(scan_result[229] == '0') and(scan_result[228] == '0') and
        (scan_result[227] == '0') and(scan_result[226] == '0') and(scan_result[225] == '0') and(scan_result[224] == '0') and
        (scan_result[305] == '0') and(scan_result[304] == '0') and(scan_result[303] == '0') and(scan_result[302] == '0') and
        (scan_result[301] == '0') and(scan_result[300] == '0') and(scan_result[299] == '0') and(scan_result[298] == '0') and
        (scan_result[297] == '0') and(scan_result[296] == '0') and(scan_result[273] == '0') and(scan_result[274] == '0') and
        (scan_result[275] == '0') and(scan_result[276] == '0') and(scan_result[277] == '0') and(scan_result[278] == '0') and
        (scan_result[309] == '0') and(scan_result[310] == '0') and(scan_result[311] == '0') and(scan_result[312] == '0') and
        (scan_result[313] == '0') and(scan_result[314] == '0') and(scan_result[315] == '0') and(scan_result[316] == '0') and
        (scan_result[317] == '0') and(scan_result[318] == '0') and(scan_result[295] == '0') and(scan_result[294] == '0') and
        (scan_result[293] == '0') and(scan_result[292] == '0') and(scan_result[291] == '0') and(scan_result[290] == '0') and
        (scan_result[289] == '0') and(scan_result[288] == '0') and(scan_result[287] == '0') and(scan_result[286] == '0') and
        (scan_result[285] == '0') and(scan_result[284] == '0') and(scan_result[283] == '0') and(scan_result[282] == '0') and
        (scan_result[281] == '0') and(scan_result[280] == '0') and(scan_result[363] == '0') and(scan_result[319] == '0') and
        (scan_result[320] == '0') and(scan_result[321] == '0') and(scan_result[322] == '0') and(scan_result[323] == '0') and
        (scan_result[324] == '0') and(scan_result[325] == '0') and(scan_result[326] == '0') and(scan_result[327] == '0') and
        (scan_result[328] == '0') and(scan_result[329] == '0') and(scan_result[330] == '0') and(scan_result[331] == '0') and
        (scan_result[332] == '0') and(scan_result[333] == '0') and(scan_result[334] == '0') and(scan_result[335] == '0')):

        RLY4.off()   #R3 OFF
    

    if (cnt >= 1):
        Fault_flag = 1
    if (cnt == 0):
        Fault_flag = 0
        
    if((Fault_flag == 0)and (LM3_flag == 0) and (LM4_flag == 0) and (LM5_flag == 0 )and (LM6_flag == 0)):
        RLY3.off()                   #RLY3 - Hooter
        #RLY4.off()   #commented on 29th                 #RLY4 - Bulb
       
    
    if(Fault_flag == 1):
        #RLY3.on()
        #RLY4.on()    #commented on 29th
        pass  
    
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
            #RLY4.off() #commented on 29th 
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

    
