/**
 * Cross-Domain Predictive Analytics Dashboard
 * Prediction Page JavaScript
 * 
 * This script handles the specialized functionality for the prediction page,
 * including parameter sliders, prediction model interaction, and results visualization.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize prediction page components
    initializePredictionSliders();
    initializePredictionModelSelection();
    initializeScenarioControls();
    setupPredictionButton();
    setupExportControls();
    
    // Create preview chart if canvas exists
    const previewCanvas = document.getElementById('predictionPreviewChart');
    if (previewCanvas) {
        createPreviewChart(previewCanvas);
    }
});

// Initialize all prediction parameter sliders
function initializePredictionSliders() {
    const sliders = document.querySelectorAll('.prediction-slider');
    
    sliders.forEach(slider => {
        // Update value display when slider changes
        slider.addEventListener('input', function() {
            const valueDisplay = document.getElementById(`${slider.id}-value`);
            if (valueDisplay) {
                // Format value display based on slider type
                if (slider.id === 'confidenceThreshold') {
                    valueDisplay.textContent = `${(slider.value * 100).toFixed(0)}%`;
                } else if (slider.id.includes('Range')) {
                    valueDisplay.textContent = slider.value;
                }
            }
            
            // Update prediction preview when parameter changes
            updatePredictionPreview();
        });
        
        // Trigger initial value display update
        const event = new Event('input');
        slider.dispatchEvent(event);
    });
}

// Initialize prediction model selection dropdown
function initializePredictionModelSelection() {
    const modelSelect = document.getElementById('predictionModelSelect');
    if (modelSelect) {
        modelSelect.addEventListener('change', function() {
            // Show/hide relevant parameter sections based on model selection
            const selectedModel = modelSelect.value;
            
            // Update prediction preview with new model selection
            updatePredictionPreview();
        });
    }
    
    const timeframeSelect = document.getElementById('predictionTimeRange');
    if (timeframeSelect) {
        timeframeSelect.addEventListener('change', function() {
            // Update prediction preview with new timeframe
            updatePredictionPreview();
        });
    }
}

// Initialize scenario save/load controls
function initializeScenarioControls() {
    // Save scenario button
    const saveScenarioBtn = document.getElementById('saveScenarioBtn');
    if (saveScenarioBtn) {
        saveScenarioBtn.addEventListener('click', function() {
            const scenarioName = prompt('Enter a name for this scenario:');
            if (scenarioName && scenarioName.trim() !== '') {
                // Collect current parameter values
                const scenarioParams = collectScenarioParameters();
                
                // Save scenario to user preferences
                saveScenario(scenarioName, scenarioParams);
                
                // Add to scenario dropdown
                addScenarioToDropdown(scenarioName);
                
                // Show success notification
                showNotification({
                    type: 'success',
                    title: 'Scenario Saved',
                    message: `Scenario "${scenarioName}" has been saved successfully.`
                });
            }
        });
    }
    
    // Load scenario dropdown items
    const scenarioDropdown = document.getElementById('scenarioDropdown');
    if (scenarioDropdown) {
        // Add event listeners to default scenario options
        const defaultOptions = scenarioDropdown.querySelectorAll('.default-option');
        defaultOptions.forEach(option => {
            option.addEventListener('click', function(e) {
                e.preventDefault();
                const scenarioName = this.getAttribute('data-scenario');
                loadDefaultScenario(scenarioName);
            });
        });
        
        // Load saved scenarios from user preferences
        loadSavedScenarios();
    }
}

// Setup prediction button click event
function setupPredictionButton() {
    const runPredictionBtn = document.getElementById('runPredictionBtn');
    if (runPredictionBtn) {
        runPredictionBtn.addEventListener('click', function() {
            // Show loading indicator
            const loadingIndicator = document.getElementById('loadingIndicator');
            if (loadingIndicator) {
                loadingIndicator.style.display = 'block';
            }
            
            // Hide previous results and error messages
            const predictionResults = document.getElementById('predictionResults');
            if (predictionResults) {
                predictionResults.style.display = 'none';
            }
            
            const noResultsMessage = document.getElementById('noResultsMessage');
            if (noResultsMessage) {
                noResultsMessage.style.display = 'none';
            }
            
            const errorContainer = document.getElementById('errorContainer');
            if (errorContainer) {
                errorContainer.style.display = 'none';
            }
            
            // Collect all parameters for prediction
            const params = collectScenarioParameters();
            
            // Call prediction API
            runPrediction(params)
                .then(results => {
                    // Update UI with prediction results
                    displayPredictionResults(results);
                    
                    // Show correlation analysis if available
                    if (results.correlations) {
                        displayCorrelationAnalysis(results.correlations);
                    }
                    
                    // Hide loading indicator
                    if (loadingIndicator) {
                        loadingIndicator.style.display = 'none';
                    }
                    
                    // Show success notification
                    showNotification({
                        type: 'success',
                        title: 'Prediction Complete',
                        message: 'Prediction model has been successfully processed.'
                    });
                })
                .catch(error => {
                    console.error('Error running prediction:', error);
                    
                    // Show error message
                    if (errorContainer) {
                        errorContainer.textContent = 'Error processing prediction. Please try again or adjust parameters.';
                        errorContainer.style.display = 'block';
                    }
                    
                    // Hide loading indicator
                    if (loadingIndicator) {
                        loadingIndicator.style.display = 'none';
                    }
                    
                    // Show error notification
                    showNotification({
                        type: 'error',
                        title: 'Prediction Error',
                        message: 'Failed to process prediction. Please try again with different parameters.'
                    });
                });
        });
    }
}

// Setup export and share controls
function setupExportControls() {
    // Export results button
    const exportResultsBtn = document.getElementById('exportResultsBtn');
    if (exportResultsBtn) {
        exportResultsBtn.addEventListener('click', function() {
            exportPredictionResults();
        });
    }
    
    // Share results button
    const shareResultsBtn = document.getElementById('shareResultsBtn');
    if (shareResultsBtn) {
        shareResultsBtn.addEventListener('click', function() {
            sharePredictionResults();
        });
    }
}

// Create preview chart for prediction preview
function createPreviewChart(canvas) {
    const ctx = canvas.getContext('2d');
    
    // Create empty chart
    window.previewChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: generateDummyDates(30),
            datasets: [{
                label: 'Predicted Trend',
                data: generateDummyData(30),
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Update prediction preview based on current parameters
function updatePredictionPreview() {
    // Collect current parameter values
    const params = collectScenarioParameters();
    
    // Show preview loading state
    const previewContainer = document.getElementById('predictionPreview');
    if (previewContainer) {
        previewContainer.innerHTML = `
            <div class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="text-muted mt-2">Updating preview...</p>
            </div>
        `;
    }
    
    // Call preview API
    fetch('/api/prediction/preview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Update preview content
        if (previewContainer) {
            // Clear loading state
            previewContainer.innerHTML = '';
            
            // Create preview chart if not exists
            if (!document.getElementById('predictionPreviewChart')) {
                const canvas = document.createElement('canvas');
                canvas.id = 'predictionPreviewChart';
                canvas.height = 200;
                previewContainer.appendChild(canvas);
                createPreviewChart(canvas);
            }
            
            // Update chart with preview data
            if (window.previewChart && data.chartData) {
                window.previewChart.data = data.chartData;
                window.previewChart.options = data.chartOptions || window.previewChart.options;
                window.previewChart.update();
            }
            
            // Update confidence indicator
            updateConfidenceIndicator(data.confidence || 0.5);
        }
    })
    .catch(error => {
        console.error('Error updating preview:', error);
        
        // Show error state in preview
        if (previewContainer) {
            previewContainer.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-exclamation-triangle text-warning fs-4"></i>
                    <p class="text-muted mt-2">Unable to generate preview with current parameters.</p>
                </div>
            `;
        }
    });
}

// Run prediction with given parameters
function runPrediction(params) {
    return fetch('/api/prediction/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}

// Display prediction results in UI
function displayPredictionResults(results) {
    const resultsContainer = document.getElementById('predictionResults');
    if (!resultsContainer) return;
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    // Create results visualizations based on prediction model type
    const modelType = document.getElementById('predictionModelSelect').value;
    
    if (modelType === 'time_series') {
        displayTimeSeriesResults(resultsContainer, results);
    } else if (modelType === 'classification') {
        displayClassificationResults(resultsContainer, results);
    } else if (modelType === 'regression') {
        displayRegressionResults(resultsContainer, results);
    } else if (modelType === 'clustering') {
        displayClusteringResults(resultsContainer, results);
    }
    
    // Display key metrics and insights
    displayResultInsights(resultsContainer, results);
    
    // Show results container
    resultsContainer.style.display = 'block';
    
    // Hide no results message
    const noResultsMessage = document.getElementById('noResultsMessage');
    if (noResultsMessage) {
        noResultsMessage.style.display = 'none';
    }
}

// Display time series prediction results
function displayTimeSeriesResults(container, results) {
    // Create container for the chart
    const chartContainer = document.createElement('div');
    chartContainer.classList.add('mb-4');
    chartContainer.style.height = '400px';
    
    // Create canvas for the chart
    const canvas = document.createElement('canvas');
    canvas.id = 'timeSeriesResultsChart';
    canvas.height = 400;
    chartContainer.appendChild(canvas);
    container.appendChild(chartContainer);
    
    // Create chart
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: results.chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: results.title || 'Time Series Prediction'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: results.yAxisLabel || 'Value'
                    },
                    beginAtZero: false
                }
            }
        }
    });
}

// Display classification prediction results
function displayClassificationResults(container, results) {
    // Create container for the chart
    const chartContainer = document.createElement('div');
    chartContainer.classList.add('mb-4');
    chartContainer.style.height = '400px';
    
    // Create canvas for the chart
    const canvas = document.createElement('canvas');
    canvas.id = 'classificationResultsChart';
    canvas.height = 400;
    chartContainer.appendChild(canvas);
    container.appendChild(chartContainer);
    
    // Create chart
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: results.chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: results.title || 'Classification Results'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Probability'
                    }
                }
            }
        }
    });
    
    // Display predicted class with confidence
    const predictionResult = document.createElement('div');
    predictionResult.classList.add('alert', 'alert-info', 'mt-3');
    predictionResult.innerHTML = `
        <strong>Predicted Class:</strong> ${results.predictedClass}
        <br>
        <strong>Confidence:</strong> ${(results.confidence * 100).toFixed(1)}%
    `;
    container.appendChild(predictionResult);
}

// Display regression prediction results
function displayRegressionResults(container, results) {
    // Create container for the chart
    const chartContainer = document.createElement('div');
    chartContainer.classList.add('mb-4');
    chartContainer.style.height = '400px';
    
    // Create canvas for the chart
    const canvas = document.createElement('canvas');
    canvas.id = 'regressionResultsChart';
    canvas.height = 400;
    chartContainer.appendChild(canvas);
    container.appendChild(chartContainer);
    
    // Create chart
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'scatter',
        data: results.chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            return `(${point.x.toFixed(2)}, ${point.y.toFixed(2)})`;
                        }
                    }
                },
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: results.title || 'Regression Analysis'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: results.xAxisLabel || 'X'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: results.yAxisLabel || 'Y'
                    }
                }
            }
        }
    });
    
    // Display regression statistics
    const statsContainer = document.createElement('div');
    statsContainer.classList.add('row', 'mt-3');
    
    // Create statistic cards
    const stats = [
        { name: 'R²', value: results.rSquared.toFixed(3) },
        { name: 'Mean Absolute Error', value: results.mae.toFixed(3) },
        { name: 'Root Mean Squared Error', value: results.rmse.toFixed(3) },
        { name: 'Confidence', value: `${(results.confidence * 100).toFixed(1)}%` }
    ];
    
    stats.forEach(stat => {
        const statCard = document.createElement('div');
        statCard.classList.add('col-md-3', 'col-sm-6', 'mb-3');
        
        statCard.innerHTML = `
            <div class="card h-100">
                <div class="card-body text-center">
                    <h6 class="card-title">${stat.name}</h6>
                    <p class="card-text fs-4">${stat.value}</p>
                </div>
            </div>
        `;
        
        statsContainer.appendChild(statCard);
    });
    
    container.appendChild(statsContainer);
}

// Display clustering prediction results
function displayClusteringResults(container, results) {
    // Create container for the chart
    const chartContainer = document.createElement('div');
    chartContainer.classList.add('mb-4');
    chartContainer.style.height = '400px';
    
    // Create canvas for the chart
    const canvas = document.createElement('canvas');
    canvas.id = 'clusteringResultsChart';
    canvas.height = 400;
    chartContainer.appendChild(canvas);
    container.appendChild(chartContainer);
    
    // Create chart
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'scatter',
        data: results.chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = context.raw;
                            return `Cluster ${point.cluster}: (${point.x.toFixed(2)}, ${point.y.toFixed(2)})`;
                        }
                    }
                },
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: results.title || 'Clustering Analysis'
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: results.xAxisLabel || 'Feature 1'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: results.yAxisLabel || 'Feature 2'
                    }
                }
            }
        }
    });
    
    // Display cluster information
    const clusterInfo = document.createElement('div');
    clusterInfo.classList.add('row', 'mt-3');
    
    results.clusters.forEach((cluster, index) => {
        const clusterCard = document.createElement('div');
        clusterCard.classList.add('col-md-4', 'col-sm-6', 'mb-3');
        
        clusterCard.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-${getBootstrapColorClass(index)}">
                    <h6 class="card-title mb-0 text-white">Cluster ${index + 1}</h6>
                </div>
                <div class="card-body">
                    <p><strong>Size:</strong> ${cluster.size} data points</p>
                    <p><strong>Centroid:</strong> (${cluster.centroid.map(val => val.toFixed(2)).join(', ')})</p>
                    <p><strong>Characteristics:</strong> ${cluster.description}</p>
                </div>
            </div>
        `;
        
        clusterInfo.appendChild(clusterCard);
    });
    
    container.appendChild(clusterInfo);
}

// Display insight section for prediction results
function displayResultInsights(container, results) {
    // Create insights section
    const insightsSection = document.createElement('div');
    insightsSection.classList.add('mt-4');
    
    insightsSection.innerHTML = `
        <h5 class="mb-3">Key Insights</h5>
        <div class="card">
            <div class="card-body">
                <ul class="insights-list">
                    ${results.insights.map(insight => `
                        <li class="insight-item">
                            <div class="insight-icon">
                                <i class="fas ${getInsightIcon(insight.type)} ${getInsightIconColor(insight.type)}"></i>
                            </div>
                            <div class="insight-content">
                                <h6>${insight.title}</h6>
                                <p>${insight.description}</p>
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;
    
    container.appendChild(insightsSection);
}

// Display correlation analysis
function displayCorrelationAnalysis(correlations) {
    const correlationMatrix = document.getElementById('correlationMatrix');
    if (!correlationMatrix) return;
    
    // Clear previous content
    correlationMatrix.innerHTML = '';
    
    // Create heatmap using D3.js
    // This will be integrated with Emmanuel's visualization code
    
    // For now, display placeholder content
    correlationMatrix.innerHTML = `
        <div class="text-center py-4">
            <p class="text-muted">Correlation analysis visualization will be integrated with Emmanuel's code.</p>
        </div>
    `;
    
    // Display correlation insights
    const insightsContainer = document.getElementById('correlationInsights');
    if (insightsContainer) {
        insightsContainer.innerHTML = '';
        
        // Create insights list
        const insightsList = document.createElement('ul');
        insightsList.classList.add('list-group');
        
        correlations.insights.forEach(insight => {
            const insightItem = document.createElement('li');
            insightItem.classList.add('list-group-item');
            
            insightItem.innerHTML = `
                <div class="d-flex align-items-center">
                    <div class="insight-strength me-3">
                        <span class="badge bg-${getCorrelationBadgeColor(insight.strength)}">${insight.strength.toFixed(2)}</span>
                    </div>
                    <div>
                        <p class="mb-1">${insight.description}</p>
                        <small class="text-muted">${insight.factors.join(' → ')}</small>
                    </div>
                </div>
            `;
            
            insightsList.appendChild(insightItem);
        });
        
        insightsContainer.appendChild(insightsList);
    }
}

// Export prediction results
function exportPredictionResults() {
    // Determine the model type
    const modelType = document.getElementById('predictionModelSelect').value;
    
    // Show export options modal
    const modalHTML = `
        <div class="modal fade" id="exportModal" tabindex="-1" aria-labelledby="exportModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exportModalLabel">Export Prediction Results</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form>
                            <div class="mb-3">
                                <label for="exportFormat" class="form-label">Export Format</label>
                                <select class="form-select" id="exportFormat">
                                    <option value="csv">CSV</option>
                                    <option value="json">JSON</option>
                                    <option value="excel">Excel</option>
                                    <option value="pdf">PDF Report</option>
                                    <option value="png">Chart Image (PNG)</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="exportFilename" class="form-label">Filename</label>
                                <input type="text" class="form-control" id="exportFilename" value="prediction_results_${new Date().toISOString().slice(0,10)}">
                            </div>
                            <div class="mb-3 form-check">
                                <input type="checkbox" class="form-check-input" id="includeInsights" checked>
                                <label class="form-check-label" for="includeInsights">Include insights</label>
                            </div>
                            <div class="mb-3 form-check">
                                <input type="checkbox" class="form-check-input" id="includeParameters" checked>
                                <label class="form-check-label" for="includeParameters">Include parameters</label>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="confirmExportBtn">Export</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to document
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer);
    
    // Initialize modal
    const exportModal = new bootstrap.Modal(document.getElementById('exportModal'));
    exportModal.show();
    
    // Set up confirmation button
    const confirmExportBtn = document.getElementById('confirmExportBtn');
    if (confirmExportBtn) {
        confirmExportBtn.addEventListener('click', function() {
            const format = document.getElementById('exportFormat').value;
            const filename = document.getElementById('exportFilename').value;
            const includeInsights = document.getElementById('includeInsights').checked;
            const includeParameters = document.getElementById('includeParameters').checked;
            
            // Hide modal
            exportModal.hide();
            
            // Show loading notification
            showNotification({
                type: 'info',
                title: 'Preparing Export',
                message: `Preparing ${format.toUpperCase()} export...`
            });
            
            // Call export API
            fetch('/api/prediction/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    format: format,
                    filename: filename,
                    includeInsights: includeInsights,
                    includeParameters: includeParameters,
                    modelType: modelType
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Export failed');
                }
                
                // Handle different formats
                if (format === 'png') {
                    return response.blob();
                } else {
                    return response.blob();
                }
            })
            .then(blob => {
                // Create download link
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = filename + '.' + format;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                
                // Show success notification
                showNotification({
                    type: 'success',
                    title: 'Export Complete',
                    message: `Results have been exported as ${format.toUpperCase()}.`
                });
            })
            .catch(error => {
                console.error('Error exporting results:', error);
                
                // Show error notification
                showNotification({
                    type: 'error',
                    title: 'Export Failed',
                    message: 'Failed to export results. Please try again.'
                });
            });
        });
    }
    
    // Clean up modal when hidden
    const exportModalElement = document.getElementById('exportModal');
    if (exportModalElement) {
        exportModalElement.addEventListener('hidden.bs.modal', function() {
            modalContainer.remove();
        });
    }
}

// Share prediction results
function sharePredictionResults() {
    // Show share options modal
    const modalHTML = `
        <div class="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="shareModalLabel">Share Prediction Results</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="shareLink" class="form-label">Shareable Link</label>
                            <div class="input-group">
                                <input type="text" class="form-control" id="shareLink" value="https://example.com/share/pred123456" readonly>
                                <button class="btn btn-outline-secondary" type="button" id="copyLinkBtn">
                                    <i class="fas fa-copy"></i>
                                </button>
                            </div>
                            <small class="form-text text-muted">This link will expire in 30 days.</small>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Share via</label>
                            <div class="d-flex gap-2">
                                <button class="btn btn-outline-primary">
                                    <i class="fas fa-envelope"></i> Email
                                </button>
                                <button class="btn btn-outline-info">
                                    <i class="fab fa-slack"></i> Slack
                                </button>
                                <button class="btn btn-outline-secondary">
                                    <i class="fab fa-teams"></i> Teams
                                </button>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="sharePermission" class="form-label">Permissions</label>
                            <select class="form-select" id="sharePermission">
                                <option value="view">View only</option>
                                <option value="edit">Edit</option>
                                <option value="admin">Full control</option>
                            </select>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to document
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = modalHTML;
    document.body.appendChild(modalContainer);
    
    // Initialize modal
    const shareModal = new bootstrap.Modal(document.getElementById('shareModal'));
    shareModal.show();
    
    // Set up copy button
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            const shareLink = document.getElementById('shareLink');
            shareLink.select();
            document.execCommand('copy');
            
            // Show feedback
            this.innerHTML = '<i class="fas fa-check"></i>';
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
            
            // Show notification
            showNotification({
                type: 'success',
                title: 'Link Copied',
                message: 'Shareable link has been copied to clipboard.'
            });
        });
    }
    
    // Clean up modal when hidden
    const shareModalElement = document.getElementById('shareModal');
    if (shareModalElement) {
        shareModalElement.addEventListener('hidden.bs.modal', function() {
            modalContainer.remove();
        });
    }
}

// Helper function to update confidence indicator
function updateConfidenceIndicator(confidence) {
    const confidenceIndicator = document.getElementById('confidenceIndicator');
    if (!confidenceIndicator) return;
    
    // Remove all existing classes
    confidenceIndicator.classList.remove('high', 'medium', 'low');
    
    // Add appropriate class based on confidence
    let text = '';
    if (confidence >= 0.7) {
        confidenceIndicator.classList.add('high');
        text = 'High Confidence';
    } else if (confidence >= 0.4) {
        confidenceIndicator.classList.add('medium');
        text = 'Medium Confidence';
    } else {
        confidenceIndicator.classList.add('low');
        text = 'Low Confidence';
    }
    
    // Update text
    confidenceIndicator.innerHTML = `
        <span class="indicator"></span>
        <span>${text} (${(confidence * 100).toFixed(0)}%)</span>
    `;
}

// Helper function to load a default scenario
function loadDefaultScenario(scenarioName) {
    let params = {};
    
    switch (scenarioName) {
        case 'default':
            // Reset all parameters to their default values
            document.querySelectorAll('.prediction-slider').forEach(slider => {
                slider.value = slider.defaultValue;
                const event = new Event('input');
                slider.dispatchEvent(event);
            });
            
            document.querySelectorAll('select.prediction-param').forEach(select => {
                select.value = select.options[0].value;
                const event = new Event('change');
                select.dispatchEvent(event);
            });
            break;
            
        case 'optimistic':
            // Set optimistic scenario parameters
            params = {
                tempRange: 25,
                precipRange: 10,
                windRange: 10,
                inflationRange: 2.0,
                gdpGrowthRange: 4.5,
                unemploymentRange: 3.5,
                sentimentRange: 0.8,
                engagementRange: 75,
                trendStrengthRange: 80,
                predictionModelSelect: 'time_series',
                predictionTimeRange: 90,
                confidenceThreshold: 0.7
            };
            applyScenarioParameters(params);
            break;
            
        case 'pessimistic':
            // Set pessimistic scenario parameters
            params = {
                tempRange: 35,
                precipRange: 80,
                windRange: 60,
                inflationRange: 8.0,
                gdpGrowthRange: -2.0,
                unemploymentRange: 12.0,
                sentimentRange: -0.6,
                engagementRange: 30,
                trendStrengthRange: 20,
                predictionModelSelect: 'time_series',
                predictionTimeRange: 30,
                confidenceThreshold: 0.8
            };
            applyScenarioParameters(params);
            break;
    }
    
    // Update preview
    updatePredictionPreview();
    
    // Show notification
    showNotification({
        type: 'info',
        title: 'Scenario Loaded',
        message: `"${scenarioName.charAt(0).toUpperCase() + scenarioName.slice(1)}" scenario has been loaded.`
    });
}

// Helper function to collect all scenario parameters
function collectScenarioParameters() {
    const params = {};
    
    // Collect slider values
    document.querySelectorAll('.prediction-slider').forEach(slider => {
        params[slider.id] = parseFloat(slider.value);
    });
    
    // Collect select values
    document.querySelectorAll('select.prediction-param').forEach(select => {
        params[select.id] = select.value;
    });
    
    return params;
}

// Helper function to apply scenario parameters to UI
function applyScenarioParameters(params) {
    // Apply to sliders
    Object.keys(params).forEach(key => {
        const element = document.getElementById(key);
        if (!element) return;
        
        if (element.classList.contains('prediction-slider')) {
            element.value = params[key];
            
            // Update value display
            const valueDisplay = document.getElementById(`${key}-value`);
            if (valueDisplay) {
                if (key === 'confidenceThreshold') {
                    valueDisplay.textContent = `${(params[key] * 100).toFixed(0)}%`;
                } else {
                    valueDisplay.textContent = params[key];
                }
            }
        } else if (element.tagName === 'SELECT') {
            element.value = params[key];
        }
    });
}

// Helper function to save scenario
function saveScenario(name, params) {
    // Make API call to save scenario
    fetch('/api/user/preferences/scenario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            params: params
        })
    })
    .catch(error => {
        console.error('Error saving scenario:', error);
        
        // Show error notification
        showNotification({
            type: 'error',
            title: 'Save Failed',
            message: 'Failed to save scenario. Please try again.'
        });
    });
}

// Helper function to add scenario to dropdown
function addScenarioToDropdown(name) {
    const dropdown = document.getElementById('scenarioDropdown');
    if (!dropdown) return;
    
    // Check if scenario already exists
    const existing = dropdown.querySelector(`[data-scenario="${name}"]`);
    if (existing) return;
    
    // Create new option
    const option = document.createElement('li');
    option.innerHTML = `<a class="dropdown-item" href="#" data-scenario="${name}">${name}</a>`;
    
    // Add event listener
    const link = option.querySelector('a');
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const scenarioName = this.getAttribute('data-scenario');
        loadSavedScenario(scenarioName);
    });
    
    // Add to dropdown
    dropdown.appendChild(option);
}

// Helper function to load saved scenarios
function loadSavedScenarios() {
    // Make API call to get saved scenarios
    fetch('/api/user/preferences/scenarios')
        .then(response => response.json())
        .then(data => {
            if (data.scenarios && data.scenarios.length > 0) {
                // Add divider if not exists
                const dropdown = document.getElementById('scenarioDropdown');
                if (dropdown) {
                    if (!dropdown.querySelector('.dropdown-divider')) {
                        const divider = document.createElement('li');
                        divider.innerHTML = '<hr class="dropdown-divider">';
                        dropdown.appendChild(divider);
                    }
                    
                    // Add each scenario
                    data.scenarios.forEach(scenario => {
                        addScenarioToDropdown(scenario.name);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error loading saved scenarios:', error);
        });
}

// Helper function to load a saved scenario
function loadSavedScenario(name) {
    // Make API call to get scenario
    fetch(`/api/user/preferences/scenario/${encodeURIComponent(name)}`)
        .then(response => response.json())
        .then(data => {
            // Apply parameters
            applyScenarioParameters(data.params);
            
            // Update preview
            updatePredictionPreview();
            
            // Show notification
            showNotification({
                type: 'info',
                title: 'Scenario Loaded',
                message: `"${name}" scenario has been loaded.`
            });
        })
        .catch(error => {
            console.error(`Error loading scenario ${name}:`, error);
            
            // Show error notification
            showNotification({
                type: 'error',
                title: 'Load Failed',
                message: `Failed to load scenario "${name}". Please try again.`
            });
        });
}

// Helper function to show notification
function showNotification(data) {
    // Create notification element
    const notification = document.createElement('div');
    notification.classList.add('toast');
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');
    notification.setAttribute('aria-atomic', 'true');
    
    // Add appropriate styling based on notification type
    notification.classList.add(`bg-${getBootstrapColorClass(data.type)}`);
    if (data.type !== 'error') {
        notification.classList.add('text-white');
    }
    
    // Set timeout for auto-hide
    notification.setAttribute('data-bs-delay', data.duration || 5000);
    
    // Create notification content
    notification.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${data.title || 'Notification'}</strong>
            <small>${data.time || 'just now'}</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${data.message}
        </div>
    `;
    
    // Add to notification container
    const container = document.getElementById('notificationContainer');
    if (container) {
        container.appendChild(notification);
        
        // Initialize toast
        const toast = new bootstrap.Toast(notification);
        toast.show();
        
        // Remove from DOM after hiding
        notification.addEventListener('hidden.bs.toast', function() {
            notification.remove();
        });
    }
}

// Helper function to get Bootstrap color class
function getBootstrapColorClass(type) {
    switch (type) {
        case 'success':
            return 'success';
        case 'error':
            return 'danger';
        case 'warning':
            return 'warning';
        case 'info':
            return 'info';
        default:
            return 'primary';
    }
}

// Helper function to get correlation badge color
function getCorrelationBadgeColor(strength) {
    const absStrength = Math.abs(strength);
    
    if (absStrength >= 0.7) {
        return 'danger';
    } else if (absStrength >= 0.4) {
        return 'warning';
    } else {
        return 'info';
    }
}

// Helper function to get insight icon
function getInsightIcon(type) {
    switch (type) {
        case 'trend':
            return 'fa-chart-line';
        case 'anomaly':
            return 'fa-exclamation-triangle';
        case 'correlation':
            return 'fa-link';
        case 'pattern':
            return 'fa-puzzle-piece';
        case 'forecast':
            return 'fa-calendar-alt';
        default:
            return 'fa-info-circle';
    }
}

// Helper function to get insight icon color
function getInsightIconColor(type) {
    switch (type) {
        case 'trend':
            return 'text-primary';
        case 'anomaly':
            return 'text-warning';
        case 'correlation':
            return 'text-success';
        case 'pattern':
            return 'text-info';
        case 'forecast':
            return 'text-purple';
        default:
            return 'text-secondary';
    }
}

// Helper function to generate dummy dates for preview
function generateDummyDates(count) {
    const dates = [];
    const today = new Date();
    
    for (let i = 0; i < count; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);
        dates.push(date.toISOString().slice(0, 10));
    }
    
    return dates;
}

// Helper function to generate dummy data for preview
function generateDummyData(count) {
    const data = [];
    let value = 50 + Math.random() * 50;
    
    for (let i = 0; i < count; i++) {
        // Add some randomness but keep a general trend
        value += (Math.random() - 0.5) * 10;
        data.push(value);
    }
    
    return data;
}