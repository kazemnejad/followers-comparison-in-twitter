# Followers Comparison in Twitter data
Data collection & scraper scripts can be found on branch "master"
Checkout results in [report.pdf](https://github.com/kazemnejad/followers-comparison-in-twitter/raw/cnn/report.pdf) & [report_slides.pdf](https://github.com/kazemnejad/followers-comparison-in-twitter/raw/cnn/report_slides.pdf)

Single layer Convolution Neural network text classifier implementation in Tensorflow <br/>
**Check branch master for Naive Bayes model*

### Model Hyper Parameters:

- Filter size: 2, 3, 4 windows
- Number filters: 32
- Word embedding size: 200
- Maximum document length: 40
- Static & dynamic word embedding is used
- Static word vectors is trained using GloVe model on "52M+ token" corpus, [check out results](https://raw.githubusercontent.com/kazemnejad/followers-comparison-in-twitter/cnn/outputs/pic.png)


![](https://raw.githubusercontent.com/kazemnejad/followers-comparison-in-twitter/cnn/outputs/graph.png "computation graph")
