import random
import time
import csv

class LinearProbing:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash(self, key):
        return key % self.size

    def insert(self, key):
        index = self.hash(key)

        for i in range(self.size):
            if self.table[index] is None:
                self.table[index] = key
                return True
            if self.table[index] == key:
                return True
            index = (index + 1) % self.size

        return False

    def search(self, key):
        index = self.hash(key)

        for i in range(self.size):
            if self.table[index] is None:
                return False
            if self.table[index] == key:
                return True
            index = (index + 1) % self.size

        return False

#modified https://www.geeksforgeeks.org/dsa/c-program-hashing-chaining/ code
class Chaining:
    def __init__(self, size):
        self.size = size
        self.table = [[] for i in range(size)]

    def hash(self, key):
        return key % self.size

    def insert(self, key):
        index = self.hash(key)
        self.table[index].append(key)

    def search(self, key):
        index = self.table[self.hash(key)]
        for i in range(len(index)):
            if index[i] == key:
                return True
        return False
    

def time_inserts(hash_type, m, keys):
    table = hash_type(m)

    start = time.perf_counter()
    for i in range(len(keys)):
        table.insert(keys[i])
    end = time.perf_counter()

    return table, (end - start)


def time_searches(table, search_keys):
    
    start = time.perf_counter()
    for i in range(len(search_keys)):
        table.search(search_keys[i])
    end = time.perf_counter()

    return end - start

def run_trials(
    min_size=4, #min_size * load_fac must be greater than 1
    max_size=500, #speed seems to plateau 1500-2000 with step 50, min 50
    step=2,
    load_fac=(0.25, 0.50, 0.60, 0.70, 0.80, 0.90),
    trials_per_load=50,
    searches_per_trial=5000,
    seed=100,
):
    
    random.seed(seed)

    for load in load_fac:
        filename = f"load_{load:.2f}.csv"

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "m",
                "load_fac",
                "Linear_I_avg",
                "Chain_I_avg",
                "Linear_S_avg",
                "Chain_S_avg",
            ])

            for m in range(min_size, max_size + 1, step):
                n = int(load * m)

                Linear_I_total = 0.0
                Chain_I_total = 0.0
                Linear_S_total = 0.0
                Chain_S_total = 0.0

                for trial in range(trials_per_load):
                    inserted_keys = random.sample(range(1, m*1000), n)

                    num_in = searches_per_trial // 2
                    num_out = searches_per_trial - num_in

                    keys_in = random.choices(inserted_keys, k=num_in)
                    keys_out = random.choices(range(m*1001, m*2000), k=num_out)

                    search_keys = keys_in + keys_out
                    random.shuffle(search_keys)

                    linear_table, Linear_I_time = time_inserts(LinearProbing, m, inserted_keys)
                    chain_table, Chain_I_time = time_inserts(Chaining, m, inserted_keys)

                    Linear_S_time = time_searches(linear_table, search_keys)
                    Chain_S_time = time_searches(chain_table, search_keys)

                    Linear_I_total += Linear_I_time
                    Chain_I_total += Chain_I_time
                    Linear_S_total += Linear_S_time
                    Chain_S_total += Chain_S_time

                Linear_I_avg_sec = Linear_I_total / trials_per_load
                Chain_I_avg_sec = Chain_I_total / trials_per_load
                Linear_S_avg_sec = Linear_S_total / trials_per_load
                Chain_S_avg_sec = Chain_S_total / trials_per_load

                writer.writerow([
                    m,
                    f"{load:.2f}",
                    Linear_I_avg_sec,
                    Chain_I_avg_sec,
                    Linear_S_avg_sec,
                    Chain_S_avg_sec,
                ])

        print(f"Wrote {filename}")



if __name__ == "__main__":
    run_trials()