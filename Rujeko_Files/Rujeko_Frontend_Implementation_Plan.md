# Cross-Domain Predictive Analytics Dashboard - Frontend Implementation

## Overview

This document outlines the implementation plan for the frontend components of the Cross-Domain Predictive Analytics Dashboard. As the Frontend Development lead, I (Rujeko) am responsible for designing and implementing the user interface, creating a responsive design, implementing interactive components, developing customization features, and designing intuitive controls for prediction scenarios.

## Technology Stack

- **Framework**: Flask (Python backend)
- **Frontend Languages**: HTML5, CSS3, JavaScript (ES6+)
- **CSS Framework**: Bootstrap 5
- **JavaScript Libraries**: 
  - jQuery for DOM manipulation
  - Chart.js for basic visualizations
  - D3.js for advanced visualizations (will integrate with Emmanuel's work)
  - Moment.js for time manipulation
- **Icons**: Font Awesome
- **AJAX/WebSockets**: For real-time updates (will integrate with Ade's work)

## Implementation Timeline

### Week 1: Initial Setup and Basic Layout
- Set up project structure
- Implement base templates and layouts
- Create responsive grid system
- Develop navigation components
- Implement basic styling

### Week 2: Interactive Components
- Develop dashboard widgets
- Implement data filters
- Create customization controls
- Build prediction scenario interfaces
- Integrate with API endpoints (coordinating with Julie)

### Week 3: Refinement and Integration
- Integrate visualization components (coordinating with Emmanuel)
- Implement real-time updates (coordinating with Ade)
- Connect ML prediction controls (coordinating with Chao)
- User testing and refinement
- Documentation

## Component Design

### 1. Dashboard Layout

The dashboard will use a modular, widget-based design that allows for:
- Drag-and-drop rearrangement
- Resizable components
- Collapsible sections
- Customizable themes
- Savable configurations

### 2. Navigation System

- Side navigation for main sections
- Top navigation for user controls, notifications, and quick actions
- Breadcrumb navigation for deeper pages
- Mobile-responsive collapsible menu

### 3. Data Filtering Components

- Date range selectors with presets
- Multi-select dropdown filters
- Search functionality
- Tag-based filtering
- Saved filter presets

### 4. Visualization Containers

- Widget containers for charts and graphs
- Expandable view options
- Export controls (PDF, PNG, CSV)
- Annotation capabilities
- Sharing options

### 5. Prediction Scenario Controls

- Slider controls for adjusting parameters
- "What-if" scenario builder
- Confidence indicator displays
- Comparison views for multiple scenarios
- Scenario saving and loading

## Code Implementations

### Base HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-Domain Analytics Dashboard</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
</head>
<body class="dashboard-body">
    <!-- Sidebar Navigation -->
    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h3>Analytics Dashboard</h3>
            <button class="btn btn-link sidebar-toggle d-md-none" id="sidebarCollapseBtn">
                <i class="fas fa-bars"></i>
            </button>
        </div>
        <ul class="sidebar-menu">
            <li class="sidebar-item active">
                <a href="{{ url_for('dashboard') }}">
                    <i class="fas fa-tachometer-alt"></i>
                    <span>Dashboard</span>
                </a>
            </li>
            <li class="sidebar-item">
                <a href="{{ url_for('predictions') }}">
                    <i class="fas fa-chart-line"></i>
                    <span>Predictions</span>
                </a>
            </li>
            <li class="sidebar-item">
                <a href="{{ url_for('data_sources') }}">
                    <i class="fas fa-database"></i>
                    <span>Data Sources</span>
                </a>
            </li>
            <li class="sidebar-item">
                <a href="{{ url_for('settings') }}">
                    <i class="fas fa-cog"></i>
                    <span>Settings</span>
                </a>
            </li>
        </ul>
    </div>

    <!-- Main Content -->
    <div class="main-content" id="mainContent">
        <!-- Top Navigation -->
        <nav class="navbar navbar-expand navbar-light bg-white topbar">
            <div class="container-fluid">
                <button class="btn btn-link sidebar-toggle d-md-none" id="sidebarToggleTop">
                    <i class="fas fa-bars"></i>
                </button>
                
                <!-- Search Bar -->
                <form class="d-none d-sm-inline-block form-inline me-auto">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Search for..." aria-label="Search">
                        <button class="btn btn-primary" type="button">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                </form>
                
                <!-- Top Navbar Items -->
                <ul class="navbar-nav ms-auto">
                    <!-- Alerts -->
                    <li class="nav-item dropdown">
                        <a class="nav-link" href="#" id="alertsDropdown" role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-bell"></i>
                            <span class="badge bg-danger badge-counter">3+</span>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
                            <!-- Alert items will be dynamically populated -->
                        </div>
                    </li>
                    
                    <!-- User Profile -->
                    <li class="nav-item dropdown">
                        <a class="nav-link" href="#" id="userDropdown" role="button" data-bs-toggle="dropdown">
                            <span class="d-none d-lg-inline me-2 text-gray-600">User Name</span>
                            <img class="img-profile rounded-circle" src="{{ url_for('static', filename='img/user.png') }}">
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
                            <a class="dropdown-item" href="{{ url_for('profile') }}">
                                <i class="fas fa-user fa-sm fa-fw me-2 text-gray-400"></i>
                                Profile
                            </a>
                            <a class="dropdown-item" href="{{ url_for('settings') }}">
                                <i class="fas fa-cogs fa-sm fa-fw me-2 text-gray-400"></i>
                                Settings
                            </a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="{{ url_for('logout') }}">
                                <i class="fas fa-sign-out-alt fa-sm fa-fw me-2 text-gray-400"></i>
                                Logout
                            </a>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>
        
        <!-- Page Content -->
        <div class="container-fluid dashboard-container">
            <!-- Breadcrumb -->
            <div class="d-sm-flex align-items-center justify-content-between mb-4">
                <h1 class="h3 mb-0 text-gray-800">{% block page_title %}Dashboard{% endblock %}</h1>
                <nav aria-label="breadcrumb">
                    <ol class="breadcrumb">
                        {% block breadcrumb %}
                        <li class="breadcrumb-item"><a href="{{ url_for('dashboard') }}">Home</a></li>
                        <li class="breadcrumb-item active" aria-current="page">Dashboard</li>
                        {% endblock %}
                    </ol>
                </nav>
            </div>
            
            <!-- Main Content Area -->
            <div class="dashboard-content">
                {% block content %}
                <!-- Default content will be overridden by child templates -->
                <div class="row">
                    <!-- Dashboard widgets will go here -->
                </div>
                {% endblock %}
            </div>
        </div>
    </div>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- jQuery -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Moment.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
    <!-- Custom Scripts -->
    <script src="{{ url_for('static', filename='js/dashboard.js') }}"></script>
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Dashboard CSS (dashboard.css)

```css
/* Dashboard Layout */
:root {
    --sidebar-width: 250px;
    --topbar-height: 60px;
    --primary-color: #4e73df;
    --secondary-color: #858796;
    --success-color: #1cc88a;
    --info-color: #36b9cc;
    --warning-color: #f6c23e;
    --danger-color: #e74a3b;
    --light-color: #f8f9fc;
    --dark-color: #5a5c69;
}

body {
    font-family: 'Nunito', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f8f9fc;
    overflow-x: hidden;
}

/* Sidebar Styles */
.sidebar {
    width: var(--sidebar-width);
    background: linear-gradient(180deg, var(--primary-color) 10%, #224abe 100%);
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    z-index: 1;
    min-height: 100vh;
    position: fixed;
    transition: all 0.3s;
}

.sidebar-header {
    padding: 1rem;
    text-align: center;
    color: white;
}

.sidebar-menu {
    padding: 0;
    list-style: none;
}

.sidebar-item {
    position: relative;
}

.sidebar-item a {
    display: flex;
    align-items: center;
    padding: 0.75rem 1.5rem;
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: all 0.3s;
}

.sidebar-item a:hover {
    color: white;
    background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-item.active a {
    color: white;
    font-weight: 600;
    background-color: rgba(255, 255, 255, 0.1);
}

.sidebar-item a i {
    margin-right: 0.5rem;
    width: 1.25rem;
    text-align: center;
}

/* Main Content Styles */
.main-content {
    margin-left: var(--sidebar-width);
    padding-top: var(--topbar-height);
    width: calc(100% - var(--sidebar-width));
    min-height: 100vh;
    transition: all 0.3s;
}

/* Topbar Styles */
.topbar {
    height: var(--topbar-height);
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    background-color: white;
    position: fixed;
    width: calc(100% - var(--sidebar-width));
    z-index: 1;
    transition: all 0.3s;
}

.dashboard-container {
    padding: 1.5rem;
}

/* Dashboard Widgets */
.widget {
    background-color: white;
    border-radius: 0.35rem;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    margin-bottom: 1.5rem;
}

.widget-header {
    padding: 0.75rem 1.25rem;
    border-bottom: 1px solid #e3e6f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.widget-title {
    margin: 0;
    font-size: 1rem;
    font-weight: 700;
    color: var(--dark-color);
}

.widget-content {
    padding: 1.25rem;
}

/* Data Filters */
.filter-bar {
    background-color: white;
    padding: 1rem;
    border-radius: 0.35rem;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15);
    margin-bottom: 1.5rem;
}

.filter-group {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    align-items: center;
}

/* Responsive Design */
@media (max-width: 768px) {
    .sidebar {
        margin-left: calc(var(--sidebar-width) * -1);
    }
    
    .sidebar.active {
        margin-left: 0;
    }
    
    .main-content {
        margin-left: 0;
        width: 100%;
    }
    
    .main-content.active {
        margin-left: var(--sidebar-width);
        width: calc(100% - var(--sidebar-width));
    }
    
    .topbar {
        width: 100%;
    }
    
    .topbar.active {
        width: calc(100% - var(--sidebar-width));
    }
}

/* Custom Dashboard Components */
.prediction-slider {
    width: 100%;
    margin: 1rem 0;
}

.confidence-indicator {
    display: flex;
    align-items: center;
    margin: 0.5rem 0;
}

.confidence-indicator .indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
}

.confidence-indicator .high {
    background-color: var(--success-color);
}

.confidence-indicator .medium {
    background-color: var(--warning-color);
}

.confidence-indicator .low {
    background-color: var(--danger-color);
}

/* Widget Drag & Drop */
.draggable-widget {
    cursor: move;
}

.widget-placeholder {
    border: 2px dashed #cccccc;
    background-color: #f8f9fc;
    min-height: 100px;
    margin-bottom: 1.5rem;
    border-radius: 0.35rem;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}
```

### Dashboard JavaScript (dashboard.js)

```javascript
/**
 * Cross-Domain Predictive Analytics Dashboard
 * Main JavaScript file for dashboard functionality
 */

// Initialize dashboard components when DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeWidgets();
    initializeFilters();
    initializePredictionControls();
    initializeCharts();
    setupRealTimeUpdates();
});

// Sidebar Toggle Functionality
function initializeSidebar() {
    const sidebarToggleTop = document.getElementById('sidebarToggleTop');
    const sidebarCollapseBtn = document.getElementById('sidebarCollapseBtn');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const topbar = document.querySelector('.topbar');
    
    function toggleSidebar() {
        sidebar.classList.toggle('active');
        mainContent.classList.toggle('active');
        topbar.classList.toggle('active');
    }
    
    if (sidebarToggleTop) {
        sidebarToggleTop.addEventListener('click', toggleSidebar);
    }
    
    if (sidebarCollapseBtn) {
        sidebarCollapseBtn.addEventListener('click', toggleSidebar);
    }
    
    // Collapse sidebar on small screens by default
    if (window.innerWidth < 768) {
        sidebar.classList.remove('active');
        mainContent.classList.remove('active');
        topbar.classList.remove('active');
    }
}

// Initialize Dashboard Widgets
function initializeWidgets() {
    // Make widgets draggable and resizable if jQuery UI is available
    if (typeof $.fn.draggable !== 'undefined' && typeof $.fn.resizable !== 'undefined') {
        $('.draggable-widget').draggable({
            handle: '.widget-header',
            containment: '.dashboard-content',
            snap: '.widget-placeholder',
            snapMode: 'outer',
            revert: 'invalid'
        });
        
        $('.resizable-widget').resizable({
            handles: 'se',
            minHeight: 100,
            minWidth: 200,
            maxWidth: 800
        });
        
        // Set up widget dropzones
        $('.widget-dropzone').droppable({
            accept: '.draggable-widget',
            activeClass: 'dropzone-active',
            hoverClass: 'dropzone-hover',
            drop: function(event, ui) {
                // Handle widget dropping logic
                const widgetId = ui.draggable.attr('id');
                const dropzoneId = $(this).attr('id');
                
                // Save widget position in user preferences
                saveWidgetPosition(widgetId, dropzoneId);
            }
        });
    }
    
    // Widget collapsible functionality
    const collapseButtons = document.querySelectorAll('.widget-collapse-btn');
    collapseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const widget = this.closest('.widget');
            const content = widget.querySelector('.widget-content');
            const icon = this.querySelector('i');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.classList.remove('fa-plus');
                icon.classList.add('fa-minus');
            } else {
                content.style.display = 'none';
                icon.classList.remove('fa-minus');
                icon.classList.add('fa-plus');
            }
            
            // Save widget state in user preferences
            const widgetId = widget.id;
            saveWidgetState(widgetId, content.style.display === 'none');
        });
    });
    
    // Widget removal functionality
    const removeButtons = document.querySelectorAll('.widget-remove-btn');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const widget = this.closest('.widget');
            const widgetId = widget.id;
            
            if (confirm('Are you sure you want to remove this widget? You can add it back from the widget gallery.')) {
                widget.remove();
                // Save widget removal in user preferences
                saveWidgetRemoval(widgetId);
            }
        });
    });
}

// Initialize Data Filters
function initializeFilters() {
    // Date range picker initialization
    if (typeof $.fn.daterangepicker !== 'undefined') {
        $('.date-range-picker').daterangepicker({
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            },
            startDate: moment().subtract(29, 'days'),
            endDate: moment()
        }, function(start, end, label) {
            // When date range changes, update dashboards
            updateDashboardData(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
        });
    }
    
    // Custom select initialization
    if (typeof $.fn.select2 !== 'undefined') {
        $('.custom-select').select2({
            theme: 'bootstrap4',
            placeholder: 'Select options',
            allowClear: true
        });
        
        // When selection changes, update dashboard
        $('.custom-select').on('change', function() {
            const filterId = $(this).attr('id');
            const selectedValues = $(this).val();
            
            updateDashboardFilters(filterId, selectedValues);
        });
    }
    
    // Save Filter Button
    const saveFilterBtn = document.getElementById('saveFilterBtn');
    if (saveFilterBtn) {
        saveFilterBtn.addEventListener('click', function() {
            const filterName = prompt('Enter a name for this filter preset:');
            if (filterName) {
                // Collect all current filter values
                const filterValues = collectFilterValues();
                
                // Save to user preferences
                saveFilterPreset(filterName, filterValues);
                
                // Add to filter preset dropdown
                addFilterPresetToDropdown(filterName);
            }
        });
    }
    
    // Load Filter Presets
    loadFilterPresets();
}

// Initialize Prediction Controls
function initializePredictionControls() {
    // Slider controls for prediction parameters
    const sliders = document.querySelectorAll('.prediction-slider');
    sliders.forEach(slider => {
        slider.addEventListener('input', function() {
            const paramId = this.id;
            const value = this.value;
            const valueDisplay = document.querySelector(`#${paramId}-value`);
            
            if (valueDisplay) {
                valueDisplay.textContent = value;
            }
            
            // Update prediction model with new parameter
            updatePredictionModel(paramId, value);
        });
    });
    
    // Scenario saving functionality
    const saveScenarioBtn = document.getElementById('saveScenarioBtn');
    if (saveScenarioBtn) {
        saveScenarioBtn.addEventListener('click', function() {
            const scenarioName = prompt('Enter a name for this scenario:');
            if (scenarioName) {
                // Collect all current prediction parameters
                const scenarioParams = collectScenarioParameters();
                
                // Save to user preferences
                saveScenario(scenarioName, scenarioParams);
                
                // Add to scenario dropdown
                addScenarioToDropdown(scenarioName);
            }
        });
    }
    
    // Run prediction button
    const runPredictionBtn = document.getElementById('runPredictionBtn');
    if (runPredictionBtn) {
        runPredictionBtn.addEventListener('click', function() {
            const params = collectScenarioParameters();
            
            // Show loading indicator
            showLoadingIndicator();
            
            // Call prediction API
            fetchPrediction(params)
                .then(response => {
                    // Update prediction results
                    updatePredictionResults(response);
                    
                    // Hide loading indicator
                    hideLoadingIndicator();
                })
                .catch(error => {
                    console.error('Error fetching prediction:', error);
                    // Show error message
                    showErrorMessage('Failed to fetch prediction results. Please try again.');
                    
                    // Hide loading indicator
                    hideLoadingIndicator();
                });
        });
    }
    
    // Load saved scenarios
    loadSavedScenarios();
}

