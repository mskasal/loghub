require.config({
    paths: {
        jquery: "vendor/jquery/jquery",
        underscore: "vendor/underscore/underscore",
        backbone: "vendor/backbone/backbone",
        bootstrap: "vendor/bootstrap/js/bootstrap",
        bootstrapSelect: 'vendor/bootstrap-select/js/bootstrap-select',
        bootstrapDatepicker: 'vendor/datepicker/js/bootstrap-datepicker',
        logger: "vendor/logger/logger",
        mustache: "vendor/mustache/mustache",
        text: 'vendor/requirejs-text/text'
    },
    shim: {
        bootstrap: {
            deps: ['jquery']
        },
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'bootstrap'
            ],
            exports: 'Backbone'
        },
        backboneLocalstorage: {
            deps: ['backbone'],
            exports: 'Store'
        }
    }
});

require([
    'backbone',
    'views/app',
    'routers/router',
    'logger'
], function(Backbone, AppView, Workspace, Logger) {
    /*jshint nonew:false*/
    // Initialize routing and start Backbone.history()
    var route = new Workspace();
    Backbone.history.start();
    route.navigate(location.hash, true)
    Logger.start();
    Logger.i("Main Initialized");
    // Initialize the application view
    new AppView();
});