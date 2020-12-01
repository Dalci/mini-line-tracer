import pickle
import numpy as np

def get_training_data():
    training_data = pickle.load( open( "re_lane.p", "rb" ), encoding="latin1" )

    n_images = len(training_data)

    trX = np.array([np.reshape(a[1], a[1].shape[0]**2) for a in training_data])
    
    trY = np.zeros((len(training_data)),dtype=np.float)
    for i, data in enumerate(training_data):
        trY[i] = float(data[0])
    return trX, trY

def get_test_data():
    test_data = pickle.load(open("test_lane.p", "rb"))
    teX = np.array([np.reshape(a, a.shape[0]**2) for a in test_data])
    
    return teX

if __name__ == '__main__':
    trX, trY = get_training_data()
    print(trX.shape)

    teX = get_test_data()
    print(teX.shape)