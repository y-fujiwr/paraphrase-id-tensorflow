import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# Step 6: Visualize the embeddings.
def plot_with_labels(final_embeddings, reverse_dictionary, filename='tsne.png'):

    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
    plot_only = min(500, len(reverse_dictionary))
    low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
    low_dim_embs = final_embeddings
    labels = [reverse_dictionary[i] for i in range(plot_only)]

    assert low_dim_embs.shape[0] >= len(labels), 'More labels than embeddings'
    # plt.figure(figsize=(18, 18))  # in inches
    colors = np.random.rand(100)
    for i, label in enumerate(labels):
        x, y = low_dim_embs[i, :]
        c = colors[i]
        print(c)
        plt.scatter(x, y, c=0.1)
        # plt.annotate(label,
        #              xy=(x, y),
        #              xytext=(5, 2),
        #              textcoords='offset points',
        #              ha='right',
        #              va='bottom')
    plt.show()
    # plt.savefig(filename)


def test():
    mu, sigma = 10, 1
    vectors = np.random.normal(mu, sigma, [100, 2])
    rev_dict = ["a_{:03d}".format(i) for i in range(8)]
    print(rev_dict)
    plot_with_labels(vectors, rev_dict)


if __name__ == '__main__':
    test()
