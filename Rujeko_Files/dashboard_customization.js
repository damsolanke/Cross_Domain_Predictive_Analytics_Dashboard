/**
 * Cross-Domain Predictive Analytics Dashboard
 * Customization Page JavaScript
 * 
 * This script handles the dashboard customization functionality,
 * including theme settings, layout customization, and notification preferences.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize drag and drop functionality
    initializeDragDrop();
    
    // Initialize theme options
    initializeThemeOptions();
    
    // Initialize filter configuration
    initializeFilterConfiguration();
    
    // Initialize notification settings
    initializeNotificationSettings();
    
    // Set up save buttons
    setupSaveButtons();
});

// Initialize drag and drop functionality for dashboard widgets
function initializeDragDrop() {
    // Check if jQuery UI is available
    if (typeof $.fn.draggable !== 'undefined' && typeof $.fn.droppable !== 'undefined') {
        // Make widgets draggable
        $('.draggable-widget').draggable({
            helper: 'clone',
            connectToSortable: '.widget-dropzone',
            revert: 'invalid',
            start: function(event, ui) {
                ui.helper.addClass('widget-dragging');
            },
            stop: function(event, ui) {
                ui.helper.removeClass('widget-dragging');
            }
        });
        
        // Make dropzones droppable and sortable
        $('.widget-dropzone').sortable({
            placeholder: 'widget-placeholder',
            connectWith: '.widget-dropzone',
            receive: function(event, ui) {
                const widgetType = ui.item.data('widget-type');
                const zoneId = $(this).attr('id');
                
                // If dragging from widget gallery, replace with actual widget
                if (ui.item.parent().attr('id') !== 'widgetGallery') {
                    return;
                }
                
                // Replace placeholder with actual widget
                const widgetHtml = createWidgetHTML(widgetType);
                ui.item.replaceWith(widgetHtml);
                
                // Remove placeholder text if this is the first widget
                $(this).find('.dropzone-placeholder').hide();
                
                // Update layout configuration
                updateLayoutConfiguration();
            },
            remove: function(event, ui) {
                // Show placeholder text if no widgets remain
                if ($(this).children('.widget-preview').length === 0) {
                    $(this).find('.dropzone-placeholder').show();
                }
                
                // Update layout configuration
                updateLayoutConfiguration();
            },
            update: function(event, ui) {
                // Update layout configuration when order changes
                updateLayoutConfiguration();
            }
        }).droppable({
            accept: '.draggable-widget',
            activeClass: 'dropzone-active',
            hoverClass: 'dropzone-hover'
        });
        
        // Set up remove buttons for widgets
        $(document).on('click', '.widget-preview-remove', function() {
            const widget = $(this).closest('.widget-preview');
            const dropzone = widget.parent();
            
            widget.remove();
            
            // Show placeholder if no widgets remain
            if (dropzone.children('.widget-preview').length === 0) {
                dropzone.find('.dropzone-placeholder').show();
            }
            
            // Update layout configuration
            updateLayoutConfiguration();
        });
        
        // Load saved layout if available
        loadSavedLayout();
    } else {
        // Fallback for when jQuery UI is not available
        console.error('jQuery UI is required for drag and drop functionality.');
        $('#widgetGallery').after('<div class="alert alert-warning">Drag and drop functionality requires jQuery UI. Please include jQuery UI in your project.</div>');
    }
}

// Create HTML for a widget preview based on widget type
function createWidgetHTML(widgetType) {
    const widgetTitle = getWidgetTitle(widgetType);
    const widgetIcon = getWidgetIcon(widgetType);
    
    return `
        <div class="widget-preview" data-widget-type="${widgetType}">
            <div class="widget-preview-header">
                <span class="widget-preview-icon"><i class="${widgetIcon}"></i></span>
                <span class="widget-preview-title">${widgetTitle}</span>
                <div class="widget-preview-controls">
                    <button type="button" class="btn btn-sm btn-link widget-preview-remove">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="widget-preview-body">
                <div class="widget-preview-content">
                    <div class="text-center py-2">
                        <span class="text-muted">${widgetTitle} Content</span>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Get widget title based on widget type
function getWidgetTitle(widgetType) {
    switch (widgetType) {
        case 'weather':
            return 'Weather Data';
        case 'economic':
            return 'Economic Indicators';
        case 'social':
            return 'Social Media Trends';
        case 'transportation':
            return 'Transportation Metrics';
        case 'health':
            return 'Health Statistics';
        case 'energy':
            return 'Energy Consumption';
        case 'prediction':
            return 'Prediction Summary';
        case 'correlation':
            return 'Correlation Matrix';
        case 'alerts':
            return 'Alert Center';
        default:
            return 'Widget';
    }
}

// Get widget icon based on widget type
function getWidgetIcon(widgetType) {
    switch (widgetType) {
        case 'weather':
            return 'fas fa-cloud';
        case 'economic':
            return 'fas fa-chart-line';
        case 'social':
            return 'fas fa-hashtag';
        case 'transportation':
            return 'fas fa-car';
        case 'health':
            return 'fas fa-heartbeat';
        case 'energy':
            return 'fas fa-bolt';
        case 'prediction':
            return 'fas fa-brain';
        case 'correlation':
            return 'fas fa-link';
        case 'alerts':
            return 'fas fa-bell';
        default:
            return 'fas fa-cube';
    }
}

// Update layout configuration based on current widget placement
function updateLayoutConfiguration() {
    const layout = {
        header: getZoneWidgets('header-zone'),
        left: getZoneWidgets('left-zone'),
        right: getZoneWidgets('right-zone'),
        footer: getZoneWidgets('footer-zone')
    };
    
    // Store layout configuration
    localStorage.setItem('dashboardLayout', JSON.stringify(layout));
}

// Get widgets in a zone
function getZoneWidgets(zoneId) {
    const widgets = [];
    
    $(`#${zoneId} .widget-preview`).each(function() {
        widgets.push($(this).data('widget-type'));
    });
    
    return widgets;
}

// Load saved layout
function loadSavedLayout() {
    const savedLayout = localStorage.getItem('dashboardLayout');
    
    if (savedLayout) {
        const layout = JSON.parse(savedLayout);
        
        // Clear all dropzones
        $('.widget-dropzone').empty();
        
        // Add placeholders
        $('.widget-dropzone').append('<div class="dropzone-placeholder"><span>Drop widgets here</span></div>');
        
        // Populate zones with saved widgets
        populateZone('header-zone', layout.header);
        populateZone('left-zone', layout.left);
        populateZone('right-zone', layout.right);
        populateZone('footer-zone', layout.footer);
    }
}

// Populate a zone with widgets
function populateZone(zoneId, widgets) {
    if (!widgets || widgets.length === 0) return;
    
    const zone = $(`#${zoneId}`);
    
    // Hide placeholder
    zone.find('.dropzone-placeholder').hide();
    
    // Add widgets
    widgets.forEach(function(widgetType) {
        const widgetHtml = createWidgetHTML(widgetType);
        zone.append(widgetHtml);
    });
}

// Initialize theme options
function initializeThemeOptions() {
    // Theme selection
    $('.theme-option').click(function() {
        $('.theme-option').removeClass('active');
        $(this).addClass('active');
        
        const theme = $(this).data('theme');
        
        // Show/hide custom theme options
        if (theme === 'custom') {
            $('#customThemeOptions').show();
        } else {
            $('#customThemeOptions').hide();
            
            // Apply selected theme
            applyTheme(theme);
        }
    });
    
    // Color pickers
    $('input[type="color"]').on('input', function() {
        const colorHex = $(this).val();
        const hexInput = $(`#${$(this).attr('id')}Hex`);
        
        // Update hex input
        hexInput.val(colorHex);
    });
    
    // Hex inputs
    $('.input-group input[type="text"]').on('input', function() {
        const colorId = $(this).attr('id').replace('Hex', '');
        const colorPicker = $(`#${colorId}`);
        
        // Update color picker if valid hex
        const hexRegex = /^#[0-9A-F]{6}$/i;
        if (hexRegex.test($(this).val())) {
            colorPicker.val($(this).val());
        }
    });
    
    // Dark mode toggle
    $('#darkModeToggle').change(function() {
        if (this.checked) {
            $('body').addClass('dark-mode');
        } else {
            $('body').removeClass('dark-mode');
        }
    });
    
    // Load saved theme
    loadSavedTheme();
    
    // Apply theme button
    $('#applyThemeBtn').click(function() {
        const activeTheme = $('.theme-option.active').data('theme');
        
        if (activeTheme === 'custom') {
            applyCustomTheme();
        } else {
            applyTheme(activeTheme);
        }
        
        // Save theme settings
        saveThemeSettings();
        
        // Show success notification
        showNotification('success', 'Theme Applied', 'Theme settings have been applied successfully.');
    });
    
    // Reset layout button
    $('#resetLayoutBtn').click(function() {
        if (confirm('Are you sure you want to reset the dashboard layout to default? This action cannot be undone.')) {
            // Clear local storage
            localStorage.removeItem('dashboardLayout');
            
            // Reload page
            location.reload();
        }
    });
}

// Apply theme based on theme name
function applyTheme(theme) {
    // Reset any custom themes
    resetCustomTheme();
    
    // Apply selected theme
    $('body').removeClass('theme-default theme-dark theme-green theme-purple theme-orange theme-custom');
    $('body').addClass(`theme-${theme}`);
    
    // Update sidebar gradient for preview
    let primary, secondary;
    
    switch (theme) {
        case 'default':
            primary = '#4e73df';
            secondary = '#224abe';
            break;
        case 'dark':
            primary = '#3a3b45';
            secondary = '#1a1a24';
            break;
        case 'green':
            primary = '#1cc88a';
            secondary = '#13855c';
            break;
        case 'purple':
            primary = '#8B5CF6';
            secondary = '#6938C8';
            break;
        case 'orange':
            primary = '#fd7e14';
            secondary = '#c85e10';
            break;
    }
    
    // Update color inputs
    $('#primaryColor').val(primary);
    $('#primaryColorHex').val(primary);
    $('#secondaryColor').val(secondary);
    $('#secondaryColorHex').val(secondary);
}

// Apply custom theme based on color inputs
function applyCustomTheme() {
    const primaryColor = $('#primaryColor').val();
    const secondaryColor = $('#secondaryColor').val();
    const successColor = $('#successColor').val();
    const dangerColor = $('#dangerColor').val();
    
    // Apply custom CSS variables
    document.documentElement.style.setProperty('--primary-color', primaryColor);
    document.documentElement.style.setProperty('--secondary-color', secondaryColor);
    document.documentElement.style.setProperty('--success-color', successColor);
    document.documentElement.style.setProperty('--danger-color', dangerColor);
    
    // Add custom theme class
    $('body').removeClass('theme-default theme-dark theme-green theme-purple theme-orange');
    $('body').addClass('theme-custom');
}

// Reset custom theme
function resetCustomTheme() {
    // Remove custom CSS variables
    document.documentElement.style.removeProperty('--primary-color');
    document.documentElement.style.removeProperty('--secondary-color');
    document.documentElement.style.removeProperty('--success-color');
    document.documentElement.style.removeProperty('--danger-color');
}

// Save theme settings
function saveThemeSettings() {
    const settings = {
        theme: $('.theme-option.active').data('theme'),
        darkMode: $('#darkModeToggle').is(':checked'),
        fontSize: $('#fontSizeSelect').val(),
        layoutStyle: $('input[name="layoutStyle"]:checked').val(),
        animations: $('#animationsToggle').is(':checked'),
        collapsibleWidgets: $('#collapsibleWidgetsToggle').is(':checked'),
        stickyHeader: $('#stickyHeaderToggle').is(':checked'),
        customColors: {
            primary: $('#primaryColor').val(),
            secondary: $('#secondaryColor').val(),
            success: $('#successColor').val(),
            danger: $('#dangerColor').val()
        }
    };
    
    // Save to local storage
    localStorage.setItem('themeSettings', JSON.stringify(settings));
    
    // Make API call to save to user preferences
    fetch('/api/user/preferences/theme', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .catch(function(error) {
        console.error('Error saving theme settings:', error);
    });
}

// Load saved theme
function loadSavedTheme() {
    const savedTheme = localStorage.getItem('themeSettings');
    
    if (savedTheme) {
        const settings = JSON.parse(savedTheme);
        
        // Apply theme
        $(`.theme-option[data-theme="${settings.theme}"]`).click();
        
        // Apply other settings
        $('#darkModeToggle').prop('checked', settings.darkMode).trigger('change');
        $('#fontSizeSelect').val(settings.fontSize);
        $(`input[name="layoutStyle"][value="${settings.layoutStyle}"]`).prop('checked', true);
        $('#animationsToggle').prop('checked', settings.animations);
        $('#collapsibleWidgetsToggle').prop('checked', settings.collapsibleWidgets);
        $('#stickyHeaderToggle').prop('checked', settings.stickyHeader);
        
        // Apply custom colors if theme is custom
        if (settings.theme === 'custom') {
            $('#primaryColor').val(settings.customColors.primary);
            $('#primaryColorHex').val(settings.customColors.primary);
            $('#secondaryColor').val(settings.customColors.secondary);
            $('#secondaryColorHex').val(settings.customColors.secondary);
            $('#successColor').val(settings.customColors.success);
            $('#successColorHex').val(settings.customColors.success);
            $('#dangerColor').val(settings.customColors.danger);
            $('#dangerColorHex').val(settings.customColors.danger);
        }
    }
}

// Initialize filter configuration
function initializeFilterConfiguration() {
    // Default date range select
    $('#defaultDateRange').change(function() {
        if ($(this).val() === 'custom') {
            $('#customDateRangeFields').show();
        } else {
            $('#customDateRangeFields').hide();
        }
    });
    
    // Load preset button
    $('#loadPresetBtn').click(function() {
        const selectedPreset = $('#filterPresetsList').val();
        
        if (selectedPreset) {
            loadFilterPreset(selectedPreset);
        }
    });
    
    // Save preset button
    $('#savePresetBtn').click(function() {
        const presetName = prompt('Enter a name for this filter preset:');
        
        if (presetName && presetName.trim() !== '') {
            saveFilterPreset(presetName);
        }
    });
    
    // Rename preset button
    $('#renamePresetBtn').click(function() {
        const selectedPreset = $('#filterPresetsList').val();
        
        if (selectedPreset && selectedPreset !== 'default') {
            const newName = prompt('Enter a new name for this preset:', selectedPreset);
            
            if (newName && newName.trim() !== '' && newName !== selectedPreset) {
                renameFilterPreset(selectedPreset, newName);
            }
        } else {
            alert('Please select a custom preset to rename. Default presets cannot be renamed.');
        }
    });
    
    // Delete preset button
    $('#deletePresetBtn').click(function() {
        const selectedPreset = $('#filterPresetsList').val();
        
        if (selectedPreset && selectedPreset !== 'default') {
            if (confirm(`Are you sure you want to delete the "${selectedPreset}" preset? This action cannot be undone.`)) {
                deleteFilterPreset(selectedPreset);
            }
        } else {
            alert('Please select a custom preset to delete. Default presets cannot be deleted.');
        }
    });
    
    // Save filter settings button
    $('#saveFilterSettingsBtn').click(function() {
        saveFilterSettings();
        
        // Show success notification
        showNotification('success', 'Settings Saved', 'Filter settings have been saved successfully.');
    });
    
    // Load saved filter settings
    loadSavedFilterSettings();
}

// Load filter preset
function loadFilterPreset(presetName) {
    // Make API call to get preset
    fetch(`/api/user/preferences/filter-preset/${encodeURIComponent(presetName)}`)
        .then(response => response.json())
        .then(data => {
            // Apply filter settings
            applyFilterSettings(data);
            
            // Show success notification
            showNotification('success', 'Preset Loaded', `"${presetName}" preset has been loaded.`);
        })
        .catch(error => {
            console.error(`Error loading preset ${presetName}:`, error);
            showNotification('error', 'Load Failed', `Failed to load "${presetName}" preset.`);
        });
}

// Save filter preset
function saveFilterPreset(presetName) {
    // Collect current filter settings
    const settings = collectFilterSettings();
    
    // Make API call to save preset
    fetch('/api/user/preferences/filter-preset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: presetName,
            settings: settings
        })
    })
    .then(response => response.json())
    .then(data => {
        // Add to presets list if new
        addPresetToList(presetName);
        
        // Show success notification
        showNotification('success', 'Preset Saved', `"${presetName}" preset has been saved.`);
    })
    .catch(error => {
        console.error(`Error saving preset ${presetName}:`, error);
        showNotification('error', 'Save Failed', `Failed to save "${presetName}" preset.`);
    });
}

// Rename filter preset
function renameFilterPreset(oldName, newName) {
    // Make API call to rename preset
    fetch('/api/user/preferences/filter-preset/rename', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            oldName: oldName,
            newName: newName
        })
    })
    .then(response => response.json())
    .then(data => {
        // Update presets list
        updatePresetInList(oldName, newName);
        
        // Show success notification
        showNotification('success', 'Preset Renamed', `Preset renamed to "${newName}".`);
    })
    .catch(error => {
        console.error(`Error renaming preset from ${oldName} to ${newName}:`, error);
        showNotification('error', 'Rename Failed', `Failed to rename preset.`);
    });
}

// Delete filter preset
function deleteFilterPreset(presetName) {
    // Make API call to delete preset
    fetch(`/api/user/preferences/filter-preset/${encodeURIComponent(presetName)}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        // Remove from presets list
        removePresetFromList(presetName);
        
        // Show success notification
        showNotification('success', 'Preset Deleted', `"${presetName}" preset has been deleted.`);
    })
    .catch(error => {
        console.error(`Error deleting preset ${presetName}:`, error);
        showNotification('error', 'Delete Failed', `Failed to delete "${presetName}" preset.`);
    });
}

// Add preset to list
function addPresetToList(presetName) {
    const list = $('#filterPresetsList');
    const autoLoadList = $('#autoLoadPreset');
    
    // Check if already exists
    if (list.find(`option[value="${presetName}"]`).length === 0) {
        list.append(`<option value="${presetName}">${presetName}</option>`);
        autoLoadList.append(`<option value="${presetName}">${presetName}</option>`);
    }
    
    // Select the new preset
    list.val(presetName);
}

// Update preset in list
function updatePresetInList(oldName, newName) {
    const list = $('#filterPresetsList');
    const autoLoadList = $('#autoLoadPreset');
    
    // Update option
    list.find(`option[value="${oldName}"]`).val(newName).text(newName);
    autoLoadList.find(`option[value="${oldName}"]`).val(newName).text(newName);
    
    // Select the renamed preset
    list.val(newName);
}

// Remove preset from list
function removePresetFromList(presetName) {
    const list = $('#filterPresetsList');
    const autoLoadList = $('#autoLoadPreset');
    
    // Remove option
    list.find(`option[value="${presetName}"]`).remove();
    autoLoadList.find(`option[value="${presetName}"]`).remove();
    
    // Select default
    list.val('default');
    
    // Update auto-load if it was set to the deleted preset
    if (autoLoadList.val() === presetName) {
        autoLoadList.val('none');
    }
}

// Collect filter settings
function collectFilterSettings() {
    return {
        dateRange: $('#defaultDateRange').val(),
        customStartDate: $('#customStartDate').val(),
        customEndDate: $('#customEndDate').val(),
        dataSources: $('#defaultDataSources').val(),
        rememberFilters: $('#rememberFiltersCheck').is(':checked'),
        autoLoadPreset: $('#autoLoadPreset').val()
    };
}

// Apply filter settings
function applyFilterSettings(settings) {
    // Apply settings to form
    $('#defaultDateRange').val(settings.dateRange).trigger('change');
    $('#customStartDate').val(settings.customStartDate);
    $('#customEndDate').val(settings.customEndDate);
    $('#defaultDataSources').val(settings.dataSources);
    $('#rememberFiltersCheck').prop('checked', settings.rememberFilters);
    $('#autoLoadPreset').val(settings.autoLoadPreset);
}

// Save filter settings
function saveFilterSettings() {
    const settings = collectFilterSettings();
    
    // Save to local storage
    localStorage.setItem('filterSettings', JSON.stringify(settings));
    
    // Make API call to save to user preferences
    fetch('/api/user/preferences/filter-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .catch(function(error) {
        console.error('Error saving filter settings:', error);
    });
}

// Load saved filter settings
function loadSavedFilterSettings() {
    const savedSettings = localStorage.getItem('filterSettings');
    
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        applyFilterSettings(settings);
    }
    
    // Load filter presets from API
    fetch('/api/user/preferences/filter-presets')
        .then(response => response.json())
        .then(data => {
            // Clear custom presets
            $('#filterPresetsList option:not([value="default"]):not([value="weatherFocus"]):not([value="economicTrends"]):not([value="socialAnalysis"]):not([value="transportationMetrics"])').remove();
            $('#autoLoadPreset option:not([value="none"]):not([value="lastUsed"]):not([value="default"]):not([value="weatherFocus"]):not([value="economicTrends"]):not([value="socialAnalysis"]):not([value="transportationMetrics"])').remove();
            
            // Add custom presets
            if (data.presets && data.presets.length > 0) {
                data.presets.forEach(function(preset) {
                    if (!$('#filterPresetsList option[value="' + preset.name + '"]').length) {
                        $('#filterPresetsList').append(`<option value="${preset.name}">${preset.name}</option>`);
                        $('#autoLoadPreset').append(`<option value="${preset.name}">${preset.name}</option>`);
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error loading filter presets:', error);
        });
}

// Initialize notification settings
function initializeNotificationSettings() {
    // Confidence threshold slider
    $('#predictionConfidenceThreshold').on('input', function() {
        $('#confidenceThresholdValue').text(Math.round($(this).val() * 100) + '%');
    });
    
    // Anomaly threshold slider
    $('#anomalyThreshold').on('input', function() {
        $('#anomalyThresholdValue').text($(this).val() + 'σ');
    });
    
    // Correlation threshold slider
    $('#correlationStrengthThreshold').on('input', function() {
        $('#correlationThresholdValue').text($(this).val());
    });
    
    // Save notification settings button
    $('#saveNotificationSettingsBtn').click(function() {
        saveNotificationSettings();
        
        // Show success notification
        showNotification('success', 'Settings Saved', 'Notification settings have been saved successfully.');
    });
    
    // Load saved notification settings
    loadSavedNotificationSettings();
}

// Save notification settings
function saveNotificationSettings() {
    const settings = {
        confidenceThreshold: $('#predictionConfidenceThreshold').val(),
        anomalyThreshold: $('#anomalyThreshold').val(),
        correlationThreshold: $('#correlationStrengthThreshold').val(),
        alerts: {
            prediction: $('#predictionAlerts').is(':checked'),
            anomaly: $('#anomalyAlerts').is(':checked'),
            correlation: $('#correlationAlerts').is(':checked'),
            system: $('#systemAlerts').is(':checked')
        },
        priorityLevel: $('#alertPriorityLevel').val(),
        sound: $('#notificationSound').val(),
        desktop: $('#desktopNotifications').is(':checked')
    };
    
    // Save to local storage
    localStorage.setItem('notificationSettings', JSON.stringify(settings));
    
    // Make API call to save to user preferences
    fetch('/api/user/preferences/notification-settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .catch(function(error) {
        console.error('Error saving notification settings:', error);
    });
}

// Load saved notification settings
function loadSavedNotificationSettings() {
    const savedSettings = localStorage.getItem('notificationSettings');
    
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        
        // Apply settings to form
        $('#predictionConfidenceThreshold').val(settings.confidenceThreshold).trigger('input');
        $('#anomalyThreshold').val(settings.anomalyThreshold).trigger('input');
        $('#correlationStrengthThreshold').val(settings.correlationThreshold).trigger('input');
        $('#predictionAlerts').prop('checked', settings.alerts.prediction);
        $('#anomalyAlerts').prop('checked', settings.alerts.anomaly);
        $('#correlationAlerts').prop('checked', settings.alerts.correlation);
        $('#systemAlerts').prop('checked', settings.alerts.system);
        $('#alertPriorityLevel').val(settings.priorityLevel);
        $('#notificationSound').val(settings.sound);
        $('#desktopNotifications').prop('checked', settings.desktop);
    }
}

// Set up save buttons
function setupSaveButtons() {
    // Save layout button
    $('#saveLayoutBtn').click(function() {
        // Already saved by updateLayoutConfiguration(), just show notification
        showNotification('success', 'Layout Saved', 'Dashboard layout has been saved successfully.');
    });
}

// Show notification
function showNotification(type, title, message) {
    // Create notification element
    const notification = $(`
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `);
    
    // Add appropriate styling based on notification type
    if (type === 'success') {
        notification.addClass('bg-success text-white');
    } else if (type === 'error') {
        notification.addClass('bg-danger text-white');
    } else if (type === 'warning') {
        notification.addClass('bg-warning');
    } else {
        notification.addClass('bg-info text-white');
    }
    
    // Add to notification container
    $('#notificationContainer').append(notification);
    
    // Initialize toast
    const toast = new bootstrap.Toast(notification, {
        autohide: true,
        delay: 5000
    });
    
    // Show toast
    toast.show();
    
    // Remove from DOM after hiding
    notification.on('hidden.bs.toast', function() {
        notification.remove();
    });
}