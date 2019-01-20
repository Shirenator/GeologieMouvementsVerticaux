from tabulate import tabulate
import pandas as pd

class GSL:
    def __init__(self, matrix, j):
        self.method = matrix[0,j]
        self.method_name = matrix[1,j]
        self.time = matrix[3:,j]
        if(matrix[2,j+2]):
            self.sea_level_min = matrix[3:,j+1]
            self.sea_level_mean = matrix[3:,j+2]
            self.sea_level_max = matrix[3:,j+3]
        else:
            self.sea_level_min = matrix[3:,j+1]
            self.sea_level_mean = matrix[3:,j+1]
            self.sea_level_max = matrix[3:,j+1]


class Location:
    #Constructor for a user-entered point
    def __init__(self, name,latitude,longitude,age_min,age_max,min_bathy,max_bathy,altitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.age_min = age_min
        self.age_max = age_max
        self.min_bathy = min_bathy
        self.max_bathy = max_bathy
        self.altitude = altitude
    #Constructor for a point at line i in the matrix
    def __init__(self, matrix, i):
        self.name = matrix[i,2]
        self.latitude = matrix[i,3]
        self.longitude = matrix[i,4]
        self.age_min = matrix[i,7]
        self.age_max = matrix[i,8]
        self.min_bathy = matrix[i,10]
        self.max_bathy = matrix[i,11]
        self.altitude = matrix[i,12]

    def __str__(self):
        return ("Location: "+self.name+", "+str(self.latitude)+", "+str(self.longitude)+", "+str(self.age_min)+", "+str(self.age_max)+", "+str(self.min_bathy)+", "+str(self.max_bathy)+", "+str(self.altitude))



class Vertical_movement(Location):
    #Constructor for a point at line i in the matrix
    def __init__(self,matrix,i,gsls):
        super().__init__(self,matrix,i)
        self.gsls = gsls

    #Constructor with a location entered
    def __init__(self,loc,gsls):
        self.name = loc.name
        self.latitude = loc.latitude
        self.longitude = loc.longitude
        self.age_min = loc.age_min
        self.age_max = loc.age_max
        self.min_bathy = loc.min_bathy
        self.max_bathy = loc.max_bathy
        self.altitude = loc.altitude
        self.gsls = gsls

    #returns a tab containing all values of vertical movement for this point
    def calc(self):
        ret = []
        ret.append(self)
        for gsl in gsls:
            vm = [] #method, method_name, min, mean, max
            time = gsl.time.tolist()
            sl_min = [x for x in gsl.sea_level_min.tolist() if x is not None]
            sl_mean = [x for x in gsl.sea_level_mean.tolist() if x is not None]
            sl_max = [x for x in gsl.sea_level_max.tolist() if x is not None]
            time_filtered = []
            sl_min_filtered = []
            sl_mean_filtered = []
            sl_max_filtered = []
            bool = True
            i = 0

            while(bool):
                if time[i] > self.age_min and time[i] < self.age_max:
                    time_filtered.append(time[i])
                    sl_min_filtered.append(sl_min[i])
                    sl_mean_filtered.append(sl_mean[i])
                    sl_max_filtered.append(sl_max[i])
                i+=1
                if(time[i]>self.age_max):
                    bool = False

            if len(sl_min_filtered) == 0 or len(sl_mean_filtered) == 0 or len(sl_max_filtered) == 0:
                vm.append(method)
                vm.append(method_name)
                vm.append(None)
            else:
                min_fvm = self.altitude-max(sl_max_filtered)+self.min_bathy
                mean_fvm = self.altitude-sum(sl_mean_filtered)/float(len(sl_mean_filtered))+((self.min_bathy)+(self.min_bathy))/2
                max_fvm = self.altitude-min(sl_min_filtered)+self.max_bathy
                method = gsl.method
                method_name = gsl.method_name
                vm.append(method)
                vm.append(method_name)
                vm.append(min_fvm)
                vm.append(mean_fvm)
                vm.append(max_fvm)
            ret.append(vm)
        return ret 
        #tab contains: Location object as first element and tabs containing [method, method_name, min vm value, mean vm value, max vm value



def read_gsl(file,sheet_name):
    xl = pd.read_excel(file,sheet_name=sheet_name,header=None)
    xl = xl.where((pd.notnull(xl)), None)
    matrix = xl.values
    gsls = []
    for j in range(matrix[0,:].size):
        if matrix[0,j]:
            gsl = GSL(matrix,j)
            gsls.append(gsl)
    return gsls

def read_locations(file,sheet_name):
    xls = pd.ExcelFile(file)
    xl = pd.read_excel(xls,sheet_name=sheet_name,header=None)
    xl = xl.where((pd.notnull(xl)), None)
    matrix = xl.values
    locations = []
    for i in range(4,matrix[:,1].size):
        if matrix[i,1]:
            loc = Location(matrix,i)
            locations.append(loc)
    return locations


'''
fileGSL = "SL_CHARTS_2012.xlsx"
fileLOC = "S1.xlsx"

gsls = read_gsl(fileGSL,0)
locations = read_locations(fileLOC,'PIACENZIAN_FVM')
for loc in locations:
    print(str(loc))

point1 = Vertical_movement(locations[0],gsls)

fvm = point1.calc() 
print(fvm)
'''
