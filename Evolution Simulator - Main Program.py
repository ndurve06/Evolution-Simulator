import random
import time
import os
import math

class EvolutionSimulator:
    def __init__(self):
        pass

    def __verify_input(self, prompt):
        while True:
            try:
                response = input(prompt).lower()
                if response not in ["y", "n"]:
                    raise ValueError("Incorrect input. Please enter y or n.")
                return response
            except ValueError as e:
                print(e)

    def __tutorial(self):
        tutorial = self.__verify_input("Would you like a tutorial (y or n): ")
        if tutorial == "y":
            previous_setup = PreviousSetup()
            previous_setup.filename = "tutorial.txt"  # Set filename
            mysimsetup = previous_setup.file_setup(context = "tutorial")
            if mysimsetup:
                self.__instance_initialisation(mysimsetup, filename = "tutorial.txt")
            print("You will now return to the main program")
        elif tutorial == "n":
            print("Proceeding without tutorial...")
            return
        
    def __existing_setup(self):
        exting_setup = self.__verify_input("Would you like to load existing setup (y or n): ")
        if exting_setup == "y":
            print("Loading existing setup...")
            previous_setup = PreviousSetup(filename = None)  # Set filename to None
            mysimsetup = previous_setup.get_filename()
            if mysimsetup:
                self.__instance_initialisation(mysimsetup)
                return mysimsetup
        elif exting_setup == "n":
            print("Proceeding without existing setup...")
            print("Starting manual setup...")
            mysimsetup = SimulationSetup()
            mysimsetup.update_size()  # Manual setup
            self.__instance_initialisation(mysimsetup)

    def __instance_initialisation(self, mysimsetup, filename = None):
        if not isinstance(mysimsetup, SimulationSetup):
            raise ValueError("Invalid setup object passed to instance_initialisation.")
        myvalue_calculator = ValueCalculator(mysimsetup)
        growth_value = myvalue_calculator.calc_growth_value()
        mutation_value = myvalue_calculator.calc_mutation_value()
        mygrid = Grid(mysimsetup) 
        mygrid.print_start()
        mysimulation = Simulation(PreviousSetup(), mysimsetup, growth_value, mutation_value, filename = filename)
        mysimulation.simulation_controller(mygrid, mysimulation)

    def main(self):
        print("Welcome to the Evolution Simulator!")
        self.__tutorial()
        self.__existing_setup()

class PreviousSetup:
    def __init__(self, filename = None):
        self.filename = filename

    def verify_filename(self):
        filename = input("Enter the file name: ") + ".txt"
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Get directory
        file_path = os.path.join(current_directory, filename)  # Join with the filename 
        print(f"File path: {file_path}")
        try:
            if not os.path.exists(file_path):
                print("The file does not exist. Please enter a valid file name.")
                return self.verify_filename()
        except FileNotFoundError as e:
            print(e)
            return self.verify_filename()
        return filename

    def get_filename(self):
        filename = self.verify_filename()
        self.filename = filename
        self.file_setup()
        return self.filename

    def file_setup(self, context = None):
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            if context == "tutorial":
                self.filename = "tutorial.txt"
            elif not self.filename:
                raise FileNotFoundError("Filename is not set.")
            self.the_file = os.path.join(current_directory, self.filename)
            mysimsetup = SimulationSetup()
            self.__load_file(self.the_file, mysimsetup)
            if "tutorial" in self.the_file:
                print(self.the_file)
                print(f"Tutorial: {mysimsetup.message_2} \n")
                print(mysimsetup.message_1)
                input("Press enter to continue: ")
            return mysimsetup
        except FileNotFoundError:
            print("File not accessible. Continuing program...")
            return

    def __load_file(self, file_path, target_object):
        try:
            # Open the file and read values
            with open(file_path, 'r') as self.filename:
                data = self.filename.readlines()
            target_object.message_1 = str(data[-1].strip()) # First part
            target_object.message_2 = str(data[-2].strip()) # Second part 
            target_object.rows = int(data[0].strip())  # Grid rows
            target_object.cols = int(data[1].strip())  # Grid cols
            target_object.genotype = int(data[2].strip())  # Genotype
            target_object.phenotype = int(data[3].strip())  # Phenotype
            target_object.environment = int(data[4].strip())  # Environment
            target_object.xray = float(data[5].strip())  # X-ray radiation
            target_object.gamma = float(data[6].strip())  # Gamma radiation
            target_object.particle = float(data[7].strip())  # Particle radiation
            target_object.start = eval(data[8].strip())  # Start coordinates
            target_object.nutrients = eval(data[9].strip())  # Nutrients
            target_object.obstacles = eval(data[10].strip())  # Obstacles
            target_object.cycles = int(data[11].strip())  # Cycles
        except Exception as e:
            print(f"Error processing file '{file_path}': {e}")


