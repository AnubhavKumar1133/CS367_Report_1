import random
import math
import numpy as np

def haversine_distance(loc1, loc2):
    R = 6371.0
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

locations = {
    'Gandhinagar': (23.2156, 72.6369),
    'Jaipur': (26.9124, 75.7873),
    'Jodhpur': (26.2389, 73.0243),
    'Udaipur': (24.5854, 73.7125),
    'Jaisalmer': (26.9157, 70.9083),
    'Bikaner': (28.0229, 73.3119),
    'Ajmer': (26.4499, 74.6399),
    'Pushkar': (26.4901, 74.5542),
    'Mount Abu': (24.5926, 72.7157),
    'Chittorgarh': (24.8887, 74.6269),
    'Alwar': (27.5587, 76.6250),
    'Bharatpur': (27.2173, 77.4901),
    'Kota': (25.2138, 75.8648),
    'Bundi': (25.4305, 75.6499),
    'Sawai Madhopur': (25.9936, 76.3667),
    'Tonk': (26.1666, 75.7894),
    'Ranthambore': (26.0173, 76.5026),
    'Barmer': (25.7527, 71.4167),
    'Nagaur': (27.2020, 73.6760),
    'Pali': (25.7711, 73.3311),
    'Sikar': (27.6094, 75.1399)
}

def create_distance_matrix(locations):
    n = len(locations)
    distance_matrix = np.zeros((n, n))
    location_list = list(locations.keys())
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = haversine_distance(locations[location_list[i]], locations[location_list[j]])
    return distance_matrix, location_list

def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i], tour[i + 1]]
    total_distance += distance_matrix[tour[-1], tour[0]]  
    return total_distance

def simulated_annealing(distance_matrix, location_list, initial_temperature, cooling_rate, iterations):
    gandhinagar_index = location_list.index('Gandhinagar')
    
    current_tour = list(range(1, len(location_list)))  
    random.shuffle(current_tour)
    current_tour = [gandhinagar_index] + current_tour
    
    current_distance = calculate_total_distance(current_tour, distance_matrix)
    
    best_tour = current_tour[:]
    best_distance = current_distance
    
    temperature = initial_temperature
    
    for i in range(iterations):
        new_tour = current_tour[:]
        a, b = random.sample(range(1, len(location_list)), 2)  # Exclude Gandhinagar (index 0)
        new_tour[a], new_tour[b] = new_tour[b], new_tour[a]
        
        new_distance = calculate_total_distance(new_tour, distance_matrix)
        
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temperature):
            current_tour = new_tour[:]
            current_distance = new_distance
        
        if current_distance < best_distance:
            best_tour = current_tour[:]
            best_distance = current_distance
        
        temperature *= cooling_rate
    
    return best_tour, best_distance

if __name__ == "__main__":
    distance_matrix, location_list = create_distance_matrix(locations)
    
    initial_temperature = 10000
    cooling_rate = 0.995
    iterations = 100000
    
    best_tour, best_distance = simulated_annealing(distance_matrix, location_list, initial_temperature, cooling_rate, iterations)
    
    print("Best tour: ")
    for idx in best_tour:
        print(location_list[idx], end=" -> ")
    print(location_list[best_tour[0]])
    print("Starting point: Gandhinagar and Ending point: Gandhinagar") 
    print(f"Best distance: {best_distance:.2f} km")