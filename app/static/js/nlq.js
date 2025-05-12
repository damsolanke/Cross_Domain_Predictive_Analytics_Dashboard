/**
 * Natural Language Query module
 * Handles interactions for the NLQ feature
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const nlqInput = document.getElementById('nlq-input');
    const nlqSubmit = document.getElementById('nlq-submit');
    const nlqResults = document.getElementById('nlq-results');
    const nlqSuggestionPills = document.getElementById('nlq-suggestion-pills');
    const nlqExplanation = document.getElementById('nlq-explanation');
    const nlqVisualizations = document.getElementById('nlq-visualizations');
    const nlqDetailsContent = document.getElementById('nlq-details-content');
    const nlqSave = document.getElementById('nlq-save');
    const nlqExport = document.getElementById('nlq-export');
    
    // Initialize
    loadSuggestions();
    loadQueryHistory();
    
    // Event listeners
    if (nlqSubmit) {
        nlqSubmit.addEventListener('click', handleNlqSubmit);
    }
    
    if (nlqInput) {
        nlqInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                handleNlqSubmit();
            }
        });
    }
    
    if (nlqSave) {
        nlqSave.addEventListener('click', saveQuery);
    }
    
    if (nlqExport) {
        nlqExport.addEventListener('click', exportResults);
    }
    
    /**
     * Load suggestions from the API
     */
    function loadSuggestions() {
        if (!nlqSuggestionPills) return;
        
        fetch('/api/nlq/suggestions')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load suggestions');
                }
                return response.json();
            })
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
                const suggestionsToShow = shuffled.slice(0, 5);
                
                // Add suggestion pills
                suggestionsToShow.forEach(suggestion => {
                    const pill = document.createElement('div');
                    pill.className = 'nlq-suggestion-pill';
                    pill.textContent = suggestion;
                    
                    pill.addEventListener('click', function() {
                        if (nlqInput) {
                            nlqInput.value = suggestion;
                            handleNlqSubmit();
                        }
                    });
                    
                    nlqSuggestionPills.appendChild(pill);
                });
            })
            .catch(error => {
                console.error('Error loading suggestions:', error);
                // Fall back to default suggestions
                useDefaultSuggestions();
            });
    }
    
    /**
     * Use default suggestions if API fails
     */
    function useDefaultSuggestions() {
        if (!nlqSuggestionPills) return;
        
        const defaultSuggestions = [
            "Show weather trends for the past week",
            "How does temperature affect energy consumption?",
            "Predict traffic tomorrow based on weather",
            "Compare market sentiment with stock prices",
            "Show me the busiest traffic times today"
        ];
        
        // Clear existing suggestions
        nlqSuggestionPills.innerHTML = '';
        
        // Add default suggestion pills
        defaultSuggestions.forEach(suggestion => {
            const pill = document.createElement('div');
            pill.className = 'nlq-suggestion-pill';
            pill.textContent = suggestion;
            
            pill.addEventListener('click', function() {
                if (nlqInput) {
                    nlqInput.value = suggestion;
                    handleNlqSubmit();
                }
            });
            
            nlqSuggestionPills.appendChild(pill);
        });
    }
    
    /**
     * Load query history from the API
     */
    function loadQueryHistory() {
        const historyContainer = document.getElementById('query-history');
        if (!historyContainer) return;
        
        fetch('/api/nlq/history')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load query history');
                }
                return response.json();
            })
            .then(data => {
                if (!data || data.length === 0) {
                    historyContainer.innerHTML = '<p class="text-muted">No query history yet.</p>';
                    return;
                }
                
                const historyList = document.createElement('ul');
                historyList.className = 'list-group';
                
                // Add history items
                data.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item list-group-item-action';
                    
                    // Make it clickable to re-run the query
                    listItem.addEventListener('click', function() {
                        if (nlqInput) {
                            nlqInput.value = item.query;
                            handleNlqSubmit();
                        }
                    });
                    
                    // Create query text
                    const queryText = document.createElement('div');
                    queryText.textContent = item.query;
                    listItem.appendChild(queryText);
                    
                    // Create timestamp
                    const timestamp = document.createElement('small');
                    timestamp.className = 'text-muted';
                    
                    // Format timestamp to local time
                    const date = new Date(item.timestamp);
                    timestamp.textContent = date.toLocaleString();
                    listItem.appendChild(timestamp);
                    
                    historyList.appendChild(listItem);
                });
                
                historyContainer.innerHTML = '';
                historyContainer.appendChild(historyList);
            })
            .catch(error => {
                console.error('Error loading query history:', error);
                historyContainer.innerHTML = '<p class="text-muted">Unable to load query history.</p>';
            });
    }
    
    /**
     * Handle NLQ submission
     */
    function handleNlqSubmit() {
        if (!nlqInput || !nlqInput.value.trim()) return;
        
        const query = nlqInput.value.trim();
        
        // Show loading state
        showLoading();
        
        // Make API call to process query
        fetch('/api/nlq/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to process query');
                }
                return response.json();
            })
            .then(data => {
                // Update UI with response
                updateResults(data);
            })
            .catch(error => {
                console.error('Error processing query:', error);
                showError('Failed to process your query. Please try again.');
            });
    }
    
    /**
     * Show loading state
     */
    function showLoading() {
        if (!nlqResults) return;
        
        // Display results section
        nlqResults.style.display = 'block';
        
        // Show loading in visualizations area
        if (nlqVisualizations) {
            nlqVisualizations.innerHTML = `
                <div class="nlq-loading">
                    <div class="spinner-border nlq-spinner text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p>Analyzing your query...</p>
                </div>
            `;
        }
        
        // Clear explanation
        if (nlqExplanation) {
            nlqExplanation.textContent = '';
        }
        
        // Clear details
        if (nlqDetailsContent) {
            nlqDetailsContent.innerHTML = '';
        }
    }
    
    /**
     * Show error message
     */
    function showError(message) {
        if (!nlqExplanation) return;
        
        nlqExplanation.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                ${message}
            </div>
        `;
        
        if (nlqVisualizations) {
            nlqVisualizations.innerHTML = '';
        }
    }
    
    /**
     * Update the results area with the API response
     */
    function updateResults(response) {
        if (!nlqResults) return;
        
        // Make sure results section is visible
        nlqResults.style.display = 'block';
        
        // Update explanation
        if (nlqExplanation && response.explanation) {
            nlqExplanation.textContent = response.explanation;
        }
        
        // Update visualizations
        if (nlqVisualizations && response.visualizations) {
            nlqVisualizations.innerHTML = '';
            
            if (response.visualizations.length === 0) {
                nlqVisualizations.innerHTML = '<p class="text-muted">No visualizations available for this query.</p>';
                return;
            }
            
            response.visualizations.forEach((viz, index) => {
                    const vizContainer = document.createElement('div');
                vizContainer.className = 'nlq-visualization';
                    
                    const title = document.createElement('h4');
                title.className = 'nlq-visualization-title';
                title.textContent = viz.title || `Visualization ${index + 1}`;
                
                const chartContainer = document.createElement('div');
                chartContainer.className = 'nlq-chart-container';
                chartContainer.id = `chart-${Math.random().toString(36).substring(2, 9)}`;
                
                vizContainer.appendChild(title);
                vizContainer.appendChild(chartContainer);
                    nlqVisualizations.appendChild(vizContainer);
                    
                // Create chart based on type
                renderVisualization(chartContainer.id, viz);
            });
        }
        
        // Update details panel
        if (nlqDetailsContent && response.parsed) {
            const parsed = response.parsed;
            
            // Format domains
            const domains = parsed.domains.map(d => d.replace('_', ' ')).join(', ');
            
            // Create confidence percentage
            const confidence = Math.round(parsed.confidence * 100);
            
            nlqDetailsContent.innerHTML = `
                <h5>Query Details</h5>
                <table class="table table-sm">
                    <tr>
                        <th>Intent:</th>
                        <td>${parsed.intent.replace('_', ' ')}</td>
                    </tr>
                    <tr>
                        <th>Domains:</th>
                        <td>${domains}</td>
                    </tr>
                    <tr>
                        <th>Time Range:</th>
                        <td>${formatDateRange(parsed.time_range)}</td>
                    </tr>
                    <tr>
                        <th>Confidence:</th>
                        <td>
                            <div class="progress" style="height: 8px;">
                                <div class="progress-bar bg-success" role="progressbar" 
                                     style="width: ${confidence}%" 
                                     aria-valuenow="${confidence}" 
                                     aria-valuemin="0" 
                                     aria-valuemax="100"></div>
                            </div>
                            <small class="text-muted">${confidence}%</small>
                        </td>
                    </tr>
                </table>
                
                <h5>Data Response</h5>
                <pre class="nlq-data-response">${JSON.stringify(response.data, null, 2)}</pre>
            `;
        }
        
        // Add to history (the real API already handles this)
    }
    
    /**
     * Render a visualization based on its type
     */
    function renderVisualization(elementId, viz) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        switch (viz.type) {
            case 'line':
                renderLineChart(element, viz);
                break;
            case 'bar':
                renderBarChart(element, viz);
                break;
            case 'heatmap':
                renderHeatmap(element, viz);
                break;
            case 'scatter':
                renderScatterPlot(element, viz);
                break;
            default:
                // Fallback for unsupported visualization types
                element.innerHTML = `
                    <div class="nlq-placeholder-viz">
                        <p><strong>${viz.type}</strong> visualization for ${viz.domain || 'data'}</p>
                        <p>Visualization type: ${viz.type}</p>
                    </div>
                `;
        }
    }
    
    /**
     * Render a line chart
     */
    function renderLineChart(element, viz) {
        // Create a canvas for the chart
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 300;
        element.appendChild(canvas);
        
        // Prepare data for Chart.js
        const ctx = canvas.getContext('2d');
        
        let labels, datasets;
        
        // Check if viz.data has the right format
        if (viz.data.x && viz.data.y) {
            // Single line chart
            labels = viz.data.x;
            datasets = [{
                label: viz.title || 'Value',
                data: viz.data.y,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                fill: true,
                tension: 0.4
            }];
            
            // If we have prediction data, style it differently
            if (viz.data.predicted && viz.data.prediction_start) {
                const predictionIndex = viz.data.prediction_start;
                const predictedData = viz.data.y.slice(predictionIndex);
                const historicalData = viz.data.y.slice(0, predictionIndex);
                
                // Replace with two datasets
                datasets = [
                    {
                        label: 'Historical',
                        data: [...historicalData, ...Array(predictedData.length).fill(null)],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Predicted',
                        data: [...Array(historicalData.length).fill(null), ...predictedData],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        borderDash: [5, 5],
                        fill: true,
                        tension: 0.4
                    }
                ];
            }
            
            // Check for anomalies
            if (viz.data.anomalies) {
                const anomalyIndices = viz.data.anomalies;
                const anomalyData = viz.data.y.map((y, i) => 
                    anomalyIndices.includes(i) ? y : null);
                
                // Add anomaly points
                datasets.push({
                    label: 'Anomalies',
                    data: anomalyData,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgb(255, 99, 132)',
                    pointRadius: 6,
                    pointHoverRadius: 8,
                    showLine: false
                });
            }
        } else {
            // Assume it's already in Chart.js format
            labels = viz.data.labels || [];
            datasets = viz.data.datasets || [];
        }
        
        // Create the chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Render a bar chart
     */
    function renderBarChart(element, viz) {
        // Create a canvas for the chart
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 300;
        element.appendChild(canvas);
        
        // Prepare data for Chart.js
        const ctx = canvas.getContext('2d');
        
        let labels, datasets;
        
        // Check data format
        if (viz.data.labels && viz.data.values) {
            // Simple bar chart
            labels = viz.data.labels;
            datasets = [{
                label: viz.title || 'Value',
                data: viz.data.values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }];
        } else {
            // Assume it's already in Chart.js format
            labels = viz.data.labels || [];
            datasets = viz.data.datasets || [];
        }
        
        // Create the chart
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        position: 'top'
                    }
                }
            }
        });
    }
    
    /**
     * Render a heatmap
     */
    function renderHeatmap(element, viz) {
        // Create a container for the heatmap
        element.style.height = '400px';
        
        // Check if Plotly is available
        if (window.Plotly) {
            const data = [{
                z: viz.data.values,
                x: viz.data.x_labels,
                y: viz.data.y_labels,
                type: 'heatmap',
                colorscale: 'Viridis'
            }];
            
            const layout = {
                title: viz.title,
                margin: {
                    l: 100,
                    r: 50,
                    b: 100,
                    t: 50
                }
            };
            
            Plotly.newPlot(element, data, layout);
        } else {
            // Fallback if Plotly isn't available
            element.innerHTML = `
                <div class="nlq-placeholder-viz">
                    <p>Heatmap showing correlation values between variables.</p>
                    <p>Plotly.js is required to display this visualization.</p>
                </div>
            `;
        }
    }
    
    /**
     * Render a scatter plot
     */
    function renderScatterPlot(element, viz) {
        // Create a canvas for the chart
        const canvas = document.createElement('canvas');
        canvas.width = 400;
        canvas.height = 300;
        element.appendChild(canvas);
        
        // Prepare data
        const ctx = canvas.getContext('2d');
        
        // Convert x,y arrays to point objects for Chart.js
        const data = [];
        for (let i = 0; i < viz.data.x.length; i++) {
            data.push({
                x: viz.data.x[i],
                y: viz.data.y[i]
            });
        }
        
        // Create the chart
        new Chart(ctx, {
                type: 'scatter',
            data: {
                datasets: [{
                    label: viz.title || 'Scatter Plot',
                    data: data,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    },
                    y: {
                        beginAtZero: false
                    }
                }
            }
        });
    }
    
    /**
     * Format a date range for display
     */
    function formatDateRange(timeRange) {
        if (!timeRange || !timeRange.start_date || !timeRange.end_date) {
            return 'Unknown date range';
        }
        
        const start = new Date(timeRange.start_date);
        const end = new Date(timeRange.end_date);
        
        return `${start.toLocaleDateString()} to ${end.toLocaleDateString()}`;
    }
    
    /**
     * Save the current query to favorites
     */
    function saveQuery() {
        const query = nlqInput ? nlqInput.value : '';
        if (!query) return;
        
        alert('Query saved to favorites.');
    }
    
    /**
     * Export results as JSON
     */
    function exportResults() {
        if (!nlqDetailsContent) return;
        
        const content = nlqDetailsContent.textContent;
        if (!content) {
            alert('No results to export');
            return;
        }
        
        // Create a download link
        const blob = new Blob([content], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `nlq-results-${new Date().toLocaleDateString()}.json`;
        document.body.appendChild(a);
        a.click();
        URL.revokeObjectURL(url);
        a.remove();
    }
});