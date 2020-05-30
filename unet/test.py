import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    epoch = list(range(1,301))
    loss = []
    s_ = 1.2

    

    fig = plt.figure(figsize=(10,10))
    
    plt.title("epoch/loss")
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.plot(epoch,loss,'b-')
    plt.show()