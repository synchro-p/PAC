import scanpy as sc
import os
from pathlib import Path


class Back:

    @staticmethod
    def from_scratch(file, n, min_genes_per_cell, min_cells_per_gene, min_mean, max_mean, n_neighbors):
        #параметры:
        #min_genes_per_cell, min_cells_per_gene in filter_cells and filter_genes
        #min_mean, max_mean, min_disp in highly_variable_genes
        #n_neighbors in neighbours
        #default: from_scratch(file, n, 500, 200, 0.0125, 3, 20)
        homepath = Path().absolute().resolve()
        path_to_report = Path(str(homepath.parent) + '/saveddata/' + str(n))
        os.makedirs(path_to_report)

        adata = sc.read(file)
        adata = adata.T

        adata.write(Path(str(path_to_report) + "/adata_pre.h5ad"))
        # pdata = pd.read_csv(file, delimiter='\t')

        sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
        sc.settings.set_figure_params(dpi=100, facecolor='white')

        sc.pl.highest_expr_genes(adata, n_top=15, log=True)

        sc.pp.filter_cells(adata, min_genes=min_genes_per_cell)
        sc.pp.filter_genes(adata, min_cells=min_cells_per_gene)

        sc.pp.normalize_total(adata, target_sum=1e4)

        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata, min_mean=min_mean, max_mean=max_mean, min_disp=0.5)

        adata.write(Path(str(path_to_report) + "/adata_mid.h5ad"))

        print("Highly variable genes: %d" % sum(adata.var.highly_variable))
        sc.pl.highly_variable_genes(adata)

        # subset for variable genes in the dataset
        adata = adata[:, adata.var['highly_variable']]
        sc.pp.scale(adata)

        adata.var["total_expression"] = adata.X.sum(0)
        highest_expr = adata.var['total_expression'].nlargest(10)

        sc.tl.pca(adata, svd_solver='arpack')
        sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
        sc.pl.pca_loadings(adata)
        sc.pl.pca(adata, color=highest_expr.index[0:3], components=['1,2', '3,4'], ncols=2)

        sc.pl.pca(adata, color=highest_expr.index[0:3], ncols=3, hspace=20, wspace=0.2, projection='3d')

        sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=40)

        sc.tl.umap(adata)

        sc.tl.leiden(adata)
        sc.pl.umap(adata, color='leiden', palette='gist_ncar')

        # экспорт номеров кластеров соотнесенных с каждым геном
        # возможно стоит сделать этот экспорт вместе с таблицей вклада гена в каждую компоненту
        # clusters_df = pd.DataFrame(adata.obs["leiden"])
        # clusters_df.to_csv("clusters.csv")
        adata.write(Path(str(path_to_report) + "/adata_post.h5ad"))
        # adata1 = sc.read("anndata.h5ad")

    @staticmethod
    def from_saved(n):
        homepath = Path().absolute().resolve()
        adata = sc.read(str(homepath.parent) + "/saveddata/" + str(n) + "/adata_pre.h5ad")
        sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
        sc.settings.set_figure_params(dpi=100, facecolor='white')
        sc.pl.highest_expr_genes(adata, n_top=15, log=True)

        adata = sc.read(str(homepath.parent) + "/saveddata/" + str(n) + "/adata_mid.h5ad")

        print("Highly variable genes: %d" % sum(adata.var.highly_variable))
        sc.pl.highly_variable_genes(adata)

        adata = sc.read(str(homepath.parent) + "/saveddata/" + str(n) + "/adata_post.h5ad")
        highest_expr = adata.var['total_expression'].nlargest(10)
        sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
        sc.pl.pca_loadings(adata)
        sc.pl.pca(adata, color=highest_expr.index[0:3], components=['1,2', '3,4'], ncols=2)
        sc.pl.pca(adata, color=highest_expr.index[0:3], ncols=3, hspace=20, wspace=0.2, projection='3d')
        sc.pl.umap(adata, color='leiden', palette='gist_ncar')
