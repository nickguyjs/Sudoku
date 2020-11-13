import numpy as np
import matplotlib.pyplot as plt

alg1easy = []
alg2easy = []
alg1med = []
alg2med = []

def readFile():
  with open('results.txt') as f:
    line = f.readline()
    cnt = 1
    while line:
      #print("{}".format(line.strip()))  
      val = line.strip()
      if "alg1" in val:
        if "easy" in val:
          alg1easy.append((int(val[10:val.index(':', 11)]), float(val[val.index(':', 11)+1:len(val)])))
        if "medium" in val:
          alg1med.append((int(val[12:val.index(':', 13)]), float(val[val.index(':', 13)+1:len(val)])))
      if "alg2" in val:
        if "easy" in val:
          alg2easy.append((int(val[10:val.index(':', 11)]), float(val[val.index(':', 11)+1:len(val)])))
        if "medium" in val:
          alg2med.append((int(val[12:val.index(':', 13)]), float(val[val.index(':', 13)+1:len(val)])))
      line = f.readline()
      cnt += 1
#  print(str(alg1easy))
#  print(str(alg2easy))
#  print(str(alg1med))
#  print(str(alg2med))


def plotter(alg):
  np.random.seed(19680801)
  readFile()
  fig = plt.figure()
  fig.subplots_adjust(top=0.8)
  ax1 = fig.add_subplot(211)
  ax1.set_ylabel('Time(seconds)')
  ax1.set_xlabel('# of recursions')
  if(alg == "1"):
    ax1.set_title('Plot of Algorithm 1 - Easy Problems')
    plt.scatter(*zip(*alg1easy))
    plt.show()
  if(alg == "2"):
    ax1.set_title('Plot of Algorithm 1 - Medium Problems')
    plt.scatter(*zip(*alg1med))
    plt.show()
  if(alg == "3"):
    ax1.set_title('Plot of Algorithm 2 - Easy Problems')
    plt.scatter(*zip(*alg2easy))
    plt.show()
  if(alg == "4"):
    ax1.set_title('Plot of Algorithm 2 - Medium Problems')
    plt.scatter(*zip(*alg1med))
    plt.show()
  if(alg == "5"):
    ax1.set_title('Plot of All Data')
    plt.scatter(*zip(*alg1easy))
    plt.scatter(*zip(*alg1med))
    plt.scatter(*zip(*alg2easy))
    plt.scatter(*zip(*alg1med))
    plt.show()
