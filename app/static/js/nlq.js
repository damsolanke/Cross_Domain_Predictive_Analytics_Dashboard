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
    
    // Example suggestions
    const suggestions = [
        "Show weather trends for the past week",
        "How does temperature affect energy consumption?",
        "Predict traffic tomorrow based on weather",
        "Compare market sentiment with stock prices",
        "Show me the busiest traffic times today"
    ];
    
    // Initialize suggestions
    initSuggestions();
    
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
     * Initialize suggestion pills
     */
    function initSuggestions() {
        if (!nlqSuggestionPills) return;
        
                // Clear existing suggestions
                nlqSuggestionPills.innerHTML = '';
                
        // Add suggestion pills
        suggestions.forEach(suggestion => {
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
     * Handle NLQ submission
     */
    function handleNlqSubmit() {
        if (!nlqInput || !nlqInput.value.trim()) return;
        
        const query = nlqInput.value.trim();
        
        // Show loading state
        showLoading();
        
        // Process the query - in a real app, this would be an API call
        // For demonstration, we'll simulate a response after a delay
        setTimeout(() => {
            processQuery(query);
        }, 1500);
    }
    
    /**
     * Show loading state
     */
    function showLoading() {
        if (!nlqVisualizations) return;
        
        nlqVisualizations.innerHTML = `
            <div class="nlq-loading">
                <div class="spinner-border nlq-spinner text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p>Analyzing your query...</p>
            </div>
        `;
        
        if (nlqExplanation) {
            nlqExplanation.textContent = '';
        }
        
        if (nlqDetailsContent) {
            nlqDetailsContent.innerHTML = '';
        }
    }
    
    /**
     * Process the natural language query
     * @param {string} query - The user's query
     */
    function processQuery(query) {
        // In a real application, this would call an API endpoint
        // For demonstration, we'll simulate different responses based on keywords
        
        let response;
        
        if (query.toLowerCase().includes('weather') || query.toLowerCase().includes('temperature')) {
            response = generateWeatherResponse(query);
        } else if (query.toLowerCase().includes('traffic')) {
            response = generateTrafficResponse(query);
        } else if (query.toLowerCase().includes('market') || query.toLowerCase().includes('stock')) {
            response = generateMarketResponse(query);
        } else if (query.toLowerCase().includes('predict') || query.toLowerCase().includes('forecast')) {
            response = generatePredictionResponse(query);
        } else if (query.toLowerCase().includes('correlate') || query.toLowerCase().includes('relationship') || 
                  query.toLowerCase().includes('affect') || query.toLowerCase().includes('impact')) {
            response = generateCorrelationResponse(query);
        } else {
            response = generateGenericResponse(query);
        }
        
        // Update the UI with the response
        updateResults(response);
        
        // Add to history (simulated)
        addToHistory(query);
    }
    
    /**
     * Update the results area with the response
     * @param {Object} response - The response object
     */
    function updateResults(response) {
        if (!nlqResults) return;
        
        // Update explanation
        if (nlqExplanation) {
            nlqExplanation.textContent = response.explanation;
        }
        
        // Update visualizations
        if (nlqVisualizations) {
            nlqVisualizations.innerHTML = '';
            
            response.visualizations.forEach(viz => {
                    const vizContainer = document.createElement('div');
                vizContainer.className = 'nlq-visualization';
                    
                    const title = document.createElement('h4');
                title.className = 'nlq-visualization-title';
                title.textContent = viz.title;
                
                const chartContainer = document.createElement('div');
                chartContainer.className = 'nlq-chart-container';
                chartContainer.id = `chart-${Math.random().toString(36).substring(2, 9)}`;
                
                vizContainer.appendChild(title);
                vizContainer.appendChild(chartContainer);
                    nlqVisualizations.appendChild(vizContainer);
                    
                // Create chart based on type
                if (viz.type === 'line') {
                    createLineChart(chartContainer.id, viz.data);
                } else if (viz.type === 'bar') {
                    createBarChart(chartContainer.id, viz.data);
                } else if (viz.type === 'pie') {
                    createPieChart(chartContainer.id, viz.data);
                } else if (viz.type === 'table') {
                    createDataTable(chartContainer, viz.data);
                }
            });
        }
        
        // Update details
        if (nlqDetailsContent) {
            nlqDetailsContent.innerHTML = `
                <h5>Query Interpretation</h5>
                <p>${response.interpretation}</p>
                <h5>Data Sources</h5>
                <ul>
                    ${response.dataSources.map(source => `<li>${source}</li>`).join('')}
                </ul>
                <h5>Confidence: ${response.confidence}%</h5>
                <div class="progress mb-3">
                    <div class="progress-bar bg-success" role="progressbar" 
                         style="width: ${response.confidence}%" 
                         aria-valuenow="${response.confidence}" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            `;
        }
    }
    
    /**
     * Generate a weather-related response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generateWeatherResponse(query) {
        return {
            explanation: `Analyzing weather patterns for the past 7 days. The data shows temperature trends with daily highs and lows, alongside precipitation levels.`,
            visualizations: [
                {
                    type: 'line',
                    title: 'Temperature Trends (Past 7 Days)',
                    data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        datasets: [
                            {
                                label: 'High (°F)',
                                data: [76, 78, 74, 82, 85, 83, 81],
                                borderColor: 'rgba(255, 99, 132, 1)',
                                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                                fill: true
                            },
                            {
                                label: 'Low (°F)',
                                data: [62, 65, 63, 68, 72, 71, 67],
                                borderColor: 'rgba(54, 162, 235, 1)',
                                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                                fill: true
                            }
                        ]
                    }
                },
                {
                    type: 'bar',
                    title: 'Precipitation (Past 7 Days)',
                    data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        datasets: [
                            {
                                label: 'Precipitation (in)',
                                data: [0, 0.2, 1.2, 0.4, 0, 0, 0.1],
                                backgroundColor: 'rgba(54, 162, 235, 0.6)'
                            }
                        ]
                    }
                }
            ],
            interpretation: `You asked about weather trends. I've analyzed temperature and precipitation data for the past week.`,
            dataSources: ['Weather Station Data', 'National Weather Service API'],
            confidence: 92
        };
    }
    
    /**
     * Generate a traffic-related response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generateTrafficResponse(query) {
        return {
            explanation: `Today's traffic congestion analysis shows peak congestion during morning and evening rush hours. The North Highway experienced the highest congestion levels.`,
            visualizations: [
                {
                    type: 'line',
                    title: 'Traffic Congestion by Hour',
                    data: {
                        labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                        datasets: [
                            {
                                label: 'Congestion Level',
                                data: [12, 8, 5, 8, 15, 35, 65, 85, 75, 50, 42, 48, 52, 48, 45, 52, 68, 88, 75, 62, 45, 30, 22, 15],
                                borderColor: 'rgba(255, 159, 64, 1)',
                                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    }
                },
                {
                    type: 'bar',
                    title: 'Congestion by Location',
                    data: {
                        labels: ['Downtown', 'North Highway', 'East Bridge', 'South Exit', 'West Corridor'],
                        datasets: [
                            {
                                label: 'Average Congestion Level',
                                data: [65, 78, 58, 42, 50],
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(255, 159, 64, 0.6)',
                                    'rgba(255, 205, 86, 0.6)',
                                    'rgba(75, 192, 192, 0.6)',
                                    'rgba(54, 162, 235, 0.6)'
                                ]
                            }
                        ]
                    }
                }
            ],
            interpretation: `You asked about traffic congestion. I've analyzed today's traffic patterns by time and location.`,
            dataSources: ['Traffic Sensor Network', 'City Transportation API', 'Vehicle Count Cameras'],
            confidence: 88
        };
    }
    
    /**
     * Generate a market-related response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generateMarketResponse(query) {
        return {
            explanation: `Analysis shows a positive correlation between social media sentiment and stock prices. When sentiment increases, stock prices tend to follow with a 1-2 day lag.`,
            visualizations: [
                {
                    type: 'line',
                    title: 'Stock Price vs Social Media Sentiment',
                    data: {
                        labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
                        datasets: [
                            {
                                label: 'Stock Price Index',
                                data: Array.from({length: 30}, (_, i) => 100 + Math.sin(i/3) * 10 + i/2),
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                                yAxisID: 'y',
                                fill: false
                            },
                            {
                                label: 'Social Sentiment Score',
                                data: Array.from({length: 30}, (_, i) => 70 + Math.sin((i-1)/3) * 15 + (i-1)/3),
                                borderColor: 'rgba(153, 102, 255, 1)',
                                backgroundColor: 'rgba(153, 102, 255, 0.1)',
                                yAxisID: 'y1',
                                fill: false
                            }
                        ]
                    }
                },
                {
                    type: 'bar',
                    title: 'Market Performance by Sector',
                    data: {
                        labels: ['Technology', 'Healthcare', 'Financial', 'Energy', 'Consumer'],
                        datasets: [
                            {
                                label: 'Performance (%)',
                                data: [8.5, 3.2, -1.5, -2.8, 4.1],
                                backgroundColor: [
                                    'rgba(75, 192, 192, 0.6)',
                                    'rgba(54, 162, 235, 0.6)',
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(75, 192, 192, 0.6)'
                                ]
                            }
                        ]
                    }
                }
            ],
            interpretation: `You asked about market sentiment and stock prices. I've analyzed the correlation between social media sentiment and stock price movements, with a sector breakdown.`,
            dataSources: ['Financial Market API', 'Social Media Sentiment Analysis', 'Economic Indicators Database'],
            confidence: 85
        };
    }
    
    /**
     * Generate a prediction-related response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generatePredictionResponse(query) {
        return {
            explanation: `Based on current weather forecasts, historical patterns, and event scheduling, tomorrow's traffic is predicted to be 15% higher than average, with peak congestion in the North and Downtown areas.`,
            visualizations: [
                {
                    type: 'line',
                    title: 'Traffic Prediction for Tomorrow',
                    data: {
                        labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                        datasets: [
                            {
                                label: 'Predicted Congestion',
                                data: [15, 10, 5, 8, 18, 40, 75, 90, 85, 55, 48, 52, 58, 52, 50, 55, 75, 95, 80, 65, 50, 35, 25, 18],
                                borderColor: 'rgba(255, 99, 132, 1)',
                                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Typical Congestion',
                                data: [12, 8, 5, 8, 15, 35, 65, 78, 70, 48, 42, 45, 50, 45, 42, 48, 65, 82, 70, 60, 45, 30, 22, 15],
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderDash: [5, 5],
                                tension: 0.3,
                                fill: false
                            }
                        ]
                    }
                },
                {
                    type: 'bar',
                    title: 'Predicted Congestion by Location',
                    data: {
                        labels: ['Downtown', 'North Highway', 'East Bridge', 'South Exit', 'West Corridor'],
                        datasets: [
                            {
                                label: 'Predicted Congestion',
                                data: [78, 85, 62, 45, 55],
                                backgroundColor: 'rgba(255, 99, 132, 0.6)'
                            },
                            {
                                label: 'Typical Congestion',
                                data: [65, 70, 58, 42, 50],
                                backgroundColor: 'rgba(54, 162, 235, 0.6)'
                            }
                        ]
                    }
                }
            ],
            interpretation: `You asked for a traffic prediction. I've analyzed historical patterns, weather forecasts, and scheduled events to predict tomorrow's traffic conditions.`,
            dataSources: ['Historical Traffic Data', 'Weather Forecast API', 'City Events Calendar', 'Road Construction Schedule'],
            confidence: 82
        };
    }
    
    /**
     * Generate a correlation-related response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generateCorrelationResponse(query) {
        return {
            explanation: `Analysis reveals a strong correlation (0.78) between temperature and energy consumption. As temperatures rise above 75°F or fall below 45°F, energy usage increases significantly.`,
            visualizations: [
                {
                    type: 'line',
                    title: 'Temperature vs. Energy Consumption',
                    data: {
                        labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
                        datasets: [
                            {
                                label: 'Temperature (°F)',
                                data: Array.from({length: 30}, (_, i) => 60 + Math.sin(i/3) * 15),
                                borderColor: 'rgba(255, 99, 132, 1)',
                                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                                yAxisID: 'y',
                                fill: false
                            },
                            {
                                label: 'Energy Consumption (MW)',
                                data: Array.from({length: 30}, (_, i) => {
                                    const temp = 60 + Math.sin(i/3) * 15;
                                    // Higher consumption at both high and low temperatures
                                    return 500 + Math.abs(temp - 60) * 10 + (Math.random() * 50 - 25);
                                }),
                                borderColor: 'rgba(54, 162, 235, 1)',
                                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                                yAxisID: 'y1',
                                fill: false
                            }
                        ]
                    }
                },
                {
                    type: 'pie',
                    title: 'Energy Usage Distribution by Source',
                    data: {
                        labels: ['Residential AC/Heating', 'Commercial HVAC', 'Industrial', 'Other'],
                        datasets: [
                            {
                                data: [45, 30, 15, 10],
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(54, 162, 235, 0.6)',
                                    'rgba(255, 205, 86, 0.6)',
                                    'rgba(75, 192, 192, 0.6)'
                                ]
                            }
                        ]
                    }
                }
            ],
            interpretation: `You asked about the relationship between temperature and energy consumption. I've analyzed 30 days of data to show the correlation pattern.`,
            dataSources: ['Weather Station Data', 'Energy Grid Consumption Metrics', 'Utility Provider API'],
            confidence: 90
        };
    }
    
    /**
     * Generate a generic response
     * @param {string} query - The user's query
     * @returns {Object} Response object with explanation and visualizations
     */
    function generateGenericResponse(query) {
        return {
            explanation: `I've analyzed your query about "${query}" and found some relevant data patterns. The cross-domain analysis suggests some interesting trends worth exploring further.`,
            visualizations: [
                {
                    type: 'bar',
                    title: 'Key Metrics Overview',
                    data: {
                        labels: ['Weather', 'Traffic', 'Economy', 'Social', 'Health'],
                        datasets: [
                            {
                                label: 'Current Values',
                                data: [72, 65, 82, 78, 68],
                                backgroundColor: 'rgba(75, 192, 192, 0.6)'
                            },
                            {
                                label: 'Baseline',
                                data: [70, 60, 75, 65, 70],
                                backgroundColor: 'rgba(153, 102, 255, 0.6)'
                            }
                        ]
                    }
                },
                {
                    type: 'table',
                    title: 'Domain Data Summary',
                    data: {
                        headers: ['Domain', 'Current Status', 'Trend', 'Confidence'],
                        rows: [
                            ['Weather', 'Normal', 'Stable', '95%'],
                            ['Traffic', 'Above Average', 'Increasing', '88%'],
                            ['Economic', 'Strong', 'Stable', '82%'],
                            ['Social Media', 'Positive', 'Improving', '75%'],
                            ['Public Health', 'Good', 'Stable', '90%']
                        ]
                    }
                }
            ],
            interpretation: `Your query was analyzed across multiple domains to identify patterns and insights.`,
            dataSources: ['Weather Data', 'Traffic Sensors', 'Economic Indicators', 'Social Media API', 'Public Health Records'],
            confidence: 75
        };
    }
    
    /**
     * Create a line chart
     * @param {string} containerId - The container element ID
     * @param {Object} data - Chart data
     */
    function createLineChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        position: 'left'
                    },
                    y1: {
                        beginAtZero: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Create a bar chart
     * @param {string} containerId - The container element ID
     * @param {Object} data - Chart data
     */
    function createBarChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    /**
     * Create a pie chart
     * @param {string} containerId - The container element ID
     * @param {Object} data - Chart data
     */
    function createPieChart(containerId, data) {
        const ctx = document.getElementById(containerId).getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    /**
     * Create a data table
     * @param {HTMLElement} container - The container element
     * @param {Object} data - Table data
     */
    function createDataTable(container, data) {
        const table = document.createElement('table');
        table.className = 'table table-striped table-hover nlq-table';
        
        // Create header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        data.headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create body
        const tbody = document.createElement('tbody');
        
        data.rows.forEach(row => {
            const tr = document.createElement('tr');
            
            row.forEach(cell => {
                const td = document.createElement('td');
                td.textContent = cell;
                tr.appendChild(td);
            });
            
            tbody.appendChild(tr);
        });
        
        table.appendChild(tbody);
        container.innerHTML = '';
        container.appendChild(table);
    }
    
    /**
     * Save the current query to history (simulated)
     */
    function saveQuery() {
        alert('Query saved to favorites.');
    }
    
    /**
     * Export results (simulated)
     */
    function exportResults() {
        alert('Results exported. Check your downloads folder.');
    }
    
    /**
     * Add query to history (simulated)
     * @param {string} query - The user's query
     */
    function addToHistory(query) {
        // This would normally call an API to save the query
        console.log('Added to history:', query);
    }
});