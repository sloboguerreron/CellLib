import math
from cell import Cell

class Simulator:
    def __init__(self, time, n, m, alpha, k, steps, V0=None):
        self.total_time = time #final time
        self.n = n #Number of cells to study
        self.M = m #Sampling time
        self.alpha = alpha #Growth  rate

        self.time = 0
        self.output = ""
        self.output_size = ""
        self.total_steps = steps
        self.num_steps = 0

        self.K = k*self.total_steps #Average size of bacteria

        self.V0 = 1
        self.F0 = 0
        self.counter = 10
        self.time = 0
        self.steps = 0.1 / self.M

        self.simulation_time = []
        self.divisions_times = []

        self.simulation_time.append(0)

        self.cells = []

        self.initialice_cells(V0)


    def initialice_cells(self, V0):
        if V0 == None:
            for i in range(self.n):
                cell = Cell(i, self.V0, 5)
                self.cells.append(cell)
                cell.F.append(self.F0)
                cell.V.append(self.V0)
        else:
            idx = 0
            for i in V0:
                cell = Cell(idx, i, 5)
                self.cells.append(cell)
                cell.F.append(self.F0)
                cell.V.append(i)
                idx += 1

        print("Cells initialized")

    def open_file(self, name="simulation_data"):
        self.file = open(name+".csv", "w")
        self.output += "time;"
        for idx in range(len(self.cells)):
            self.output += "cell "+str(idx+1)+";"
        self.output += "\n"

        self.file_size = open("simulation_size.csv", "w")
        self.output_size += "initial size;division size;    \n"


    def simulate(self, export=False):
        if self.total_time < 0.001:
            self.total_time = 0.001

        if export:
            self.open_file()
            for index in range(1, self.total_time):
                for cell in self.cells:
                    Vn = cell.V[index-1] + self.M * (self.alpha*cell.V[index-1])
                    Fn = cell.F[index-1] + self.M * (1-cell.F[index-1]) * self.K * Vn
                    if Fn > cell.rv:
                        cell.num_steps += 1
                        if cell.num_steps >= cell.total_steps:
                            cell.division(Vn)
                            self.output_size += str(self.truncate(cell.V0, 4))+";"+str(self.truncate(Vn, 4))+";   \n "
                            cell.num_steps = 0
                        else:
                            cell.change(Vn)
                    else:
                        cell.add_growth(Vn, Fn)

                if self.counter == 10:
                    self.output += str((index*self.M))+";"
                    for cell in self.cells:
                        self.output += str(self.truncate(cell.get_size(index), 4))+";"
                    self.output += "\n"
                    self.counter = 0

                self.counter += 1

            print("Simulation Successful")
            return self.cells

        else:
            for index in range(1, self.total_time):
                for cell in self.cells:
                    Vn = cell.V[index-1] + self.M * (self.alpha*cell.V[index-1])
                    Fn = cell.F[index-1] + self.M * (1-cell.F[index-1]) * self.K * Vn
                    if Fn > cell.rv:
                        cell.num_steps += 1
                        if cell.num_steps >= cell.total_steps:
                            cell.division(Vn)
                            self.output_size += str(self.truncate(cell.V0, 4))+";"+str(self.truncate(Vn, 4))+";   \n "
                            cell.num_steps = 0
                        else:
                            cell.change(Vn)
                    else:
                        cell.add_growth(Vn, Fn)

            print("Simulation Successful")
            return self.cells



    def export_data(self, name="simulation_data"):
        self.file.write(self.output)
        self.file_size.write(self.output_size)
        self.file.close()
        self.file_size.close()
        print("Simulation Successful")

    def get_last_f(self, n):
        return self.cells[n].F[-1]

    def show_f(self, n, cells=[]):
        if len(cells)>0:
            return cells[n].F
        else:
            return self.cells[n].F

    def show_array(self):
        output = ""
        for cell in self.cells:
            output += str(cell)+"\n"
        return output

    def truncate(self, num, ciphers):
        pos = pow(10.0, ciphers)
        return math.trunc(pos * num)/pos


    def __str__(self):
        out = "Initial Params: {\n   time: "+str(self.total_time)+", \n   n: "+str(self.n)+", \n   m: "+str(self.M)+", \n   alpha: "+str(self.alpha)+", \n   k: "+str(self.K)+"\n}"
        for cell in self.cells:
            out+= str(cell)+"\n"
        return out


sim = Simulator(10000, 10, 0.001, 1, 1, 5, [1,2,1,2])
sim.simulate(export=True)
print(sim.show_f(2))
sim.export_data()
