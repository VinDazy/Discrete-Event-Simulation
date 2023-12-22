import csv
import simpy

def run():
    NUM_CARS = 10000  # Total number of cars
    NUM_BOOTHS = 1  # Number of museum entry gate booths
    SIMULATION_TIME = 480  # Assuming it's an 8-hour work day (8x60)

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
        # For deterministic workload, set service time constant to 1.5 minutes
        service_time = 1.5
        
        # Generate arrival times (not used in deterministic scenario, but included for consistency)
        arrival_times = [0] * NUM_CARS  # Arrival times are not variable in the deterministic case
        
        # Store arrival times and constant service time for each rate
        arrival_times_data[rate] = {'arrival_times': arrival_times, 'service_time': service_time}

    # Define the car arrival and processing process
    def car_generator(arrival_times, service_time, acquired_resource):
        for i in range(NUM_CARS):
            acquired_resource = yield env.process(car(arrival_times[i], service_time, i, acquired_resource))

    # Define the car process
    def car(arrival_time, service_time, car_index, acquired_resource):
        yield env.timeout(arrival_time)
        with museum_booth.request() as request:
            yield request
            acquired_resource[car_index] = True  # Set to True when the car acquires the resource
            yield env.timeout(service_time)
        return acquired_resource

    queueing_delays = {}

    for rate in arrival_rates:
        arrival_times = arrival_times_data[rate]['arrival_times']
        service_time = arrival_times_data[rate]['service_time']
        acquired_resource = [False] * NUM_CARS  # Track if each car acquired the resource

        # Run the simulation for each rate
        env.process(car_generator(arrival_times, service_time, acquired_resource))
        env.run(until=SIMULATION_TIME)  # Run the simulation

        # Calculate queueing delay for each car
        queueing_delay = [env.now - arrival_times[i] if not acquired_resource[i] else 0 for i in range(NUM_CARS)]
        queueing_delays[rate] = queueing_delay

        # Update SIMULATION_TIME to ensure sufficient duration for the next simulation
        completion_time = max(env.now, SIMULATION_TIME)
        SIMULATION_TIME = int(completion_time + 100)  # Adding extra time for the next simulation

    # Save deterministic service time to a CSV fil

    # Save deterministic average queueing delay to a CSV file
    with open('Data\\Deterministic_Average_Queueing_Delay.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Arrival Rate', 'Average Queueing Delay'])
        for rate, delays in queueing_delays.items():
            average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0
            writer.writerow([rate, round(average_delay, 2)])

    # Analyze queueing delays for different arrival rates
    print("FOR DETERMINISTIC SERVICE TIMES")
    for rate, delays in queueing_delays.items():
        average_delay = sum(delays) / len(delays) if len(delays) > 0 else 0  # Handle division by zero
        print(f"\tAverage queueing delay for arrival rate {rate}: {round(average_delay,2)}")

# Run the simulation