// Initialize Charts
function initializeCharts() {
    // Sample chart initialization using Chart.js
    const chartElements = document.querySelectorAll('.dashboard-chart');
    chartElements.forEach(chartElement => {
        const chartId = chartElement.id;
        const chartType = chartElement.dataset.chartType || 'line';
        const chartContext = chartElement.getContext('2d');
        
        // Fetch initial chart data
        fetchChartData(chartId)
            .then(data => {
                // Create chart with data
                createChart(chartContext, chartType, data);
            })
            .catch(error => {
                console.error(`Error fetching data for chart ${chartId}:`, error);
                // Show error message in chart container
                showChartError(chartElement);
            });
    });
}

// Set up real-time updates (will integrate with Ade's work)
function setupRealTimeUpdates() {
    // Check if socket.io is available
    if (typeof io !== 'undefined') {
        // Connect to WebSocket server
        const socket = io();
        
        // Listen for real-time data updates
        socket.on('data_update', function(data) {
            // Update relevant dashboard components with new data
            updateDashboardWithRealTimeData(data);
        });
        
        // Listen for prediction updates
        socket.on('prediction_update', function(data) {
            // Update prediction results with new data
            updatePredictionResults(data);
        });
        
        // Listen for alert notifications
        socket.on('alert_notification', function(data) {
            // Show notification to user
            showNotification(data);
        });
    } else {
        // Fallback to AJAX polling if WebSockets are not available
        setupAjaxPolling();
    }
}

