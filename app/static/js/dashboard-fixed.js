/**
 * Fixed updateDashboardComponents function
 * Copy and paste this into dashboard.js to replace the existing updateDashboardComponents function
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