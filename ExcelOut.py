import pandas as pd
import openpyxl
import time

class ExcelPrinter:
    
    def __init__(self, directory = "res/output", fileName = "DAI"):
        self.directory = directory
        self.fileName = fileName
        self.data = pd.DataFrame({'Data': [], 'Time': [], 'DAI' : [], 'DAI coordinates: x' : [],
                                'DAI coordinates: y' : [], 'DAI coordinates: w' : [], 'DAI coordinates: h' : [],
                                'Angle' : []})
        pass
    
    def addObservation(self, DAI, DAIcoord, angles): 
        t = time.localtime()
        current_time = time.strftime("%X", t)
        current_data = time.strftime("%x", t)
        for i in range(len(DAI)):
            name = DAI[i]
            a = angles[i]
            x = DAIcoord[4 * i]
            y = DAIcoord[4 * i + 1]
            w = DAIcoord[4 * i + 2]
            h = DAIcoord[4 * i + 3]
            new_row = {'Data': current_data,'Time': current_time, 'DAI' : name, 'DAI coordinates: x' : x,
                        'DAI coordinates: y' : y, 'DAI coordinates: w' : w, 'DAI coordinates: h' : h, 'Angle' : a}
            self.data = self.data.append(new_row, ignore_index=True)
        with pd.ExcelWriter("{0}/{1}.xlsx".format(self.directory, self.fileName), mode="w", engine='openpyxl') as writer:
            self.data.to_excel(writer, sheet_name="DAI")
            
        
    def newfile(self):
        with pd.ExcelWriter("{0}/DAI.xlsx".format(self.directory), engine='xlsxwriter') as writer:
            self.data.to_excel(writer, sheet_name='DAI')
            writer.save()
