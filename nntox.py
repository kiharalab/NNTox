# Copyright (C) 2019 Aashish Jain, Daisuke Kihara, and Purdue University.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import numpy as np
import tensorflow as tf

class ToxinModel:
    
    def __init__(self):
        self.name = 'Toxin_Model'
        
    def run_model(self,test_data):
        
        sess = tf.Session()
        saver = tf.train.import_meta_graph('./model/saved_toxin_model/model_toxin.meta')
        saver.restore(sess,tf.train.latest_checkpoint('./model/saved_toxin_model/'))
        
        graph = tf.get_default_graph()

        weights = {
            'h1': graph.get_tensor_by_name("h1:0"),
            'h2': graph.get_tensor_by_name("h2:0"),
            'h3': graph.get_tensor_by_name("h3:0"),
            'out': graph.get_tensor_by_name("hout:0")
        }
        biases = {
            'b1': graph.get_tensor_by_name("b1:0"),
            'b2': graph.get_tensor_by_name("b2:0"),
            'b3': graph.get_tensor_by_name("b3:0"),
            'out': graph.get_tensor_by_name("bout:0")
        }
        
        X = tf.placeholder("float", [None,2596])

        def neural_net(x):

            layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
            layer_1 = tf.sigmoid(layer_1)
            layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
            layer_2 = tf.sigmoid(layer_2)
            layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
            layer_3 = tf.sigmoid(layer_3)
            out_layer = tf.matmul(layer_3, weights['out']) + biases['out']

            return out_layer

        logits = neural_net(X)
        prediction = tf.nn.sigmoid(logits)
        
        res = sess.run(prediction, feed_dict={X: test_data})
        res = list(np.argmax(res,axis=1))

        for i in range(len(res)):
            if res[i] == 0:
                res[i] = 'Toxin'
            else:
                res[i] = 'Non Toxin'

        
        return res

class KeywordModel:
    
    def __init__(self):
        self.name = 'Keyword_Model'
        
    def run_model(self,test_data):
        
        sess = tf.Session()
        saver = tf.train.import_meta_graph('./model/saved_keyword_model/model_keyword.meta')
        saver.restore(sess,tf.train.latest_checkpoint('./model/saved_keyword_model/'))
        
        graph = tf.get_default_graph()

        weights = {
            'h1': graph.get_tensor_by_name("h1:0"),
            'h2': graph.get_tensor_by_name("h2:0"),
            'h3': graph.get_tensor_by_name("h3:0"),
            'out': graph.get_tensor_by_name("hout:0")
        }
        biases = {
            'b1': graph.get_tensor_by_name("b1:0"),
            'b2': graph.get_tensor_by_name("b2:0"),
            'b3': graph.get_tensor_by_name("b3:0"),
            'out': graph.get_tensor_by_name("bout:0")
        }
        
        X = tf.placeholder("float", [None,2596])

        def neural_net(x):

            layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
            layer_1 = tf.sigmoid(layer_1)
            layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
            layer_2 = tf.sigmoid(layer_2)
            layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
            layer_3 = tf.sigmoid(layer_3)
            out_layer = tf.matmul(layer_3, weights['out']) + biases['out']

            return out_layer

        logits = neural_net(X)
        prediction = tf.nn.sigmoid(logits)
        
        res = sess.run(prediction, feed_dict={X: test_data})
        res = np.round(res)

        class_names = ['Cardiotoxin','Enterotoxin','Neurotoxin','Ion channel impairing toxin','Myotoxin','Dermonecrotic toxin','Hemostasis impairing toxin','G-protein coupled receptor impairing toxin','Complement system impairing toxin','Cell adhesion impairing toxin','Viral exotoxin']

        mode_of_action = []
        for i in range(len(res)):
            keyword_name = []
            for j in range(len(res[i])):
                    if res[i][j] == 1:
                        keyword_name.append(class_names[j])

            mode_of_action.append(keyword_name)
        
        return mode_of_action

def create_feature_vector(goterm_file):
    
    interested_goterm = np.load('./data/feature_vectore_goterms.npy')
    interested_goterm = interested_goterm.tolist()
    for i in range(len(interested_goterm)):
        interested_goterm[i] = interested_goterm[i].decode('UTF-8')

    #print(len(interested_goterm))

    inputs = []
    names = []

    f = open(goterm_file,'r')
    for row in f:
        r = row.strip()
        tmp = r.split()
        name = tmp[0]
        goterm = tmp[1].split(',')
        feature_vector = np.zeros(len(interested_goterm) + 1)
        other_count = 0

        if len(goterm) > 0:
            for term in goterm:
                if term in interested_goterm:
                    feature_vector[interested_goterm.index(term)] = 1
                else:
                    other_count += 1

        feature_vector[-1] = other_count
        feature_vector[943] = 0 

        inputs.append(feature_vector)
        names.append(name)

    return inputs,names

if __name__ == '__main__':

    goterm_file = sys.argv[1]

    try:
        mode = sys.argv[2]
    except:
        mode = 'toxin'

    inputs,names = create_feature_vector(goterm_file)

    if mode == 'toxin':

        toxin_model = ToxinModel()
        predictions = toxin_model.run_model(inputs)

        for i in range(len(predictions)):
            print(names[i],predictions[i])


    if mode == 'mode_of_action':

        keyword_model = KeywordModel()
        keyword_predictions = keyword_model.run_model(inputs)
        
        for i in range(len(keyword_predictions)):
            print(names[i],','.join(keyword_predictions[i]))
