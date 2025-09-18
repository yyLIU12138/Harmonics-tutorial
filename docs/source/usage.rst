Usage
=====

Import the package
-----------------

.. code-block:: python

    from Harmonics import *


Initialize the model
-------------------

.. code-block:: python

    model = Harmonics_Model(
        adata_list,
        slice_name_list,
        cond_list=cond_list,
        cond_name_list=cond_name_list,
        concat_label='slice_name',
        proportion_label=None,
        refine_k=0,
        seed=1234,
        parallel=True,
        verbose=True,
    )

**Parameters**

- **adata_list**: list of `anndata` objects. Whole dataset for condition-agnostic analysis, control group for case-control study, or reference data for label transfer.  
- **slice_name_list**: list of strings, names of slices corresponding to `adata_list`.  
- **cond_list**: Default: `None`. list of `anndata` objects or `None`. `None` for condition-agnostic analysis, case group for case-control study, or query data for label transfer.
- **cond_name_list**: Default: `None`. list of strings or `None`, names of slices corresponding to `cond_list`.  
- **concat_label**: Default: `'slice_name'`. string, key in `.obs` to store slice names.  
- **proportion_label**: Default: `None`. string or `None`, key in `.obsm` storing cell type proportions for low-resolution data.  
- **refine_k**: Default: `0`. int, number of cell types with highest proportion used for niche refinement; set `0` to skip refinement.  
- **seed**: Default: `1234`. int, random seed.  
- **parallel**: Default: `True`. bool, whether to run computations in parallel.  
- **verbose**: Default: `True`. bool, whether to print progress messages.  


Construct cell representations
------------------------------

.. code-block:: python

    model.preprocess(
        ct_key='celltype',
        spatial_key='spatial',
        method='joint',
        n_step=3,
        n_neighbors=20,
        cut_percentage=99,
    )

**Parameters**

- **ct_key**: Default: `'celltype'`. string, key in `.obs` storing the cell type information.  
- **spatial_key**: Default: `'spatial'`. string, key in `.obsm` storing the spatial coordinates.  
- **method**: Default: `'joint'`. string or `None`, method for graph construction. Options:  
  - `'joint'`: n-step hop Delaunay triangulation with graph completion to at least `n_neighbors` per cell.  
  - `'delaunay'`: n-step hop Delaunay triangulation.  
  - `'knn'`: connect `n_neighbors` neighbors per cell.  
  - `None`: directly use cell type composition (for low-resolution data).  
- **n_step**: Default: `3`. int, number of steps for n-step Delaunay triangulation.  
- **n_neighbors**: Default: `20`. int, minimum number of neighbors per cell when method is `'joint'` or `'knn'`.  
- **cut_percentage**: Default: `99`. int, percentage of shortest edges to keep in the Delaunay triangulation adjacency graph. 


Over-clustering initialization (whole dataset / control group / reference)
---------------------------------------------------------------------------

.. code-block:: python

    model.initialize_clusters(
        dim_reduction=True,
        explained_var=None,
        n_components=None,
        n_components_max=100,
        standardize=True,
        method='kmeans',
        Qmax=20,
    )

**Parameters**

- **dim_reduction**: Default: `True`. bool, whether to perform dimensionality reduction (PCA) before clustering.  
- **explained_var**: Default: `None`. float or `None`, target cumulative explained variance for dimensionality reduction.  
- **n_components**: Default: `None`. int or `None`, number of components to retain after dimensionality reduction. If `None`, retain no more than `n_components_max`.  
- **n_components_max**: Default: `100`. int, maximum number of components allowed during reduction.  
- **standardize**: Default: `True`. bool, whether to z-score normalize each feature before dimensionality reduction.  
- **method**: Default: `'kmeans'`. string, clustering method for initialization. Options: `'kmeans'`, `'gmm'`.  
- **Qmax**: Default: `20`. int, number of clusters for initialization.  


Perform HDM to find solution
----------------------------

.. code-block:: python

    model.hier_dist_match(
        assign_metric='jsd',
        weighted_merge=True,
        max_iters=100,
        tol=1e-4,
        Qmin=2,
    )

**Parameters**

- **assign_metric**: Default: `'jsd'`. string, metric used to evaluate distribution similarity between niches.  
- **weighted_merge**: Default: `True`. bool, whether to use weighted JSD (WJSD) during merging phase.  
- **max_iters**: Default: `100`. int, maximum number of iterations for convergence.  
- **tol**: Default: `1e-4`. float, tolerance for convergence.  
- **Qmin**: Default: `2`. int, minimum number of niches to consider.  