// Helper function to create a Chart.js chart
function createChart(context, type, data) {
    return new Chart(context, {
        type: type,
        data: data.chartData,
        options: data.chartOptions || {
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

// Helper function to fetch chart data from API
function fetchChartData(chartId) {
    return fetch(`/api/chart-data/${chartId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
}

// Helper function to update prediction model
function updatePredictionModel(paramId, value) {
    // This will be connected to Chao's ML model
    console.log(`Updating prediction model: ${paramId} = ${value}`);
    
    // Make API call to update model parameter
    fetch('/api/prediction/update-param', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            param_id: paramId,
            value: value
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update confidence indicators
        updateConfidenceIndicators(data.confidence);
        
        // Update prediction preview if available
        if (data.preview) {
            updatePredictionPreview(data.preview);
        }
    })
    .catch(error => {
        console.error('Error updating prediction model:', error);
    });
}

// Helper function to collect all filter values
function collectFilterValues() {
    const filters = {};
    
    // Date range
    const dateRange = $('.date-range-picker').data('daterangepicker');
    if (dateRange) {
        filters.startDate = dateRange.startDate.format('YYYY-MM-DD');
        filters.endDate = dateRange.endDate.format('YYYY-MM-DD');
    }
    
    // Select filters
    document.querySelectorAll('.filter-select').forEach(select => {
        filters[select.id] = select.value;
    });
    
    // Checkbox filters
    document.querySelectorAll('.filter-checkbox:checked').forEach(checkbox => {
        if (!filters[checkbox.name]) {
            filters[checkbox.name] = [];
        }
        filters[checkbox.name].push(checkbox.value);
    });
    
    return filters;
}

// Helper function to collect scenario parameters
function collectScenarioParameters() {
    const params = {};
    
    // Get all sliders and their values
    document.querySelectorAll('.prediction-slider').forEach(slider => {
        params[slider.id] = slider.value;
    });
    
    // Get all other input parameters
    document.querySelectorAll('.prediction-param').forEach(input => {
        params[input.id] = input.value;
    });
    
    return params;
}

// Helper function to save widget position in user preferences
function saveWidgetPosition(widgetId, dropzoneId) {
    // Make API call to save widget position
    fetch('/api/user/preferences/widget-position', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            widget_id: widgetId,
            dropzone_id: dropzoneId
        })
    })
    .catch(error => {
        console.error('Error saving widget position:', error);
    });
}

// Helper function to save widget state (collapsed/expanded)
function saveWidgetState(widgetId, isCollapsed) {
    // Make API call to save widget state
    fetch('/api/user/preferences/widget-state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            widget_id: widgetId,
            is_collapsed: isCollapsed
        })
    })
    .catch(error => {
        console.error('Error saving widget state:', error);
    });
}

// Helper function to save widget removal
function saveWidgetRemoval(widgetId) {
    // Make API call to save widget removal
    fetch('/api/user/preferences/widget-removal', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            widget_id: widgetId
        })
    })
    .catch(error => {
        console.error('Error saving widget removal:', error);
    });
}

// Helper function to save filter preset
function saveFilterPreset(name, values) {
    // Make API call to save filter preset
    fetch('/api/user/preferences/filter-preset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            values: values
        })
    })
    .catch(error => {
        console.error('Error saving filter preset:', error);
    });
}

// Helper function to add filter preset to dropdown
function addFilterPresetToDropdown(name) {
    const dropdown = document.getElementById('filterPresetDropdown');
    if (dropdown) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.setAttribute('href', '#');
        option.setAttribute('data-preset', name);
        option.textContent = name;
        
        option.addEventListener('click', function(e) {
            e.preventDefault();
            loadFilterPreset(name);
        });
        
        dropdown.appendChild(option);
    }
}

// Helper function to load filter presets
function loadFilterPresets() {
    // Make API call to get saved filter presets
    fetch('/api/user/preferences/filter-presets')
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            const dropdown = document.getElementById('filterPresetDropdown');
            if (dropdown) {
                // Keep only the default options
                const defaultOptions = dropdown.querySelectorAll('.default-option');
                dropdown.innerHTML = '';
                
                defaultOptions.forEach(option => {
                    dropdown.appendChild(option);
                });
                
                // Add divider if there are presets
                if (data.presets && data.presets.length > 0) {
                    const divider = document.createElement('div');
                    divider.classList.add('dropdown-divider');
                    dropdown.appendChild(divider);
                    
                    // Add each preset
                    data.presets.forEach(preset => {
                        addFilterPresetToDropdown(preset.name);
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error loading filter presets:', error);
        });
}

// Helper function to load a specific filter preset
function loadFilterPreset(name) {
    // Make API call to get preset values
    fetch(`/api/user/preferences/filter-preset/${encodeURIComponent(name)}`)
        .then(response => response.json())
        .then(data => {
            // Apply filter values
            applyFilterValues(data.values);
            
            // Update dashboard with new filters
            updateDashboardWithFilters(data.values);
        })
        .catch(error => {
            console.error(`Error loading filter preset ${name}:`, error);
        });
}

// Helper function to apply filter values to UI
function applyFilterValues(values) {
    // Date range
    if (values.startDate && values.endDate) {
        const dateRange = $('.date-range-picker').data('daterangepicker');
        if (dateRange) {
            dateRange.setStartDate(values.startDate);
            dateRange.setEndDate(values.endDate);
        }
    }
    
    // Select filters
    Object.keys(values).forEach(key => {
        const element = document.getElementById(key);
        if (element && element.tagName === 'SELECT') {
            element.value = values[key];
            
            // Trigger change event for custom selects
            if (typeof $.fn.select2 !== 'undefined' && $(element).hasClass('custom-select')) {
                $(element).trigger('change');
            }
        }
    });
    
    // Checkbox filters
    document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
        if (values[checkbox.name] && Array.isArray(values[checkbox.name])) {
            checkbox.checked = values[checkbox.name].includes(checkbox.value);
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
    });
}

// Helper function to add scenario to dropdown
function addScenarioToDropdown(name) {
    const dropdown = document.getElementById('scenarioDropdown');
    if (dropdown) {
        const option = document.createElement('a');
        option.classList.add('dropdown-item');
        option.setAttribute('href', '#');
        option.setAttribute('data-scenario', name);
        option.textContent = name;
        
        option.addEventListener('click', function(e) {
            e.preventDefault();
            loadScenario(name);
        });
        
        dropdown.appendChild(option);
    }
}

// Helper function to load saved scenarios
function loadSavedScenarios() {
    // Make API call to get saved scenarios
    fetch('/api/user/preferences/scenarios')
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            const dropdown = document.getElementById('scenarioDropdown');
            if (dropdown) {
                // Keep only the default options
                const defaultOptions = dropdown.querySelectorAll('.default-option');
                dropdown.innerHTML = '';
                
                defaultOptions.forEach(option => {
                    dropdown.appendChild(option);
                });
                
                // Add divider if there are scenarios
                if (data.scenarios && data.scenarios.length > 0) {
                    const divider = document.createElement('div');
                    divider.classList.add('dropdown-divider');
                    dropdown.appendChild(divider);
                    
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

// Helper function to load a specific scenario
function loadScenario(name) {
    // Make API call to get scenario parameters
    fetch(`/api/user/preferences/scenario/${encodeURIComponent(name)}`)
        .then(response => response.json())
        .then(data => {
            // Apply scenario parameters
            applyScenarioParameters(data.params);
            
            // Update prediction model with new parameters
            updatePredictionModelWithParams(data.params);
        })
        .catch(error => {
            console.error(`Error loading scenario ${name}:`, error);
        });
}

// Helper function to apply scenario parameters to UI
function applyScenarioParameters(params) {
    // Apply to sliders
    Object.keys(params).forEach(key => {
        const element = document.getElementById(key);
        if (element && element.classList.contains('prediction-slider')) {
            element.value = params[key];
            
            // Update value display
            const valueDisplay = document.querySelector(`#${key}-value`);
            if (valueDisplay) {
                valueDisplay.textContent = params[key];
            }
        } else if (element && element.classList.contains('prediction-param')) {
            element.value = params[key];
        }
    });
}

// Helper function to update prediction model with multiple parameters
function updatePredictionModelWithParams(params) {
    // Make API call to update model with all parameters
    fetch('/api/prediction/update-params', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            params: params
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update confidence indicators
        updateConfidenceIndicators(data.confidence);
        
        // Update prediction preview if available
        if (data.preview) {
            updatePredictionPreview(data.preview);
        }
    })
    .catch(error => {
        console.error('Error updating prediction model with parameters:', error);
    });
}

// Helper function to show loading indicator
function showLoadingIndicator() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
}

