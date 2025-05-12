/**
 * Dashboard JavaScript for real-time updates and dynamic visualizations
 */

// Dashboard controller
class DashboardController {
    constructor() {
        this.socket = io('/system-updates');
        this.dataCache = {
            weather: [],
            economic: [],
            transportation: [],
            'social-media': [],
            'cross-domain': []
        };
        this.chartInstances = {};
        this.updateInterval = 30000; // Fallback polling interval
        this.initializeEventHandlers();
    }

    /**
     * Initialize event handlers for WebSocket and UI
     */
    initializeEventHandlers() {
        // WebSocket event handlers
        this.socket.on('connect', () => {
            console.log('Connected to real-time updates');
            this.setConnectionStatus(true);
            
            // Reset reconnect delay on successful connection
            this.reconnectDelay = 0;
            
            // Subscribe to all update types
            this.socket.emit('subscribe_to_updates', { update_type: 'all' });
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from real-time updates');
            this.setConnectionStatus(false);
            
            // Set up polling as fallback
            this.startPolling();
            
            // Try to reconnect
            this.retryConnection();
        });
        
        this.socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
            this.setConnectionStatus(false);
            
            // Show error message
            this.showErrorMessage('Connection error. Using polling for updates.');
            
            // Set up polling as fallback
            this.startPolling();
            
            // Try to reconnect
            this.retryConnection();
        });

        this.socket.on('connection_response', (data) => {
            console.log('Connection response:', data);
        });

        this.socket.on('subscription_response', (data) => {
            console.log('Subscription response:', data);
        });

        // Data update event
        this.socket.on('data_update', (data) => {
            console.log('Data update received:', data);
            this.handleDataUpdate(data);
        });

        // Alert notification event
        this.socket.on('alert_notification', (data) => {
            console.log('Alert notification received:', data);
            this.handleAlertNotification(data);
        });
        
        // Correlation data event
        this.socket.on('correlation_data', (data) => {
            console.log('Correlation data received:', data);
            this.handleCorrelationDataUpdate(data);
        });
        
        // Correlation insight event
        this.socket.on('correlation_insight', (data) => {
            console.log('Correlation insight received:', data);
            this.handleCorrelationInsight(data);
        });
        
        // Correlation anomaly event
        this.socket.on('correlation_anomaly', (data) => {
            console.log('Correlation anomaly received:', data);
            this.handleCorrelationAnomaly(data);
        });

        // Initialize tabs and other UI elements
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeTabs();
            this.initializeControls();
            this.loadInitialData();
        });
    }

    /**
     * Initialize tab switching
     */
    initializeTabs() {
        const tabs = document.querySelectorAll('[data-tab-target]');
        const tabContents = document.querySelectorAll('[data-tab-content]');

        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Deactivate all tabs
                tabs.forEach(t => t.classList.remove('active'));
                tabContents.forEach(tc => tc.classList.remove('active'));
                
                // Activate clicked tab
                tab.classList.add('active');
                const target = document.querySelector(tab.dataset.tabTarget);
                if (target) {
                    target.classList.add('active');
                    
                    // Refresh charts when tab becomes visible
                    this.refreshChartsInContainer(target);
                }
            });
        });
    }

    /**
     * Initialize dashboard controls
     */
    initializeControls() {
        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.loadInitialData();
            });
        }

        // Auto-refresh toggle
        const autoRefreshToggle = document.getElementById('autoRefreshToggle');
        if (autoRefreshToggle) {
            autoRefreshToggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    this.startPolling();
                } else {
                    this.stopPolling();
                }
            });
        }

        // Time range selector
        const timeRangeSelector = document.getElementById('timeRangeSelector');
        if (timeRangeSelector) {
            timeRangeSelector.addEventListener('change', (e) => {
                this.updateTimeRange(e.target.value);
            });
        }
        
        // Correlation settings form
        const correlationSettingsForm = document.getElementById('correlation-settings-form');
        if (correlationSettingsForm) {
            correlationSettingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const timeWindow = document.getElementById('correlation-time-window').value;
                this.updateCorrelationSettings(timeWindow);
            });
        }
    }
    
    /**
     * Update correlation settings
     */
    updateCorrelationSettings(timeWindow) {
        // Send settings to server
        fetch('/api/system/correlation/configure', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                time_window_hours: parseInt(timeWindow)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show success message
                this.showErrorMessage('Correlation settings updated successfully');
                
                // Request updated correlation data
                this.socket.emit('get_correlation_data');
            } else {
                // Show error message
                this.showErrorMessage('Error updating correlation settings: ' + data.message);
            }
        })
        .catch(error => {
            this.showErrorMessage('Error updating correlation settings: ' + error);
        });
    }

    /**
     * Set connection status indicator
     */
    setConnectionStatus(connected) {
        const statusIndicator = document.getElementById('connectionStatus');
        if (statusIndicator) {
            if (connected) {
                statusIndicator.classList.remove('bg-danger');
                statusIndicator.classList.add('bg-success');
                statusIndicator.textContent = 'Connected';
            } else {
                statusIndicator.classList.remove('bg-success');
                statusIndicator.classList.add('bg-danger');
                statusIndicator.textContent = 'Disconnected';
            }
        }
    }

    /**
     * Start polling for updates (fallback when WebSocket is unavailable)
     */
    startPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
        }
        
        this.pollingInterval = setInterval(() => {
            this.fetchDashboardData();
        }, this.updateInterval);
        
        console.log(`Started polling every ${this.updateInterval / 1000} seconds`);
    }

    /**
     * Stop polling for updates
     */
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
            console.log('Stopped polling');
        }
    }

    /**
     * Load initial dashboard data
     */
    loadInitialData() {
        this.showLoadingIndicator(true);
        this.fetchDashboardData();
        
        // Request correlation data
        this.socket.emit('get_correlation_data');
        this.socket.emit('get_correlation_insights');
        
        // Set a timeout to hide the loading indicator in case the WebSocket connection
        // or data loading takes too long
        setTimeout(() => {
            this.showLoadingIndicator(false);
            
            // Check if we're still not connected and show a warning
            if (!this.socket.connected) {
                this.showErrorMessage('WebSocket connection failed. Using polling for updates.');
                this.startPolling();
            }
        }, 5000);
    }

    /**
     * Fetch dashboard data from API
     */
    fetchDashboardData() {
        fetch('/api/dashboard/data')
            .then(response => response.json())
            .then(data => {
                this.processApiData(data);
                this.showLoadingIndicator(false);
            })
            .catch(error => {
                console.error('Error fetching dashboard data:', error);
                this.showLoadingIndicator(false);
                this.showErrorMessage('Failed to load dashboard data');
            });
    }

    /**
     * Process API data and update dashboard
     */
    processApiData(apiData) {
        // Update data cache
        for (const domain in apiData.data) {
            if (apiData.data[domain].length > 0) {
                this.dataCache[domain] = apiData.data[domain];
            }
        }
        
        // Update system health indicators
        this.updateSystemHealth(apiData.health);
        
        // Update visualizations
        this.updateVisualizations();
    }

    /**
     * Handle real-time data update
     */
    handleDataUpdate(updateData) {
        const dataType = updateData.type;
        const data = updateData.data;
        
        if (dataType === 'system_metrics') {
            // Update system health indicators
            this.updateSystemHealth(data.health);
        } else if (dataType === 'processed_data') {
            // Add to appropriate domain cache
            const source = data.source || 'unknown';
            if (this.dataCache[source]) {
                this.dataCache[source].push(data);
                
                // Keep cache size reasonable
                if (this.dataCache[source].length > 100) {
                    this.dataCache[source] = this.dataCache[source].slice(-100);
                }
                
                // Update visualizations
                this.updateDomainVisualizations(source);
            }
        }
    }

    /**
     * Handle alert notification
     */
    handleAlertNotification(alertData) {
        // Create alert element
        this.addAlertToDisplay(alertData);
        
        // Play notification sound if enabled
        this.playNotificationSound();
    }

    /**
     * Add alert to alerts display
     */
    addAlertToDisplay(alertData) {
        const alertsContainer = document.getElementById('alertsContainer');
        if (!alertsContainer) return;
        
        // Create alert element
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${this.getAlertClass(alertData.level)} alert-dismissible fade show`;
        alertElement.setAttribute('role', 'alert');
        
        // Create alert content
        alertElement.innerHTML = `
            <strong>${alertData.type}:</strong> ${alertData.message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Add to container
        alertsContainer.prepend(alertElement);
        
        // Remove after 30 seconds
        setTimeout(() => {
            alertElement.classList.remove('show');
            setTimeout(() => alertElement.remove(), 500);
        }, 30000);
    }

    /**
     * Map alert level to Bootstrap class
     */
    getAlertClass(level) {
        switch (level) {
            case 'critical': return 'danger';
            case 'warning': return 'warning';
            case 'info': return 'info';
            default: return 'secondary';
        }
    }

    /**
     * Play notification sound
     */
    playNotificationSound() {
        // Check if notifications are enabled
        const notificationsEnabled = document.getElementById('notificationsToggle')?.checked;
        if (!notificationsEnabled) return;
        
        // Create and play audio element
        const audio = new Audio('/static/audio/notification.mp3');
        audio.play().catch(e => console.log('Error playing notification sound:', e));
    }

    /**
     * Update system health indicators
     */
    updateSystemHealth(healthData) {
        if (!healthData) return;
        
        // Update uptime
        const uptimeElement = document.getElementById('systemUptime');
        if (uptimeElement && healthData.uptime_seconds) {
            const uptime = this.formatUptime(healthData.uptime_seconds);
            uptimeElement.textContent = uptime;
        }
        
        // Update processing rate
        const processingRateElement = document.getElementById('processingRate');
        if (processingRateElement && healthData.processing_rate !== undefined) {
            processingRateElement.textContent = `${healthData.processing_rate.toFixed(2)} items/sec`;
        }
        
        // Update component counts
        const componentsElement = document.getElementById('componentCount');
        if (componentsElement && healthData.component_counts) {
            const total = Object.values(healthData.component_counts).reduce((a, b) => a + b, 0);
            componentsElement.textContent = total;
        }
        
        // Update queue sizes
        const queueElement = document.getElementById('queueSize');
        if (queueElement && healthData.queue_sizes) {
            const total = Object.values(healthData.queue_sizes).reduce((a, b) => a + b, 0);
            queueElement.textContent = total;
        }
    }

    /**
     * Format uptime seconds into human-readable string
     */
    formatUptime(seconds) {
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        
        if (days > 0) {
            return `${days}d ${hours}h ${minutes}m`;
        } else if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else {
            return `${minutes}m ${Math.floor(seconds % 60)}s`;
        }
    }

    /**
     * Update all visualizations
     */
    updateVisualizations() {
        // Update domain-specific visualizations
        for (const domain in this.dataCache) {
            this.updateDomainVisualizations(domain);
        }
        
        // Update cross-domain visualizations
        this.updateCrossDomainVisualizations();
    }

    /**
     * Update visualizations for a specific domain
     */
    updateDomainVisualizations(domain) {
        const data = this.dataCache[domain];
        if (!data || data.length === 0) return;
        
        // Get domain container
        const container = document.querySelector(`[data-domain="${domain}"]`);
        if (!container) return;
        
        // Update charts in this container
        this.updateChartsInContainer(container, domain, data);
    }

    /**
     * Update cross-domain visualizations
     */
    updateCrossDomainVisualizations() {
        const crossDomainData = this.dataCache['cross-domain'];
        if (!crossDomainData) return;
        
        // Get cross-domain container
        const container = document.querySelector('[data-domain="cross-domain"]');
        if (!container) return;
        
        // Update correlation matrix or heatmap
        if (crossDomainData.heatmap_data) {
            this.updateCorrelationHeatmap(container, crossDomainData.heatmap_data);
        }
        
        // Update network graph if data is available
        if (crossDomainData.network_data) {
            this.updateCorrelationNetwork(container, crossDomainData.network_data);
        }
        
        // Update cross-domain insights
        if (crossDomainData.insights) {
            this.updateCrossDomainInsights(container, crossDomainData.insights);
        }
    }

    /**
     * Update charts in a container
     */
    updateChartsInContainer(container, domain, data) {
        // Find all chart containers in this domain
        const chartContainers = container.querySelectorAll('[data-chart]');
        
        chartContainers.forEach(chartContainer => {
            const chartType = chartContainer.getAttribute('data-chart');
            const chartId = chartContainer.id;
            
            // Create or update chart based on type
            switch (chartType) {
                case 'time-series':
                    this.updateTimeSeriesChart(chartId, domain, data);
                    break;
                case 'gauge':
                    this.updateGaugeChart(chartId, domain, data);
                    break;
                case 'bar':
                    this.updateBarChart(chartId, domain, data);
                    break;
                case 'map':
                    this.updateMapVisualization(chartId, domain, data);
                    break;
                default:
                    console.log(`Unknown chart type: ${chartType}`);
            }
        });
    }

    /**
     * Refresh charts in a container (when tab becomes visible)
     */
    refreshChartsInContainer(container) {
        // Find all chart instances in this container
        const chartContainers = container.querySelectorAll('[data-chart]');
        
        chartContainers.forEach(chartContainer => {
            const chartId = chartContainer.id;
            if (this.chartInstances[chartId]) {
                this.chartInstances[chartId].reflow();
            }
        });
    }

    /**
     * Update time series chart
     */
    updateTimeSeriesChart(chartId, domain, data) {
        // Extract time series data based on domain
        let seriesData = [];
        let title = '';
        
        if (domain === 'weather') {
            seriesData = this.extractWeatherTimeSeries(data);
            title = 'Weather Trends';
        } else if (domain === 'economic') {
            seriesData = this.extractEconomicTimeSeries(data);
            title = 'Economic Indicators';
        } else if (domain === 'transportation') {
            seriesData = this.extractTransportationTimeSeries(data);
            title = 'Transportation Metrics';
        } else if (domain === 'social-media') {
            seriesData = this.extractSocialMediaTimeSeries(data);
            title = 'Social Media Trends';
        }
        
        // Create or update chart
        if (this.chartInstances[chartId]) {
            // Update existing chart
            const chart = this.chartInstances[chartId];
            
            // Update series data
            seriesData.forEach((series, index) => {
                if (chart.series[index]) {
                    chart.series[index].setData(series.data, false);
                } else {
                    chart.addSeries(series, false);
                }
            });
            
            // Remove extra series
            while (chart.series.length > seriesData.length) {
                chart.series[chart.series.length - 1].remove(false);
            }
            
            chart.redraw();
        } else {
            // Create new chart
            this.chartInstances[chartId] = Highcharts.chart(chartId, {
                chart: {
                    type: 'line',
                    animation: true,
                    style: {
                        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
                    }
                },
                time: {
                    useUTC: false
                },
                title: {
                    text: title
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: 'Time'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Value'
                    }
                },
                tooltip: {
                    shared: true,
                    crosshairs: true
                },
                plotOptions: {
                    series: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                series: seriesData,
                responsive: {
                    rules: [{
                        condition: {
                            maxWidth: 500
                        },
                        chartOptions: {
                            legend: {
                                layout: 'horizontal',
                                align: 'center',
                                verticalAlign: 'bottom'
                            }
                        }
                    }]
                }
            });
        }
    }

    /**
     * Update gauge chart
     */
    updateGaugeChart(chartId, domain, data) {
        // Extract gauge data based on domain
        let gaugeData = 0;
        let title = '';
        let min = 0;
        let max = 100;
        
        if (domain === 'weather') {
            gaugeData = this.extractWeatherGaugeData(data);
            title = 'Current Temperature';
            min = -20;
            max = 40;
        } else if (domain === 'economic') {
            gaugeData = this.extractEconomicGaugeData(data);
            title = 'Economic Health';
        } else if (domain === 'transportation') {
            gaugeData = this.extractTransportationGaugeData(data);
            title = 'Congestion Level';
            max = 1;
        } else if (domain === 'social-media') {
            gaugeData = this.extractSocialMediaGaugeData(data);
            title = 'Sentiment Index';
            min = -1;
            max = 1;
        }
        
        // Create or update chart
        if (this.chartInstances[chartId]) {
            // Update existing chart
            const point = this.chartInstances[chartId].series[0].points[0];
            point.update(gaugeData);
        } else {
            // Create new chart
            this.chartInstances[chartId] = Highcharts.chart(chartId, {
                chart: {
                    type: 'gauge',
                    plotBackgroundColor: null,
                    plotBackgroundImage: null,
                    plotBorderWidth: 0,
                    plotShadow: false,
                    height: '80%'
                },
                title: {
                    text: title
                },
                pane: {
                    startAngle: -150,
                    endAngle: 150,
                    background: [{
                        backgroundColor: {
                            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                            stops: [
                                [0, '#FFF'],
                                [1, '#333']
                            ]
                        },
                        borderWidth: 0,
                        outerRadius: '109%'
                    }, {
                        backgroundColor: {
                            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                            stops: [
                                [0, '#333'],
                                [1, '#FFF']
                            ]
                        },
                        borderWidth: 1,
                        outerRadius: '107%'
                    }, {
                        // default background
                    }, {
                        backgroundColor: '#DDD',
                        borderWidth: 0,
                        outerRadius: '105%',
                        innerRadius: '103%'
                    }]
                },
                yAxis: {
                    min: min,
                    max: max,
                    minorTickInterval: 'auto',
                    minorTickWidth: 1,
                    minorTickLength: 10,
                    minorTickPosition: 'inside',
                    minorTickColor: '#666',
                    tickPixelInterval: 30,
                    tickWidth: 2,
                    tickPosition: 'inside',
                    tickLength: 10,
                    tickColor: '#666',
                    labels: {
                        step: 2,
                        rotation: 'auto'
                    },
                    title: {
                        text: ''
                    },
                    plotBands: this.getGaugePlotBands(domain, min, max)
                },
                series: [{
                    name: title,
                    data: [gaugeData],
                    tooltip: {
                        valueSuffix: this.getGaugeValueSuffix(domain)
                    }
                }]
            });
        }
    }

    /**
     * Update bar chart
     */
    updateBarChart(chartId, domain, data) {
        // Extract bar chart data based on domain
        let categories = [];
        let seriesData = [];
        let title = '';
        
        if (domain === 'weather') {
            [categories, seriesData] = this.extractWeatherBarData(data);
            title = 'Weather Comparison';
        } else if (domain === 'economic') {
            [categories, seriesData] = this.extractEconomicBarData(data);
            title = 'Economic Indicators';
        } else if (domain === 'transportation') {
            [categories, seriesData] = this.extractTransportationBarData(data);
            title = 'Transportation Metrics';
        } else if (domain === 'social-media') {
            [categories, seriesData] = this.extractSocialMediaBarData(data);
            title = 'Social Media Engagement';
        }
        
        // Create or update chart
        if (this.chartInstances[chartId]) {
            // Update existing chart
            const chart = this.chartInstances[chartId];
            
            // Update categories
            chart.xAxis[0].setCategories(categories);
            
            // Update series data
            seriesData.forEach((series, index) => {
                if (chart.series[index]) {
                    chart.series[index].setData(series.data, false);
                } else {
                    chart.addSeries(series, false);
                }
            });
            
            // Remove extra series
            while (chart.series.length > seriesData.length) {
                chart.series[chart.series.length - 1].remove(false);
            }
            
            chart.redraw();
        } else {
            // Create new chart
            this.chartInstances[chartId] = Highcharts.chart(chartId, {
                chart: {
                    type: 'column'
                },
                title: {
                    text: title
                },
                xAxis: {
                    categories: categories
                },
                yAxis: {
                    title: {
                        text: 'Value'
                    }
                },
                tooltip: {
                    shared: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: seriesData
            });
        }
    }

    /**
     * Update map visualization
     */
    updateMapVisualization(chartId, domain, data) {
        // Implementation depends on the mapping library you choose
        // This is a placeholder for map visualization
        console.log(`Map visualization for ${domain} would be updated here`);
    }

    /**
     * Update correlation heatmap
     */
    updateCorrelationHeatmap(container, heatmapData) {
        // Find correlation heatmap container
        const chartContainer = container.querySelector('[data-chart="correlation-heatmap"]');
        if (!chartContainer) return;
        
        const chartId = chartContainer.id;
        
        // Get the first heatmap dataset if available
        if (!heatmapData || heatmapData.length === 0) return;
        
        const dataset = heatmapData[0];
        if (!dataset || !dataset.data) return;
        
        // Get x and y categories from the dataset
        const xCategories = [];
        const yCategories = [];
        const formattedData = [];
        
        // Extract categories and format data for the heatmap
        dataset.data.forEach(item => {
            if (!xCategories.includes(item.x)) {
                xCategories.push(item.x);
            }
            
            if (!yCategories.includes(item.y)) {
                yCategories.push(item.y);
            }
        });
        
        // Format data as [x_index, y_index, value]
        dataset.data.forEach(item => {
            const xIndex = xCategories.indexOf(item.x);
            const yIndex = yCategories.indexOf(item.y);
            formattedData.push([xIndex, yIndex, item.value]);
        });
        
        const title = dataset.domain_pair ? 
            `Correlation: ${dataset.domain_pair.replace('_vs_', ' vs ')}` : 
            'Cross-Domain Correlations';
        
        // Create or update chart
        if (this.chartInstances[chartId]) {
            // Update existing chart
            const chart = this.chartInstances[chartId];
            chart.update({
                title: {
                    text: title
                },
                xAxis: {
                    categories: xCategories
                },
                yAxis: {
                    categories: yCategories
                },
                series: [{
                    data: formattedData
                }]
            });
        } else {
            // Create new chart
            this.chartInstances[chartId] = Highcharts.chart(chartId, {
                chart: {
                    type: 'heatmap',
                    marginTop: 40,
                    marginBottom: 80,
                    plotBorderWidth: 1
                },
                title: {
                    text: title
                },
                xAxis: {
                    categories: xCategories
                },
                yAxis: {
                    categories: yCategories,
                    title: null
                },
                colorAxis: {
                    min: -1,
                    max: 1,
                    stops: [
                        [0, '#c4463a'],   // Red for negative correlation
                        [0.5, '#fffbbc'], // Yellow for no correlation
                        [1, '#3060cf']    // Blue for positive correlation
                    ]
                },
                legend: {
                    align: 'right',
                    layout: 'vertical',
                    margin: 0,
                    verticalAlign: 'top',
                    y: 25,
                    symbolHeight: 280
                },
                tooltip: {
                    formatter: function () {
                        return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> and <b>' +
                            this.series.yAxis.categories[this.point.y] + '</b><br>' +
                            'Correlation: <b>' + this.point.value.toFixed(2) + '</b>';
                    }
                },
                series: [{
                    name: 'Correlation',
                    borderWidth: 1,
                    data: formattedData,
                    dataLabels: {
                        enabled: true,
                        color: '#000000',
                        format: '{point.value:.2f}'
                    }
                }]
            });
        }
    }
    
    /**
     * Update correlation network
     */
    updateCorrelationNetwork(container, networkData) {
        // Find correlation network container
        const chartContainer = container.querySelector('[data-chart="correlation-network"]');
        if (!chartContainer) return;
        
        // Clear previous network
        chartContainer.innerHTML = '';
        
        // Check if we have valid network data
        if (!networkData.nodes || !networkData.links || networkData.nodes.length === 0) {
            chartContainer.innerHTML = '<div class="alert alert-info">No correlation network data available</div>';
            return;
        }
        
        // Set up SVG
        const width = chartContainer.clientWidth;
        const height = 500;
        
        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width)
            .attr('height', height);
        
        // Define the forces
        const simulation = d3.forceSimulation(networkData.nodes)
            .force('link', d3.forceLink(networkData.links).id(d => d.id))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2));
        
        // Add domain group colors
        const color = d3.scaleOrdinal(d3.schemeCategory10);
        
        // Create links
        const link = svg.append('g')
            .selectAll('line')
            .data(networkData.links)
            .enter().append('line')
            .attr('stroke-width', d => Math.max(1, d.value * 3))
            .attr('stroke', d => d.direction === 'positive' ? '#3060cf' : '#c4463a')
            .attr('stroke-opacity', 0.6);
        
        // Create nodes
        const node = svg.append('g')
            .selectAll('circle')
            .data(networkData.nodes)
            .enter().append('circle')
            .attr('r', 8)
            .attr('fill', d => color(d.group))
            .call(d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended));
        
        // Add labels
        const label = svg.append('g')
            .selectAll('text')
            .data(networkData.nodes)
            .enter().append('text')
            .text(d => d.id.split(':')[1] || d.id) // Show only variable name if possible
            .attr('font-size', 10)
            .attr('dx', 12)
            .attr('dy', '.35em');
        
        // Set up tick function
        simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node
                .attr('cx', d => d.x)
                .attr('cy', d => d.y);
            
            label
                .attr('x', d => d.x)
                .attr('y', d => d.y);
        });
        
        // Drag functions
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    }

    /**
     * Update cross-domain insights
     */
    updateCrossDomainInsights(container, insights) {
        // Find insights container
        const insightsContainer = container.querySelector('[data-content="insights"]');
        if (!insightsContainer) return;
        
        // Check if we have valid insights
        if (!insights || insights.length === 0) {
            insightsContainer.innerHTML = '<div class="alert alert-info">No correlation insights available yet</div>';
            return;
        }
        
        // Update insights container
        insightsContainer.innerHTML = '';
        
        // Add each insight
        insights.forEach(insight => {
            const insightElement = document.createElement('div');
            insightElement.className = 'card mb-3';
            
            // Create card header
            const header = document.createElement('div');
            header.className = 'card-header';
            
            // Set header content
            if (insight.domain1 && insight.domain2) {
                header.textContent = `${insight.domain1.toUpperCase()} ↔ ${insight.domain2.toUpperCase()}`;
            } else if (insight.title) {
                header.textContent = insight.title;
            } else {
                header.textContent = 'Correlation Insight';
            }
            
            // Create card body
            const body = document.createElement('div');
            body.className = 'card-body';
            
            // Add description
            const description = document.createElement('p');
            description.className = 'card-text';
            description.textContent = insight.description;
            body.appendChild(description);
            
            // Add details if available
            if (insight.correlation_value !== undefined) {
                const details = document.createElement('ul');
                details.className = 'list-group list-group-flush mt-2';
                
                const correlationItem = document.createElement('li');
                correlationItem.className = 'list-group-item';
                correlationItem.innerHTML = `<strong>Correlation:</strong> ${insight.correlation_value.toFixed(2)}`;
                details.appendChild(correlationItem);
                
                if (insight.variable1 && insight.variable2) {
                    const variablesItem = document.createElement('li');
                    variablesItem.className = 'list-group-item';
                    variablesItem.innerHTML = `<strong>Variables:</strong> ${insight.variable1} & ${insight.variable2}`;
                    details.appendChild(variablesItem);
                }
                
                body.appendChild(details);
            }
            
            // Add timestamp if available
            if (insight.timestamp) {
                const timestamp = document.createElement('small');
                timestamp.className = 'text-muted d-block mt-2';
                timestamp.textContent = new Date(insight.timestamp).toLocaleString();
                body.appendChild(timestamp);
            }
            
            // Assemble card
            insightElement.appendChild(header);
            insightElement.appendChild(body);
            
            // Add to container
            insightsContainer.appendChild(insightElement);
        });
    }

    /**
     * Extract weather time series data
     */
    extractWeatherTimeSeries(data) {
        // Find weather forecasts
        const temperatureSeries = {
            name: 'Temperature',
            data: []
        };
        
        const humiditySeries = {
            name: 'Humidity',
            data: [],
            yAxis: 1
        };
        
        // Process weather data
        data.forEach(item => {
            if (item.predictions && item.predictions.length) {
                item.predictions.forEach(prediction => {
                    if (prediction.timestamp && prediction.temperature) {
                        const timestamp = new Date(prediction.timestamp).getTime();
                        temperatureSeries.data.push([timestamp, prediction.temperature]);
                    }
                });
            }
            
            if (item.original && item.original.current) {
                const current = item.original.current;
                if (current.temp) {
                    const timestamp = new Date().getTime();
                    temperatureSeries.data.push([timestamp, current.temp]);
                }
                
                if (current.humidity) {
                    const timestamp = new Date().getTime();
                    humiditySeries.data.push([timestamp, current.humidity]);
                }
            }
        });
        
        // Sort by timestamp
        temperatureSeries.data.sort((a, b) => a[0] - b[0]);
        humiditySeries.data.sort((a, b) => a[0] - b[0]);
        
        return [temperatureSeries, humiditySeries];
    }

    /**
     * Extract economic time series data
     */
    extractEconomicTimeSeries(data) {
        // Example: return empty series
        return [{
            name: 'GDP Growth',
            data: []
        }, {
            name: 'Inflation',
            data: []
        }];
    }

    /**
     * Extract transportation time series data
     */
    extractTransportationTimeSeries(data) {
        // Example: return empty series
        return [{
            name: 'Congestion',
            data: []
        }, {
            name: 'Avg Speed',
            data: []
        }];
    }

    /**
     * Extract social media time series data
     */
    extractSocialMediaTimeSeries(data) {
        // Example: return empty series
        return [{
            name: 'Positive Sentiment',
            data: []
        }, {
            name: 'Negative Sentiment',
            data: []
        }];
    }

    /**
     * Extract weather gauge data
     */
    extractWeatherGaugeData(data) {
        // Find latest temperature
        for (let i = data.length - 1; i >= 0; i--) {
            const item = data[i];
            if (item.original && item.original.current && item.original.current.temp) {
                return item.original.current.temp;
            }
        }
        
        return 20; // Default
    }

    /**
     * Extract economic gauge data
     */
    extractEconomicGaugeData(data) {
        // Example: return dummy value
        return 50;
    }

    /**
     * Extract transportation gauge data
     */
    extractTransportationGaugeData(data) {
        // Example: return dummy value
        return 0.4;
    }

    /**
     * Extract social media gauge data
     */
    extractSocialMediaGaugeData(data) {
        // Example: return dummy value
        return 0.2;
    }

    /**
     * Extract weather bar data
     */
    extractWeatherBarData(data) {
        // Example: return dummy data
        const categories = ['Location A', 'Location B', 'Location C'];
        const series = [{
            name: 'Temperature',
            data: [20, 15, 25]
        }];
        
        return [categories, series];
    }

    /**
     * Extract economic bar data
     */
    extractEconomicBarData(data) {
        // Example: return dummy data
        const categories = ['GDP', 'Inflation', 'Interest Rate'];
        const series = [{
            name: 'Current',
            data: [2.5, 2.0, 3.0]
        }];
        
        return [categories, series];
    }

    /**
     * Extract transportation bar data
     */
    extractTransportationBarData(data) {
        // Example: return dummy data
        const categories = ['Morning', 'Afternoon', 'Evening'];
        const series = [{
            name: 'Congestion',
            data: [0.7, 0.5, 0.8]
        }];
        
        return [categories, series];
    }

    /**
     * Extract social media bar data
     */
    extractSocialMediaBarData(data) {
        // Example: return dummy data
        const categories = ['Twitter', 'Facebook', 'Instagram'];
        const series = [{
            name: 'Engagement',
            data: [500, 300, 800]
        }];
        
        return [categories, series];
    }

    /**
     * Extract correlation data from cross-domain data
     */
    extractCorrelationData(data) {
        // Look for correlation data
        for (let i = data.length - 1; i >= 0; i--) {
            const item = data[i];
            
            if (item.correlations && item.domains) {
                const domains = item.domains;
                const matrix = [];
                
                // Create matrix data for heatmap
                for (let i = 0; i < domains.length; i++) {
                    for (let j = 0; j < domains.length; j++) {
                        let value = 0;
                        
                        // Find correlation between these domains
                        if (i !== j) {
                            for (const correlation of item.correlations) {
                                if (correlation.domains.includes(domains[i]) && 
                                    correlation.domains.includes(domains[j])) {
                                    value = correlation.correlation;
                                    break;
                                }
                            }
                        }
                        
                        matrix.push([i, j, value]);
                    }
                }
                
                return {
                    domains: domains,
                    data: matrix
                };
            }
        }
        
        // Default empty result
        return {
            domains: [],
            data: []
        };
    }

    /**
     * Extract cross-domain insights
     */
    extractCrossDomainInsights(data) {
        // Look for insights
        for (let i = data.length - 1; i >= 0; i--) {
            const item = data[i];
            
            if (item.predictions && item.predictions.key_insights) {
                return item.predictions.key_insights;
            }
        }
        
        return [];
    }

    /**
     * Get gauge plot bands based on domain
     */
    getGaugePlotBands(domain, min, max) {
        if (domain === 'weather') {
            return [
                {
                    from: min,
                    to: 0,
                    color: '#8AD8FF',
                    innerRadius: '105%',
                    outerRadius: '150%'
                },
                {
                    from: 0,
                    to: 25,
                    color: '#AEFF8A',
                    innerRadius: '105%',
                    outerRadius: '150%'
                },
                {
                    from: 25,
                    to: max,
                    color: '#FF8A8A',
                    innerRadius: '105%',
                    outerRadius: '150%'
                }
            ];
        } else if (domain === 'transportation') {
            return [
                {
                    from: 0,
                    to: 0.4,
                    color: '#C6F6BE',
                    innerRadius: '105%',
                    outerRadius: '150%'
                },
                {
                    from: 0.4,
                    to: 0.7,
                    color: '#FEFEC0',
                    innerRadius: '105%',
                    outerRadius: '150%'
                },
                {
                    from: 0.7,
                    to: max,
                    color: '#FFC1BE',
                    innerRadius: '105%',
                    outerRadius: '150%'
                }
            ];
        }
        
        // Default
        return [
            {
                from: min,
                to: min + (max - min) / 3,
                color: '#DF5353',
                innerRadius: '105%',
                outerRadius: '150%'
            },
            {
                from: min + (max - min) / 3,
                to: min + 2 * (max - min) / 3,
                color: '#DDDF0D',
                innerRadius: '105%',
                outerRadius: '150%'
            },
            {
                from: min + 2 * (max - min) / 3,
                to: max,
                color: '#55BF3B',
                innerRadius: '105%',
                outerRadius: '150%'
            }
        ];
    }

    /**
     * Get gauge value suffix based on domain
     */
    getGaugeValueSuffix(domain) {
        if (domain === 'weather') {
            return ' °C';
        } else if (domain === 'economic') {
            return ' %';
        } else if (domain === 'transportation') {
            return '';
        } else if (domain === 'social-media') {
            return '';
        }
        
        return '';
    }

    /**
     * Show/hide loading indicator
     */
    showLoadingIndicator(show) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'flex' : 'none';
        }
    }

    /**
     * Show error message
     */
    showErrorMessage(message) {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.textContent = message;
            errorContainer.style.display = 'block';
            
            // Hide after 5 seconds
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 5000);
        }
    }

    /**
     * Update time range for visualizations
     */
    updateTimeRange(range) {
        console.log(`Time range changed to: ${range}`);
        // Implementation depends on how you want to filter data by time range
    }
    
    /**
     * Handle correlation data update
     */
    handleCorrelationDataUpdate(data) {
        console.log('Processing correlation data update:', data);
        
        // Skip if no data
        if (!data || !data.data) {
            console.log('No correlation data to process');
            return;
        }
        
        // Update cross-domain data cache
        if (!this.dataCache['cross-domain']) {
            this.dataCache['cross-domain'] = [];
        }
        
        // Add to cache or update existing
        this.dataCache['cross-domain'].push(data.data);
        
        // Keep cache size reasonable
        if (this.dataCache['cross-domain'].length > 10) {
            this.dataCache['cross-domain'] = this.dataCache['cross-domain'].slice(-10);
        }
        
        // Update cross-domain visualizations
        this.updateCrossDomainVisualizations();
    }
    
    /**
     * Handle correlation insight
     */
    handleCorrelationInsight(insight) {
        console.log('Processing correlation insight:', insight);
        
        // Skip if no insight
        if (!insight || !insight.data) {
            console.log('No correlation insight to process');
            return;
        }
        
        // Update cross-domain insights
        if (!this.dataCache['cross-domain']) {
            this.dataCache['cross-domain'] = [];
        }
        
        // Add insights to dataCache
        if (!this.dataCache['cross-domain'].insights) {
            this.dataCache['cross-domain'].insights = [];
        }
        
        // Add new insights
        if (Array.isArray(insight.data)) {
            this.dataCache['cross-domain'].insights = insight.data;
        } else {
            this.dataCache['cross-domain'].insights.push(insight.data);
            
            // Keep insights at a reasonable size
            if (this.dataCache['cross-domain'].insights.length > 10) {
                this.dataCache['cross-domain'].insights = this.dataCache['cross-domain'].insights.slice(-10);
            }
        }
        
        // Update cross-domain visualizations
        this.updateCrossDomainVisualizations();
    }
    
    /**
     * Handle correlation anomaly
     */
    handleCorrelationAnomaly(anomaly) {
        console.log('Processing correlation anomaly:', anomaly);
        
        // Skip if no anomaly
        if (!anomaly || !anomaly.data) {
            console.log('No correlation anomaly to process');
            return;
        }
        
        // Create alert for anomaly
        this.handleAlertNotification({
            type: 'correlation_anomaly',
            level: anomaly.data.severity || 'warning',
            message: anomaly.data.description || 'Correlation anomaly detected',
            data: anomaly.data
        });
        
        // Update cross-domain data
        if (!this.dataCache['cross-domain']) {
            this.dataCache['cross-domain'] = [];
        }
        
        // Add anomaly to dataCache
        if (!this.dataCache['cross-domain'].anomalies) {
            this.dataCache['cross-domain'].anomalies = [];
        }
        
        this.dataCache['cross-domain'].anomalies.push(anomaly.data);
        
        // Keep anomalies at a reasonable size
        if (this.dataCache['cross-domain'].anomalies.length > 10) {
            this.dataCache['cross-domain'].anomalies = this.dataCache['cross-domain'].anomalies.slice(-10);
        }
        
        // Update cross-domain visualizations
        this.updateCrossDomainVisualizations();
    }

    /**
     * Retry WebSocket connection with exponential backoff
     */
    retryConnection() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
        }
        
        // Start with 1 second, then double each time, up to 30 seconds
        if (!this.reconnectDelay) {
            this.reconnectDelay = 1000;
        } else {
            this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
        }
        
        console.log(`Attempting to reconnect in ${this.reconnectDelay/1000} seconds...`);
        
        this.reconnectTimer = setTimeout(() => {
            console.log('Attempting to reconnect...');
            
            // Force disconnect and reconnect
            if (this.socket) {
                this.socket.disconnect();
                this.socket.connect();
            } else {
                // If socket doesn't exist for some reason, create a new one
                this.socket = io('/system-updates');
                this.initializeEventHandlers();
            }
        }, this.reconnectDelay);
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Highcharts global options
    Highcharts.setOptions({
        colors: ['#058DC7', '#50B432', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
        chart: {
            style: {
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
            }
        },
        credits: {
            enabled: false
        }
    });
    
    // Create dashboard controller
    window.dashboardController = new DashboardController();
});