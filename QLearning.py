from numpy import matrix, zeros, array, argmax

class QLearning(object):

    def __init__(self, n_states, n_actions, alpha_input = 0.3, r=1, gamma_input = 0.5):
        '''
            Is an array consist of all possible states
            A is an array consist of all posiible actions
        '''
        self.sn    = n_states
        self.an    = n_actions

        #Resetting the Q-Matrix
        self.qMat = zeros((n_states, n_actions))
        matrix_to_csv(self.qMat)

        #Reading the Q-matrix from file
        qMat_file = open('qMat.csv', 'r')
        self.qMat = csv_to_matrix(qMat_file)
        qMat_file.close()

        self.alpha = alpha_input
        self.gamma = gamma_input

    def train(self, s0, a0, s1, a1, r):
        self.qMat[s0, a0] += self.alpha*(r + self.gamma*max(self.qMat[s1]) - self.qMat[s0, a0])
        matrix_to_csv(self.qMat)

    def predict(self, s):
        return argmax(self.qMat[s])


def csv_to_matrix(f):
    return array(map(lambda x: map(lambda y: float(y), x.split(',')), f.read().splitlines()))

def matrix_to_csv(mat):
    qMat_file = open('qMat.csv', 'w')
    dim = mat.shape
    tmp_str = ''
    for i in range(dim[0]):
        for j in range(dim[1]):
            tmp_str+= '{},'.format(mat[i,j])
        tmp_str=tmp_str[:-1] + '\n' #removing the last + add the new line symbol
    qMat_file.write(tmp_str)
    qMat_file.close() #close the file object

def main():
    QLearning(100, 3)

if __name__ == '__main__':
    main()
