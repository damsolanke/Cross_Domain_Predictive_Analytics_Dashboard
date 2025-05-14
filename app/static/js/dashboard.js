/**
 * Cross-Domain Predictive Analytics Dashboard
 * Main dashboard JavaScript for loading and rendering dashboard components
 */

// Dashboard state
const dashboardState = {
    isLoading: false,
    lastUpdated: null,
    dataCache: {},
    components: [],
    settings: {
        autoRefresh: true,
        notificationsEnabled: true,
        timeRange: '1d',
        lastTabSelected: 'overview'
    }
};

// Configuration
const config = {
    apiEndpoints: {
        dashboardData: '/api/dashboard-data',
        correlations: '/api/correlations',
        systemStatus: '/system/api/system-status'
    },
    refreshInterval: 30000, // 30 seconds

    // Cache expiry times by time range (in milliseconds)
    cacheExpiry: {
        '1h': 15000,   // 15 seconds for 1 hour data
        '6h': 30000,   // 30 seconds for 6 hour data
        '1d': 60000,   // 1 minute for 1 day data
        '7d': 300000,  // 5 minutes for 7 day data
        '30d': 900000, // 15 minutes for 30 day data
        '90d': 1800000, // 30 minutes for 90 day data
        '180d': 3600000, // 1 hour for 180 day data
        '365d': 7200000, // 2 hours for 1 year data
        'default': 60000 // Default: 1 minute
    },

    // Storage options
    storage: {
        useLocalStorage: true,   // Enable localStorage caching for persistence
        maxCacheItems: 20        // Maximum number of items to store in cache
    }
};

/**
 * Initialize the dashboard
 */
