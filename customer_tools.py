import numpy as np
import pandas as pd

#Transition probabilities matrix
df_Q = pd.read_csv('data/Q_matrix.csv', index_col=0)

#States of Markov chain
STATES = ['entrance', 'drinks', 'dairy', 'fruit', 'spices', 'checkout']

class Customer:
    '''
    Customer class that simulates a Markov chain for one customer based
    on Markov states defined above and a transition probability matrix
    '''
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.state = 'entrance'
        self.nb_state = 1
        self.gen = self.markov()
        self.history = ['entrance']

    def __repr__(self):
        return f"The customer number {self.customer_id} is at {self.state}"

    def get_next_state(self):
        return next(self.gen)

    def markov(self):

        while self.state != 'checkout':

            # calculate the next state
            next_state = np.random.choice(STATES, 1, p=df_Q.loc[f'{self.state}'])[0]

            if next_state == 'checkout':
                self.state = 'checkout'
                self.history.append(self.state)
                self.nb_state += 1
                yield self.state

            else:
                self.state = next_state
                self.history.append(self.state)
                self.nb_state += 1
                yield self.state
