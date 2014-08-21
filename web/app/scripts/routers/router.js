/*global define*/
define([
    'backbone',
    'collections/applications',
    'collections/logs',
    'collections/alarms',
    'common',
    'models/alarmsModel',
    'views/alarmsView',
    'models/loginModel',
    'views/loginView',
    'models/logsModel',
    'views/logsView',
    'models/dashboardModel',
    'views/dashboardView',
    'views/applicationsView',
    'logger'
], function(Backbone, Applications, Logs, Alarms, Common, AlarmsModel, AlarmsView, LoginModel, LoginView, LogsModel, LogsView, DashboardModel, DashboardView, ApplicationsView, Logger) {
    'use strict';

    var MyRouter = Backbone.Router.extend({

        /**
         * define roots and callbacks
         */
        routes: {
            '': 'index',
            'dashboard': 'dashboard',
            'dashboard/applications': 'applications',
            'dashboard/alarms': 'alarms',
            'dashboard/logs': 'logs',
            'dashboard/users': 'users',
            'login': 'login'
        },

        /**
         * Initialize route
         */
        initialize: function() {

            if (!this.dashboardModel)
                this.dashboardModel = new DashboardModel();
            if (!this.dashboardView) {
                this.dashboardView = new DashboardView({
                    model: this.dashboardModel
                });
            }
            this.dashboardView.render();
            Logger.i("Route Initialized");
        },

        /**
         * Navigating dashboard, callback
         */
        dashboard: function(page) {
            
            Logger.i("Navigating Dashboard");

            this.dashboardView.render();
        },

        /**
         * Navigating index, callback
         */
        index: function() {
            Logger.i("Navigating Index");
        },

        /**
         * Navigating login, callback
         */
        login: function() {

            if (!this.loginModel)
                this.loginModel = new LoginModel();
            if (!this.loginView)
                this.loginView = new LoginView({
                    model: this.loginModel
                });
            this.loginView.render();

            Logger.i("Navigating Login");
        },

        /**
         * Navigating applications, callback
         */
        applications: function() {
            if (!this.applicationsView)
                this.applicationsView = new ApplicationsView({
                    collection: Applications
                });

            this.applicationsView.render();

            Logger.i("Navigating Applications");
        },

        /**
         * Navigating users, callback
         */
        users: function() {

            Logger.i("Navigating Users");
        },

        /**
         * Navigating logs, callback
         */
        logs: function() {

            Logger.i("Navigating Logs");

            if (!this.logsView)
                this.logsView = new LogsView({
                    collection: Logs
                });

            this.logsView.render();
        },

        /**
         * Navigating alarms, callback
         */
        alarms: function() {

            Logger.i("Navigating Alarms");

            if (!this.alarmsView)
                this.alarmsView = new AlarmsView({
                    collection: Alarms
                });

            this.alarmsView.render();
        }
    });

    return MyRouter;
});