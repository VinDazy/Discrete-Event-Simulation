import simpy
import numpy as np
import csv

def run():
    NUM_CARS = 10000  # Total number of cars
    NUM_BOOTHS = 1  # Number of museum entry gate booths
    SIMULATION_TIME = 480  # Simulation time in minutes (assuming an 8-hour work day)

    # Arrival rates (lambda) for varying scenarios
    arrival_rates = [0.5, 0.55, 0.6, 0.65]  # Arrival rates from 0.5 to 0.65 in steps of 0.05

    # Correlation coefficient
    correlation = 0.2

    # Create a Simpy environment
    env = simpy.Environment()

    # Define additional resources or data structures if needed for the simulation
    # For example, a resource for the museum entry gate booth
    museum_booth = simpy.Resource(env, capacity=NUM_BOOTHS)

    # Dictionary to store arrival times for different arrival rates
    arrival_times_data = {}

    for rate in arrival_rates:
        # Generate exponentially distributed service times for each car with correlation
        mean = 1.5
        cov_matrix = np.array([[1.0, correlation], [correlation, 1.0]])  # Covariance matrix
        service_times = np.random.multivariate_normal([mean, mean], cov_matrix, size=NUM_CARS)
        service_times = np.abs(service_times)  # Ensure service times are positive

        # Store service times for each rate
        arrival_times_data[rate] = {'service_times': service_times}

    queueing_delays = {}

    def car(arrival_time, service_time, car_index, acquired_resource):
        yield env.timeout(arrival_time)
        with museum_booth.request() as request:
            yield request
            acquired_resource[car_index] = True
            yield env.timeout(service_time)

    def simulate(rate):
        nonlocal SIMULATION_TIME  # Access the enclosing function's local variable
        service_times = arrival_times_data[rate]['service_times']

        # Initialize acquired_resource list
        acquired_resource = [False] * len(service_times)

        # Iterate over each car
        for i in range(len(service_times)):
            # Run the car process and update acquired_resource accordingly
            env.process(car(0, service_times[i][0], i, acquired_resource))

        # Run the simulation until the simulation time
        current_time = env.now

        if SIMULATION_TIME <= current_time:
            SIMULATION_TIME = current_time + 1

        env.run(until=SIMULATION_TIME)

        # Calculate queueing delay for each car
        queueing_delay = [service_times[i][0] if not acquired_resource[i] else 0 for i in range(NUM_CARS)]
        queueing_delays[rate] = queueing_delay

    # Perform simulation for each arrival rate
    for rate in arrival_rates:
        simulate(rate)

    # After the simulation loop, the queueing_delays dictionary is populated
    with open('Data\\Coorelated_Exponential_Average_Queueing_Delay.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Arrival Rate', 'Average Queueing Delay'])
        for rate, delays in queueing_delays.items():
            average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0
            writer.writerow([rate, round(average_delay, 2)])

    # Analyze queueing delays for different arrival rates and visualize results
    print("FOR COORELATED-EXPONENTIAL SERVICE TIMES")
    for rate, delays in queueing_delays.items():
        average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0
        print(f"\tAverage queueing delay for arrival rate {rate}: {round(average_delay, 2)}")

# Run the simulation

