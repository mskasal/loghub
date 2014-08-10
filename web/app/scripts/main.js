require.config({
    paths: {
        jquery: "vendor/jquery/jquery",
        underscore: "vendor/underscore/underscore",
        backbone: "vendor/backbone/backbone",
        bootstrap: "vendor/bootstrap/js/bootstrap",
        logger: "vendor/logger/logger",
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
                'jquery',
                'logger'
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
    new Workspace();
    Backbone.history.start({});
    Logger.start();
    Logger.i("test loger")
    // Initialize the application view
    new AppView();
});