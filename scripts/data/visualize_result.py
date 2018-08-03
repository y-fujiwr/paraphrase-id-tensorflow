import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

label_map = {
    '2': 'DownloadFromWeb',
    '3': 'SecureHash',
    '4': 'CopyFile',
    '5': 'Decompressziparchive.',
    '6': 'ConnecttoFTPServer',
    '7': 'BubbleSortArray',
    '8': 'SetupSGV',
    '9': 'SetupSGVEventHandler',
    '10': 'Executeupdateandrollback.',
    '11': 'InitializeJavaEclipseProject.',
}


def plot_pairs(file_path):
    df = np.genfromtxt(file_path, delimiter=',')
    # print(df.shape)
    _, categories, _, encodings = np.hsplit(df, [3, 4, 8, ])
    e1, e2 = np.hsplit(encodings, 2)
    # print(e1.shape, e2.shape)
    embeddings = np.concatenate((e1, e2))
    categories = np.vstack((categories, categories))
    # print(embeddings.shape)
    # print(categories)
    _plot(embeddings, categories, 20)


def _plot(final_embeddings, categories, plot_max=500, filename='tsne.png'):
    colors = list(map(lambda x: "C{:d}".format(int(x) % 10), categories))
    # print(colors)

    tsne = TSNE(perplexity=30, n_components=2, init='pca', n_iter=5000)
    plot_only = min(plot_max, len(final_embeddings))
    print(plot_only)
    low_dim_embs = tsne.fit_transform(final_embeddings[:plot_only, :])
    # low_dim_embs = final_embeddings

    x, y = np.hsplit(low_dim_embs, 2)

    alpha = 0.7
    # plt.figure(figsize=(18, 18))  # in inches
    fig, ax = plt.subplots()
    for i, _ in enumerate(x):
        category = int(categories[i])
        color = "C{:d}".format(category % 10)
        label = label_map[str(category)]
        ax.scatter(x[i], y[i], c=color, marker='.', alpha=0.7, label=label)
    # ax.scatter(x, y, c=colors, alpha=alpha, marker='.')
    ax.legend(loc=2)
    plt.show()
    return

    for i in range(plot_only):
        x, y = low_dim_embs[i, :]
        c = colors[i]
        print(c)
        plt.scatter(x, y, c='C1', alpha=0.5)
        # plt.annotate(label,
        #              xy=(x, y),
        #              xytext=(5, 2),
        #              textcoords='offset points',
        #              ha='right',
        #              va='bottom')
    plt.show()
    # plt.savefig(filename)


def _plot_colors():
    import random
    fig, ax = plt.subplots()
    for i in range(2, 12):
        category = i
        color = "C{:d}".format(category % 10)
        label = label_map[str(category)]
        ax.scatter(random.random(), random.random(), c=color, marker='.', alpha=0.7, label=label)
    # ax.scatter(x, y, c=colors, alpha=alpha, marker='.')
    ax.legend(loc=2)
    plt.show()


def test():
    plot_pairs('/home/wuyuhao/PycharmProjects/paraphrase-id-tensorflow/data/processed/bcb/clone_and_false_positives'
               '/balanced/all-balanced/clone-with-categories/test.5000.csv.output_predictions.csv')


if __name__ == '__main__':
    # test()
    _plot_colors()
