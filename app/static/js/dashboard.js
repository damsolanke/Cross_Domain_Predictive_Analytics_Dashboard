/**
 * Cross-Domain Predictive Analytics Dashboard
 * Main dashboard JavaScript for loading and rendering dashboard components
 */

// Dashboard state
const dashboardState = {
    isLoading: false,
    lastUpdated: null,
    dataCache: {},
    components: []
};

// Configuration
const config = {
    apiEndpoints: {
        dashboardData: '/api/dashboard-data',
        correlations: '/api/correlations',
        systemStatus: '/api/system-status'
    },
    refreshInterval: 30000, // 30 seconds
    cacheExpiry: 60000, // 60 seconds
};

/**
 * Initialize the dashboard
 */
function initDashboard() {
    console.log('Initializing dashboard...');
    
    // Register components to be loaded
    registerComponents();
    
    // Set up loading indicator
    setupLoadingIndicator();
    
    // Load core components first (lazy loading)
    loadCoreComponents().then(() => {
        // Then load data for those components
        loadDashboardData().then(() => {
            // Finally, load secondary components
            loadSecondaryComponents();
        });
    });
    
    // Set up refresh interval
    setupRefreshInterval();
    
    // Set up socket connections for real-time updates
    setupSocketConnections();
}

/**
 * Register dashboard components
 */
function registerComponents() {
    dashboardState.components = [
        { id: 'weather-widget', priority: 'core', loaded: false },
        { id: 'economic-indicators', priority: 'core', loaded: false },
        { id: 'transportation-status', priority: 'core', loaded: false },
        { id: 'social-media-trends', priority: 'core', loaded: false },
        { id: 'correlation-insights', priority: 'secondary', loaded: false },
        { id: 'system-health', priority: 'secondary', loaded: false }
    ];
}

/**
 * Set up loading indicator
 */
function setupLoadingIndicator() {
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        // Show initially
        loadingIndicator.style.display = 'block';
        
        // Update loading state
        dashboardState.isLoading = true;
    }
}

/**
 * Load core dashboard components
 */
