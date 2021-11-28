# %%
# import clustimage
# print(dir(clustimage))
# print(clustimage.__version__)
# 
# Read image according the preprocessing steps

# %%
# Import library
from clustimage import Clustimage

# Init with settings such as PCA
cl = Clustimage(method='pca')

# load example with flowers
pathnames = cl.import_example(data='flowers')

# Cluster flowers
results = cl.fit_transform(pathnames)

# Read the unseen image. Note that it is import to use the cl.imread functionality as these will perform exactly the same preprocessing steps as for the clustering.
# img = cl.imread(unseen_image)
# plt.figure(); plt.imshow(img.reshape((128,128,3)));plt.axis('off')

# Find images using the path location.
results_find = cl.find(pathnames[0:2], k=0, alpha=0.05)

# Show whatever is found. This looks pretty good.
cl.plot_find()
cl.scatter()


# %% fotos on disk
from clustimage import Clustimage
# Init
cl = Clustimage(method='pca', grayscale=True)
# Load example with faces
face_results = cl.detect_faces('D://magweg1//')
# Preproceesing, cluster detection
results = cl.fit_transform(face_results['pathnames_face'])

cl.cluster(min_clust=7)
cl.clusteval.plot()
cl.scatter(zoom=None)

# out = cl.unique()
cl.plot_unique(img_mean=False)

out = cl.find(face_results['pathnames_face'][20], k=None, alpha=0.05, metric='euclidean')
cl.plot_find()

out = cl.find(face_results['pathnames_face'][20], k=5, alpha=None, metric='euclidean')
cl.plot_find()

cl.plot_faces(eyes=False)

# cluster labels
labels = results['labels']

# Plot dendrogram
cl.dendrogram()
# Scatter
cl.scatter()
cl.scatter(zoom=None)
# Plot faces
cl.plot_faces(eyes=False)
# Make plot
cl.plot(labels=15, show_hog=True)
# Cleaning files
cl.clean_files()


cl.clusteval.plot()
cl.clusteval.scatter(cl.results['feat'])
cl.clusteval.scatter(cl.results['xycoord'])
cl.pca.plot()
cl.pca.scatter(legend=False, label=False)

cl.save(overwrite=True)
cl.load()


# %% FLOWERS
# Load library
from clustimage import Clustimage

# Init with default settings
cl = Clustimage(method='hog', params_hog={'orientations':8, 'pixels_per_cell':(8,8)})
# cl = Clustimage(method='pca')
# load example with flowers
pathnames = cl.import_example(data='flowers')
# Detect cluster
results = cl.fit_transform(pathnames, min_clust=3, max_clust=13)

# cl.cluster(min_clust=3, max_clust=13)
# Plot the evaluation of the number of clusters
cl.clusteval.plot()
# cl.pca.plot()

# uiimgs = cl.unique()
cl.plot_unique(img_mean=False, show_hog=True)
cl.plot_unique(img_mean=True, show_hog=True)

# Scatter
cl.scatter(dotsize=50)
cl.scatter(dotsize=50, img_mean=False, zoom=0.5)
# Plot clustered images
cl.plot()
cl.plot(labels=[3], show_hog=True)
cl.plot(show_hog=False)
# Plot dendrogram
cl.dendrogram()

# Make prediction
results_find = cl.find(pathnames[0:5], k=10, alpha=0.05)
cl.plot_find()

# Plot the explained variance
if cl.params['method']=='pca': cl.pca.plot()
# Make scatter plot of PC1 vs PC2
if cl.params['method']=='pca': cl.pca.scatter(legend=False, label=True)
# Plot the evaluation of the number of clusters
cl.clusteval.plot()
# Make silhouette plot
cl.clusteval.scatter(cl.results['xycoord'])

# %% FACES
from clustimage import Clustimage
# Init
cl = Clustimage(method='hog', grayscale=True, params_hog={'orientations':8, 'pixels_per_cell':(8,8)})
# cl = Clustimage(method='pca', grayscale=True)
# Load example with faces
pathnames = cl.import_example(data='faces')
# Detect faces
face_results = cl.detect_faces(pathnames)
# Preproceesing, cluster detection
results = cl.fit_transform(face_results['pathnames_face'])


cl.clusteval.plot(figsize=(10,6))


out = cl.unique()
cl.plot_unique(img_mean=True)
cl.plot_unique(img_mean=False, show_hog=True)


out = cl.find(face_results['pathnames_face'][20], k=None, alpha=0.05, metric='euclidean')
cl.plot_find()

out = cl.find(face_results['pathnames_face'][20], k=5, alpha=None, metric='euclidean')
cl.plot_find()

