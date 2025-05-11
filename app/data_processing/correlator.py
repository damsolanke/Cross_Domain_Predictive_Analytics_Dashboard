"""
Cross-domain correlator class for analyzing relationships between different data domains.
Provides methods for correlation analysis and feature importance calculation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
import logging
from scipy import stats
from sklearn.feature_selection import mutual_info_regression
import seaborn as sns
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class CrossDomainCorrelator:
    def __init__(self):
        """Initialize the cross-domain correlator."""
        self.correlation_history = []
    
    def align_time_series(self, dfs: Dict[str, pd.DataFrame], 
                         time_columns: Dict[str, str],
                         freq: str = '1H') -> Dict[str, pd.DataFrame]:
        """
        Align multiple time series dataframes to a common time index.
        
        Args:
            dfs (Dict[str, pd.DataFrame]): Dictionary of dataframes to align
            time_columns (Dict[str, str]): Dictionary mapping dataframe names to their time columns
            freq (str): Frequency for resampling
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary of aligned dataframes
        """
        try:
            aligned_dfs = {}
            
            # Create common time index
            all_times = []
            for name, df in dfs.items():
                if time_columns[name] in df.columns:
                    all_times.extend(df[time_columns[name]].tolist())
            
            common_index = pd.date_range(
                start=min(all_times),
                end=max(all_times),
                freq=freq
            )
            
            # Align each dataframe
            for name, df in dfs.items():
                if time_columns[name] in df.columns:
                    # Set time column as index
                    df_aligned = df.set_index(time_columns[name])
                    
                    # Resample to common frequency
                    df_aligned = df_aligned.resample(freq).mean()
                    
                    # Reindex to common index
                    df_aligned = df_aligned.reindex(common_index)
                    
                    aligned_dfs[name] = df_aligned
            
            self.correlation_history.append({
                'timestamp': datetime.now(),
                'operation': 'align_time_series',
                'dataframes': list(dfs.keys()),
                'frequency': freq
            })
            
            return aligned_dfs
            
        except Exception as e:
            logger.error(f"Error aligning time series: {str(e)}")
            raise
    
    def calculate_correlations(self, dfs: Dict[str, pd.DataFrame],
                             target_domain: str,
                             target_column: str) -> pd.DataFrame:
        """
        Calculate correlations between target column and all other numeric columns.
        
        Args:
            dfs (Dict[str, pd.DataFrame]): Dictionary of aligned dataframes
            target_domain (str): Name of the dataframe containing target column
            target_column (str): Name of the target column
            
        Returns:
            pd.DataFrame: Correlation results
        """
        try:
            correlations = []
            
            # Get target series
            target_series = dfs[target_domain][target_column]
            
            # Calculate correlations for each dataframe
            for name, df in dfs.items():
                for col in df.select_dtypes(include=[np.number]).columns:
                    if col != target_column or name != target_domain:
                        # Calculate Pearson correlation
                        pearson_corr, pearson_pval = stats.pearsonr(
                            target_series.dropna(),
                            df[col].dropna()
                        )
                        
                        # Calculate Spearman correlation
                        spearman_corr, spearman_pval = stats.spearmanr(
                            target_series.dropna(),
                            df[col].dropna()
                        )
                        
                        # Calculate mutual information
                        mi_score = mutual_info_regression(
                            df[col].dropna().values.reshape(-1, 1),
                            target_series.dropna()
                        )[0]
                        
                        correlations.append({
                            'domain': name,
                            'column': col,
                            'pearson_correlation': pearson_corr,
                            'pearson_pvalue': pearson_pval,
                            'spearman_correlation': spearman_corr,
                            'spearman_pvalue': spearman_pval,
                            'mutual_information': mi_score
                        })
            
            # Convert to DataFrame
            corr_df = pd.DataFrame(correlations)
            
            # Sort by absolute Pearson correlation
            corr_df['abs_pearson'] = corr_df['pearson_correlation'].abs()
            corr_df = corr_df.sort_values('abs_pearson', ascending=False)
            corr_df = corr_df.drop('abs_pearson', axis=1)
            
            self.correlation_history.append({
                'timestamp': datetime.now(),
                'operation': 'calculate_correlations',
                'target_domain': target_domain,
                'target_column': target_column
            })
            
            return corr_df
            
        except Exception as e:
            logger.error(f"Error calculating correlations: {str(e)}")
            raise
    
    def plot_correlation_heatmap(self, corr_df: pd.DataFrame,
                               method: str = 'pearson',
                               top_n: int = 20) -> plt.Figure:
        """
        Plot correlation heatmap for top N correlated features.
        
        Args:
            corr_df (pd.DataFrame): Correlation results
            method (str): Correlation method ('pearson' or 'spearman')
            top_n (int): Number of top correlations to plot
            
        Returns:
            plt.Figure: Correlation heatmap figure
        """
        try:
            # Select top N correlations
            top_corr = corr_df.nlargest(top_n, f'{method}_correlation')
            
            # Create correlation matrix
            corr_matrix = top_corr.pivot(
                index='domain',
                columns='column',
                values=f'{method}_correlation'
            )
            
            # Create heatmap
            plt.figure(figsize=(12, 8))
            sns.heatmap(
                corr_matrix,
                annot=True,
                cmap='RdBu_r',
                center=0,
                fmt='.2f'
            )
            plt.title(f'Top {top_n} {method.capitalize()} Correlations')
            plt.tight_layout()
            
            self.correlation_history.append({
                'timestamp': datetime.now(),
                'operation': 'plot_correlation_heatmap',
                'method': method,
                'top_n': top_n
            })
            
            return plt.gcf()
            
        except Exception as e:
            logger.error(f"Error plotting correlation heatmap: {str(e)}")
            raise
    
    def get_feature_importance(self, corr_df: pd.DataFrame,
                             method: str = 'mutual_information',
                             top_n: int = 10) -> pd.DataFrame:
        """
        Get top N most important features based on correlation metrics.
        
        Args:
            corr_df (pd.DataFrame): Correlation results
            method (str): Method to use for ranking ('pearson', 'spearman', or 'mutual_information')
            top_n (int): Number of top features to return
            
        Returns:
            pd.DataFrame: Top N important features
        """
        try:
            # Select correlation column based on method
            if method == 'pearson':
                corr_col = 'pearson_correlation'
            elif method == 'spearman':
                corr_col = 'spearman_correlation'
            else:
                corr_col = 'mutual_information'
            
            # Get top N features
            top_features = corr_df.nlargest(top_n, corr_col)
            
            self.correlation_history.append({
                'timestamp': datetime.now(),
                'operation': 'get_feature_importance',
                'method': method,
                'top_n': top_n
            })
            
            return top_features
            
        except Exception as e:
            logger.error(f"Error getting feature importance: {str(e)}")
            raise
    
    def get_correlation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of correlation operations performed.
        
        Returns:
            List[Dict[str, Any]]: List of correlation operations
        """
        return self.correlation_history 