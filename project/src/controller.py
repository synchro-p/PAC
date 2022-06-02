from os import path
import pickle

from back import Back


class Controller(object):
    def __init__(self):
        self.mappath = "..\\saveddata\\cacheinfo.pkl"
        self.back = Back()

    def map_exists(self):
        return path.exists(self.mappath)

    def run_back(self, file, min_genes_per_cell, min_cells_per_gene, min_mean, max_mean, n_neighbors):
        if self.map_exists():
            with open(self.mappath, 'rb') as handle:
                save_dict = pickle.load(handle)
        else:
            save_dict = {}

        try:
            n = save_dict[file]
            self.back.from_saved(n)
        except KeyError:
            next_n = len(save_dict)
            save_dict[file] = next_n
            with open(self.mappath, 'wb') as handle:
                pickle.dump(save_dict, handle)
            self.back.from_scratch(file, next_n, min_genes_per_cell, min_cells_per_gene, min_mean, max_mean, n_neighbors)
