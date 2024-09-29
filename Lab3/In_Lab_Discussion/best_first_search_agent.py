import heapq
import copy

class BestFirstSearchAgent:
    def __init__(self, problem):
        self.problem = problem
        self.visited_states = set()

    def search(self):
        states_explored = 1
        initial_state = copy.deepcopy(self.problem.initial_state)
        initial_state_tuple = tuple(map(tuple, initial_state))
        priority_queue = [(self.problem.marbles_left_heuristic(initial_state), 0, initial_state_tuple)]
        heapq.heapify(priority_queue)

        while priority_queue:
            _, path_cost, current_state = heapq.heappop(priority_queue)

            if self.problem.is_goal_state([list(state) for state in current_state]):
                return (path_cost, states_explored)

            current_state_tuple = tuple(map(tuple, current_state))
            if current_state_tuple in self.visited_states:
                continue
            
            self.visited_states.add(current_state_tuple)

            new_states = self.problem.get_next_states([list(state) for state in current_state])

            for new_state in new_states:
                new_state_tuple = tuple(map(tuple, new_state))
                new_cost = path_cost + 1
                if new_state_tuple in self.visited_states:
                    continue

                found = False
                for i, (heu, cost, state) in enumerate(priority_queue):
                    if state == new_state_tuple:
                        found = True
                        if new_cost < cost:
                            priority_queue[i] = (heu, new_cost, new_state_tuple)
                            heapq.heapify(priority_queue)
                        break
                
                if not found:
                    heapq.heappush(priority_queue, (self.problem.marbles_left_heuristic(new_state), new_cost, new_state_tuple))
                    states_explored += 1

        return (None, states_explored)