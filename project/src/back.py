import scanpy as sc


class Back:
    @staticmethod
    def do_prep(file):
        adata = sc.read_csv(file, delimiter='\t')
        adata = adata.T

        # pdata = pd.read_csv(file, delimiter='\t')

        sc.settings.verbosity = 3  # verbosity: errors (0), warnings (1), info (2), hints (3)
        sc.settings.set_figure_params(dpi=100, facecolor='white')

        sc.pl.highest_expr_genes(adata, n_top=15)

        sc.pp.filter_cells(adata, min_genes=500)
        sc.pp.filter_genes(adata, min_cells=200)

        sc.pp.normalize_total(adata, target_sum=1e4)

        sc.pp.log1p(adata)

        sc.pp.highly_variable_genes(adata)
        sc.pl.highly_variable_genes(adata)

        sc.pp.scale(adata)

        (adata.var.highly_variable == True).sum()

        return adata

    @staticmethod
    def do_main(adata):
        sc.tl.pca(adata, n_comps=100)
        sc.pl.pca(adata)

        sc.pl.pca_variance_ratio(adata, n_pcs=100, log=True)

        sc.pl.pca_loadings(adata)

        sc.pl.pca(adata, color=['ML07214a', 'ML25764a', 'ML14383a'], ncols=3, hspace=0.1, wspace=0.2)

        sc.pl.pca(adata, color=['ML07214a', 'ML25764a', 'ML14383a'], ncols=3, hspace=20, wspace=0.2, projection='3d')

        sc.pp.neighbors(adata, n_neighbors=20, n_pcs=40)

        sc.tl.umap(adata)

        sc.tl.leiden(adata)
        sc.pl.umap(adata, color='leiden', palette='gist_ncar')