async function loadCoreComponents() {
    console.log('Loading core components...');
    
    const coreComponents = dashboardState.components.filter(comp => comp.priority === 'core');
    const startTime = performance.now();
    
    // Create empty component containers first
    for (const component of coreComponents) {
        const elem = document.getElementById(component.id);
        if (elem) {
            elem.innerHTML = '<div class="component-loading">Loading component...</div>';
        }
    }
    
    // Stagger loading to improve responsiveness
    let delay = 0;
    const loadPromises = coreComponents.map(component => {
        return new Promise(resolve => {
            setTimeout(() => {
                const elem = document.getElementById(component.id);
                if (elem) {
                    // Set up a placeholder with appropriate height to avoid layout shifts
                    elem.innerHTML = `
                        <div class="card">
                            <div class="card-header">
                                <h5 class="card-title">${getComponentTitle(component.id)}</h5>
                            </div>
                            <div class="card-body">
                                <div class="d-flex justify-content-center align-items-center" style="height: 200px;">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Loading...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    component.loaded = true;
                }
                resolve();
            }, delay);
            delay += 50; // 50ms delay between components
        });
    });
    
    await Promise.all(loadPromises);
    
    const loadTime = Math.round(performance.now() - startTime);
    console.log(`Core components loaded in ${loadTime}ms`);
}

/**
 * Get component title based on its ID
 */
function getComponentTitle(id) {
    const titles = {
        'weather-widget': 'Weather Conditions',
        'economic-indicators': 'Economic Indicators',
        'transportation-status': 'Transportation Status',
        'social-media-trends': 'Social Media Trends',
        'correlation-insights': 'Correlation Insights',
        'system-health': 'System Health'
    };
    
    return titles[id] || 'Loading...';
}

/**
 * Load secondary dashboard components
 */
async function loadSecondaryComponents() {
    console.log('Loading secondary components...');
    
    const secondaryComponents = dashboardState.components.filter(comp => comp.priority === 'secondary');
    
    // Create loading placeholder for secondary components
    for (const component of secondaryComponents) {
        const elem = document.getElementById(component.id);
        if (elem) {
            elem.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h5 class="card-title">${getComponentTitle(component.id)}</h5>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-center align-items-center" style="height: 200px;">
                            <div class="spinner-border text-secondary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    // Load data for secondary components with a longer delay (async)
    // This allows the dashboard to be interactive while secondary components load
    setTimeout(() => {
        // Check if the page is still visible before loading secondary data
        if (document.visibilityState === 'visible') {
            loadSecondaryData().then(() => {
                secondaryComponents.forEach(comp => comp.loaded = true);
                console.log('Secondary components loaded');
            });
        } else {
            // If page is not visible (tab not active), delay loading further
            // This saves resources when the user isn't actively viewing the page
            console.log('Page not visible, delaying secondary component load');
            
            // Set up visibility change listener to load when page becomes visible
            document.addEventListener('visibilitychange', function onVisibilityChange() {
                if (document.visibilityState === 'visible') {
                    loadSecondaryData().then(() => {
                        secondaryComponents.forEach(comp => comp.loaded = true);
                        console.log('Secondary components loaded after visibility change');
                    });
                    document.removeEventListener('visibilitychange', onVisibilityChange);
                }
            });
        }
    }, 1500); // 1.5 second delay
}

/**
 * Load dashboard data from API
 */
async function loadDashboardData() {
    console.log('Loading dashboard data...');
    
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
    
    // Record start time to measure performance
    const startTime = performance.now();
    
    try {
        // Check cache first
        const now = new Date().getTime();
        if (dashboardState.dataCache.dashboardData && 
            (now - dashboardState.dataCache.dashboardData.timestamp) < config.cacheExpiry) {
            console.log('Using cached dashboard data');
            updateDashboardComponents(dashboardState.dataCache.dashboardData.data);
            
            // Hide loading indicator quickly when using cache
            if (loadingIndicator) {
                loadingIndicator.style.display = 'none';
            }
            
            dashboardState.isLoading = false;
            return;
        }
        
        // Fetch fresh data with timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
        
        try {
            console.log('Fetching fresh dashboard data...');
            const response = await fetch(config.apiEndpoints.dashboardData, {
                signal: controller.signal,
                headers: {
                    'Cache-Control': 'max-age=60'
                }
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Cache the data
            dashboardState.dataCache.dashboardData = {
                data: data,
                timestamp: now
            };
            
            // Calculate load time
            const loadTime = Math.round(performance.now() - startTime);
            console.log(`Dashboard data loaded in ${loadTime}ms`);
            
            // Update dashboard components with the data
            updateDashboardComponents(data);
            
            // Update last updated timestamp
            dashboardState.lastUpdated = now;
            updateLastUpdatedDisplay();
            
        } catch (fetchError) {
            clearTimeout(timeoutId);
            
            // If we have cached data, use it as fallback when fetch fails
            if (dashboardState.dataCache.dashboardData) {
                console.warn('Fetch failed, using cached data as fallback');
                updateDashboardComponents(dashboardState.dataCache.dashboardData.data);
            } else {
                throw fetchError;
            }
        }
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showErrorMessage('Failed to load dashboard data. Please try refreshing the page.');
    } finally {
        // Hide loading indicator
        if (loadingIndicator) {
            // Add a small delay before hiding to avoid flickering
            setTimeout(() => {
                loadingIndicator.style.display = 'none';
            }, 200);
        }
        
        dashboardState.isLoading = false;
        }
    }

    /**
 * Load data for secondary components
 */
async function loadSecondaryData() {
    console.log('Loading secondary data...');
    
    try {
        // Load correlation data
        const response = await fetch(config.apiEndpoints.correlations);
        const data = await response.json();
        
        // Update correlation insights
        updateCorrelationInsights(data);
        
        // Load system status
        const statusResponse = await fetch(config.apiEndpoints.systemStatus);
        const statusData = await statusResponse.json();
        
        // Update system health
        updateSystemHealth(statusData);
        
    } catch (error) {
        console.error('Error loading secondary data:', error);
    }
}

/**
 * Update dashboard components with data
 */
function updateDashboardComponents(data) {
    // Update weather widget
    updateWeatherWidget(data.weather);
    
    // Update economic indicators
    updateEconomicIndicators(data.economic);
    
    // Update transportation status
    updateTransportationStatus(data.transportation);
    
    // Update social media trends
    updateSocialMediaTrends(data.social_media);
}

/**
 * Update weather widget with data
 */
function updateWeatherWidget(weatherData) {
    const widget = document.getElementById('weather-widget');
    if (!widget) return;
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Weather Conditions</h5>
            </div>
            <div class="card-body">
                <div class="current-weather">
                    <h2>${weatherData.temperature}°F</h2>
                    <p>${weatherData.condition}</p>
                </div>
                <div class="forecast">
                    ${weatherData.forecast.map(day => `
                        <div class="forecast-day">
                            <div class="day">${day.day}</div>
                            <div class="high-low">${day.high}° / ${day.low}°</div>
                            <div class="condition">${day.condition}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

/**
 * Update economic indicators with data
 */
function updateEconomicIndicators(economicData) {
    const widget = document.getElementById('economic-indicators');
    if (!widget) return;
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Economic Indicators</h5>
            </div>
            <div class="card-body">
                <div class="market-index">
                    <h3>Market Index: ${economicData.market_index}</h3>
                    <span class="${economicData.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                        ${economicData.change_percent >= 0 ? '▲' : '▼'} ${Math.abs(economicData.change_percent)}%
                    </span>
                </div>
                <div class="indicators-list">
                    ${economicData.indicators.map(indicator => `
                        <div class="indicator-item">
                            <span class="indicator-name">${indicator.name}:</span>
                            <span class="indicator-value">${indicator.value}</span>
                            <span class="indicator-trend ${getTrendClass(indicator.trend)}">
                                ${getTrendIcon(indicator.trend)}
                            </span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

/**
 * Update transportation status with data
 */
function updateTransportationStatus(transportationData) {
    const widget = document.getElementById('transportation-status');
    if (!widget) return;
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Transportation Status</h5>
            </div>
            <div class="card-body">
                <div class="overall-status">
                    <div class="congestion">
                        <h4>Congestion Level</h4>
                        <div class="progress">
                            <div class="progress-bar ${getCongestionClass(transportationData.congestion_level)}" 
                                 role="progressbar" 
                                 style="width: ${transportationData.congestion_level}%" 
                                 aria-valuenow="${transportationData.congestion_level}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${transportationData.congestion_level}%
                            </div>
                        </div>
                    </div>
                    <div class="avg-speed">
                        <h4>Avg. Speed: ${transportationData.average_speed} mph</h4>
                    </div>
                </div>
                <div class="hotspots">
                    <h4>Traffic Hotspots</h4>
                    <ul class="list-group">
                        ${transportationData.hotspots.map(hotspot => `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                ${hotspot.location}
                                <span class="badge ${getCongestionClass(hotspot.level)} rounded-pill">
                                    ${hotspot.level}% ${getTrendIcon(hotspot.trend)}
                                </span>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
}

/**
 * Update social media trends with data
 */
function updateSocialMediaTrends(socialData) {
    const widget = document.getElementById('social-media-trends');
    if (!widget) return;
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Social Media Trends</h5>
            </div>
            <div class="card-body">
                <div class="sentiment">
                    <h4>Overall Sentiment: ${socialData.sentiment}%</h4>
                    <div class="progress">
                        <div class="progress-bar ${getSentimentClass(socialData.sentiment)}" 
                             role="progressbar" 
                             style="width: ${socialData.sentiment}%" 
                             aria-valuenow="${socialData.sentiment}" 
                             aria-valuemin="0" 
                             aria-valuemax="100">
                            ${socialData.sentiment}%
                        </div>
                    </div>
                </div>
                <div class="trending-topics">
                    <h4>Trending Topics</h4>
                    <ul class="list-group">
                        ${socialData.trending_topics.map(topic => `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                ${topic.topic}
                                <div>
                                    <span class="badge ${getSentimentClass(topic.sentiment)} rounded-pill me-2">
                                        ${topic.sentiment}%
                                    </span>
                                    <small class="text-muted">${formatNumber(topic.volume)} mentions</small>
                                </div>
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
}

/**
 * Update correlation insights
 */
function updateCorrelationInsights(data) {
    const widget = document.getElementById('correlation-insights');
    if (!widget) return;
    
    // If we don't have actual data, use placeholder
    if (!data || !data.correlations) {
        data = {
            correlations: [
                {factor1: 'Weather', factor2: 'Energy Demand', correlation: 0.85, strength: 'strong'},
                {factor1: 'Traffic', factor2: 'Air Quality', correlation: 0.72, strength: 'strong'},
                {factor1: 'Social Media', factor2: 'Consumer Behavior', correlation: 0.68, strength: 'moderate'}
            ]
        };
    }
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">Cross-Domain Correlations</h5>
            </div>
            <div class="card-body">
                <ul class="list-group">
                    ${data.correlations.map(corr => `
                        <li class="list-group-item">
                            <div class="d-flex justify-content-between">
                                <div>${corr.factor1} ↔ ${corr.factor2}</div>
                                <div>
                                    <span class="badge ${getCorrelationClass(corr.correlation)}">
                                        ${Math.abs(corr.correlation).toFixed(2)} ${corr.strength}
                                    </span>
                                </div>
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `;
}

/**
 * Update system health display
 */
function updateSystemHealth(data) {
    const widget = document.getElementById('system-health');
    if (!widget) return;
    
    // If we don't have actual data, use placeholder
    if (!data) {
        data = {
            status: 'healthy',
            uptime: 3600,
            processors: 4,
            data_sources: 5,
            queue_size: 0
        };
    }
    
    widget.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5 class="card-title">System Health</h5>
            </div>
            <div class="card-body">
                <div class="d-flex justify-content-between mb-3">
                    <div>Status:</div>
                    <div>
                        <span class="badge ${data.status === 'healthy' ? 'bg-success' : 'bg-warning'}">
                            ${data.status}
                        </span>
                    </div>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <div>Uptime:</div>
                    <div>${formatUptime(data.uptime)}</div>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <div>Components:</div>
                    <div>${data.processors}</div>
                </div>
                <div class="d-flex justify-content-between mb-2">
                    <div>Data Sources:</div>
                    <div>${data.data_sources}</div>
                </div>
                <div class="d-flex justify-content-between">
                    <div>Queue Size:</div>
                    <div>${data.queue_size}</div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Set up automatic refresh interval
 */
function setupRefreshInterval() {
    // Refresh data periodically
    setInterval(() => {
        if (!dashboardState.isLoading) {
            loadDashboardData();
        }
    }, config.refreshInterval);
}

/**
 * Set up SocketIO connections for real-time updates
 */
function setupSocketConnections() {
    // Check if SocketIO is available
    if (typeof io !== 'undefined') {
        console.log('Setting up Socket.IO connections...');
        
        // Use a short timeout to defer socket connection until after initial page load
        setTimeout(() => {
            // Connect to system-updates namespace with options
            const socket = io('/system-updates', {
                reconnectionAttempts: 5,        // Only try to reconnect 5 times
                reconnectionDelay: 1000,        // Start with 1 second delay
                reconnectionDelayMax: 10000,    // Maximum 10 second delay
                timeout: 20000,                 // Connection timeout
                autoConnect: true,              // Auto connect on initialization
                transports: ['websocket', 'polling'] // Prefer WebSocket
            });
            
            socket.on('connect', () => {
                console.log('Connected to system-updates socket');
                
                // Update connection status indicator
                const connectionStatus = document.getElementById('connectionStatus');
                if (connectionStatus) {
                    connectionStatus.className = 'badge bg-success me-2';
                    connectionStatus.textContent = 'Connected';
                }
                
                // Subscribe to various update types
                socket.emit('subscribe_to_updates', { update_type: 'all' });
            });
            
            socket.on('disconnect', () => {
                console.log('Disconnected from system-updates socket');
                
                // Update connection status indicator
                const connectionStatus = document.getElementById('connectionStatus');
                if (connectionStatus) {
                    connectionStatus.className = 'badge bg-danger me-2';
                    connectionStatus.textContent = 'Disconnected';
                }
            });
            
            socket.on('reconnect_attempt', (attemptNumber) => {
                console.log(`Attempting to reconnect (${attemptNumber})...`);
                
                // Update connection status indicator
                const connectionStatus = document.getElementById('connectionStatus');
                if (connectionStatus) {
                    connectionStatus.className = 'badge bg-warning me-2';
                    connectionStatus.textContent = 'Reconnecting...';
                }
            });
            
            // Listen for real-time updates
            socket.on('processed_data', (data) => {
                console.log('Received real-time data update');
                // Update relevant components without full page refresh
                updateComponentsWithRealtimeData(data);
            });
            
            socket.on('correlation_data', (data) => {
                console.log('Received correlation update');
                if (data.status === 'success') {
                    updateCorrelationInsights(data.data);
                }
            });
            
            socket.on('system_metrics', (data) => {
                console.log('Received system metrics update');
                updateSystemHealth(data);
            });
            
            socket.on('connect_error', (error) => {
                console.error('Socket connection error:', error);
                
                // Update connection status indicator
                const connectionStatus = document.getElementById('connectionStatus');
                if (connectionStatus) {
                    connectionStatus.className = 'badge bg-danger me-2';
                    connectionStatus.textContent = 'Connection Error';
                }
            });
            
            // Store socket reference in dashboardState
            dashboardState.socket = socket;
        }, 1000); // 1-second delay before establishing socket connection
        
    } else {
        console.log('Socket.IO not available, real-time updates disabled');
    }
}

/**
 * Update components with real-time data
 */
function updateComponentsWithRealtimeData(data) {
    // Process real-time updates
    if (data.source === 'weather') {
        // Update just the weather component
        updateWeatherWidget(data);
    } else if (data.source === 'economic') {
        // Update economic indicators
        updateEconomicIndicators(data);
    }
    // Add other real-time update handlers as needed
}

/**
 * Update the last updated display
 */
function updateLastUpdatedDisplay() {
    const lastUpdatedElem = document.getElementById('last-updated');
    if (lastUpdatedElem && dashboardState.lastUpdated) {
        const date = new Date(dashboardState.lastUpdated);
        lastUpdatedElem.textContent = date.toLocaleTimeString();
    }
}

/**
 * Show error message
 */
function showErrorMessage(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger';
    alertDiv.textContent = message;
    
    const dashboardContainer = document.querySelector('.dashboard-container');
    if (dashboardContainer) {
        dashboardContainer.prepend(alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

/**
 * Utility function to get trend CSS class
 */
function getTrendClass(trend) {
    switch(trend) {
        case 'increasing':
            return 'text-success';
        case 'decreasing':
            return 'text-danger';
        default:
            return 'text-muted';
    }
}

/**
 * Utility function to get trend icon
 */
function getTrendIcon(trend) {
    switch(trend) {
        case 'increasing':
            return '▲';
        case 'decreasing':
            return '▼';
        default:
            return '▬';
    }
}

/**
 * Utility function to get congestion CSS class
 */
function getCongestionClass(level) {
    if (level > 80) return 'bg-danger';
    if (level > 60) return 'bg-warning';
    if (level > 40) return 'bg-info';
    return 'bg-success';
}

/**
 * Utility function to get sentiment CSS class
 */
function getSentimentClass(sentiment) {
    if (sentiment > 80) return 'bg-success';
    if (sentiment > 60) return 'bg-info';
    if (sentiment > 40) return 'bg-warning';
    return 'bg-danger';
}

/**
 * Utility function to get correlation CSS class
 */
function getCorrelationClass(correlation) {
    const abs = Math.abs(correlation);
    if (abs > 0.8) return 'bg-danger';
    if (abs > 0.6) return 'bg-warning';
    if (abs > 0.4) return 'bg-info';
    return 'bg-secondary';
}

/**
 * Format a number with commas for thousands
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Format uptime in a readable format
 */
function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    let result = '';
    if (days > 0) result += `${days}d `;
    if (hours > 0 || days > 0) result += `${hours}h `;
    result += `${minutes}m`;
    
    return result;
}

// Initialize dashboard when the DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);