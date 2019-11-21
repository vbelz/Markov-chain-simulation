from customer_tools import Customer
import numpy as np
import pandas as pd


def arrival_time_from_hour_distribution(df, date):
    """ This function takes as input the average number of customer
        entering the shop per hour and return a randomly sampled
        arrival time per minute to simulate arrival time of customers
        in the shop for one day"""
    #Get min and max hours
    hour_min = df.index.min()
    hour_max = df.index.max()+1
    hours = np.arange(hour_min,hour_max,1)
    minutes = np.arange(0,60,1)
    list_entrance = []

    for h in hours:
        #Get the number of people per hour
        nb_people = df.loc[df.index == h ,'entrance count'].values[0]
        #Randomly distribute these expected arrivals as minutes
        minutes_entrance = np.random.choice(minutes,nb_people,replace=True)
        minutes_in_h=[]
        for m in minutes_entrance :
            time = f'{h}:{m}:00'
            list_entrance.append(time)

    #Create dataframe with customer id and time arrival
    day_customer = {'time':list_entrance}
    df_time = pd.DataFrame(day_customer)
    df_time = pd.to_timedelta(df_time['time'], unit='s').copy()
    df_time = df_time.sort_values(ascending=True)
    df_time = df_time.reset_index()
    df_time.drop(columns=['index'],inplace=True)
    df_time['date'] = date
    df_time['date'] = pd.to_datetime(df_time['date'])
    df_time['time'] = df_time['date'] + df_time['time']
    d = {'time':df_time['time'],'customer_id':df_time.index+1}
    df_time = pd.DataFrame(d)

    return df_time


def simulate_customers(df_entry):
    """
    This function takes the hour/minute arrival time and the id number of
    customers and will simulate the behaviour in the shop for each customer
    and return a dataframe with minute by minute location for each customer
    """
    df_simulation = pd.DataFrame()

    #Simulate behaviour in the shop for each customer id
    for id in df_entry['customer_id']:
        df_customer = df_entry.loc[df_entry['customer_id']==id,:].copy()
        #Create a new customer class
        new_customer = Customer(id)
        #Calling all generators to have access to history
        all_states = list(new_customer.gen)
        #Getting the entry time in good format for date_range
        entry_time = df_customer.loc[df_customer['customer_id']==id,'time'].iloc[0]
        #Number of minute to add to entry time to have leaving time
        minutes_to_add = new_customer.nb_state-1
        leaving_time = pd.to_datetime(df_entry.loc[df_entry['customer_id']==id,'time']) + pd.Timedelta(f'{minutes_to_add} min')
        #Getting leaving time in good format
        leaving_time = leaving_time.iloc[0]
        #Creating time range from arrival to leaving time
        minute_index = pd.date_range(entry_time,leaving_time, freq="min")

        #Put new customer infos in a dataframe to append
        d={'time':minute_index,'location':new_customer.history}
        df_new_customer = pd.DataFrame(d)
        df_new_customer['customer_id'] = id

        df_simulation = pd.concat([df_simulation, df_new_customer])

    return df_simulation