function initDashboard() {
    console.log('Initializing dashboard...');

    // Load saved settings
    loadDashboardSettings();

    // Register components to be loaded
    registerComponents();

    // Set up loading indicator
    setupLoadingIndicator();

    // Set up UI event handlers
    setupEventHandlers();

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
 * Load dashboard settings from localStorage
 */
function loadDashboardSettings() {
    if (window.localStorage && config.storage.useLocalStorage) {
        try {
            const savedSettings = localStorage.getItem('dashboardSettings');
            if (savedSettings) {
                const parsedSettings = JSON.parse(savedSettings);
                dashboardState.settings = {
                    ...dashboardState.settings,
                    ...parsedSettings
                };
                console.log('Loaded settings from localStorage:', dashboardState.settings);

                // Apply UI settings
                applySettings();
            }
        } catch (error) {
            console.error('Error loading settings from localStorage:', error);
        }
    }
}

/**
 * Save dashboard settings to localStorage
 */
function saveDashboardSettings() {
    if (window.localStorage && config.storage.useLocalStorage) {
        try {
            localStorage.setItem('dashboardSettings', JSON.stringify(dashboardState.settings));
            console.log('Saved settings to localStorage');
        } catch (error) {
            console.error('Error saving settings to localStorage:', error);
        }
    }
}

/**
 * Apply loaded settings to UI elements
 */
function applySettings() {
    // Apply time range
    const timeRangeSelector = document.getElementById('timeRangeSelector');
    if (timeRangeSelector && dashboardState.settings.timeRange) {
        timeRangeSelector.value = dashboardState.settings.timeRange;
    }

    // Apply auto-refresh setting
    const autoRefreshToggle = document.getElementById('autoRefreshToggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.checked = dashboardState.settings.autoRefresh;
    }

    // Apply notifications setting
    const notificationsToggle = document.getElementById('notificationsToggle');
    if (notificationsToggle) {
        notificationsToggle.checked = dashboardState.settings.notificationsEnabled;
    }

    // Apply selected tab
    if (dashboardState.settings.lastTabSelected) {
        const tabLinks = document.querySelectorAll('[data-tab-target]');
        const targetTab = document.querySelector(`[data-tab-target="#${dashboardState.settings.lastTabSelected}"]`);

        if (targetTab) {
            tabLinks.forEach(link => link.classList.remove('active'));
            targetTab.classList.add('active');

            // Show the active tab content
            const tabContents = document.querySelectorAll('[data-tab-content]');
            tabContents.forEach(content => content.classList.remove('active'));

            const activeContent = document.getElementById(dashboardState.settings.lastTabSelected);
            if (activeContent) {
                activeContent.classList.add('active');
            }
        }
    }
}

/**
 * Set up UI event handlers
 */
function setupEventHandlers() {
    // Time range selector
    const timeRangeSelector = document.getElementById('timeRangeSelector');
    if (timeRangeSelector) {
        timeRangeSelector.addEventListener('change', function() {
            dashboardState.settings.timeRange = this.value;
            saveDashboardSettings();

            // Force reload all timeframe-dependent data
            dashboardState.dataCache = {}; // Clear all caches to force reload

            // Reload dashboard and correlation data
            loadDashboardData();
            loadCorrelationData(true); // Force correlation data refresh too
        });
    }

    // Auto-refresh toggle
    const autoRefreshToggle = document.getElementById('autoRefreshToggle');
    if (autoRefreshToggle) {
        autoRefreshToggle.addEventListener('change', function() {
            dashboardState.settings.autoRefresh = this.checked;
            saveDashboardSettings();
        });
    }

    // Notifications toggle
    const notificationsToggle = document.getElementById('notificationsToggle');
    if (notificationsToggle) {
        notificationsToggle.addEventListener('change', function() {
            dashboardState.settings.notificationsEnabled = this.checked;
            saveDashboardSettings();
        });
    }

    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            loadDashboardData();
        });
    }

    // Domain tabs
    const domainTabs = document.querySelectorAll('[data-tab-target]');
    domainTabs.forEach(tab => {
        tab.addEventListener('click', function(event) {
            event.preventDefault();

            // Get the target tab
            const targetId = this.getAttribute('data-tab-target').substring(1);
            dashboardState.settings.lastTabSelected = targetId;
            saveDashboardSettings();

            // Show the tab
            domainTabs.forEach(tab => tab.classList.remove('active'));
            this.classList.add('active');

            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });

            const targetPane = document.querySelector(this.getAttribute('data-tab-target'));
            if (targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // Set up correlation UI handlers
    setupCorrelationEventHandlers();
}

/**
 * Set up correlation tab event handlers
 */
function setupCorrelationEventHandlers() {
    // Correlation strength filter
    const strengthFilter = document.getElementById('correlation-strength-filter');
    if (strengthFilter) {
        strengthFilter.addEventListener('change', function() {
            // Reload correlation data
            loadCorrelationData();
        });
    }

    // Domain filter
    const domainFilter = document.getElementById('correlation-domain-filter');
    if (domainFilter) {
        domainFilter.addEventListener('change', function() {
            // Reload correlation data
            loadCorrelationData();
        });
    }

    // Refresh analysis button
    const refreshAnalysisBtn = document.getElementById('correlation-analysis-refresh');
    if (refreshAnalysisBtn) {
        refreshAnalysisBtn.addEventListener('click', function() {
            loadCorrelationData(true); // Force refresh
        });
    }

    // Temporal correlation pair selector
    const temporalPairSelector = document.getElementById('temporal-correlation-pair');
    if (temporalPairSelector) {
        temporalPairSelector.addEventListener('change', function() {
            updateTemporalCorrelationChart();
        });
    }

    // Network animation toggle
    const animatedNetworkToggle = document.getElementById('animated-network-toggle');
    if (animatedNetworkToggle) {
        animatedNetworkToggle.addEventListener('change', function() {
            // Reload the network with new animation setting
            const correlations = getFilteredCorrelations();
            if (correlations) {
                updateCorrelationNetwork(correlations);
            }
        });
    }

    // Correlation settings form
    const correlationSettingsForm = document.getElementById('correlation-settings-form');
    if (correlationSettingsForm) {
        correlationSettingsForm.addEventListener('submit', function(event) {
            event.preventDefault();

            // Get form values
            const resolution = document.getElementById('correlation-time-resolution').value;
            const lagWindow = document.getElementById('correlation-lag-window').value;
            const autoRefresh = document.getElementById('correlation-auto-refresh').checked;

            // Save settings
            dashboardState.settings.correlationSettings = {
                resolution: resolution,
                lagWindow: parseInt(lagWindow),
                autoRefresh: autoRefresh
            };
            saveDashboardSettings();

            // Reload correlation data
            loadCorrelationData(true);
        });
    }
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
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        // Show initially
        loadingIndicator.style.display = 'flex';

        // Update loading state
        dashboardState.isLoading = true;

        // Hide loading indicator after 5 seconds even if data hasn't loaded yet
        // This prevents UI being stuck in loading state if there's an issue
        setTimeout(() => {
            if (dashboardState.isLoading) {
                loadingIndicator.style.display = 'none';
                dashboardState.isLoading = false;
                console.warn('Loading timeout reached, forcing dashboard to display');
            }
        }, 5000);
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

    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorContainer = document.getElementById('errorContainer');

    if (loadingIndicator) {
        loadingIndicator.style.display = 'flex';
    }

    if (errorContainer) {
        errorContainer.style.display = 'none';
    }

    // Record start time to measure performance
    const startTime = performance.now();

    try {
        // Get the selected time range
        const timeRangeSelector = document.getElementById('timeRangeSelector');
        const timeRange = timeRangeSelector ? timeRangeSelector.value : '1d';

        // Check cache first - but only if the time range matches
        const now = new Date().getTime();
        if (dashboardState.dataCache.dashboardData &&
            dashboardState.dataCache.dashboardData.timeRange === timeRange &&
            (now - dashboardState.dataCache.dashboardData.timestamp) < config.cacheExpiry) {

            console.log('Using cached dashboard data for time range: ' + timeRange);
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
            console.log('Fetching fresh dashboard data for time range: ' + timeRange);

            // Add time range to the API request
            // Try both with and without leading slash for API endpoint
            let url;
            try {
                url = new URL(config.apiEndpoints.dashboardData, window.location.origin);
            } catch (e) {
                // If URL creation fails, try with a leading slash
                url = new URL((config.apiEndpoints.dashboardData.startsWith('/') ? '' : '/') + config.apiEndpoints.dashboardData, window.location.origin);
            }
            url.searchParams.append('timeRange', timeRange);

            console.log('Fetching from URL:', url.toString());

            const response = await fetch(url, {
                signal: controller.signal,
                headers: {
                    'Cache-Control': 'max-age=60'
                }
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                // Show detailed error in console
                console.error(`Server responded with status ${response.status} (${response.statusText})`);
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Received dashboard data:', data);

            // Add debug info about data structure
            console.log('Data contains:', Object.keys(data));
            console.log('Weather data:', data.weather ? 'present' : 'missing');
            console.log('Economic data:', data.economic ? 'present' : 'missing');
            console.log('Transportation data:', data.transportation ? 'present' : 'missing');
            console.log('Social media data:', data.social_media ? 'present' : 'missing');

            // Cache the data with the time range
            dashboardState.dataCache.dashboardData = {
                data: data,
                timestamp: now,
                timeRange: timeRange
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
            console.error('Fetch error details:', fetchError);

            // If we have cached data, use it as fallback when fetch fails
            if (dashboardState.dataCache.dashboardData) {
                console.warn('Fetch failed, using cached data as fallback');
                updateDashboardComponents(dashboardState.dataCache.dashboardData.data);

                // Show a warning message that we're using cached data
                showErrorMessage('Using cached data. Server connection issue detected.');
            } else {
                // Generate demo data as a last resort
                console.warn('No cached data available, generating demo data');
                const demoData = generateDemoData(timeRange);
                updateDashboardComponents(demoData);

                showErrorMessage('Unable to connect to server. Showing demo data.');
                throw fetchError;
            }
        }

    } catch (error) {
        console.error('Error loading dashboard data:', error);

        if (errorContainer) {
            // Set error content with icon
            errorContainer.innerHTML = `
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <div>Failed to load dashboard data: ${error.message}</div>
            `;
            errorContainer.style.display = 'flex';

            // Auto-hide after 10 seconds
            setTimeout(() => {
                errorContainer.style.display = 'none';
            }, 10000);

            // Generate demo data as a fallback
            console.warn('Error handling - generating demo data as fallback');
            const demoData = generateDemoData(timeRange || '1d');
            updateDashboardComponents(demoData);
        }
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
 * Set up improved refresh interval
 */
function setupRefreshInterval() {
    // Refresh data periodically based on auto-refresh setting
    setInterval(() => {
        if (!dashboardState.isLoading && dashboardState.settings.autoRefresh) {
            loadDashboardData();

            // Also refresh correlation data if on correlation tab
            if (dashboardState.settings.lastTabSelected === 'crossDomainTab' &&
                dashboardState.settings.correlationSettings?.autoRefresh) {
                loadCorrelationData();
            }
        }
    }, config.refreshInterval);
}

/**
 * Get filtered correlation data
 */
function getFilteredCorrelations() {
    // Check if there are cached correlations
    if (!dashboardState.dataCache.correlations) {
        return null;
    }

    // Get filter settings
    const strengthFilter = document.getElementById('correlation-strength-filter');
    const domainFilter = document.getElementById('correlation-domain-filter');

    const strengthValue = strengthFilter ? strengthFilter.value : 'all';
    const domainValue = domainFilter ? domainFilter.value : 'all';

    // Filter correlations
    let filteredCorrelations = dashboardState.dataCache.correlations.correlations;

    // Filter by strength
    if (strengthValue !== 'all') {
        filteredCorrelations = filteredCorrelations.filter(corr => {
            const absCorr = Math.abs(corr.correlation);
            switch(strengthValue) {
                case 'strong':
                    return absCorr > 0.7;
                case 'moderate':
                    return absCorr >= 0.4 && absCorr <= 0.7;
                case 'weak':
                    return absCorr < 0.4;
                default:
                    return true;
            }
        });
    }

    // Filter by domain
    if (domainValue !== 'all') {
        filteredCorrelations = filteredCorrelations.filter(corr =>
            corr.domain1.toLowerCase() === domainValue ||
            corr.domain2.toLowerCase() === domainValue
        );
    }

    return filteredCorrelations;
}

/**
 * Load correlation data
 */
function loadCorrelationData(forceRefresh = false) {
    console.log('Loading correlation data...');

    const timeRangeSelector = document.getElementById('timeRangeSelector');
    const timeRange = timeRangeSelector ? timeRangeSelector.value : '1d';

    // Check cache first, unless forced refresh
    const now = new Date().getTime();
    const cacheExpiryTime = config.cacheExpiry[timeRange] || config.cacheExpiry.default;

    if (!forceRefresh &&
        dashboardState.dataCache.correlations &&
        dashboardState.dataCache.correlations.timeRange === timeRange &&
        (now - dashboardState.dataCache.correlations.timestamp) < cacheExpiryTime) {

        console.log('Using cached correlation data for time range: ' + timeRange);

        // Update UI with cached data
        const filteredCorrelations = getFilteredCorrelations();
        if (filteredCorrelations) {
            updateCorrelationInsights({
                correlations: filteredCorrelations,
                summary: dashboardState.dataCache.correlations.summary
            });
        }

        return Promise.resolve();
    }

    // Get settings for correlation analysis
    const settings = dashboardState.settings.correlationSettings || {
        resolution: 'daily',
        lagWindow: 3,
        autoRefresh: true
    };

    // Prepare URL
    const url = new URL(config.apiEndpoints.correlations, window.location.origin);
    url.searchParams.append('timeRange', timeRange);
    url.searchParams.append('resolution', settings.resolution);
    url.searchParams.append('lagWindow', settings.lagWindow);

    // Fetch fresh data
    console.log('Fetching fresh correlation data...');

    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            // Cache the data
            dashboardState.dataCache.correlations = {
                ...data,
                timestamp: now,
                timeRange: timeRange,
                settings: settings
            };

            // Save to localStorage if enabled
            if (config.storage.useLocalStorage) {
                try {
                    localStorage.setItem('correlationData_' + timeRange, JSON.stringify({
                        data: data,
                        timestamp: now,
                        timeRange: timeRange,
                        settings: settings
                    }));
                } catch (error) {
                    console.warn('Failed to save correlation data to localStorage:', error);
                }
            }

            // Update UI with new data
            updateCorrelationInsights(data);

            return data;
        })
        .catch(error => {
            console.error('Error loading correlation data:', error);

            // Try to load from localStorage as fallback
            if (config.storage.useLocalStorage) {
                try {
                    const savedData = localStorage.getItem('correlationData_' + timeRange);
                    if (savedData) {
                        const parsedData = JSON.parse(savedData);

                        console.log('Using localStorage correlation data for time range: ' + timeRange);
                        dashboardState.dataCache.correlations = parsedData.data;

                        // Update UI with localStorage data
                        updateCorrelationInsights(parsedData.data);

                        return parsedData.data;
                    }
                } catch (storageError) {
                    console.error('Error loading correlation data from localStorage:', storageError);
                }
            }

            // If there's no cache, use demo data
            generateDemoCorrelationData();

            return null;
        });
}

/**
 * Generate demo correlation data
 */
function generateDemoCorrelationData() {
    console.log('Generating demo correlation data...');

    const timeRangeSelector = document.getElementById('timeRangeSelector');
    const timeRange = timeRangeSelector ? timeRangeSelector.value : '1d';

    // Generate detailed placeholder data
    const demoData = {
        correlations: [
            {domain1: 'Weather', metric1: 'Temperature', domain2: 'Energy', metric2: 'Demand', correlation: 0.85, strength: 'strong', confidence: 0.92, lag: 0},
            {domain1: 'Weather', metric1: 'Precipitation', domain2: 'Transportation', metric2: 'Accidents', correlation: 0.72, strength: 'strong', confidence: 0.89, lag: 0},
            {domain1: 'Economic', metric1: 'Market Index', domain2: 'Social Media', metric2: 'Sentiment', correlation: 0.68, strength: 'moderate', confidence: 0.78, lag: 1},
            {domain1: 'Transportation', metric1: 'Congestion', domain2: 'Economic', metric2: 'Retail Sales', correlation: -0.52, strength: 'moderate', confidence: 0.81, lag: 2},
            {domain1: 'Social Media', metric1: 'Volume', domain2: 'Economic', metric2: 'Volatility', correlation: 0.45, strength: 'moderate', confidence: 0.76, lag: 0},
            {domain1: 'Weather', metric1: 'Temperature', domain2: 'Transportation', metric2: 'Congestion', correlation: 0.32, strength: 'weak', confidence: 0.65, lag: 0},
            {domain1: 'Social Media', metric1: 'Sentiment', domain2: 'Weather', metric2: 'Precipitation', correlation: -0.24, strength: 'weak', confidence: 0.71, lag: 3}
        ],
        summary: {
            strongest: {domain1: 'Weather', metric1: 'Temperature', domain2: 'Energy', metric2: 'Demand', correlation: 0.85},
            negative: {domain1: 'Transportation', metric1: 'Congestion', domain2: 'Economic', metric2: 'Retail Sales', correlation: -0.52},
            trending: {domain1: 'Social Media', metric1: 'Sentiment', domain2: 'Economic', metric2: 'Market Index', correlation_change: 0.15},
            timeRange: timeRange
        },
        demo_data: true
    };

    // Cache the demo data
    dashboardState.dataCache.correlations = {
        ...demoData,
        timestamp: new Date().getTime(),
        timeRange: timeRange
    };

    // Update the UI
    updateCorrelationInsights(demoData);
}

function generateDemoData(timeRange) {
    console.log('Generating demo data for time range: ' + timeRange);

    // Calculate number of data points based on time range
    let dataPoints = 24; // Default to 24 hours

    switch(timeRange) {
        case '1h':
            dataPoints = 60; // 60 minutes
            break;
        case '6h':
            dataPoints = 72; // 12 data points per hour
            break;
        case '1d':
            dataPoints = 24; // 24 hours
            break;
        case '7d':
            dataPoints = 168; // 7 days with hourly data
            break;
        case '30d':
            dataPoints = 30; // 30 days
            break;
        case '90d':
            dataPoints = 90; // 90 days
            break;
        case '180d':
            dataPoints = 180; // 180 days
            break;
        case '365d':
            dataPoints = 52; // Weekly data for a year
            break;
    }

    // Generate weather data
    const weatherData = {
        temperature: Math.round(Math.random() * 30 + 50), // 50-80°F
        condition: ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy"][Math.floor(Math.random() * 5)],
        forecast: Array.from({length: 7}, (_, i) => ({
            day: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][(new Date().getDay() + i) % 7],
            high: Math.round(Math.random() * 15 + 65), // 65-80°F
            low: Math.round(Math.random() * 15 + 45), // 45-60°F
            condition: ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy"][Math.floor(Math.random() * 5)]
        }))
    };

    // Generate economic data
    const economicData = {
        market_index: Math.round(Math.random() * 1000 + 9000), // 9000-10000
        change_percent: (Math.random() * 4 - 2).toFixed(2), // -2% to +2%
        indicators: [
            {name: "Interest Rate", value: (Math.random() * 3 + 1).toFixed(2) + "%", trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {name: "Inflation", value: (Math.random() * 4 + 1).toFixed(2) + "%", trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {name: "Unemployment", value: (Math.random() * 3 + 3).toFixed(2) + "%", trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {name: "GDP Growth", value: (Math.random() * 3 + 1).toFixed(2) + "%", trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]}
        ]
    };

    // Generate transportation data
    const transportationData = {
        congestion_level: Math.round(Math.random() * 70 + 20), // 20-90%
        average_speed: Math.round(Math.random() * 30 + 20), // 20-50 mph
        hotspots: [
            {location: "Downtown", level: Math.round(Math.random() * 40 + 60), trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {location: "Highway I-95", level: Math.round(Math.random() * 40 + 40), trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {location: "East Bridge", level: Math.round(Math.random() * 40 + 50), trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]},
            {location: "West Exit", level: Math.round(Math.random() * 40 + 30), trend: ["increasing", "stable", "decreasing"][Math.floor(Math.random() * 3)]}
        ]
    };

    // Generate social media data
    const socialMediaData = {
        sentiment: Math.round(Math.random() * 50 + 40), // 40-90%
        trending_topics: [
            {topic: "Latest Product Launch", sentiment: Math.round(Math.random() * 30 + 60), volume: Math.round(Math.random() * 10000 + 5000)},
            {topic: "Economic Policy", sentiment: Math.round(Math.random() * 40 + 30), volume: Math.round(Math.random() * 8000 + 2000)},
            {topic: "Weather Conditions", sentiment: Math.round(Math.random() * 30 + 50), volume: Math.round(Math.random() * 5000 + 1000)},
            {topic: "Traffic Updates", sentiment: Math.round(Math.random() * 30 + 40), volume: Math.round(Math.random() * 3000 + 1000)}
        ]
    };

    return {
        weather: weatherData,
        economic: economicData,
        transportation: transportationData,
        social_media: socialMediaData,
        demo_data: true // Mark as demo data
    };
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
    console.log('Updating dashboard components with data:', data);

    // Check if we have the expected data structure
    if (!data) {
        console.error('No data provided to updateDashboardComponents');
        return;
    }

    // Handle different data structures returned by API
    // Check if data is wrapped in a data property (from the old API)
    if (data.data && typeof data.data === 'object') {
        console.log('Data is wrapped in data property, unwrapping...');
        // If it has organized_data format with weather, economic, etc keys
        if (data.data.weather && Array.isArray(data.data.weather)) {
            console.log('Found array data in old format, generating compatible format');
            // Convert from old format to new format
            data = {
                weather: {
                    temperature: 78,
                    condition: 'Partly Cloudy',
                    forecast: [
                        {'day': 'Today', 'high': 78, 'low': 65, 'condition': 'Partly Cloudy'},
                        {'day': 'Tomorrow', 'high': 82, 'low': 68, 'condition': 'Sunny'},
                        {'day': 'Wednesday', 'high': 85, 'low': 70, 'condition': 'Sunny'},
                        {'day': 'Thursday', 'high': 79, 'low': 68, 'condition': 'Cloudy'},
                        {'day': 'Friday', 'high': 76, 'low': 64, 'condition': 'Rainy'}
                    ]
                },
                economic: {
                    market_index: 32415,
                    change_percent: 0.5,
                    consumer_confidence: 110,
                    indicators: [
                        {'name': 'GDP Growth', 'value': 2.3, 'trend': 'stable'},
                        {'name': 'Unemployment', 'value': 3.6, 'trend': 'decreasing'},
                        {'name': 'Inflation', 'value': 2.1, 'trend': 'increasing'},
                        {'name': 'Interest Rate', 'value': 1.5, 'trend': 'stable'}
                    ]
                },
                transportation: {
                    congestion_level: 65,
                    average_speed: 35,
                    hotspots: [
                        {'location': 'Downtown', 'level': 85, 'trend': 'increasing'},
                        {'location': 'Highway 101', 'level': 70, 'trend': 'stable'},
                        {'location': 'East Bridge', 'level': 90, 'trend': 'increasing'},
                        {'location': 'North Exit', 'level': 45, 'trend': 'decreasing'}
                    ]
                },
                social_media: {
                    sentiment: 72,
                    trending_topics: [
                        {'topic': 'New Product Launch', 'sentiment': 85, 'volume': 12500},
                        {'topic': 'Weather Concerns', 'sentiment': 45, 'volume': 8300},
                        {'topic': 'Traffic Conditions', 'sentiment': 30, 'volume': 7200},
                        {'topic': 'Economic News', 'sentiment': 65, 'volume': 6100}
                    ]
                }
            };
            console.log('Created compatible data format:', data);
        }
    }

    // Update system metrics
    if (data.health) {
        updateSystemMetrics(data.health);
    }

    // Update weather widget if data exists
    if (data.weather) {
        console.log('Updating weather widget with:', data.weather);
        updateWeatherWidget(data.weather);
    } else {
        console.error('Missing weather data');
        // Use demo data as a fallback
        updateWeatherWidget({
            temperature: 78,
            condition: 'Partly Cloudy',
            forecast: [
                {'day': 'Today', 'high': 78, 'low': 65, 'condition': 'Partly Cloudy'},
                {'day': 'Tomorrow', 'high': 82, 'low': 68, 'condition': 'Sunny'},
                {'day': 'Wednesday', 'high': 85, 'low': 70, 'condition': 'Sunny'},
                {'day': 'Thursday', 'high': 79, 'low': 68, 'condition': 'Cloudy'},
                {'day': 'Friday', 'high': 76, 'low': 64, 'condition': 'Rainy'}
            ]
        });
    }

    // Update economic indicators if data exists
    if (data.economic) {
        console.log('Updating economic indicators with:', data.economic);
        updateEconomicIndicators(data.economic);
    } else {
        console.error('Missing economic data');
        // Use demo data as a fallback
        updateEconomicIndicators({
            market_index: 32415,
            change_percent: 0.5,
            consumer_confidence: 110,
            indicators: [
                {'name': 'GDP Growth', 'value': 2.3, 'trend': 'stable'},
                {'name': 'Unemployment', 'value': 3.6, 'trend': 'decreasing'},
                {'name': 'Inflation', 'value': 2.1, 'trend': 'increasing'},
                {'name': 'Interest Rate', 'value': 1.5, 'trend': 'stable'}
            ]
        });
    }

    // Update transportation status if data exists
    if (data.transportation) {
        console.log('Updating transportation status with:', data.transportation);
        updateTransportationStatus(data.transportation);
    } else {
        console.error('Missing transportation data');
        // Use demo data as a fallback
        updateTransportationStatus({
            congestion_level: 65,
            average_speed: 35,
            hotspots: [
                {'location': 'Downtown', 'level': 85, 'trend': 'increasing'},
                {'location': 'Highway 101', 'level': 70, 'trend': 'stable'},
                {'location': 'East Bridge', 'level': 90, 'trend': 'increasing'},
                {'location': 'North Exit', 'level': 45, 'trend': 'decreasing'}
            ]
        });
    }

    // Update social media trends if data exists
    if (data.social_media) {
        console.log('Updating social media trends with:', data.social_media);
        updateSocialMediaTrends(data.social_media);
    } else {
        console.error('Missing social_media data');
        // Use demo data as a fallback
        updateSocialMediaTrends({
            sentiment: 72,
            trending_topics: [
                {'topic': 'New Product Launch', 'sentiment': 85, 'volume': 12500},
                {'topic': 'Weather Concerns', 'sentiment': 45, 'volume': 8300},
                {'topic': 'Traffic Conditions', 'sentiment': 30, 'volume': 7200},
                {'topic': 'Economic News', 'sentiment': 65, 'volume': 6100}
            ]
        });
    }
}

/**
 * Update weather widget with data
 */
function updateWeatherWidget(weatherData) {
    console.log('Looking for weather widget elements to update');

    // Update the weather widget in the overview tab
    const weatherGaugeSmall = document.getElementById('weatherGaugeSmall');
    if (weatherGaugeSmall) {
        console.log('Found weatherGaugeSmall element to update');

        // Get a weather icon based on condition
        const weatherIcon = getWeatherIcon(weatherData.condition);

        // Update with a modern gauge display
        weatherGaugeSmall.innerHTML = `
            <div class="text-center d-flex flex-column align-items-center p-3">
                <i class="bi ${weatherIcon} mb-2" style="font-size: 2rem; color: #4cc9f0;"></i>
                <h2 class="mb-1">${weatherData.temperature}°F</h2>
                <span class="badge bg-info text-white mb-2">${weatherData.condition}</span>
                <div class="temperature-scale mt-2" style="width: 100%; height: 8px; background: linear-gradient(90deg, #3498db, #f1c40f, #e74c3c); border-radius: 4px;">
                    <div class="temperature-marker" style="position: relative; left: ${Math.min(100, Math.max(0, (weatherData.temperature - 32) / 100 * 100))}%; transform: translateX(-50%);">
                        <div style="width: 4px; height: 10px; background-color: white; border: 2px solid #4cc9f0; border-radius: 2px;"></div>
                    </div>
                </div>
            </div>
        `;
    } else {
        console.error('Could not find weatherGaugeSmall element');
    }

    // Update the weather widget in the weather tab
    const weatherGauge = document.getElementById('weatherGauge');
    if (weatherGauge) {
        console.log('Found weatherGauge element to update');

        // Get a weather icon based on condition
        const weatherIcon = getWeatherIcon(weatherData.condition);

        // Calculate temperature on a scale from cold to hot (0-100%)
        const tempPercent = Math.min(100, Math.max(0, (weatherData.temperature - 32) / 100 * 100));

        // Create a visually appealing gauge with icon and details
        weatherGauge.innerHTML = `
            <div class="text-center d-flex flex-column align-items-center p-3">
                <i class="bi ${weatherIcon} mb-3" style="font-size: 3rem; color: #4cc9f0;"></i>
                <h2 class="mb-2">${weatherData.temperature}°F</h2>
                <span class="badge bg-info text-white mb-3" style="font-size: 0.9rem; padding: 0.5rem 1rem;">${weatherData.condition}</span>

                <div class="w-100 mt-2">
                    <div class="d-flex justify-content-between mb-1">
                        <small class="text-muted">Cold</small>
                        <small class="text-muted">Hot</small>
                    </div>
                    <div class="progress" style="height: 10px;">
                        <div class="progress-bar" role="progressbar"
                             style="width: ${tempPercent}%; background: linear-gradient(90deg, #3498db, #f1c40f, #e74c3c);"
                             aria-valuenow="${tempPercent}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                </div>

                <div class="mt-4">
                    <h6 class="mb-3">Forecast</h6>
                    <div class="d-flex justify-content-between">
                        ${weatherData.forecast.slice(0, 4).map(day => `
                            <div class="text-center px-2">
                                <div class="mb-2" style="font-size: 0.85rem; font-weight: 500;">${day.day}</div>
                                <i class="bi ${getWeatherIcon(day.condition)}" style="font-size: 1.2rem; color: #4cc9f0;"></i>
                                <div class="mt-1" style="font-size: 0.8rem; font-weight: 600;">${day.high}°/${day.low}°</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // Update the weather comparison chart
    const weatherComparisonChart = document.getElementById('weatherComparisonChart');
    if (weatherComparisonChart) {
        console.log('Found weatherComparisonChart element to update');
        weatherComparisonChart.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" style="width: 1.5rem; height: 1.5rem;"></div><span class="ms-2">Loading chart data...</span></div>';
        // Will implement chart visualization later with Highcharts
    }

    // Update the weather temp chart
    const weatherTempChart = document.getElementById('weatherTempChart');
    if (weatherTempChart) {
        console.log('Found weatherTempChart element to update');
        weatherTempChart.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" style="width: 1.5rem; height: 1.5rem;"></div><span class="ms-2">Loading chart data...</span></div>';
        // Will implement chart visualization later with Highcharts
    }

    // Update the weather map
    const weatherMap = document.getElementById('weatherMap');
    if (weatherMap) {
        console.log('Found weatherMap element to update');
        weatherMap.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border text-primary" style="width: 1.5rem; height: 1.5rem;"></div><span class="ms-2">Loading map data...</span></div>';
        // Will implement map visualization later
    }
}

/**
 * Update economic indicators with data
 */
function updateEconomicIndicators(economicData) {
    console.log('Looking for economic indicator elements to update');

    // Update the economic gauge in the overview tab
    const economicGaugeSmall = document.getElementById('economicGaugeSmall');
    if (economicGaugeSmall) {
        console.log('Found economicGaugeSmall element to update');
        economicGaugeSmall.innerHTML = `
            <div class="text-center">
                <h3>Index: ${economicData.market_index}</h3>
                <span class="${economicData.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                    ${economicData.change_percent >= 0 ? '▲' : '▼'} ${Math.abs(economicData.change_percent)}%
                </span>
            </div>
        `;
    } else {
        console.error('Could not find economicGaugeSmall element');
    }

    // Update the economic gauge in the economic tab
    const economicGauge = document.getElementById('economicGauge');
    if (economicGauge) {
        console.log('Found economicGauge element to update');
        economicGauge.innerHTML = `
            <div class="text-center">
                <h3>Market Index: ${economicData.market_index}</h3>
                <span class="${economicData.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                    ${economicData.change_percent >= 0 ? '▲' : '▼'} ${Math.abs(economicData.change_percent)}%
                </span>
            </div>
        `;
    }

    // Update the economic trends chart
    const economicTrendsChart = document.getElementById('economicTrendsChart');
    if (economicTrendsChart) {
        console.log('Found economicTrendsChart element to update');
        // Will implement chart visualization later
    }

    // Update the economic comparison chart
    const economicComparisonChart = document.getElementById('economicComparisonChart');
    if (economicComparisonChart) {
        console.log('Found economicComparisonChart element to update');
        // Will implement chart visualization later
    }

    // Update the economic map
    const economicMap = document.getElementById('economicMap');
    if (economicMap) {
        console.log('Found economicMap element to update');
        // Will implement map visualization later
    }
}

/**
 * Update transportation status with data
 */
function updateTransportationStatus(transportationData) {
    console.log('Looking for transportation elements to update');

    // Update the transportation gauge in the overview tab
    const transportationGaugeSmall = document.getElementById('transportationGaugeSmall');
    if (transportationGaugeSmall) {
        console.log('Found transportationGaugeSmall element to update');
        transportationGaugeSmall.innerHTML = `
            <div class="text-center">
                <h3>Congestion: ${transportationData.congestion_level}%</h3>
                <p>Avg. Speed: ${transportationData.average_speed} mph</p>
            </div>
        `;
    } else {
        console.error('Could not find transportationGaugeSmall element');
    }

    // Update the congestion gauge in the transportation tab
    const congestionGauge = document.getElementById('congestionGauge');
    if (congestionGauge) {
        console.log('Found congestionGauge element to update');
        congestionGauge.innerHTML = `
            <div class="text-center">
                <h3>Congestion Level: ${transportationData.congestion_level}%</h3>
                <div class="progress mt-2">
                    <div class="progress-bar ${getCongestionClass(transportationData.congestion_level)}"
                         role="progressbar"
                         style="width: ${transportationData.congestion_level}%"
                         aria-valuenow="${transportationData.congestion_level}"
                         aria-valuemin="0"
                         aria-valuemax="100">
                        ${transportationData.congestion_level}%
                    </div>
                </div>
                <p class="mt-2">Avg. Speed: ${transportationData.average_speed} mph</p>
            </div>
        `;
    }

    // Update the traffic trends chart
    const trafficTrendsChart = document.getElementById('trafficTrendsChart');
    if (trafficTrendsChart) {
        console.log('Found trafficTrendsChart element to update');
        // Will implement chart visualization later
    }

    // Update the transportation comparison chart
    const transportationComparisonChart = document.getElementById('transportationComparisonChart');
    if (transportationComparisonChart) {
        console.log('Found transportationComparisonChart element to update');
        // Will implement chart visualization later
    }

    // Update the traffic map
    const trafficMap = document.getElementById('trafficMap');
    if (trafficMap) {
        console.log('Found trafficMap element to update');
        // Will implement map visualization later
    }

    // Update the hotspots list if we have one
    const hotspotsList = document.querySelector('.hotspots .list-group');
    if (hotspotsList) {
        console.log('Found hotspotsList element to update');
        hotspotsList.innerHTML = transportationData.hotspots.map(hotspot => `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${hotspot.location}
                <span class="badge ${getCongestionClass(hotspot.level)} rounded-pill">
                    ${hotspot.level}% ${getTrendIcon(hotspot.trend)}
                </span>
            </li>
        `).join('');
    }
}

/**
 * Update social media trends with data
 */
function updateSocialMediaTrends(socialData) {
    console.log('Looking for social media elements to update');

    // Update the social media gauge in the overview tab
    const socialMediaGaugeSmall = document.getElementById('socialMediaGaugeSmall');
    if (socialMediaGaugeSmall) {
        console.log('Found socialMediaGaugeSmall element to update');
        socialMediaGaugeSmall.innerHTML = `
            <div class="text-center">
                <h3>Sentiment: ${socialData.sentiment}%</h3>
            </div>
        `;
    } else {
        console.error('Could not find socialMediaGaugeSmall element');
    }

    // Update the sentiment gauge in the social media tab
    const sentimentGauge = document.getElementById('sentimentGauge');
    if (sentimentGauge) {
        console.log('Found sentimentGauge element to update');
        sentimentGauge.innerHTML = `
            <div class="text-center">
                <h3>Sentiment Index: ${socialData.sentiment}%</h3>
                <div class="progress mt-2">
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
        `;
    }

    // Update the sentiment trends chart
    const sentimentTrendsChart = document.getElementById('sentimentTrendsChart');
    if (sentimentTrendsChart) {
        console.log('Found sentimentTrendsChart element to update');
        // Will implement chart visualization later
    }

    // Update the social media comparison chart
    const socialMediaComparisonChart = document.getElementById('socialMediaComparisonChart');
    if (socialMediaComparisonChart) {
        console.log('Found socialMediaComparisonChart element to update');
        // Will implement chart visualization later
    }

    // Update trending topics
    const trendingTopics = document.getElementById('trendingTopics');
    if (trendingTopics) {
        console.log('Found trendingTopics element to update');
        trendingTopics.innerHTML = socialData.trending_topics.map(topic => `
            <div class="list-group-item d-flex justify-content-between align-items-center">
                ${topic.topic}
                <div>
                    <span class="badge ${getSentimentClass(topic.sentiment)} rounded-pill me-2">
                        ${topic.sentiment}%
                    </span>
                    <small class="text-muted">${formatNumber(topic.volume)} mentions</small>
                </div>
            </div>
        `).join('');
    }
}

/**
 * Update correlation insights
 */
function updateCorrelationInsights(data) {
    const widget = document.getElementById('correlation-insights');
    if (!widget) return;

    // Get the selected timeRange
    const timeRangeSelector = document.getElementById('timeRangeSelector');
    const timeRange = timeRangeSelector ? timeRangeSelector.value : '1d';

    // Get the correlation strength filter
    const strengthFilter = document.getElementById('correlation-strength-filter');
    const strengthValue = strengthFilter ? strengthFilter.value : 'strong';

    // Get the domain filter
    const domainFilter = document.getElementById('correlation-domain-filter');
    const domainValue = domainFilter ? domainFilter.value : 'all';

    // If we don't have actual data, use more detailed placeholder
    if (!data || !data.correlations) {
        data = {
            correlations: [
                {domain1: 'Weather', metric1: 'Temperature', domain2: 'Energy', metric2: 'Demand', correlation: 0.85, strength: 'strong', confidence: 0.92, lag: 0},
                {domain1: 'Weather', metric1: 'Precipitation', domain2: 'Transportation', metric2: 'Accidents', correlation: 0.72, strength: 'strong', confidence: 0.89, lag: 0},
                {domain1: 'Economic', metric1: 'Market Index', domain2: 'Social Media', metric2: 'Sentiment', correlation: 0.68, strength: 'moderate', confidence: 0.78, lag: 1},
                {domain1: 'Transportation', metric1: 'Congestion', domain2: 'Economic', metric2: 'Retail Sales', correlation: -0.52, strength: 'moderate', confidence: 0.81, lag: 2},
                {domain1: 'Social Media', metric1: 'Volume', domain2: 'Economic', metric2: 'Volatility', correlation: 0.45, strength: 'moderate', confidence: 0.76, lag: 0},
                {domain1: 'Weather', metric1: 'Temperature', domain2: 'Transportation', metric2: 'Congestion', correlation: 0.32, strength: 'weak', confidence: 0.65, lag: 0},
                {domain1: 'Social Media', metric1: 'Sentiment', domain2: 'Weather', metric2: 'Precipitation', correlation: -0.24, strength: 'weak', confidence: 0.71, lag: 3}
            ],
            summary: {
                strongest: {domain1: 'Weather', metric1: 'Temperature', domain2: 'Energy', metric2: 'Demand', correlation: 0.85},
                negative: {domain1: 'Transportation', metric1: 'Congestion', domain2: 'Economic', metric2: 'Retail Sales', correlation: -0.52},
                trending: {domain1: 'Social Media', metric1: 'Sentiment', domain2: 'Economic', metric2: 'Market Index', correlation_change: 0.15},
                timeRange: timeRange
            }
        };
    }

    // Filter correlations based on user selection
    let filteredCorrelations = data.correlations;

    // Filter by strength
    if (strengthValue !== 'all') {
        filteredCorrelations = filteredCorrelations.filter(corr => {
            const absCorr = Math.abs(corr.correlation);
            switch(strengthValue) {
                case 'strong':
                    return absCorr > 0.7;
                case 'moderate':
                    return absCorr >= 0.4 && absCorr <= 0.7;
                case 'weak':
                    return absCorr < 0.4;
                default:
                    return true;
            }
        });
    }

    // Filter by domain
    if (domainValue !== 'all') {
        filteredCorrelations = filteredCorrelations.filter(corr =>
            corr.domain1.toLowerCase() === domainValue ||
            corr.domain2.toLowerCase() === domainValue
        );
    }

    // Sort by absolute correlation strength (descending)
    filteredCorrelations.sort((a, b) => Math.abs(b.correlation) - Math.abs(a.correlation));

    // Limit to top 5 for display
    const topCorrelations = filteredCorrelations.slice(0, 5);

    // Update the heatmap and network visualizations
    updateCorrelationHeatmap(filteredCorrelations);
    updateCorrelationNetwork(filteredCorrelations);
    updateCorrelationTable(filteredCorrelations);

    // Generate key insights
    const timeRangeText = getTimeRangeDisplay(timeRange);
    let insightsHtml = '';

    if (topCorrelations.length === 0) {
        insightsHtml = `
            <div class="alert alert-info">
                No significant correlations found with the current filters.
                Try adjusting your correlation strength or domain filters.
            </div>
        `;
    } else {
        // Summary and insights
        insightsHtml = `
            <div class="correlation-insight-summary">
                <p>Analysis based on data from the ${timeRangeText}. Found ${filteredCorrelations.length} correlations matching your criteria.</p>

                <h6 class="mt-3">Key Findings:</h6>
                <ul class="insight-list">
                    ${topCorrelations.map(corr => `
                        <li class="insight-item">
                            <div class="d-flex align-items-center mb-2">
                                <span class="badge ${getCorrelationClass(corr.correlation)} me-2">
                                    ${Math.abs(corr.correlation).toFixed(2)}
                                </span>
                                <strong>${corr.domain1} (${corr.metric1}) ${corr.correlation >= 0 ? '→' : '⊣'} ${corr.domain2} (${corr.metric2})</strong>
                            </div>
                            <p class="small text-muted mb-1">
                                ${getCorrelationDescription(corr)}
                                ${corr.lag > 0 ? `<span class="fst-italic">Lag: ${corr.lag} day(s)</span>` : ''}
                            </p>
                            <div class="progress mb-3" style="height: 4px;">
                                <div class="progress-bar ${getCorrelationClass(corr.correlation)}"
                                     role="progressbar"
                                     style="width: ${Math.abs(corr.correlation) * 100}%"
                                     aria-valuenow="${Math.abs(corr.correlation) * 100}"
                                     aria-valuemin="0"
                                     aria-valuemax="100"></div>
                            </div>
                        </li>
                    `).join('')}
                </ul>

                ${data.summary ? `
                <h6 class="mt-3">Trending Changes:</h6>
                <div class="alert alert-info">
                    ${data.summary.trending ? `
                        <i class="bi bi-arrow-up-right me-1"></i>
                        <strong>${data.summary.trending.domain1} ${data.summary.trending.metric1}</strong> and
                        <strong>${data.summary.trending.domain2} ${data.summary.trending.metric2}</strong> correlation
                        increased by ${(data.summary.trending.correlation_change * 100).toFixed(1)}% compared to previous period.
                    ` : 'No significant trending changes detected.'}
                </div>
                ` : ''}
            </div>
        `;
    }

    // Update the correlation-insights div
    widget.innerHTML = insightsHtml;

    // Also update the temporal correlation chart
    updateTemporalCorrelationChart();
}

/**
 * Update the correlation heatmap visualization
 */
function updateCorrelationHeatmap(correlations) {
    const heatmapContainer = document.getElementById('correlation-heatmap');
    if (!heatmapContainer) return;

    // Clear any existing chart
    heatmapContainer.innerHTML = '';

    // If no data, show a message
    if (!correlations || correlations.length === 0) {
        heatmapContainer.innerHTML = `
            <div class="alert alert-info">
                No correlation data available for the selected filters.
            </div>
        `;
        return;
    }

    // Extract unique domains and metrics for the heatmap
    const domains = new Set();
    const metrics = new Set();
    const domainMetrics = new Set();

    correlations.forEach(corr => {
        domains.add(corr.domain1);
        domains.add(corr.domain2);
        metrics.add(corr.metric1);
        metrics.add(corr.metric2);
        domainMetrics.add(`${corr.domain1}:${corr.metric1}`);
        domainMetrics.add(`${corr.domain2}:${corr.metric2}`);
    });

    // Convert to arrays and sort
    const domainMetricsArray = Array.from(domainMetrics).sort();

    // Prepare heatmap data
    const heatmapData = [];

    // Create a matrix of all domain:metric combinations
    for (let i = 0; i < domainMetricsArray.length; i++) {
        const [domain1, metric1] = domainMetricsArray[i].split(':');

        for (let j = 0; j < domainMetricsArray.length; j++) {
            const [domain2, metric2] = domainMetricsArray[j].split(':');

            // Skip self-correlations
            if (i === j) continue;

            // Find if this correlation exists
            const correlation = correlations.find(
                c => (c.domain1 === domain1 && c.metric1 === metric1 &&
                     c.domain2 === domain2 && c.metric2 === metric2) ||
                    (c.domain1 === domain2 && c.metric1 === metric2 &&
                     c.domain2 === domain1 && c.metric2 === metric1)
            );

            // Only add if correlation exists
            if (correlation) {
                heatmapData.push([
                    i, // x-axis index
                    j, // y-axis index
                    correlation.correlation // value
                ]);
            }
        }
    }

    // Create heatmap with Highcharts
    try {
        Highcharts.chart(heatmapContainer, {
            chart: {
                type: 'heatmap',
                margin: [60, 10, 80, 80],
                backgroundColor: 'transparent'
            },
            title: {
                text: null
            },
            xAxis: {
                categories: domainMetricsArray.map(dm => {
                    const [domain, metric] = dm.split(':');
                    return `${domain}:<br>${metric}`;
                }),
                title: null,
                labels: {
                    useHTML: true
                }
            },
            yAxis: {
                categories: domainMetricsArray.map(dm => {
                    const [domain, metric] = dm.split(':');
                    return `${domain}: ${metric}`;
                }),
                title: null
            },
            colorAxis: {
                min: -1,
                max: 1,
                stops: [
                    [0, '#c4463a'], // deep red for strong negative correlation
                    [0.25, '#F8696B'], // light red for weak negative correlation
                    [0.5, '#F5F5F5'], // white for no correlation
                    [0.75, '#63BE7B'], // light green for weak positive correlation
                    [1, '#277f2a'] // deep green for strong positive correlation
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
                    const [domain1, metric1] = domainMetricsArray[this.point.x].split(':');
                    const [domain2, metric2] = domainMetricsArray[this.point.y].split(':');
                    return `<b>${domain1} (${metric1}) ↔ ${domain2} (${metric2})</b><br>` +
                           `Correlation: <b>${this.point.value.toFixed(2)}</b>`;
                }
            },
            series: [{
                name: 'Correlation',
                borderWidth: 1,
                data: heatmapData,
                dataLabels: {
                    enabled: true,
                    color: '#000000',
                    style: {
                        textOutline: 'none'
                    },
                    formatter: function () {
                        return this.point.value !== null ? this.point.value.toFixed(2) : '';
                    }
                }
            }]
        });
    } catch (error) {
        console.error('Error creating heatmap:', error);
        heatmapContainer.innerHTML = `
            <div class="alert alert-danger">
                Error creating heatmap visualization: ${error.message}
            </div>
        `;
    }
}

/**
 * Update correlation network visualization
 */
function updateCorrelationNetwork(correlations) {
    const networkContainer = document.getElementById('correlation-network');
    if (!networkContainer) return;

    // Clear any existing content
    networkContainer.innerHTML = '';

    // If no data, show a message
    if (!correlations || correlations.length === 0) {
        networkContainer.innerHTML = `
            <div class="alert alert-info">
                No correlation data available for the selected filters.
            </div>
        `;
        return;
    }

    // Calculate node sizes based on their total correlation strength
    const nodeStrengths = {};
    correlations.forEach(corr => {
        const key1 = `${corr.domain1}:${corr.metric1}`;
        const key2 = `${corr.domain2}:${corr.metric2}`;

        nodeStrengths[key1] = (nodeStrengths[key1] || 0) + Math.abs(corr.correlation);
        nodeStrengths[key2] = (nodeStrengths[key2] || 0) + Math.abs(corr.correlation);
    });

    // Create nodes array
    const nodes = [];
    const nodeMap = {};

    Object.keys(nodeStrengths).forEach((key, index) => {
        const [domain, metric] = key.split(':');
        const node = {
            id: key,
            name: `${domain}: ${metric}`,
            domain: domain,
            metric: metric,
            color: getDomainColor(domain),
            marker: {
                radius: 7 + (nodeStrengths[key] * 5) // Size based on total correlation strength
            }
        };
        nodes.push(node);
        nodeMap[key] = index;
    });

    // Create links array
    const links = correlations.map(corr => {
        const source = `${corr.domain1}:${corr.metric1}`;
        const target = `${corr.domain2}:${corr.metric2}`;

        return {
            from: nodeMap[source],
            to: nodeMap[target],
            weight: Math.abs(corr.correlation) * 3, // Line width
            color: corr.correlation >= 0 ?
                   'rgba(99, 190, 123, ' + Math.abs(corr.correlation) + ')' : // Green for positive
                   'rgba(248, 105, 107, ' + Math.abs(corr.correlation) + ')', // Red for negative
            dashStyle: corr.correlation >= 0 ? 'solid' : 'shortdash'
        };
    });

    // Create network chart with Highcharts
    try {
        const isAnimated = document.getElementById('animated-network-toggle')?.checked || false;

        Highcharts.chart(networkContainer, {
            chart: {
                type: 'networkgraph',
                height: '100%',
                backgroundColor: 'transparent'
            },
            title: {
                text: null
            },
            plotOptions: {
                networkgraph: {
                    keys: ['from', 'to', 'weight'],
                    layoutAlgorithm: {
                        enableSimulation: isAnimated,
                        integration: 'verlet',
                        linkLength: 100,
                        friction: -0.9
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    const node = this.point;
                    const connectedNodes = this.series.nodes.filter(n =>
                        this.series.data.some(link =>
                            (link.from === node.index && link.to === n.index) ||
                            (link.to === node.index && link.from === n.index)
                        )
                    );

                    let tooltip = `<b>${node.name}</b><br>`;

                    if (connectedNodes.length > 0) {
                        tooltip += 'Connected to:<br>';
                        connectedNodes.forEach(connectedNode => {
                            if (connectedNode.index !== node.index) {
                                const link = this.series.data.find(link =>
                                    (link.from === node.index && link.to === connectedNode.index) ||
                                    (link.to === node.index && link.from === connectedNode.index)
                                );

                                const correlation = link ? link.weight / 3 : 0;
                                const sign = link && link.color.includes('190') ? '+' : '-';
                                tooltip += `${connectedNode.name}: ${sign}${correlation.toFixed(2)}<br>`;
                            }
                        });
                    }

                    return tooltip;
                }
            },
            series: [{
                dataLabels: {
                    enabled: true,
                    linkFormat: '',
                    allowOverlap: false,
                    style: {
                        textOutline: 'none'
                    }
                },
                nodes: nodes,
                data: links
            }]
        });
    } catch (error) {
        console.error('Error creating network visualization:', error);
        networkContainer.innerHTML = `
            <div class="alert alert-danger">
                Error creating network visualization: ${error.message}
            </div>
        `;
    }
}

/**
 * Update correlation table
 */
function updateCorrelationTable(correlations) {
    const tableBody = document.getElementById('correlation-table-body');
    if (!tableBody) return;

    // Clear the table body
    tableBody.innerHTML = '';

    // If no data, show a message
    if (!correlations || correlations.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center">No correlation data available for the selected filters.</td>
            </tr>
        `;
        return;
    }

    // Populate the table
    correlations.forEach(corr => {
        const row = document.createElement('tr');

        // Determine the strength label
        let strengthLabel = 'Weak';
        if (Math.abs(corr.correlation) > 0.7) {
            strengthLabel = 'Strong';
        } else if (Math.abs(corr.correlation) >= 0.4) {
            strengthLabel = 'Moderate';
        }

        row.innerHTML = `
            <td>${corr.domain1}</td>
            <td>${corr.metric1}</td>
            <td>${corr.domain2}</td>
            <td>${corr.metric2}</td>
            <td><span class="badge ${getCorrelationClass(corr.correlation)}">${corr.correlation.toFixed(2)}</span></td>
            <td>${strengthLabel}</td>
            <td>${corr.confidence ? (corr.confidence * 100).toFixed(0) + '%' : 'N/A'}</td>
        `;

        tableBody.appendChild(row);
    });

    // Set up the view toggle buttons
    const viewToggleButtons = document.querySelectorAll('.correlation-view-toggle');
    const heatmapView = document.getElementById('correlation-heatmap');
    const tableView = document.getElementById('correlation-table');

    viewToggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const view = this.getAttribute('data-view');

            // Remove active class from all buttons
            viewToggleButtons.forEach(btn => btn.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            // Show the appropriate view
            if (view === 'heatmap') {
                heatmapView.style.display = 'block';
                tableView.style.display = 'none';
            } else if (view === 'table') {
                heatmapView.style.display = 'none';
                tableView.style.display = 'block';
            }
        });
    });
}

/**
 * Update the temporal correlation chart
 */
function updateTemporalCorrelationChart() {
    const chartContainer = document.getElementById('temporal-correlation-chart');
    if (!chartContainer) return;

    console.log('Updating temporal correlation chart');

    // Get the selected correlation pair
    const correlationPairSelect = document.getElementById('temporal-correlation-pair');
    const selectedPair = correlationPairSelect ? correlationPairSelect.value : 'weather_temperature-transportation_congestion';

    // Parse the pair
    const [domain1Metric1, domain2Metric2] = selectedPair.split('-');
    const [domain1, metric1] = domain1Metric1.split('_');
    const [domain2, metric2] = domain2Metric2.split('_');

    // Generate demo data for the temporal chart
    const timeRangeSelector = document.getElementById('timeRangeSelector');
    const timeRange = timeRangeSelector ? timeRangeSelector.value : '1d';

    console.log(`Temporal correlation chart using time range: ${timeRange}`);

    // Determine number of data points based on time range
    let dataPoints = 24;
    switch(timeRange) {
        case '1h': dataPoints = 60; break; // 60 minutes
        case '6h': dataPoints = 72; break; // 12 data points per hour
        case '1d': dataPoints = 24; break; // 24 hours
        case '7d': dataPoints = 168; break; // 7 days with hourly data
        case '30d': dataPoints = 30; break; // 30 days
        case '90d': dataPoints = 90; break; // 90 days
        case '180d': dataPoints = 180; break; // 180 days
        case '365d': dataPoints = 52; break; // Weekly data for a year
    }

    // Generate dates based on time range
    const dates = [];
    const now = new Date();

    if (timeRange === '1h') {
        // Generate minutes
        for (let i = 0; i < dataPoints; i++) {
            const date = new Date(now);
            date.setMinutes(date.getMinutes() - (dataPoints - i));
            dates.push(date);
        }
    } else if (timeRange === '6h') {
        // Generate 5-minute intervals
        for (let i = 0; i < dataPoints; i++) {
            const date = new Date(now);
            date.setMinutes(date.getMinutes() - (dataPoints - i) * 5);
            dates.push(date);
        }
    } else if (timeRange === '1d') {
        // Generate hourly data
        for (let i = 0; i < dataPoints; i++) {
            const date = new Date(now);
            date.setHours(date.getHours() - (dataPoints - i));
            dates.push(date);
        }
    } else if (timeRange === '7d') {
        // Generate hourly data for 7 days
        for (let i = 0; i < dataPoints; i++) {
            const date = new Date(now);
            date.setHours(date.getHours() - (dataPoints - i));
            dates.push(date);
        }
    } else {
        // Generate daily data
        for (let i = 0; i < dataPoints; i++) {
            const date = new Date(now);
            date.setDate(date.getDate() - (dataPoints - i));
            dates.push(date);
        }
    }

    // Generate series data
    const basePattern = [0.3, 0.32, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.82, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3];
    const pattern = [];

    // Generate realistic looking correlation data with some noise and trends
    for (let i = 0; i < dataPoints; i++) {
        const baseIndex = i % basePattern.length;
        const baseValue = basePattern[baseIndex];
        const noise = (Math.random() - 0.5) * 0.1; // Random noise between -0.05 and 0.05

        // Add some trend based on time range
        let trend = 0;
        if (timeRange === '30d' || timeRange === '90d') {
            trend = i / dataPoints * 0.2; // Slight upward trend for monthly data
        } else if (timeRange === '180d' || timeRange === '365d') {
            // Seasonal pattern for longer time ranges
            trend = Math.sin(i / dataPoints * Math.PI * 2) * 0.15;
        }

        // Combine base pattern, noise and trend, ensuring value is between -1 and 1
        let value = baseValue + noise + trend;
        value = Math.max(-1, Math.min(1, value));

        pattern.push(value);
    }

    // Create chart data
    const data = dates.map((date, i) => [date.getTime(), pattern[i]]);

    // Create the chart
    try {
        Highcharts.chart(chartContainer, {
            chart: {
                type: 'spline',
                backgroundColor: 'transparent'
            },
            title: {
                text: null
            },
            xAxis: {
                type: 'datetime',
                labels: {
                    formatter: function() {
                        if (timeRange === '1h' || timeRange === '6h') {
                            return Highcharts.dateFormat('%H:%M', this.value);
                        } else if (timeRange === '1d' || timeRange === '7d') {
                            return Highcharts.dateFormat('%H:%M', this.value);
                        } else {
                            return Highcharts.dateFormat('%b %e', this.value);
                        }
                    }
                }
            },
            yAxis: {
                title: {
                    text: 'Correlation Coefficient'
                },
                min: -1,
                max: 1,
                plotLines: [{
                    value: 0,
                    color: 'gray',
                    dashStyle: 'shortdash',
                    width: 1
                }]
            },
            tooltip: {
                formatter: function() {
                    const formattedDate = timeRange === '1h' || timeRange === '6h' ?
                        Highcharts.dateFormat('%H:%M', this.x) :
                        Highcharts.dateFormat('%b %e, %Y %H:%M', this.x);

                    return `<b>${domain1} (${metric1}) ↔ ${domain2} (${metric2})</b><br>` +
                           `Time: ${formattedDate}<br>` +
                           `Correlation: <b>${this.y.toFixed(2)}</b>`;
                }
            },
            plotOptions: {
                series: {
                    marker: {
                        enabled: false,
                        symbol: 'circle',
                        radius: 2
                    },
                    lineWidth: 2,
                    zones: [{
                        value: -0.7,
                        color: '#c4463a' // Strong negative
                    }, {
                        value: -0.4,
                        color: '#F8696B' // Moderate negative
                    }, {
                        value: -0.1,
                        color: '#FFAAAA' // Weak negative
                    }, {
                        value: 0.1,
                        color: '#DDDDDD' // No correlation
                    }, {
                        value: 0.4,
                        color: '#AAFFAA' // Weak positive
                    }, {
                        value: 0.7,
                        color: '#63BE7B' // Moderate positive
                    }, {
                        color: '#277f2a' // Strong positive
                    }]
                }
            },
            series: [{
                name: `${domain1} ${metric1} ↔ ${domain2} ${metric2}`,
                data: data
            }]
        });
    } catch (error) {
        console.error('Error creating temporal correlation chart:', error);
        chartContainer.innerHTML = `
            <div class="alert alert-danger">
                Error creating chart: ${error.message}
            </div>
        `;
    }
}

/**
 * Get a textual description of a correlation
 */
function getCorrelationDescription(correlation) {
    const corrValue = correlation.correlation;
    const domain1 = correlation.domain1;
    const metric1 = correlation.metric1;
    const domain2 = correlation.domain2;
    const metric2 = correlation.metric2;

    let relationshipType;
    if (corrValue > 0.7) {
        relationshipType = "Strong positive correlation";
    } else if (corrValue > 0.4) {
        relationshipType = "Moderate positive correlation";
    } else if (corrValue > 0.1) {
        relationshipType = "Weak positive correlation";
    } else if (corrValue > -0.1) {
        relationshipType = "No significant correlation";
    } else if (corrValue > -0.4) {
        relationshipType = "Weak negative correlation";
    } else if (corrValue > -0.7) {
        relationshipType = "Moderate negative correlation";
    } else {
        relationshipType = "Strong negative correlation";
    }

    return `${relationshipType} between ${domain1} ${metric1} and ${domain2} ${metric2}. `;
}

/**
 * Get color for a domain
 */
function getDomainColor(domain) {
    const domainColors = {
        'Weather': '#4285F4',
        'Economic': '#EA4335',
        'Transportation': '#FBBC05',
        'Social': '#34A853',
        'Social Media': '#34A853',
        'Energy': '#7B3FC9'
    };

    return domainColors[domain] || '#999999';
}

/**
 * Get display text for time range
 */
function getTimeRangeDisplay(timeRange) {
    switch(timeRange) {
        case '1h': return 'last hour';
        case '6h': return 'last 6 hours';
        case '1d': return 'last 24 hours';
        case '7d': return 'last 7 days';
        case '30d': return 'last 30 days';
        case '90d': return 'last 90 days';
        case '180d': return 'last 180 days';
        case '365d': return 'last year';
        default: return 'selected time period';
    }
}

/**
 * Cache management function to prune old items when cache is full
 */
function manageCacheSize() {
    if (!config.storage.useLocalStorage || !window.localStorage) {
        return;
    }

    try {
        // Get all cache keys
        const cacheKeys = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('dashboardData_') || key.startsWith('correlationData_')) {
                cacheKeys.push(key);
            }
        }

        // If we have too many items, remove the oldest ones
        if (cacheKeys.length > config.storage.maxCacheItems) {
            console.log('Pruning cache items, current count:', cacheKeys.length);

            // Get timestamps for each item
            const itemAges = [];
            for (const key of cacheKeys) {
                try {
                    const data = JSON.parse(localStorage.getItem(key));
                    itemAges.push({
                        key: key,
                        timestamp: data.timestamp || 0
                    });
                } catch (e) {
                    // If we can't parse it, mark it for removal with timestamp 0
                    itemAges.push({
                        key: key,
                        timestamp: 0
                    });
                }
            }

            // Sort by timestamp (oldest first)
            itemAges.sort((a, b) => a.timestamp - b.timestamp);

            // Remove oldest items to get back to max size
            const itemsToRemove = itemAges.slice(0, itemAges.length - config.storage.maxCacheItems);
            for (const item of itemsToRemove) {
                console.log('Removing cache item:', item.key);
                localStorage.removeItem(item.key);
            }
        }
    } catch (error) {
        console.error('Error managing cache size:', error);
    }
}

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
 * Set up socket connections for real-time updates
 */
function setupSocketConnections() {
    console.log('Setting up socket connections...');
    
    // Check if Socket.IO is available
    if (typeof io === 'undefined') {
        console.warn('Socket.IO is not available. Real-time updates will be disabled.');
        
        // Change connection status indicator
        const connectionStatus = document.getElementById('connectionStatus');
        if (connectionStatus) {
            connectionStatus.className = 'badge bg-warning me-2';
            connectionStatus.textContent = 'Offline Mode';
        }
        
        return;
    }
    
    try {
        // Connect to the Socket.IO server
        const socket = io.connect(window.location.origin, {
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            timeout: 20000
        });
        
        // Connection established
        socket.on('connect', function() {
            console.log('Connected to Socket.IO server');
            
            // Update connection status
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                connectionStatus.className = 'badge bg-success me-2';
                connectionStatus.textContent = 'Connected';
            }
            
            // Request initial data
            socket.emit('request_update', { timeRange: dashboardState.settings.timeRange });
        });
        
        // Connection lost
        socket.on('disconnect', function() {
            console.warn('Disconnected from Socket.IO server');
            
            // Update connection status
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                connectionStatus.className = 'badge bg-danger me-2';
                connectionStatus.textContent = 'Disconnected';
                
                // Try to reconnect after a delay
                setTimeout(function() {
                    socket.connect();
                }, 5000);
            }
        });
        
        // Connection error
        socket.on('connect_error', function(error) {
            console.error('Socket.IO connection error:', error);
            
            // Update connection status
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                connectionStatus.className = 'badge bg-danger me-2';
                connectionStatus.textContent = 'Connection Error';
            }
            
            // Show a user-friendly message
            showErrorMessage('Unable to establish real-time connection. Using cached data.');
        });
        
        // Handle dashboard updates
        socket.on('dashboard_update', function(data) {
            console.log('Received real-time dashboard update:', data);
            
            // Update the dashboard with the received data
            updateDashboardComponents(data);
            
            // Update last updated timestamp
            dashboardState.lastUpdated = new Date().getTime();
            updateLastUpdatedDisplay();
            
            // Flash the status to indicate data refresh
            const connectionStatus = document.getElementById('connectionStatus');
            if (connectionStatus) {
                const originalClass = connectionStatus.className;
                connectionStatus.className = 'badge bg-info me-2';
                
                setTimeout(function() {
                    connectionStatus.className = originalClass;
                }, 500);
            }
        });
        
        // Handle alerts
        socket.on('alert', function(alertData) {
            console.log('Received alert:', alertData);
            
            // Only show notifications if enabled in settings
            if (dashboardState.settings.notificationsEnabled) {
                // Create a notification if the browser supports it
                if ('Notification' in window) {
                    // Check if we already have permission
                    if (Notification.permission === 'granted') {
                        createNotification(alertData);
                    } else if (Notification.permission !== 'denied') {
                        // Request permission if not denied
                        Notification.requestPermission().then(function(permission) {
                            if (permission === 'granted') {
                                createNotification(alertData);
                            }
                        });
                    }
                }
                
                // Also update the alerts container on the page
                updateAlertsContainer(alertData);
            }
        });
        
        // Set up periodic data requests if auto-refresh is enabled
        setInterval(function() {
            if (socket.connected && dashboardState.settings.autoRefresh) {
                socket.emit('request_update', { timeRange: dashboardState.settings.timeRange });
            }
        }, config.refreshInterval);
        
    } catch (error) {
        console.error('Error setting up Socket.IO connection:', error);
        
        // Update connection status
        const connectionStatus = document.getElementById('connectionStatus');
        if (connectionStatus) {
            connectionStatus.className = 'badge bg-danger me-2';
            connectionStatus.textContent = 'Connection Failed';
        }
        
        // Show an error message
        showErrorMessage('Failed to establish real-time connection. Using cached data.');
    }
}

/**
 * Create a notification
 */
function createNotification(alertData) {
    const notification = new Notification(alertData.title || 'Dashboard Alert', {
        body: alertData.message || 'No additional information available',
        icon: '/static/img/notification-icon.png'
    });
    
    notification.onclick = function() {
        window.focus();
        
        // Navigate to the relevant tab if specified
        if (alertData.tabId) {
            const tabLink = document.querySelector(`[data-tab-target="#${alertData.tabId}"]`);
            if (tabLink) {
                tabLink.click();
            }
        }
        
        this.close();
    };
}

/**
 * Update alerts container
 */
function updateAlertsContainer(alertData) {
    const alertsContainer = document.getElementById('alertsContainer');
    if (!alertsContainer) return;
    
    // Create a new alert element
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${alertData.type || 'info'} alert-dismissible fade show`;
    alertElement.innerHTML = `
        <strong>${alertData.title || 'Alert'}</strong> ${alertData.message || ''}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to the alerts container
    alertsContainer.prepend(alertElement);
    
    // Update alert count badge
    const alertCount = document.getElementById('alertCount');
    if (alertCount) {
        const currentCount = parseInt(alertCount.textContent) || 0;
        alertCount.textContent = currentCount + 1;
    }
    
    // Auto-remove after 60 seconds
    setTimeout(function() {
        if (alertElement.parentNode) {
            alertElement.classList.remove('show');
            setTimeout(() => alertElement.remove(), 500);
            
            // Update alert count badge
            if (alertCount) {
                const newCount = parseInt(alertCount.textContent) || 0;
                if (newCount > 0) {
                    alertCount.textContent = newCount - 1;
                }
            }
        }
    }, 60000);
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

/**
 * Get a weather icon based on the condition
 */
function getWeatherIcon(condition) {
    if (!condition) return 'bi-thermometer-half';

    condition = condition.toLowerCase();

    if (condition.includes('sun') || condition.includes('clear')) {
        return 'bi-sun-fill';
    } else if (condition.includes('cloud') && condition.includes('part')) {
        return 'bi-cloud-sun-fill';
    } else if (condition.includes('cloud')) {
        return 'bi-cloud-fill';
    } else if (condition.includes('rain') || condition.includes('shower')) {
        return 'bi-cloud-rain-fill';
    } else if (condition.includes('storm') || condition.includes('thunder')) {
        return 'bi-cloud-lightning-rain-fill';
    } else if (condition.includes('snow')) {
        return 'bi-snow';
    } else if (condition.includes('fog') || condition.includes('mist')) {
        return 'bi-cloud-haze-fill';
    } else if (condition.includes('wind')) {
        return 'bi-wind';
    } else {
        return 'bi-thermometer-half';
    }
}

/**
 * Update system metrics displays
 */
function updateSystemMetrics(healthData) {
    console.log('Updating system metrics with:', healthData);

    // If no health data provided, use default values
    if (!healthData) {
        healthData = {
            uptime: 3600,
            processing_rate: 42.5,
            components: { api: true, ml: true, viz: true, integration: true },
            queue_size: 0
        };
    }

    // Update system uptime
    const systemUptime = document.getElementById('systemUptime');
    if (systemUptime) {
        systemUptime.textContent = formatUptime(healthData.uptime || 0);
    }

    // Update processing rate
    const processingRate = document.getElementById('processingRate');
    if (processingRate) {
        processingRate.textContent = (healthData.processing_rate || 0).toFixed(2);
    }

    // Update component count
    const componentCount = document.getElementById('componentCount');
    if (componentCount) {
        const count = healthData.components ? Object.keys(healthData.components).length : 0;
        componentCount.textContent = count.toString();
    }

    // Update queue size
    const queueSize = document.getElementById('queueSize');
    if (queueSize) {
        queueSize.textContent = (healthData.queue_size || 0).toString();
    }
}

// Initialize dashboard when the DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);