cl.plot_faces(eyes=False)

# cluster labels
labels = results['labels']

# Plot dendrogram
cl.dendrogram()
# Scatter
cl.scatter()
cl.scatter(zoom=None)
# Plot faces
cl.plot_faces(eyes=False)
# Make plot
cl.plot(labels=17, show_hog=True)
# Cleaning files
cl.clean_files()


cl.clusteval.plot()
cl.clusteval.scatter(cl.results['feat'])
cl.clusteval.scatter(cl.results['xycoord'])
cl.pca.plot()
cl.pca.scatter(legend=False, label=False)

cl.save(overwrite=True)
cl.load()


# %% MNIST DATAST
import matplotlib.pyplot as plt
from clustimage import Clustimage
# init
# cl = Clustimage(method='pca')
cl = Clustimage(method='hog', grayscale=False, params_hog={'pixels_per_cell':(2,2)})
# cl = Clustimage(method='hog', embedding='tsne', grayscale=False, dim=(8,8), params_pca={'n_components':50})
# Example data
X = cl.import_example(data='mnist')
# Preprocessing, feature extraction and cluster evaluation
results = cl.fit_transform(X)

cl.clusteval.plot()

# Scatter
cl.scatter(zoom=3, img_mean=False)
cl.scatter(zoom=None, img_mean=False)


cl.clusteval.plot()
cl.clusteval.scatter(X)

cl.pca.plot()


cl.plot_unique(img_mean=True, show_hog=True)
cl.plot(cmap='binary', labels=[4,5])

results_find = cl.find(X[0:2,:])
cl.plot_find()

cl.plot_unique(img_mean=False, show_hog=True)
cl.plot_unique(img_mean=True, show_hog=True)

# labx = cl.cluster()
# labx = cl.cluster(cluster_space='high', cluster='agglomerative', evaluate='silhouette', metric='euclidean', linkage='ward', min_clust=2, max_clust=25)

# Plot the clustered images
cl.plot(cmap='binary', labels=[1,2], show_hog=True)
cl.plot(cmap='binary')
# Plotting
cl.dendrogram()


# %% FLOWERS HOG FEATURES

import matplotlib.pyplot as plt
from clustimage import Clustimage
# init
cl = Clustimage()
# cl = Clustimage(method='hog')
# Load example data
path_to_imgs = cl.import_example(data='flowers')
# Read image according the preprocessing steps
img = cl.imread(path_to_imgs[0], dim=(128,128))
# Extract HOG features
img_hog = cl.extract_hog(img)

plt.figure();
fig,axs=plt.subplots(1,2)
axs[0].imshow(img.reshape(128,128,3))
axs[0].axis('off')
axs[0].set_title('Preprocessed image', fontsize=10)
axs[1].imshow(img_hog.reshape(128,128), cmap='binary')
axs[1].axis('off')
axs[1].set_title('HOG', fontsize=10)


# %% 101_ObjectCategories
# import clustimage as cl
# pathnames = cl.listdir('D://magweg//101_ObjectCategories//')
# idx=[]
# for i in range(0,500):
#     idx.append(np.random.randint(9000))
# idx = np.unique(np.array(idx))
# pathnames = list(np.array(pathnames)[idx])
# print(len(pathnames))

from clustimage import Clustimage
# init
# cl = Clustimage(method='pca', params_pca={'n_components':0.95})
cl = Clustimage(method='pca-hog', grayscale=True, params_hog={'pixels_per_cell':(4,4)})
# Collect samples

# Preprocessing and feature extraction
# 
results = cl.fit_transform('D://magweg//101_ObjectCategories//', min_clust=60, max_clust=110)
results = cl.fit_transform(pathnames, min_clust=15, max_clust=50)
# Cluster
# cl.cluster(evaluate='silhouette', min_clust=15, max_clust=60)

cl.clusteval.plot()
cl.pca.plot()

# Scatter
cl.scatter(dotsize=8, zoom=0.2, img_mean=True)
cl.scatter(dotsize=8, zoom=None)

# uiimgs = cl.unique()
cl.plot_unique(img_mean=True, show_hog=True)
cl.plot_unique(img_mean=False)

# Plot the clustered images
cl.plot(labels=8)
# Plotting
cl.dendrogram()

import os
y_pred = results['labx']
y_true=[]
for path in results['pathnames']:
    getpath=os.path.split(results['pathnames'][0])[0]
    y_true.append(os.path.split(getpath)[1])

# %%
cl.model.plot()
cl.model.scatter(legend=False)
cl.model.results.keys()

# %%
from clusteval import clusteval
ce = clusteval()
ce.fit()

