from make_gif_tools import save_each_state, make_gif_from_states

#Number of customers to simulate
Nb_customers = 100

#Simulate Nb_customers, assign a random colour for each customer and save the states
save_each_state(Nb_customers)
#Make a gif of all the states for all customers in the order of occurence
make_gif_from_states(Nb_customers)