Select the solution
-------------------

.. code-block:: python

    adata_list, adata_concat = model.select_solution(
        n_niche=None,
        niche_key='niche_label',
        auto=True,
        metric='jsd',
        threshold=0.1,
        return_adata=True,
        plot=True,
        save=False,
        fig_size=(10, 6),
        save_dir=None,
        file_name='score_vs_nichecount_basic.pdf',
    )

**Parameters**

- **n_niche**: Default: `None`. int or `None`, number of niches to select. If `None`, solution is selected automatically using `metric`.  
- **niche_key**: Default: `'niche_label'`. string, key in `.obs` to store niche assignment results.  
- **auto**: Default: `True`. bool, whether to automatically determine the solution if `n_niche=None`.  
- **metric**: Default: `'jsd'`. string, metric used for evaluating solutions, e.g., minimum JSD score.  
- **threshold**: Default: `0.1`. float, threshold for selecting solution based on `metric`.  
- **return_adata**: Default: `True`. bool, whether to return an `anndata` object with niche assignments.  
- **plot**: Default: `True`. bool, whether to plot the minJSD curve.  
- **save**: Default: `False`. bool, whether to save the minJSD plot.  
- **fig_size**: Default: `(10, 6)`. tuple, figure size for plotting.  
- **save_dir**: Default: `None`. string or `None`, directory to save the plot.  
- **file_name**: Default: `'score_vs_nichecount_basic.pdf'`. string, name of the saved plot file.  


Over-clustering initialization (case group)
-------------------------------------------

.. code-block:: python

    model.initialize_clusters_cond(
        assign_metric='jsd',
        threshold=0.1,
        min_cell_per_niche=100,
        dim_reduction=True,
        explained_var=None,
        n_components=None,
        n_components_max=100,
        standardize=True,
        method='kmeans',
        Rmax=10,
    )

**Parameters**

- **assign_metric**: Default: `'jsd'`. string, metric used for evaluating distribution similarity when assigning cells to BCNs.  
- **threshold**: Default: `0.1`. float, minimum divergence threshold below which cells are assigned to BCNs.  
- **min_cell_per_niche**: Default: `100`. int, minimum average number of cells per new niche.  
- **dim_reduction**: Default: `True`. bool, whether to perform dimensionality reduction (PCA) before clustering.  
- **explained_var**: Default: `None`. float or `None`, target cumulative explained variance for dimensionality reduction.  
- **n_components**: Default: `None`. int or `None`, number of components to retain after dimensionality reduction. If `None`, retain no more than `n_components_max`.  
- **n_components_max**: Default: `100`. int, maximum number of components allowed during reduction.  
- **standardize**: Default: `True`. bool, whether to z-score normalize each feature before dimensionality reduction.  
- **method**: Default: `'kmeans'`. string, clustering method for initialization.  
- **Rmax**: Default: `10`. int, number of clusters for initialization.  


Perform HDM to find solution (case group)
-----------------------------------------

.. code-block:: python

    model.hier_dist_match_cond(
        assign_metric='jsd',
        weighted_merge=True,
        max_iters=100,
        tol=1e-4,
    )

**Parameters**

- **assign_metric**: Default: `'jsd'`. string, metric used to evaluate distribution similarity between niches.  
- **weighted_merge**: Default: `True`. bool, whether to use weighted JSD (WJSD) during merging phase.  
- **max_iters**: Default: `100`. int, maximum number of iterations for convergence.  
- **tol**: Default: `1e-4`. float, tolerance for convergence.  


Select the solution (case group)
--------------------------------

.. code-block:: python

    cond_list, cond_concat = model.select_solution_cond(
        n_csn=None,
        niche_key='niche_label',
        csn_key='csn_label',
        auto=True,
        metric='jsd',
        threshold=0.1,
        return_adata=True,
        plot=True,
        save=False,
        fig_size=(10, 6),
        save_dir=None,
        file_name='score_vs_nichecount_cond.pdf',
    )

**Parameters**

