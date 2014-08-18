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
        routes: {
            '': 'index',
            'dashboard': 'dashboard',
            'dashboard/applications': 'applications',
            'dashboard/alarms': 'alarms',
            'dashboard/logs': 'logs',
            'dashboard/users': 'users',
            'login': 'login'
        },
        initialize: function() {
            Logs.add([{
                    "APP_TOKEN": "1",
                    "message": "1",
                    "level": "info",
                    "date": "1",
                    "metadata": "1"
                }, {
                    "APP_TOKEN": "2",
                    "message": "2",
                    "level": "info",
                    "date": "2",
                    "metadata": "2"
                }, {
                    "APP_TOKEN": "3",
                    "message": "3",
                    "level": "info",
                    "date": "3",
                    "metadata": "3"
                }, {
                    "APP_TOKEN": "4",
                    "message": "4",
                    "level": "info",
                    "date": "4",
                    "metadata": "4"
                }

            ], {
                merge: true
            })

            Applications.add([{
                "id": "1",
                "name": "MyUberWebsite",
                "createdAt": "2014-03-18 20:16:32",
                "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
            }, {
                "id": "2",
                "name": "MyUberWebsite",
                "createdAt": "2014-03-18 20:16:32",
                "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
            }, {
                "id": "3",
                "name": "MyUberWebsite",
                "createdAt": "2014-03-18 20:16:32",
                "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
            }, {
                "id": "4",
                "name": "MyUberWebsite",
                "createdAt": "2014-03-18 20:16:32",
                "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
            }, {
                "id": "5",
                "name": "MyUberWebsite",
                "createdAt": "2014-03-18 20:16:32",
                "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
            }], {
                merge: true
            });

            Alarms.add([{
                "id": "1"
            }, {
                "id": "2"
            }, {
                "id": "3"
            }, {
                "id": "4"
            }, {
                "id": "5"
            }, {
                "id": "6"
            }], {
                merge: true
            })

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

            this.dashboardView.render();
            Logger.i("Navigating Dashboard");
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
        logs: function() {
            if (!this.logsView)
                this.logsView = new LogsView({
                    collection: Logs
                });

            this.logsView.render();
            Logger.i("Navigating Logs");
        },
        alarms: function() {
            if (!this.alarmsView)
                this.alarmsView = new AlarmsView({
                    collection: Alarms
                });

            this.alarmsView.render();
            Logger.i("Navigating Alarms");
        }
    });

    return MyRouter;
});