// Helper function to hide loading indicator
function hideLoadingIndicator() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }
}

// Helper function to show error message
function showErrorMessage(message) {
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

// Helper function to update confidence indicators
function updateConfidenceIndicators(confidence) {
    const confidenceElement = document.getElementById('confidenceIndicator');
    if (confidenceElement) {
        // Remove all existing classes
        confidenceElement.classList.remove('high', 'medium', 'low');
        
        // Add appropriate class based on confidence level
        if (confidence >= 0.7) {
            confidenceElement.classList.add('high');
            confidenceElement.textContent = 'High Confidence';
        } else if (confidence >= 0.4) {
            confidenceElement.classList.add('medium');
            confidenceElement.textContent = 'Medium Confidence';
        } else {
            confidenceElement.classList.add('low');
            confidenceElement.textContent = 'Low Confidence';
        }
    }
}

// Helper function to update prediction preview
function updatePredictionPreview(preview) {
    const previewContainer = document.getElementById('predictionPreview');
    if (previewContainer) {
        // Update with preview data
        // This will depend on the specific format of the preview data
        // For example, it might update a chart or display text predictions
        
        // For a chart preview
        if (preview.chartData && window.previewChart) {
            window.previewChart.data = preview.chartData;
            window.previewChart.update();
        }
        
        // For text predictions
        if (preview.textPrediction) {
            const textElement = previewContainer.querySelector('.prediction-text');
            if (textElement) {
                textElement.textContent = preview.textPrediction;
            }
        }
    }
}

// Function to handle fetching prediction results
function fetchPrediction(params) {
    return fetch('/api/prediction/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            params: params
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    });
}

