# Carthage Road Trip Simulation

This document serves as a user manual for the trace-driven discrete-event simulation model.

The program simulates a queueing system based on varying arrival rates and service times using Simpy and Poisson arrival process.

## Requirements

- Python 3.x
- Required Python packages: Simpy, NumPy, CSV

## Installation

1. **Clone the Repository:**

    https://github.com/VinDazy/Discrete-Event-Simulation

2. **Install Dependencies:**

     `pip install -r requirements.txt`


## Configuration

- Open the `Resources` directory, in which you can make any necessary configurations, such as adjusting simulation parameters, number of cars, arrival rates, or service times for any workload model.

## Usage

1. **Run the Simulation:**

    Run the simulation by executing the `main.py` and chose the desired Workload Model.

2. **View Output:**
- The program will output the average queueing delays for different arrival rates to the console.
- Additionally, a CSV file will be generated:
  - `{Workload_Model}_Average_Queueing_Delay.csv`: Contains average queueing delays for the chosen Workload Model.
3. **Simulation Results**

| Arrival Rate | DETERMINISTIC | Exponential | Hyper Exponential  | Coorelated Exponential |
|--------------|---------------|-------------|--------------------|------------------------|
| 0.5          | 463.95        | 464.64      | 463.39             | 1.51                   |
| 0.55         | 479.18        | 578.03      | 479.18             | 1.56                   |
| 0.6          | 480.37        | 678.5       | 480.32             | 1.55                   |
| 0.65         | 481.49        | 778.75      | 481.42             | 1.57                   |

### Observations
For the Deterministic service time model, queueing delays increase as arrival rates increase.
Exponential and Hyper-Exponential models showcase relatively consistent queueing delays across different arrival rates.

In contrast, the Coorelated-Exponential model demonstrates extremely low and relatively constant queueing delays across different arrival rates, indicating the effect of positive correlation between successive service times.

## Acknowledgment
Due to the obscurity of the task and the deadline faced, I was unable to save the service time for each simulation as they will be intense files of 10000 lines each representing just numbers that won't even be checked by the user themselves, so why bother? 
