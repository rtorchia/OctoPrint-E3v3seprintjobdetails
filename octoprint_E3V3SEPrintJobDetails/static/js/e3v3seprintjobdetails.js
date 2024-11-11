// static/js/e3v3seprintjobdetails.js
$(function() {
    function E3v3seprintjobdetailsViewModel(parameters) {
        var self = this;
        self.settingsViewModel = parameters[0];
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: E3v3seprintjobdetailsViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#settings_plugin_E3V3SEPrintJobDetails"]
    });
});