import time

from marble_solitaire import MarbleSolitaire
from priority_queue_agent import PriorityQueueAgent
from best_first_search_agent import BestFirstSearchAgent
from a_star_search_agent import AStarSearchAgent

marble_solitaire = MarbleSolitaire()

selected_agent = input("Select an agent from the following:\n1. Priority queue based agent\n2. Best first search based agent\n3. A* search based agent\n")

if selected_agent == 1:
    agent = PriorityQueueAgent(marble_solitaire)
elif selected_agent == 2:
    agent = BestFirstSearchAgent(marble_solitaire)
else:
    agent = AStarSearchAgent(marble_solitaire)

print("Calculating...")
start_time = time.process_time()
solution = agent.search()
end_time = time.process_time()

if solution[0] is not None:
    print("\nSolution found!\nPath cost:", solution[0], "\nNumber of states explored:", solution[1], "\nTime elapsed:", end_time-start_time)
else:
    print("\nNo solution found.\nNumber of states explored:", solution[1], "\nTime elpased:", end_time-start_time)
