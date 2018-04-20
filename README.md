# Followers Comparison in Twitter data

Single layer Convolution Neural network text classifier implementation in Tensorflow

### Model Hyper Parameters:

- Filter size: 2, 3, 4 windows
- Number filters: 32
- Word embedding size: 200
- Maximum document length: 40
- SoftMax output layer
- Static & dynamic word embedding is used
- Static word vectors is trained using GloVe model on "52M+ token" corpus, [check out results](https://raw.githubusercontent.com/kazemnejad/followers-comparison-in-twitter/cnn/outputs/pic.png)


![](https://raw.githubusercontent.com/kazemnejad/followers-comparison-in-twitter/cnn/outputs/graph.png "computation graph")
