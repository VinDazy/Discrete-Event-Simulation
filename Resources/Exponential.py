import simpy
import csv
import numpy as np

NUM_CARS = 10000  # Total number of cars
NUM_BOOTHS = 1  # Number of museum entry gate booths
SIMULATION_TIME = 480  # Simulation time in minutes (assuming it's an 8-hour work day)

# Arrival rates (lambda) for varying scenarios
arrival_rates = [0.5, 0.55, 0.6, 0.65]  # Arrival rates from 0.5 to 0.65 in steps of 0.05

# Create a Simpy environment
env = simpy.Environment()

# Define additional resources or data structures if needed for the simulation
# For example, a resource for the museum entry gate booth
museum_booth = simpy.Resource(env, capacity=NUM_BOOTHS)

# Dictionary to store arrival times for different arrival rates
arrival_times_data = {}

for rate in arrival_rates:
    # Generate arrival times (not used in exponential scenario, but included for consistency)
    arrival_times = np.random.exponential(scale=1/rate, size=NUM_CARS)
    
    # Generate exponentially distributed service times for each car
    service_times = np.random.exponential(scale=1.5, size=NUM_CARS)  # Mean service time of 1.5 minutes

    # Store arrival times and service times for each rate
    arrival_times_data[rate] = {'arrival_times': arrival_times, 'service_times': service_times}

queueing_delays = {}

# Define the car process
def car(arrival_time, service_time, car_index, acquired_resource):
    yield env.timeout(arrival_time)
    with museum_booth.request() as request:
        yield request
        acquired_resource[car_index] = True  # Set to True when the car acquires the resource
        yield env.timeout(service_time)

# Define the car generator process
def car_generator(arrival_times, service_times):
    acquired_resource = [False] * len(arrival_times)
    for i in range(len(arrival_times)):
        yield env.process(car(arrival_times[i], service_times[i], i, acquired_resource))
    return acquired_resource

def simulate(rate):
    global SIMULATION_TIME  # Access the global variable inside the function
    arrival_times = arrival_times_data[rate]['arrival_times']
    service_times = arrival_times_data[rate]['service_times']

    acquired_resource = [False] * len(arrival_times)

    for i in range(len(arrival_times)):
        env.process(car(arrival_times[i], service_times[i], i, acquired_resource))

    current_time = env.now

    if SIMULATION_TIME <= current_time:
        SIMULATION_TIME = current_time + 1

    env.run(until=SIMULATION_TIME)
    queueing_delay = [env.now - arrival_times[i] if not acquired_resource[i] else 0 for i in range(NUM_CARS)]
    queueing_delays[rate] = queueing_delay
    with open('Data\\Exponential_Average_Queueing_Delay.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Arrival Rate', 'Average Queueing Delay'])
        for rate, delays in queueing_delays.items():
            average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0
            writer.writerow([rate, round(average_delay, 2)])

def run():
    # Perform simulation for each arrival rate
    for rate in arrival_rates:
        simulate(rate)

    # Analyze queueing delays for different arrival rates and visualize results
    print("FOR EXPONENTIAL SERVICE TIMES")
    for rate, delays in queueing_delays.items():
        average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0
        print(f"\tAverage queueing delay for arrival rate {rate}: {round(average_delay, 2)}")

# Run the simulation
