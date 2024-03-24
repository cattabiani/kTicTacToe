import random
import torch
import os
import pickle


class QAgent:
    def __init__(
        self,
        learning_rate: float = 0.3,
        discount_factor: float = 0.9,
        epsilon: float = 0.1,
    ):
        self.qt = {}
        self.filename = "./data/qgent.pkl"
        if os.path.exists(self.filename):
            self.load_from_file()

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def save_to_file(self):
        print(f"save to file: {self.filename}")
        with open(self.filename, "wb") as file:
            pickle.dump(self.qt, file)

    def load_from_file(self):
        print(f"load from file: {self.filename}")
        with open(self.filename, "rb") as file:
            self.qt = pickle.load(file)

    def get_qtable(self, state):
        if state not in self.qt:
            self.qt[state] = torch.rand(1, 9)
        return self.qt[state]

    def get_move(self, state):

        r = random.random()
        if r < self.epsilon:
            return random.randint(0, 8)

        return torch.argmax(self.get_qtable(state)).item()

    def update(self, state, action, reward, next_state):
        if reward > 0:
            self.qt[state] = torch.zeros(1, 9)
            self.qt[state][0, action] = 1
            return

        if reward < 0:
            self.qt[state][0, action] -= 100
            return

        best_next_action_value = self.get_qtable(next_state).max()

        td_error = (
            reward
            - self.discount_factor * best_next_action_value
            - self.get_qtable(state)[0, action]
        )

        # print(reward, self.discount_factor*best_next_action_value, self.get_qtable(state)[0, action])
        self.qt[state][0, action] += self.learning_rate * td_error
        # print("after", self.qt[state][0, action])