class SimulationSetup:
    def __init__(self):
        self.rows = None
        self.cols = None
        self.genotype = None
        self.phenotype = None
        self.xray = None
        self.gamma = None
        self.particle = None
        self.environment = None
        self.start = []
        self.__user_start = []
        self.nutrients = []
        self.__user_nutrients = []
        self.obstacles = []
        self.__user_obstacles = []
        self.cycles = None
        # Setups up all the parameters
    
    def clear_console(self):
        time.sleep(0.1)
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear') 
        #  Considers non-Windows devices
        #  Clear screen for clarity
        #  Time delay to allow users to "see" the simulation
        #  Time delay shows the "evloution after each cycle"

    def __get_coordinate(self):
        while True:
            try:
                col_user = int(input("Enter x: "))
                col = col_user - 1 
                row_user = int(input("Enter y: "))
                row = self.rows - row_user
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    return col, row, col_user, row_user
                else:
                    print("Invalid values. Please try again.")
            except ValueError:
                print("Incorrect data type. Please enter integer values.")
        #  Coordinates are requried for start, nutrient, obstacle
        #  Seperate fuction being repeated saves lines
        #  Acceptable values handled here instead of main funciton
        #  Maintains single task per method 

    def __get_mode(self):
        while True:
            try:
                mode = int(input("Enter number(1 - 5): "))
                if 1 <= mode <= 5:
                    return mode
                else:
                    print("Invalid mode")
            except ValueError:
                print("Incorrect data type")
        #  Number input required for genotype, phenotype and environment

    def __radiation_value(self):
        while True:
            try:
                value = float(input("Value 0-1: "))
                if 0 <= value <= 1:
                    value = round(value, 2)
                    return value
                else:
                    print("Invalid value")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 1.")
        #  Required for x-ray, gamma and particle
    
    def __nonentity_count(self):
        max_value = math.floor((self.rows**2) * 0.25)
        print(f"Your grid size is {self.rows}*{self.rows} and max value is {max_value}")
        
        while True:
            try:
                value = int(input("Number: "))
                if 0 <= value <= max_value:
                    return value
                else:
                    print("Number not in range, try again")
            except ValueError:
                print("Invalid input. Please enter a number")

    def update_size(self):
        while True:
            try:
                print("Enter the size of the grid (10 to 100 inclusive): ")
                size = int(input("Size: "))
                if 10 <= size <= 100:
                    self.rows = self.cols = size
                    break
                print("Enter a number between 10 and 100 inclusive.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        self.clear_console()  
        self.__update_genotype() 

    def __update_genotype(self):
        print("Genotypes: Fast Growth, Slow Growth, High food consumption, Low food consumption, No specific change")
        update_genotype = self.__get_mode()
        self.genotype = update_genotype
        self.clear_console()
        self.__update_phenotype()
        return update_genotype

    def __update_phenotype(self):
        print("Phenotypes: Small, Large, Round, Square, Mixed")
        update_phenotype = self.__get_mode()
        self.phenotype = update_phenotype
        self.clear_console()
        self.__update_environment()
        return update_phenotype

    def __update_environment(self):
        print("Environment: Rain, Sun, Warm, Cold, No specific change")
        update_environment = self.__get_mode()
        self.environment = update_environment
        self.clear_console()
        self.__update_radiation()
        return update_environment

    def __update_radiation(self):
        radiation_known = input("Are all X-Ray, Gamma and Particle radiation values known? (y/n): ").lower()
        update_xray, update_gamma, update_particle = None, None, None
        if radiation_known == "y":
            print("X-ray")
            update_xray = self.__radiation_value()
            print("Gamma")
            update_gamma = self.__radiation_value()
            print("Particle")
            update_particle = self.__radiation_value()
        elif radiation_known == "n":
            update_xray = 0.01
            update_gamma = 0.01
            update_particle = 0.01
        else:
            print("Please enter y or n")
            self.__update_radiation()
            return
        self.xray = update_xray
        self.gamma = update_gamma
        self.particle = update_particle
        self.clear_console()
        self.__start_point()

    def __start_point(self):
        print("Enter coordinates for the start point")
        col, row, col_user, row_user = self.__get_coordinate()
        self.start.append((row, col))
        self.__user_start.append((col_user, row_user))
        self.clear_console()
        self.__set_nutrients()

    def __set_nutrients(self):
        print(f"Start: {self.__user_start}")
        print("Enter the number of nurtients, can't exceed 25% of total area")
        value = self.__nonentity_count()
        for i in range(value):
            while True:
                print(f"Enter coordinates for the nutrients {(i+1)}/{value}")
                print(f"Current nutrients {self.__user_nutrients}")
                col, row, col_user, row_user = self.__get_coordinate()
                if (row, col) in self.start:
                    print("Can't be the same as start!")
                elif (row, col) in self.nutrients:
                    print("Two nutrients can't be in the same place!")
                else:
                    self.__user_nutrients.append((col_user, row_user))
                    self.nutrients.append((row, col))
                    break
        self.clear_console()
        self.__set_obstacles()

    def __set_obstacles(self):
        print(f"Start: {self.__user_start}")
        print(f"Nutrients: {self.__user_nutrients}")
        print("Enter the number of obstacles, can't exceed 25% of total area")
        value = self.__nonentity_count()
        for i in range(value):
            while True:
                print(f"Enter coordinates for the obstacles {(i+1)}/{value}")
                print(f"Current obstacles {self.__user_obstacles}")
                col, row, col_user, row_user = self.__get_coordinate()
                if (row, col) in self.start:
                    print("Can't be the same as start!")
                elif (row, col) in self.nutrients:
                    print("Can't overlap with nutrients")
                elif (row, col) in self.obstacles:
                    print("Two obstacles can't be in the same place!")
                else:
                    self.__user_obstacles.append((col_user, row_user))
                    self.obstacles.append((row, col))
                    break
        self.clear_console()
        self.__set_cycles()

    def __set_cycles(self):
        while True:
            try:
                update_cycles = int(input("Enter the number of cycles: "))
                if 0 <= update_cycles <= 10000:
                    print(update_cycles)
                    self.cycles = update_cycles
                    break 
                else:
                    print("Value too small or too big. Try again.")
            except ValueError:
                print("Incorrect data type. Please enter an integer.")



class ValueCalculator(SimulationSetup):
    def __init__(self, sim_setup):
        self.genotype = sim_setup.genotype
        self.phenotype = sim_setup.phenotype
        self.environment = sim_setup.environment
        self.xray = sim_setup.xray
        self.gamma = sim_setup.gamma
        self.particle = sim_setup.particle
        self.start = sim_setup.start
        self.nutrients = sim_setup.nutrients
        self.rows = sim_setup.rows
        self._growth_value_cached = None 
        self.growth_value = None
        self.mutation_value = None

    def __sigmoid(self, normalised_value):
        try:
            value = 1 / (1 + math.exp(-1 * normalised_value))
            #  Normalised_value maps a value between 0 and 1 according to dictionary from user input
            #  print(f"Sigmoid calculation for {normalised_value}: {value}")
            return value
        except OverflowError as e: 
            #  print(f"Sigmoid calculation error for {normalised_value}: {e}")
            return 0.5
    
    def __find_nutrients(self): 
        try:
            self.temporary = random.choice(self.start)
            print(f"Selected starting point: {self.temporary}")
            xc, yc = self.temporary
            nutrients_found = 0
            for i in range(-1, 2):  
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    xn = xc + i
                    yn = yc + j
                    # Ensure the coordinates are valid
                    if 0 <= xn < self.rows and 0 <= yn < self.rows:
                        if (xn, yn) in self.nutrients:
                            nutrients_found += 1
            #  print(f"Nutrients found near {self.temporary}: {nutrients_found}")
            return nutrients_found
        except Exception as e:
            #  print(f"Error during find_nutrients: {e}")
            return 0.5

    def calc_growth_value(self):
        if self._growth_value_cached is not None:
            return self._growth_value_cached
        try:
            genotypes = {1: 0.8, 2: 0.2, 3: 0.3, 4: 0.7, 5: 0.05}
            phenotypes = {1: 0.8, 2: 0.4, 3: 0.6, 4: 0.6, 5: 0.5}
            environments = {1: 0.7, 2: 0.2, 3: 0.6, 4: 0.3, 5: 0.5}
            genotype_value = genotypes.get(self.genotype, 0)
            phenotype_value = phenotypes.get(self.phenotype, 0)
            environment_value = environments.get(self.environment, 0)
            corresponding_array = [genotype_value, phenotype_value, environment_value]
            nutrient_value = (self.__find_nutrients()) / 8
            corresponding_array.append(nutrient_value)
            total = sum(self.__sigmoid(value) for value in corresponding_array)
            mean = total / len(corresponding_array)
            print(f"Final growth value: {mean}")
            self._growth_value_cached = mean 
            return mean
        except ZeroDivisionError:
            return 0.5

    def calc_mutation_value(self):
        try:
            total = self.xray + self.gamma + self.particle
            mean = round(total / 3, 2)
            self.mutation_value = mean
            return mean
        except Exception as e:
            print(f"Error during mutation value calculation: {e}")
            return 0

class Grid:
    def __init__(self, setup):
        self.rows = setup.rows
        self.cols = setup.cols
        self.__grid = [["-" for i in range(self.cols)] for i in range(self.rows)]
        self.start = setup.start
        self.nutrients = setup.nutrients
        self.obstacles = setup.obstacles

    def print_start(self):
        for row, col in self.start:
            self.__grid[row][col] = "E"
        self.__print_nutrients()

    def __print_nutrients(self):
        for row, col in self.nutrients:
            self.__grid[row][col] = "N"
        self.__print_obstacles()

    def __print_obstacles(self):
        for row, col in self.obstacles:
            self.__grid[row][col] = "O"
        self.__display()

    def __display(self):
        for row in self.__grid:
            print(" ".join(row))

class Simulation(ValueCalculator, EvolutionSimulator):
    def __init__(self, previous_setup, sim_setup, growth_value, mutation_value, filename = None):
        super().__init__(sim_setup)
        self.previous_setup = previous_setup
        self.filename = filename
        self.sim_setup = sim_setup
        self.start = sim_setup.start
        self.nutrients = sim_setup.nutrients
        self.obstacles = sim_setup.obstacles
        self.cycles = sim_setup.cycles
        self.growth_value = growth_value
        self.mutation_value = mutation_value
        self.__selected_cell = []
        self.__surrounding_cell = []
        self.__negative_value = False
        self.mutation_count = 0
        self.survival_chance = 3
        self.cycle_count = 0

    def simulation_controller(self, mygrid, mysimulation):
        original = self.growth_value
        cycles = self.cycles
        for i in range(cycles):
            self.__entity_cell()
            self.clear_console()
            print(mygrid.print_start())
            print(f"Current cycle count: {(i+1)}")
            print(f"Current mutation count: {self.mutation_count}")
            if self.__negative_value:
                break
        self.clear_console()
        print("Final grid: ")
        print(mygrid.print_start())
        print(f"Final Cycle count: {(i+1)}")
        self.cycle_count = (i+1)
        print(f"Final Mutation count: {self.mutation_count}")
        print(f"Original growth value: {round(original, 4)}")
        print(f"Final growth value: {round(self.growth_value, 4)}")
        if self.filename == "tutorial.txt":
            print("Tutorial simulation complete. No file will be saved.")
            return
        saving = SaveSimulation(self.sim_setup, mysimulation, self.previous_setup)
        saving.save_simulation()
    
    def __entity_cell(self):
        if self.start:
            self.working_cell = random.choice(self.start) 
            self.__selected_cell.append(self.working_cell)
        else: #  Ideally never called
            print("No cells available in the start list")
            self.simulation_controller()
        self.__change_cell()

    def __change_cell(self):
        xc = self.__selected_cell[0][0]  # xc current x point
        yc = self.__selected_cell[0][1]  # yc current y point
        xn = random.randint(-1, 1) + xc  # xn new x point
        yn = random.randint(-1, 1) + yc  # yn new y point
        if xn <= 0:
            xn = xn + 1
        elif xn >= self.rows:
            xn = xn - 1
        if yn <= 0:
            yn = yn + 1
        elif yn >= self.rows:
            yn = yn - 1
        self.__surrounding_cell.append((xn, yn))
        self.__compare_values(xn, yn)
        return xn, yn

    def __compare_values(self, xn, yn):
        if self.__surrounding_cell [0] in self.start:
            self.growth_value = self.growth_value - 0.01
        elif self.__surrounding_cell [0] in self.nutrients:
            self.growth_value = self.growth_value + 0.05
            self.start.append((xn, yn))
            self.nutrients.remove((xn, yn))
        elif self.__surrounding_cell [0] in self.obstacles:
            self.growth_value = self.growth_value - 0.01
        else:
            if random.random() < self.growth_value:
                self.start.append((xn, yn))
                self.growth_value = self.growth_value - 0.01
            else: 
                self.growth_value = self.growth_value - 0.01
        print(f"Current Growth Value: {self.growth_value}")
        self.__selected_cell.pop(-1)
        self.__surrounding_cell.pop(-1)
        self.__mutation_effect()

    def __mutation_effect(self):
        if random.random() < self.mutation_value:
            print("Mutation!")
            self.mutation_count = self.mutation_count + 1
            change = round(random.uniform(-0.05, 0.05), 2)
            self.growth_value = self.growth_value + change
            time.sleep(1)
        self.__negative_growth_value()
    
    def __negative_growth_value(self):
        if self.growth_value <= 0:
            print("Entity short of nutrients, survival is difficult!")
            self.survival_chance = self.survival_chance - 1
            if self.survival_chance == 0:
                self.__negative_value = True
            time.sleep(2)
            nutrient_count = len(self.nutrients)
            if nutrient_count > (0.01 * self.rows**2):
                self.growth_value = self.growth_value + 0.025
            else:
                print("Enity unlikley to survive from here!")
                time.sleep(2)
                self.__negative_value = True


class SaveSimulation(EvolutionSimulator):
    def __init__(self, sim_setup, mysimulation, previous_setup):
        self.sim_setup = sim_setup
        self.mysimulation = mysimulation
        self.previous_setup = previous_setup
        self.filename = None
        self.start = sim_setup.start
        self.nutrients = sim_setup.nutrients
        self.obstacles = sim_setup.obstacles
        self.mutation_count = mysimulation.mutation_count
        self.final_growth = mysimulation.growth_value
        self.cycle_count = mysimulation.cycle_count

    def save_simulation(self):
        self.filename = self.previous_setup.verify_filename()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.the_file = os.path.join(current_directory, self.filename)
        with open(self.the_file, 'w') as file:
            file.write(str(self.start) + "\n")
            file.write(str(self.nutrients) + "\n")
            file.write(str(self.obstacles) + "\n")
            file.write(str(self.mutation_count) + "\n")
            file.write(str(self.final_growth) + "\n")
            file.write(str(self.cycle_count) + "\n")
        print("Saving Complete")
        #  print(f"Variables have been written to {self.the_file}")


if __name__ == "__main__":
    simulator = EvolutionSimulator()
    simulator.main()
