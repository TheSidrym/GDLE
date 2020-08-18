# My code is unreadable

import os, sys, zlib, base64

class Local:
    def __init__(self, path):
        self.base = "kS38,1_40_2_125_3_255_11_255_12_255_13_255_4_-1_6_1000_7_1_15_1_18_0_8_1|1_0_2_102_3_255_11_255_12_255_13_255_4_-1_6_1001_7_1_15_1_18_0_8_1|1_0_2_102_3_255_11_255_12_255_13_255_4_-1_6_1009_7_1_15_1_18_0_8_1|1_255_2_255_3_255_11_255_12_255_13_255_4_-1_6_1002_5_1_7_1_15_1_18_0_8_1|1_255_2_255_3_255_11_255_12_255_13_255_4_-1_6_1005_5_1_7_1_15_1_18_0_8_1|1_255_2_255_3_255_11_255_12_255_13_255_4_-1_6_1006_5_1_7_1_15_1_18_0_8_1|{color},kA13,0,kA15,0,kA16,0,kA14,,kA6,0,kA7,0,kA17,0,kA18,0,kS39,0,kA2,0,kA3,0,kA8,0,kA4,0,kA9,0,kA10,0,kA11,0;"
        self.savePath = os.getenv('localappdata')+"\\GeometryDash\\"+path
        self.levelsData = self.getLevels(self.savePath)

    def getLevels(self, savePath):
        with open(savePath, 'r') as f:
            data = f.read()
        try: 
            return self.Decrypt(self.Xor(data.encode(),11)).decode()
        except: 
            return data

    def getLevelIndexByName(self):
        s = ["H4s","kS38"]
        index = self.levelsData.find(f">{self.lName}<")
        if index == -1:
            print("Failed to find a level")
            sys.exit()
        for x in s:
            j = self.levelsData.find(x, index)
            if j != -1:
                return j
        print("Failed")
        sys.exit()

    def getLevelByName(self, lName):
        self.lName = lName
        return self.levelsData[self.getLevelIndexByName():].split('<')[0]

    def Decrypt(self, data):
        return zlib.decompress(base64.b64decode(data.replace('-','+').replace('_','/').encode())[10:],-zlib.MAX_WBITS)

    def Xor(self, data: bytes, key: int):
        res = []
        for i in data:
            res.append(i^key)
        return bytearray(res).decode()

    def replaceLevel(self, level):
        fIndex = self.getLevelIndexByName()
        lIndex = len(self.levelsData[self.getLevelIndexByName():].split('<')[0])+fIndex
        self.levelsData = self.levelsData[:fIndex]+level+self.levelsData[lIndex:]
        return self.levelsData

    def save(self, lvl):
        level, colors = lvl
        self.base = self.base.format(color=colors)
        s = self.replaceLevel(self.base+level)
        with open(self.savePath, 'w') as fw:
            fw.write(s)

class Level:
    def __init__(self):
        self.blockStep = 30
        self.lvlStr = ""
        self.colors = ""

    def __call__(self):
        return [self.lvlStr, self.colors]

    def addBlock(self, block: str):
        self.lvlStr += block

    def addColor(self, colorID, rgb: tuple):
        self.colors += f"1_{rgb[0]}_2_{rgb[1]}_3_{rgb[2]}_11_255_12_255_13_255_4_-1_6_{colorID}_7_1_15_1_18_0_8_1|"

class Block:
    def __init__(self, params: dict):
        self.params = params
        self.allParams = {"id":"1",
                          "x":"2",
                          "y":"3",
                          "flipX":"4",
                          "flipY":"5",
                          "rotation":"6",
                          "colorBase":"21",
                          "colorDetail":"22"}
        requiredParams = ["id","x","y"]
        optionalParams = ["colorBase","colorDetail","HSVBase","HSVDetail","groupIDs"]
        #blockBasedParams = ["Text"]    
        for i in requiredParams:
            if i not in params:
                print('Parameters id, x, y are required')
                sys.exit()
        self.blockStr = self.createBlock()

    def __call__(self):
        return self.blockStr

    def createBlock(self):
        fin = ""
        for ap in self.allParams:
            for p in self.params:
                if p in ap:
                    par = self.params[p]
                    parInd = self.allParams[ap]
                    if type(par) == int:
                        par = str(par)
                    fin += parInd+","+par+","
        return fin[:-1]+";"