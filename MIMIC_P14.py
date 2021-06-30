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
    
    #if there is no fault 
    else: 
        RLY4.off()   #R3 OFF
    
    # R1 - M8, M9, M10
    if((scan_result[587] == '1')  or(scan_result[586] == '1') or (scan_result[585] == '1') or (scan_result[588] == '1') or
        (scan_result[589] == '1')  or(scan_result[590] == '1')  or(scan_result[592] == '1')  or(scan_result[581] == '1')  or
        (scan_result[580] == '1')  or(scan_result[593] == '1')  or(scan_result[594] == '1')  or(scan_result[579] == '1')  or
        (scan_result[578] == '1')  or(scan_result[595] == '1')  or(scan_result[596] == '1') ):

        RLY1.on()
    else:
        RLY1.off()


    # R4 - M26, M28, M29
    if((scan_result[361] == '1')  or(scan_result[360] == '1') or (scan_result[365] == '1') or (scan_result[366] == '1') or
        (scan_result[358] == '1')  or(scan_result[359] == '1')  or(scan_result[357] == '1')  or(scan_result[356] == '1')  or
        (scan_result[355] == '1')  or(scan_result[354] == '1')  or(scan_result[353] == '1')  or(scan_result[352] == '1')  or
        (scan_result[351] == '1')  or(scan_result[350] == '1')  or(scan_result[349] == '1')  or (scan_result[348] == '1')  or
        (scan_result[347] == '1')  or(scan_result[346] == '1') or (scan_result[345] == '1') or (scan_result[367] == '1') or
        (scan_result[368] == '1')  or(scan_result[369] == '1')  or(scan_result[370] == '1')  or(scan_result[371] == '1')  or
        (scan_result[372] == '1')  or(scan_result[373] == '1')  or(scan_result[374] == '1')  or(scan_result[375] == '1')  or
        (scan_result[376] == '1')  or(scan_result[377] == '1')  or(scan_result[378] == '1') or(scan_result[379] == '1')  or
        (scan_result[380] == '1')  or(scan_result[381] == '1')  or(scan_result[343] == '1')  or(scan_result[342] == '1')  or
        (scan_result[341] == '1')  or(scan_result[340] == '1')  or(scan_result[339] == '1')  or(scan_result[337] == '1')  or
        (scan_result[336] == '1')  or(scan_result[419] == '1')  or(scan_result[418] == '1')  or (scan_result[417] == '1')  or
        (scan_result[416] == '1')  or(scan_result[415] == '1') or (scan_result[383] == '1') or (scan_result[384] == '1') or
        (scan_result[385] == '1')  or(scan_result[386] == '1')  or(scan_result[387] == '1')  or(scan_result[389] == '1')  or
        (scan_result[390] == '1')  or(scan_result[391] == '1')  or(scan_result[420] == '1')  or(scan_result[421] == '1')  or
        (scan_result[422] == '1')  or(scan_result[423] == '1') ):

        RLY5.on()
    else:
        RLY5.off()

    # R2 - M11, M12, M13, M14,M15, M16    

    if((scan_result[577] == '1')  or(scan_result[576] == '1') or (scan_result[575] == '1') or (scan_result[574] == '1') or
        (scan_result[573] == '1') or(scan_result[572] == '1') or(scan_result[571] == '1') or(scan_result[570] == '1') or
        (scan_result[569] == '1') or(scan_result[568] == '1') or(scan_result[567] == '1') or(scan_result[566] == '1') or
        (scan_result[597] == '1') or(scan_result[598] == '1') or(scan_result[599] == '1') or(scan_result[600] == '1') or
        (scan_result[601] == '1') or(scan_result[602] == '1') or(scan_result[603] == '1') or(scan_result[604] == '1') or
        (scan_result[605] == '1') or(scan_result[606] == '1') or(scan_result[607] == '1') or(scan_result[608] == '1') or
        (scan_result[565] == '1') or(scan_result[564] == '1') or(scan_result[563] == '1') or(scan_result[562] == '1') or
        (scan_result[561] == '1') or(scan_result[27] == '1') or(scan_result[26] == '1') or(scan_result[25] == '1') or
        (scan_result[24] == '1') or(scan_result[609] == '1') or(scan_result[610] == '1') or(scan_result[611] == '1') or
        (scan_result[612] == '1') or(scan_result[613] == '1') or(scan_result[615] == '1') or(scan_result[28] == '1') or
        (scan_result[29] == '1') or(scan_result[30] == '1') or(scan_result[23] == '1') or(scan_result[22] == '1') or
        (scan_result[21] == '1') or(scan_result[20] == '1') or(scan_result[19] == '1') or(scan_result[18] == '1') or
        (scan_result[17] == '1') or(scan_result[16] == '1') or(scan_result[15] == '1') or(scan_result[14] == '1') or
        (scan_result[13] == '1') or(scan_result[12] == '1') or(scan_result[11] == '1') or(scan_result[10] == '1') or
        (scan_result[9] == '1') or(scan_result[8] == '1') or(scan_result[31] == '1') or(scan_result[32] == '1') or
        (scan_result[33] == '1') or(scan_result[34] == '1') or(scan_result[35] == '1') or(scan_result[36] == '1') or
        (scan_result[37] == '1') or(scan_result[38] == '1') or(scan_result[39] == '1') or(scan_result[40] == '1') or
        (scan_result[41] == '1') or(scan_result[42] == '1') or(scan_result[43] == '1') or(scan_result[44] == '1') or
        (scan_result[45] == '1') or(scan_result[46] == '1') or(scan_result[7] == '1') or(scan_result[6] == '1') or
        (scan_result[5] == '1') or(scan_result[4] == '1') or(scan_result[1] == '1') or(scan_result[0] == '1') or
        (scan_result[83] == '1') or(scan_result[82] == '1') or(scan_result[81] == '1') or(scan_result[80] == '1') or
        (scan_result[79] == '1') or(scan_result[78] == '1') or(scan_result[47] == '1') or(scan_result[48] == '1') or
        (scan_result[49] == '1') or(scan_result[50] == '1') or
        (scan_result[53] == '1') or(scan_result[54] == '1') or(scan_result[55] == '1') or(scan_result[84] == '1') or
        (scan_result[85] == '1') or(scan_result[86] == '1') or(scan_result[87] == '1') or(scan_result[88] == '1') or
        (scan_result[77] == '1') or(scan_result[76] == '1') or(scan_result[75] == '1') or(scan_result[74] == '1') or
        (scan_result[73] == '1') or(scan_result[72] == '1') or(scan_result[71] == '1') or(scan_result[70] == '1') or
        (scan_result[69] == '1') or(scan_result[68] == '1') or(scan_result[67] == '1') or(scan_result[66] == '1') or
        (scan_result[65] == '1') or(scan_result[64] == '1') or(scan_result[63] == '1') or(scan_result[62] == '1') or
        (scan_result[89] == '1') or(scan_result[90] == '1') or(scan_result[91] == '1') or(scan_result[92] == '1') or
        (scan_result[93] == '1') or(scan_result[94] == '1') or(scan_result[95] == '1') or(scan_result[96] == '1') or
        (scan_result[97] == '1') or(scan_result[98] == '1') or(scan_result[99] == '1') or(scan_result[100] == '1') or
        (scan_result[101] == '1') or(scan_result[102] == '1') or(scan_result[103] == '1') or(scan_result[104] == '1') or
        (scan_result[61] == '1') or(scan_result[60] == '1') or(scan_result[59] == '1') or(scan_result[58] == '1') or
        (scan_result[139] == '1') or(scan_result[138] == '1') or(scan_result[137] == '1') or(scan_result[136] == '1') or
        (scan_result[135] == '1') or(scan_result[134] == '1') or(scan_result[133] == '1') or(scan_result[132] == '1') or
        (scan_result[105] == '1') or(scan_result[106] == '1') or(scan_result[107] == '1') or(scan_result[108] == '1') or
        (scan_result[111] == '1') or(scan_result[140] == '1') or(scan_result[141] == '1') or(scan_result[142] == '1') or
        (scan_result[143] == '1') or(scan_result[144] == '1') or(scan_result[145] == '1') or(scan_result[146] == '1')):

        RLY2.on()
    
    else:
        RLY2.off()


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

    