// Function to update prediction results UI
function updatePredictionResults(results) {
    const resultsContainer = document.getElementById('predictionResults');
    if (!resultsContainer) return;
    
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    // Create results visualization based on the type of prediction
    if (results.type === 'time-series') {
        createTimeSeriesVisualization(resultsContainer, results);
    } else if (results.type === 'classification') {
        createClassificationVisualization(resultsContainer, results);
    } else if (results.type === 'regression') {
        createRegressionVisualization(resultsContainer, results);
    } else if (results.type === 'clustering') {
        createClusteringVisualization(resultsContainer, results);
    } else {
        // Generic results display
        createGenericResultsDisplay(resultsContainer, results);
    }
    
    // Show the results container
    resultsContainer.style.display = 'block';
}

// Function to create time series visualization
function createTimeSeriesVisualization(container, results) {
    // Create canvas for chart
    const canvas = document.createElement('canvas');
    canvas.id = 'timeSeriesChart';
    container.appendChild(canvas);
    
    // Create chart using Chart.js
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: results.timestamps,
            datasets: [{
                label: 'Historical Data',
                data: results.historicalData,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderWidth: 1,
                pointRadius: 1,
                fill: true
            }, {
                label: 'Predicted Data',
                data: results.predictedData,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top',
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
                        text: results.xAxisLabel || 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: results.yAxisLabel || 'Value'
                    }
                }
            }
        }
    });
    
    // Add confidence indicator
    const confidenceElement = document.createElement('div');
    confidenceElement.classList.add('confidence-indicator');
    
    const indicator = document.createElement('span');
    indicator.classList.add('indicator');
    
    if (results.confidence >= 0.7) {
        indicator.classList.add('high');
    } else if (results.confidence >= 0.4) {
        indicator.classList.add('medium');
    } else {
        indicator.classList.add('low');
    }
    
    const confidenceText = document.createElement('span');
    confidenceText.textContent = `Prediction Confidence: ${Math.round(results.confidence * 100)}%`;
    
    confidenceElement.appendChild(indicator);
    confidenceElement.appendChild(confidenceText);
    container.appendChild(confidenceElement);
}

