/**
 * Natural Language Query functionality
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initNaturalLanguageQuery();
});

function initNaturalLanguageQuery() {
    const nlqInput = document.getElementById('nlq-input');
    const nlqSubmit = document.getElementById('nlq-submit');
    const nlqSuggestionPills = document.getElementById('nlq-suggestion-pills');
    const nlqResults = document.getElementById('nlq-results');
    const nlqExplanation = document.getElementById('nlq-explanation');
    const nlqVisualizations = document.getElementById('nlq-visualizations');
    const nlqDetailsContent = document.getElementById('nlq-details-content');
    const nlqSave = document.getElementById('nlq-save');
    const nlqExport = document.getElementById('nlq-export');
    
    // Hide results initially
    if (nlqResults) {
        nlqResults.style.display = 'none';
    }
    
    // Load query suggestions
    loadQuerySuggestions();
    
    // Set up event listeners
    if (nlqInput && nlqSubmit) {
        // Submit on Enter key
        nlqInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitQuery();
            }
        });
        
        // Submit on button click
        nlqSubmit.addEventListener('click', submitQuery);
    }
    
    // Handle suggestion clicks
    if (nlqSuggestionPills) {
        nlqSuggestionPills.addEventListener('click', function(e) {
            if (e.target.classList.contains('suggestion-pill')) {
                nlqInput.value = e.target.textContent;
                submitQuery();
            }
        });
    }
    
    // Handle save button
    if (nlqSave) {
        nlqSave.addEventListener('click', saveQuery);
    }
    
    // Handle export button
    if (nlqExport) {
        nlqExport.addEventListener('click', exportResults);
    }
    
    /**
     * Load query suggestions from the API
     */
    function loadQuerySuggestions() {
        if (!nlqSuggestionPills) return;
        
        fetch('/api/nlq/suggestions')
            .then(response => response.json())
            .then(data => {
                // Clear existing suggestions
                nlqSuggestionPills.innerHTML = '';
                
                // Flatten and shuffle suggestions
                const allSuggestions = [
                    ...data.simple_queries || [],
                    ...data.correlation_queries || [],
                    ...data.prediction_queries || [],
                    ...data.analysis_queries || []
                ];
                
                // Shuffle array
                const shuffled = allSuggestions.sort(() => 0.5 - Math.random());
                
                // Display first 5 suggestions
                for (let i = 0; i < Math.min(5, shuffled.length); i++) {
                    const pill = document.createElement('span');
                    pill.classList.add('suggestion-pill');
                    pill.textContent = shuffled[i];
                    nlqSuggestionPills.appendChild(pill);
                }
            })
            .catch(error => {
                console.error('Error loading suggestions:', error);
            });
    }
    
    /**
     * Submit the query to the API
     */
    function submitQuery() {
        if (!nlqInput || !nlqInput.value.trim()) return;
        
        const query = nlqInput.value.trim();
        
        // Show loading state
        if (nlqResults) {
            nlqResults.style.display = 'block';
            nlqExplanation.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
            nlqVisualizations.innerHTML = '';
        }
        
        // Make API call
        fetch('/api/nlq/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
            })
            .catch(error => {
                console.error('Error submitting query:', error);
                if (nlqExplanation) {
                    nlqExplanation.innerHTML = `<div class="alert alert-danger">Error processing your query. Please try again.</div>`;
                }
            });
    }
    
    /**
     * Display query results
     */
    function displayResults(data) {
        if (!nlqResults) return;
        
        // Show results section
        nlqResults.style.display = 'block';
        
        // Show the results row if it exists (for dashboard integration)
        const resultsRow = document.getElementById('nlq-results-row');
        if (resultsRow) {
            resultsRow.style.display = 'flex';
        }
        
        // Set title based on query intent
        const title = document.getElementById('nlq-results-title');
        if (title) {
            let titleText = 'Query Results';
            if (data.parsed && data.parsed.intent) {
                switch (data.parsed.intent) {
                    case 'simple_data': 
                        titleText = 'Data Results';
                        break;
                    case 'correlation': 
                        titleText = 'Correlation Analysis';
                        break;
                    case 'prediction': 
                        titleText = 'Prediction Results';
                        break;
                    case 'comparison': 
                        titleText = 'Comparison Results';
                        break;
                    case 'anomaly': 
                        titleText = 'Anomaly Detection';
                        break;
                }
            }
            title.textContent = titleText;
        }
        
        // Display explanation
        if (nlqExplanation) {
            if (data.error) {
                nlqExplanation.innerHTML = `<div class="alert alert-warning">${data.error}</div>`;
                if (data.suggestion) {
                    nlqExplanation.innerHTML += `<p>Suggestion: ${data.suggestion}</p>`;
                }
            } else if (data.explanation) {
                nlqExplanation.innerHTML = `<p>${data.explanation}</p>`;
            } else {
                nlqExplanation.innerHTML = `<p>Here are the results for your query.</p>`;
            }
        }
        
        // Display visualizations
        if (nlqVisualizations) {
            nlqVisualizations.innerHTML = '';
            
            if (data.visualizations && data.visualizations.length > 0) {
                data.visualizations.forEach(viz => {
                    // Create visualization container
                    const vizContainer = document.createElement('div');
                    vizContainer.classList.add('nlq-visualization-container');
                    
                    // Add title
                    const title = document.createElement('h4');
                    title.textContent = viz.title || 'Visualization';
                    vizContainer.appendChild(title);
                    
                    // Create viz element
                    const vizElement = document.createElement('div');
                    vizElement.classList.add('nlq-viz');
                    vizElement.id = `viz-${Math.random().toString(36).substring(2, 9)}`;
                    vizContainer.appendChild(vizElement);
                    
                    nlqVisualizations.appendChild(vizContainer);
                    
                    // Render the visualization based on type
                    renderVisualization(vizElement.id, viz);
                });
            } else {
                nlqVisualizations.innerHTML = '<p>No visualizations available for this query.</p>';
            }
        }
        
        // Display details
        if (nlqDetailsContent) {
            // Show raw data in a formatted way
            nlqDetailsContent.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        }
    }
    
    /**
     * Render a visualization based on its type
     */
    function renderVisualization(elementId, vizData) {
        // This would be replaced with actual visualization rendering
        // using libraries like Plotly, D3, etc.
        const element = document.getElementById(elementId);
        if (!element) return;
        
        // Placeholder visualization
        element.innerHTML = `<div class="placeholder-viz">
            <p><strong>${vizData.type}</strong> visualization for ${vizData.domain || 'multiple domains'}</p>
            <p>In a production environment, this would render an interactive ${vizData.type} chart</p>
        </div>`;
        
        // In a real implementation, we would use a visualization library based on the type
        // For example:
        
        /*
        if (vizData.type === 'heatmap') {
            Plotly.newPlot(elementId, [{
                z: vizData.data.values,
                x: vizData.data.x_labels,
                y: vizData.data.y_labels,
                type: 'heatmap',
                colorscale: 'Viridis'
            }]);
        } else if (vizData.type === 'network') {
            // D3.js network graph rendering
            const network = new NetworkGraph(elementId, vizData.data);
            network.render();
        } else if (vizData.type === 'line') {
            Plotly.newPlot(elementId, [{
                x: vizData.data.x,
                y: vizData.data.y,
                type: 'scatter',
                mode: 'lines+markers'
            }]);
        }
        */
    }
    
    /**
     * Save the current query
     */
    function saveQuery() {
        // This would be replaced with actual save functionality
        alert('Query saved to favorites');
    }
    
    /**
     * Export the results
     */
    function exportResults() {
        // This would be replaced with actual export functionality
        alert('Results exported');
    }
}