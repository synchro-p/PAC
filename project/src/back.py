from distutils.log import error
import scanpy as sc

class Back:
    @staticmethod
    def do_prep(file):
        adata = sc.read(file);
        adata = adata.T

        # pdata = pd.read_csv(file, delimiter='\t')

        sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
        sc.settings.set_figure_params(dpi=100, facecolor='white')

        sc.pl.highest_expr_genes(adata, n_top=15, log = True)

        sc.pp.filter_cells(adata, min_genes=500)
        sc.pp.filter_genes(adata, min_cells=200)

        sc.pp.normalize_total(adata, target_sum=1e4)

        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
        print("Highly variable genes: %d"%sum(adata.var.highly_variable))
        sc.pl.highly_variable_genes(adata)

        # subset for variable genes in the dataset
        adata = adata[:, adata.var['highly_variable']]
        sc.pp.scale(adata)

        return adata

    @staticmethod
    def do_main(adata):
        sc.pl.pca_variance_ratio(adata, n_pcs=50, log=True)
        sc.pl.pca_loadings(adata)

        adata.var["total_expression"] = adata.X.sum(0)
        highest_expr = adata.var['total_expression'].nlargest(10)

        sc.tl.pca(adata, svd_solver='arpack')
        sc.pl.pca(adata, color = highest_expr.index[0:3], components = ['1,2','3,4'], ncols = 2)

        sc.pl.pca(adata, color = highest_expr.index[0:3], ncols=3, hspace=20, wspace=0.2, projection='3d')

        sc.pp.neighbors(adata, n_neighbors=20, n_pcs=40)

        sc.tl.umap(adata)

        sc.tl.leiden(adata)
        sc.pl.umap(adata, color='leiden', palette='gist_ncar')

        #экспорт номеров кластеров соотнесенных с каждым геном
        #возможно стоит сделать этот экспорт вместе с таблицей вклада гена в каждую компоненту
        clusters_df = sc.pd.DataFrame(adata.obs["leiden"])
        clusters_df.to_csv("clusters.csv")