// Function to create classification visualization
function createClassificationVisualization(container, results) {
    // Create canvas for chart
    const canvas = document.createElement('canvas');
    canvas.id = 'classificationChart';
    container.appendChild(canvas);
    
    // Create chart using Chart.js
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: results.categories,
            datasets: [{
                label: 'Probability',
                data: results.probabilities,
                backgroundColor: results.probabilities.map(value => {
                    if (value >= 0.7) return 'rgba(75, 192, 192, 0.8)';
                    if (value >= 0.4) return 'rgba(255, 206, 86, 0.8)';
                    return 'rgba(255, 99, 132, 0.8)';
                }),
                borderColor: results.probabilities.map(value => {
                    if (value >= 0.7) return 'rgba(75, 192, 192, 1)';
                    if (value >= 0.4) return 'rgba(255, 206, 86, 1)';
                    return 'rgba(255, 99, 132, 1)';
                }),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: results.title || 'Classification Prediction'
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
    
    // Add predicted class
    const predictedElement = document.createElement('div');
    predictedElement.classList.add('predicted-class');
    predictedElement.innerHTML = `<strong>Predicted Class:</strong> ${results.predictedClass}`;
    container.appendChild(predictedElement);
}

// Fallback polling function if WebSockets are not available
function setupAjaxPolling() {
    // Poll for data updates every 30 seconds
    setInterval(() => {
        fetch('/api/data/updates')
            .then(response => response.json())
            .then(data => {
                // Update dashboard with new data
                updateDashboardWithRealTimeData(data);
            })
            .catch(error => {
                console.error('Error polling for updates:', error);
            });
    }, 30000);
    
    // Poll for prediction updates every 60 seconds
    setInterval(() => {
        fetch('/api/prediction/updates')
            .then(response => response.json())
            .then(data => {
                // Update prediction results with new data
                updatePredictionResults(data);
            })
            .catch(error => {
                console.error('Error polling for prediction updates:', error);
            });
    }, 60000);
}

// Update dashboard with real-time data
function updateDashboardWithRealTimeData(data) {
    // Update charts
    if (data.chartUpdates) {
        Object.keys(data.chartUpdates).forEach(chartId => {
            const chartInstance = Chart.getChart(chartId);
            if (chartInstance) {
                chartInstance.data = data.chartUpdates[chartId];
                chartInstance.update();
            }
        });
    }
    
    // Update metrics
    if (data.metricUpdates) {
        Object.keys(data.metricUpdates).forEach(metricId => {
            const metricElement = document.getElementById(metricId);
            if (metricElement) {
                metricElement.textContent = data.metricUpdates[metricId];
            }
        });
    }
    
    // Update alerts
    if (data.alerts && data.alerts.length > 0) {
        data.alerts.forEach(alert => {
            showNotification(alert);
        });
    }
}

// Function to show notification
function showNotification(data) {
    // Create notification element
    const notification = document.createElement('div');
    notification.classList.add('toast');
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'assertive');
    notification.setAttribute('aria-atomic', 'true');
    
    // Add appropriate styling based on notification type
    notification.classList.add(`toast-${data.type || 'info'}`);
    
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
        new bootstrap.Toast(notification).show();
        
        // Remove from DOM after hiding
        notification.addEventListener('hidden.bs.toast', function() {
            notification.remove();
        });
    }
}