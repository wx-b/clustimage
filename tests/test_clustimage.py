from clustimage import Clustimage
import itertools as it
import numpy as np
import unittest

class TestCLUSTIMAGE(unittest.TestCase):

    def test_import_data(self):
        cl = Clustimage()
        # Check initialization results
        assert cl.results=={'img': None, 'feat': None, 'xycoord': None, 'pathnames': None, 'labels': None}
        # Import flowers example
        X = cl.import_example(data='flowers')
        
        # Check numpy array imports
        assert cl.import_data(np.array(X))
        assert cl.import_data(X[0])
        assert cl.import_data([X[0]])
        
        # Check output
        cl = Clustimage(dim=(128,128), grayscale=False)
        _ =  cl.import_data(X)
        assert np.all(np.isin([*cl.results.keys()], ['img', 'feat', 'xycoord', 'pathnames', 'labels', 'filenames']))
        assert cl.results['img'].shape==(210, 49152)
        # Check grayscale parameter with imports
        cl = Clustimage(dim=(128,128), grayscale=True)
        _ = cl.import_data(X)
        assert cl.results['img'].shape==(210, 16384)

        # Import mnist example
        X = cl.import_example(data='mnist')
        cl = Clustimage()
        _ = cl.import_data(X)
        assert np.all(np.isin([*cl.results.keys()], ['img', 'feat', 'xycoord', 'pathnames', 'labels', 'filenames']))
        assert cl.results['img'].shape==(1797, 64)
        assert len(cl.results['pathnames'])==X.shape[0]
        assert len(cl.results['filenames'])==X.shape[0]

    def test_extract_feat(self):
        cl = Clustimage(method='pca')
        # Import flowers example
        X = cl.import_example(data='flowers')
        X = cl.import_data(X)
        _ = cl.extract_feat(X)
        assert cl.results['feat'].shape==(X['img'].shape[0], 154)

    def test_embedding(self):
        cl = Clustimage(method='pca')
        # Import flowers example
        X = cl.import_example(data='flowers')
        X = cl.import_data(X)
        Xfeat = cl.extract_feat(X)
        _ = cl.embedding(Xfeat)
        assert cl.results['xycoord'].shape==(X['img'].shape[0], 2)

    def test_embedding(self):
        cl = Clustimage(method='pca')
        # Import flowers example
        X = cl.import_example(data='flowers')
        X = cl.import_data(X)
        Xfeat = cl.extract_feat(X)
        xycoord = cl.embedding(Xfeat)
        labels = cl.cluster()
        assert len(cl.results['labels'])==X['img'].shape[0]

    def test_cluster(self):
        cl = Clustimage()
        X = cl.import_example(data='flowers')
        results = cl.fit_transform(X)
        assert np.all(np.isin([*cl.results.keys()], ['img', 'feat', 'xycoord', 'pathnames', 'filenames', 'labels']))
        assert len(cl.cluster())==len(X)
    
        # Parameters combinations to check
        param_grid = {
        	'cluster_space':['high','low'],
        	'cluster':['agglomerative'],
        	'evaluate' : ['silhouette', 'dbindex'],
            'min_clust' : [2, 4, 6],
            'max_clust' : [10, 20, 30],
        	}
        # Make the combinatinos
        allNames = param_grid.keys()
        combinations = list(it.product(*(param_grid[Name] for Name in allNames)))
        for combination in combinations:
            labx = cl.cluster(cluster_space=combination[0], cluster=combination[1], evaluate=combination[2], metric='euclidean', linkage='ward', min_clust=combination[3], max_clust=combination[4])
            assert len(labx)==len(X)
    
    def test_find(self):
        cl = Clustimage(method='pca', grayscale=False)
        # load example with flowers
        path_to_imgs = cl.import_example(data='flowers')
        # Extract features (raw images are not stored and handled per-image to save memory)
        results = cl.fit_transform(path_to_imgs, min_clust=10)
    
        # Predict
        results_find = cl.find(path_to_imgs[0:5], k=None, alpha=0.05)
        assert np.all(np.isin([*results_find.keys()], ['feat', '0001.png', '0002.png', '0003.png', '0004.png', '0005.png']))
        assert len(results_find['0001.png']['y_idx'])>=1
        assert len(results_find['0002.png']['y_idx'])>=1
        assert len(results_find['0003.png']['y_idx'])>=30
        assert len(results_find['0004.png']['y_idx'])>=1
        assert len(results_find['0005.png']['y_idx'])>=1

        results_find = cl.find(path_to_imgs[0:5], k=1, alpha=None)
        assert len(results_find['0001.png']['y_idx'])==1
        assert len(results_find['0002.png']['y_idx'])==1
        assert len(results_find['0003.png']['y_idx'])==1
        assert len(results_find['0004.png']['y_idx'])==1
        assert len(results_find['0005.png']['y_idx'])==1

    def test_predict(self):
        # Init
        cl = Clustimage(method='pca', grayscale=True, params_pca={'n_components':14})
        # Load example with faces
        X = cl.import_example(data='flowers')
        # Cluster
        results = cl.fit_transform(X)
        assert np.all(np.isin([*cl.results.keys()], ['img', 'feat', 'xycoord', 'pathnames', 'filenames', 'labels']))

    def test_fit_transform(self):
        # Example data
        cl = Clustimage()
        Xflowers = cl.import_example(data='flowers')
        Xdigits = cl.import_example(data='mnist')
        Xfaces = cl.import_example(data='faces')
        # Parameters combinations to check
        param_grid = {
        	'method':['ahash', 'pca', 'hog', None],
        	'embedding':['tsne', None],
        	'cluster_space' : ['high', 'low'],
        	'grayscale' : [True, False],
            'dim' : [(8,8), (128,128), (256,256)],
            'data' : [Xflowers, Xdigits]
        	}
        # Make the combinatinos
        allNames = param_grid.keys()
        combinations = list(it.product(*(param_grid[Name] for Name in allNames)))
        # Iterate over all combinations
        for i, combination in enumerate(tqdm(combinations)):
            # init
            cl = Clustimage(method=combination[0], embedding=combination[1], grayscale=combination[3], dim=combination[4], verbose=30, params_pca={'n_components':50})
            # Preprocessing and feature extraction
            assert cl.fit_transform(combination[5], cluster_space=combination[2])

