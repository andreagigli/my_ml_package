from pandas import DataFramefrom sklearn.ensemble import IsolationForestfrom src.eda.eda_misc import plot_data_distribution, plot_clusters_2d, plot_pairwise_scatterplots, compute_mutual_information, compute_relationshipfrom src.utils.my_dataframe import custom_infodef eda(gcr: DataFrame) -> None:    """    Performs exploratory data analysis (EDA) on the provided dataset to prepare it for more effective modeling and insights derivation.    Objectives and Techniques:    - Features sanity, types, and values: Evaluate if the features contain nan values, and attempt to distinguish continuous from discrete ones.        Discrete features could be natively numerical or arising from encoding of boolean or categorical variables.        Use df.info() and df.nunique() to check the number of nans, the feature type and the number of unique values each feature assumes.    - Distribution and Outliers: Evaluate the distribution of features and the target. The aim is assessing the data is well-conditioned for learning (scale, statistical assumptions, no outliers).        Use histograms, boxplots, violinplots, countplots, and shape statistics to assess distribution.        Use Tukey thresholding or isolation forests for univariate and multivariate outlier detection.    - Existing Clusters: Use scatterplots, optionally preceeded by dimensionality reduction techniques like PCA or t-SNE, to visualize and assess data separability for classification and expected number of clusters.    - Feature-Target Relationships: Characterize relationships between features and the target in terms of strength and nature to inform feature engineering and model selection.        Perform a quick assessment, use pairplots and feature ranking based on mutual information. The pairplot, or specific scatter plots, is also important for the next steps.        To assess linearity/monotonicity in regression, use the Pearson and Spearman correlation coefficients for continuous features or grouped boxplots for discrete ones.        To assess homoscedasticity in regression, check for fan-shaped patterns in the pairplot (homoscedasticity involves feat-residuals, but feat-target can be a model-agnostic indication).        To assess linear class separability in binary classification (or one-hot encoded target class), use statistical feature selection based on ANOVA f-score if the feature is continuous or chi2 if the feature is discrete.        To assess linear class separability in multiclass classification (label-encoded target class), just check the pairplot.    - Feature Interactions: Investigate relationships between features to inform feature engineering or gain insights into the underlying processes.        To assess feature redundancy, check if the pearson corrcoef or the cramer V approach 1 for continuous-continuous or discrete-discrete relationships, respectively.        To evaluate feature combination or gain insights on underlying process, check feature pairs that have high spearman corrcoef or cramer V for continuous-continuous or discrete-discrete relationships, respectively.        To identify and explain complex phenomena, check for abrupt trend changes in the scatterplot.    Args:        gcr (DataFrame): A pandas DataFrame containing the data to be analyzed.    Returns:        Outputs various visualizations that illustrate the data's characteristics and summaries of statistical tests to guide further data preprocessing and feature engineering decisions.    """    # Distinguish continuous from discrete columns, in this case based on a heuristic thresholding    print(f"Number of nans, type, and number of unique values for each column of the DataFrame: \n{custom_info(gcr)}")    cols_continuous = gcr.nunique().loc[gcr.nunique() > 8].index.to_list()    cols_discrete = gcr.nunique().loc[gcr.nunique() <= 8].index.to_list()    # Feature Sanity Check    print("### Feature Sanity Check ###\n")    print("Evaluating data types and missing values:\n")    print(f"{custom_info(gcr)}\n")  # Assumes custom_info is a function returning formatted string    # Distribution and Outliers    print("### Distribution and Outliers ###\n")    print("Visualizing distribution of continuous and discrete variables:")    plot_data_distribution(gcr, discrete_features_mask=[col in cols_discrete for col in gcr.columns])    print("\nDetecting outliers with Random Isolation Forest:")    isofor = IsolationForest(n_estimators=100, random_state=0).fit(gcr[cols_continuous])    outliers = isofor.predict(gcr[cols_continuous]) == -1    print(f"Number of identified outliers: {outliers.sum()}\n")    # Feature clusters    print("### Feature cluster ###\n")    print("Plot a 2D projections of the continuous features to identify natural clusters.")    fig_cont_clusters = plot_clusters_2d(gcr, columns_to_plot=cols_continuous, color_labels=gcr["Good Risk"])    # Feature-Target Relationships    print("\n### Feature-Target Relationships ###\n")    print("Pairplot of features vs target ('Good Risk').\nUseful to inform feature engineering and model selection.\n")    plot_pairwise_scatterplots(gcr, target_columns=["Good Risk"], color_labels=gcr["Good Risk"], sample_size=100)    print("General relationships between features and target ('Good Risk').\nMutual information is used to explore nonlinear relationships regardless of their discrete or continuous type.\nUseful to inform feature engineering and model selection.\n")    # This function handles automatically the correct mutual information criterion depending on the target type and the 'discrete_features' argument depending on the feature type    compute_mutual_information(gcr, columns_of_interest=gcr.columns, target="Good Risk", discrete_features_mask=[col in cols_discrete for col in gcr.columns], plot_heatmap=True, include_diagonal=False)    # # For regression tasks, one can check the existence of linear or monotonic feature-target relationships. This is not the case in this analysis.    # print("Linear relationships between features and target ('...').\nUseful to inform selection of regression models.")    # compute_relationship(gcr, score_func="pearson", columns_of_interest=gcr.columns, target="Good Risk", sample_size=1000, plot_heatmap=True, include_diagonal=True)    #    # print("Monotonic relationships between features and target ('...').\nUseful to inform the adoption of simple linearizing features.")    # compute_relationship(gcr, score_func="spearman", columns_of_interest=gcr.columns, target="Good Risk", sample_size=1000, plot_heatmap=True, include_diagonal=True)    # Feature-Feature Relationships    print("\n### Feature-Feature Relationships ###\n")    print("Pairplot of feature vs feature.\nUseful to explain underlying processes and spot edge conditions, inform the feature elimination or feature joining.")    # For classification tasks, use column_labels to color the samples    plot_pairwise_scatterplots(gcr, columns_to_plot=[col for col in gcr.columns.to_list() if col != "Good Risk"], color_labels=gcr["Good Risk"], color_interpretation="Good Risk", sample_size=100)    print("General relationships between pairs of features.\nComputed with mutual information and reported separately for continuous 'target features' and for discrete 'target features'.\nUseful to explain underlying processes.")    compute_mutual_information(gcr, columns_of_interest=gcr.columns, discrete_features_mask=[col in cols_discrete for col in gcr.columns], plot_heatmap=True, include_diagonal=False)    print("Linear relationships between pairs of continuous features.\nUseful to inform feature elimination.")    compute_relationship(gcr, score_func="pearson", columns_of_interest=cols_continuous, sample_size=1000, plot_heatmap=True, include_diagonal=True)    print("Monotonic relationships between pairs of continuous features.\nUseful to inform feature combination.")    compute_relationship(gcr, score_func="spearman", columns_of_interest=cols_continuous, sample_size=1000, plot_heatmap=True, include_diagonal=True)    print("\n--- EDA Completed ---\n")