- **n_csn**: Default: `None`. int or `None`, number of CSNs to select. If `None`, solution is selected automatically using `metric`.  
- **niche_key**: Default: `'niche_label'`. string, key in `.obs` to store niche assignment results.  
- **csn_key**: Default: `'csn_label'`. string, key in `.obs` to store CSN assignment results.  
- **auto**: Default: `True`. bool, whether to automatically determine the solution if `n_csn=None`.  
- **metric**: Default: `'jsd'`. string, metric used for evaluating solutions, e.g., minimum JSD score.  
- **threshold**: Default: `0.1`. float, threshold for selecting solution based on `metric`.  
- **return_adata**: Default: `True`. bool, whether to return an `anndata` object with CSN assignments.  
- **plot**: Default: `True`. bool, whether to plot the minJSD curve.  
- **save**: Default: `False`. bool, whether to save the minJSD plot.  
- **fig_size**: Default: `(10, 6)`. tuple, figure size for plotting.  
- **save_dir**: Default: `None`. string or `None`, directory to save the plot.  
- **file_name**: Default: `'score_vs_nichecount_cond.pdf'`. string, name of the saved plot file.  


Label transfer
--------------

.. code-block:: python

    trans_list, trans_concat = model.label_transfer(
        assign_metric='jsd',
        niche_key='niche_label',
        return_adata=True,
    )

**Parameters**

- **assign_metric**: Default: `'jsd'`. string, metric used to evaluate distribution similarity when assigning cells to niches.  
- **niche_key**: Default: `'niche_label'`. string, key in `.obs` to store niche assignment results.  
- **return_adata**: Default: `True`. bool, whether to return an `anndata` object with niche assignments.  


Cell type enrichment test
-------------------------

.. code-block:: python

    ct_results = ct_enrichment_test(
        niche_dist,
        cell_count_niche,
        idx2ct_dict,
        niche_summary,
        method='fisher',
        alpha=0.05,
        fdr_method='fdr_by',
        log2fc_threshold=1,
        prop_threshold=0.01,
        verbose=True,
        eps=1e-10,
    )

**Parameters**

- **niche_dist**: array-like or sparse matrix, shape `(n_niche, n_celltype)`, representing the proportion of each cell type in each niche.  
- **cell_count_niche**: array-like, shape `(n_niche,)`, number of cells in each niche.  
- **idx2ct_dict**: dict, mapping from cell type indices to cell type names.  
- **niche_summary**: list of strings, names or labels for each niche.  
- **method**: Default: `'fisher'`. string, statistical test method. Options:  
  - `'fisher'`: two-sided Fisher's exact test.  
  - `'fisher_greater'`: one-sided Fisher's exact test (greater).  
  - `'chi2'`: chi-square test.  
- **alpha**: Default: `0.05`. float, significance level for multiple testing correction.  
- **fdr_method**: Default: `'fdr_by'`. string, method for false discovery rate correction.  
- **log2fc_threshold**: Default: `1`. float, minimum log2 fold-change required for enrichment.  
- **prop_threshold**: Default: `0.01`. float, minimum proportion of cell type in niche required for enrichment.  
- **verbose**: Default: `True`. bool, whether to print progress messages.  
- **eps**: Default: `1e-10`. float, small value to avoid division by zero.  

**Returns**

- **ct_results**: `pandas.DataFrame` containing enrichment results with columns:  
  - `niche_idx`: index of the niche  
  - `niche`: name of the niche  
  - `celltype_idx`: index of the cell type  
  - `celltype`: name of the cell type  
  - `oddsratio` or `chi2_stat`: test statistic  
  - `p-value`: raw p-value  
  - `q-value`: FDR-corrected p-value  
  - `log2fc`: log2 fold-change  
  - `prop`: proportion of cell type in niche  
  - `enrichment`: bool, whether cell type is significantly enriched.


Cell-cell interaction enrichment test
-------------------------------------------

.. code-block:: python

    cci_results, test_norm_list, bg_norm_list, test_edge_count_list, bg_edge_count_list = cci_enrichment_test(
        adata_list,
        niche_key,
        ct_key,
        niche_summary=None,
        spatial_key='spatial',
        cut_percentage=99,
        method='fisher',
        alpha=0.05,
        fdr_method='fdr_by',
        log2fc_threshold=1,
        prop_threshold=0.01,
        verbose=True,
        eps=1e-10,
    )

**Parameters**

- **adata_list**: `anndata` object or list of `anndata` objects, input datasets to test CCI enrichment.  
- **niche_key**: string, key in `.obs` representing niche labels.  
- **ct_key**: string, key in `.obs` representing cell type labels.  
- **niche_summary**: Default: `None`. list of niche names to test; if `None`, all unique niches in `adata_list` are used.  
- **spatial_key**: Default: `'spatial'`. string, key in `.obsm` representing spatial coordinates.  
- **cut_percentage**: Default: `99`. float, percentage of shortest edges to retain in Delaunay adjacency graph.  
- **method**: Default: `'fisher'`. string, statistical test method. Options:  
  - `'fisher'`: two-sided Fisher's exact test.  
  - `'fisher_greater'`: one-sided Fisher's exact test (greater).  
