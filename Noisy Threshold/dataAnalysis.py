import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle

class dataAnalysis():
    def __init__(self, subjects):
        self.subjects = subjects
    
    def parseList(self, arr):
        result = []
        for row in arr:
            element = row[1:len(row)-1].split(" ")
            element = [int(i) for i in element] 
            result.append(element)
        return np.array(result)

    def computeAccuracy(self):
        user_correctness = []
        lines = ["-","--","-.",":"]
        linecycler = cycle(lines)
        for subject in self.subjects:
            df = pd.read_csv(os.path.join(subject, "trial_data.csv"))
            num_trials = df.shape[0]
            user_order = df['User Order']
            ground_truth = df['Ground Truth']

            user_order = self.parseList(user_order)
            ground_truth = self.parseList(ground_truth)

            subject_correctness = []
            for trial_num in range(num_trials):
                num_correct = np.sum(user_order[trial_num] == ground_truth[trial_num])
                subject_correctness.append(num_correct)

            user_correctness.append(subject_correctness) 

            print(subject_correctness)
            plt.plot(range(num_trials), subject_correctness, label = subject, ls = next(linecycler))
            plt.xticks(range(num_trials))
            plt.yticks(range(1,4))
            plt.title('User Correctness')
            plt.xlabel('Trial Number')
            plt.ylabel('Number of correct predictions')
            
        user_correctness = np.array(user_correctness)
        plt.legend()
        plt.show()

if __name__ == '__main__':
    subjects = ["Nithin", "Phani", "Rahul", "Rathin"]
    da = dataAnalysis(subjects)
    da.computeAccuracy()