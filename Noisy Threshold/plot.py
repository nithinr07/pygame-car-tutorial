import os
import matplotlib.pyplot as plt

def plot_graph(path):
    files = os.listdir(path)
    thresholds = [30,50,70]
    x = {}
    y = {}
    for threshold in thresholds:
        x[threshold] = []
        y[threshold] = []
    trial=1
    for file in files:
        print(file)
        for threshold in thresholds:
            x[threshold].append(trial)
            y[threshold].append(0)
        trial+=1
        with open(path+'/'+file) as f:
            j = 0
            for line in f:
                if(j==0):
                    j+=1 
                    continue
                val = line.split(',')
                val = [float(x) for x in val[1:]]
                th = val[1]
                score = val[3]
                y[th][-1] = max(y[th][-1],score)
    plt.figure()
    legend = []
    for threshold in thresholds:
        plt.plot(x[threshold],y[threshold])
        legend.append("Th: {}".format(threshold))
    plt.legend(legend)
    # plt.xticks(range(1,1+len(x[30])))
    plt.xlabel("Trials")
    plt.ylabel("Score (num of coins)")
    plt.title('Plot of {}'.format(path[:-1]))
    plt.grid()

                
if __name__ == '__main__':
    plot_graph('Arvind/')
    plot_graph('Ajay/')
    plt.show()