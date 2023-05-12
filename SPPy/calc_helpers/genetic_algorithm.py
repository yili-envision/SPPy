import numpy as np
import pandas as pd
from tqdm import tqdm

def pop_initialization(n_genes, n_chromosones, bounds):
    """
    Returns a DataFrame with initial population.
    :param n_genes:
    :param n_chromosones:
    :param bounds:
    :return:
    """
    pop = np.zeros((n_chromosones, n_genes))
    for c_index in range(n_chromosones):
        for g_index in range(n_genes):
            a = np.random.uniform(bounds[g_index][0], bounds[g_index][1])
            pop[c_index, g_index] = a
    return pd.DataFrame(pop)

def fitness_calc(obj_func, df):
    fitness_list = []
    for index, row in df.iterrows():
        fitness = obj_func(row)
        fitness_list.append(fitness)
    df['fitness'] = fitness_list
    return df

def mating_pool(n_pool, df):
    df = df.sort_values(by = 'fitness').reset_index(drop = True).iloc[:n_pool]
    df.drop('fitness', axis = 1, inplace= True)
    return df

def new_pop(n_chromosomes, n_genes, n_elite, df):
    df_new = df.iloc[:n_elite]
    df = df.to_numpy()
    for i in range(n_chromosomes - n_elite):
        random_index = np.random.choice(df.shape[0], 2, replace=False)
        alpha = np.random.uniform(0,1)
        row_list = []
        for g in range(n_genes):
            child = alpha*df[random_index[0],g] + \
                    (1-alpha)*df[random_index[1], g]
            row_list.append(child)
        temp_df = pd.DataFrame([row_list])
        df_new = pd.concat([df_new, temp_df], ignore_index= True)
    return df_new

def mutate(n_chromosomes, n_genes, n_elite, c_f, df):
    pop_to_mutate = int((n_chromosomes - n_elite) * (1 - c_f))
    random_index = np.random.choice(df.iloc[1:].index, pop_to_mutate, replace= False)
    for i in random_index:
        for g in range(n_genes):
            df.iloc[i,g] = df.iloc[i,g] + df.std(axis=0)[g] * np.random.uniform(0,1)
    return df

def ga(objective_func, n_generation, n_chromosones, n_genes, bounds, n_pool, n_elite, c_f):
    df_results = pd.DataFrame()
    df = pop_initialization(n_genes, n_chromosones, bounds)
    for gen in range(n_generation):
        df = fitness_calc(objective_func, df)
        df = mating_pool(n_pool,df)
        df = new_pop(n_chromosones, n_genes, n_elite, df)
        df = mutate(n_chromosones, n_genes, n_elite, 0.8, df)
        df_results = pd.concat([df_results, df.iloc[0]], ignore_index= True)
        print('---------------------------------------------------------------------------------------')
        print(f'gen: {gen}, objective func value: {fitness_calc(objective_func, df).iloc[0,-1]:.5f}')
        print('----------------------------------------------------------------------------------------')
    return df_results, df.iloc[0].to_numpy(), fitness_calc(objective_func, df).iloc[0,-1]