- **alpha**: Default: `0.05`. float, significance level for multiple testing correction.  
- **fdr_method**: Default: `'fdr_by'`. string, method for false discovery rate correction.  
- **log2fc_threshold**: Default: `1`. float, minimum log2 fold-change required for enrichment.  
- **prop_threshold**: Default: `0.01`. float, minimum proportion of cell type pairs in niche required for enrichment.  
- **verbose**: Default: `True`. bool, whether to print progress messages.  
- **eps**: Default: `1e-10`. float, small value to avoid division by zero.  

**Returns**

- **cci_results**: `pandas.DataFrame` containing CCI enrichment results with columns:  
  - `niche_idx`: index of the niche  
  - `niche`: name of the niche  
  - `ct1_idx`, `ct2_idx`: indices of interacting cell types  
  - `ct1`, `ct2`: names of interacting cell types  
  - `test_edge_count`, `bg_edge_count`: number of observed and background edges  
  - `test_edge_prop`, `bg_edge_prop`: proportion of observed and background edges  
  - `oddsratio`: odds ratio from statistical test  
  - `p-value`: raw p-value  
  - `q-value`: FDR-corrected p-value  
  - `log2fc`: log2 fold-change  
  - `enrichment`: bool, whether interaction is significantly enriched  
- **test_norm_list**: list of normalized test adjacency matrices for each niche.  
- **bg_norm_list**: list of normalized background adjacency matrices for each niche.  
- **test_edge_count_list**: list of total test edges per niche.  
- **bg_edge_count_list**: list of total background edges per niche.  


Niche-niche colocalization enrichment test
---------------------------------

.. code-block:: python

    df_results, edge_prop_mtx, n1_count = nnc_enrichment_test(
        adata_list,
        niche_key,
        niche_summary=None,
        spatial_key='spatial',
        cut_percentage=99,
        method='fisher',
        alpha=0.05,
        fdr_method='fdr_by',
        log2fc_threshold=1,
        prop_threshold=0.01,
        verbose=True,
        eps=1e-10,
    )

**Parameters**

- **adata_list**: `anndata` object or list of `anndata` objects, input datasets for NNC enrichment testing.  
- **niche_key**: string, key in `.obs` representing niche labels.  
- **niche_summary**: Default: `None`. list of niche names to test; if `None`, all unique niches in `adata_list` are used.  
- **spatial_key**: Default: `'spatial'`. string, key in `.obsm` representing spatial coordinates.  
- **cut_percentage**: Default: `99`. float, percentage of shortest edges to retain in Delaunay adjacency graph.  
- **method**: Default: `'fisher'`. string, statistical test method. Options:  
  - `'fisher'`: two-sided Fisher's exact test.  
  - `'fisher_greater'`: one-sided Fisher's exact test (greater).  
  - `'chi2'`: chi-square test with continuity correction.  
- **alpha**: Default: `0.05`. float, significance level for multiple testing correction.  
- **fdr_method**: Default: `'fdr_by'`. string, method for false discovery rate correction.  
- **log2fc_threshold**: Default: `1`. float, minimum log2 fold-change required for enrichment.  
- **prop_threshold**: Default: `0.01`. float, minimum proportion of edges between niches required for enrichment.  
- **verbose**: Default: `True`. bool, whether to print progress messages.  
- **eps**: Default: `1e-10`. float, small value to avoid division by zero.  

**Returns**

- **df_results**: `pandas.DataFrame` containing NNC enrichment results with columns:  
  - `niche1_idx`, `niche2_idx`: indices of interacting niches. Niche 1 is source niche and niche 2 is target niche.  
  - `niche1`, `niche2`: names of interacting niches. Niche 1 is source niche and niche 2 is target niche.  
  - `edge_count`: number of edges observed between niche pairs  
  - `edge_prop`: proportion of edges between niche pairs for the source niche
  - `oddsratio` or `chi2_stat`: statistic from the test  
  - `p-value`: raw p-value  
  - `q-value`: FDR-corrected p-value  
  - `log2fc`: log2 fold-change  
  - `enrichment`: bool, whether the interaction is significantly enriched  
- **edge_prop_mtx**: numpy array, normalized edge proportions between all niche pairs.  
- **n1_count**: numpy array, total outgoing edges for each niche.  