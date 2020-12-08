'''
 일원화된 라벨링 이미지 데이터셋을 가져오는 프로그램 -> learn_test_self.py
'''
import pickle
import numpy as np

# 라벨링된 데이터셋. 형식: (n, 256) / (n, 16, 16)
DATA_P = "lane2_thres.p"

data = pickle.load(open(DATA_P, "rb"), encoding="latin1" )
n_images = len(data)
# 데이터셋 1/3을 학습데이터로 사용.
test, training = data[0:int(n_images/3)], data[int(n_images/3):]

def get_training_data():
    
    trX = np.array([np.reshape(a[1], a[1].shape[1]**2) for a in training])
    #trX = np.array([a[1] for a in training])
    shape = np.shape(trX)[1]
    
    trY = np.zeros((len(training)),dtype=np.float)
    for i, data in enumerate(training):
        trY[i] = float(data[0])
    return trX, trY

def get_test_data():
    teX = np.array([np.reshape(a[1], a[1].shape[1]**2) for a in test])
    teY = np.zeros((len(test)),dtype=np.float)
    for i, data in enumerate(test):
        teY[i] = float(data[0])
    return teX,teY

if __name__ == '__main__':
    trX, trY = get_training_data()
    print(trX)
    teX, teY = get_test_data()
    print(teX)