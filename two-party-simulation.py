# Fed valuation for two parties
import random
import numpy as np
import time

def PSI_size_server(sets_1, sets_2):
    PSI_sizes = []
    for set1 in sets_1:
        for set2 in sets_2:
            PSI_sizes.append(len(set(set1) & set(set2)))
    return PSI_sizes

def generate_sets(sample_num, value_num, sample_copy_times):
    whole_set = list(range(sample_num))
    # split the whole set into value num groups randomly
    random.shuffle(whole_set)
    val_idxes = random.sample(range(1, sample_num), value_num-1)
    val_idxes.append(0)
    val_idxes.append(sample_num)
    val_idxes.sort()
    split_sets = []
    for i in range(len(val_idxes)-1):
        split_set = whole_set[val_idxes[i]:val_idxes[i+1]]
        dup_split_set = split_set.copy()
        split_set_np = np.array(split_set)
        # do copies
        for j in range(1, sample_copy_times):
            copied_set = list(split_set_np + sample_num * j)
            dup_split_set.extend(copied_set)
     
        split_sets.append(dup_split_set)
    return split_sets

if __name__ == "__main__":
    sample_num = int(100000)
    sample_copy_times = 3
    data_party_value_num = 2
    task_party_value_num = 2 * 2

    repeated_times = 5

    server_runtimes = []
    for _ in range(repeated_times):

        # client side (each party has its own feature value-split sample sets)
        print("sample_num", sample_num, ", copy_times", sample_copy_times, ", data_party_value_num", data_party_value_num, ", task_party_value_num", task_party_value_num)
        data_party_sets = generate_sets(sample_num, data_party_value_num, sample_copy_times)
        task_party_sets = generate_sets(sample_num, task_party_value_num, sample_copy_times)

        #print(data_party_sets)
        #print(task_party_sets)

        # server side (compute PSI size)
        server_start_time = time.time()
        PSI_sizes = PSI_size_server(data_party_sets, task_party_sets)
        server_end_time = time.time()
        server_runtime = server_end_time - server_start_time

        print("sum of PSI sizes:", np.sum(PSI_sizes))
        print("server running time", server_runtime, "seconds")
        server_runtimes.append(server_runtime)
        # print("PSI sizes", PSI_sizes)

    print("server running time (avg): ", np.mean(server_runtimes), ", std: ", np.std(server_runtimes))