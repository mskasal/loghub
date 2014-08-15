/*global define*/
define([
    'backbone',
    'collections/applications',
    'common',
    'models/loginModel',
    'views/loginView',
    'models/dashboardModel',
    'views/dashboardView',
    'views/applicationsView',
    'logger'
], function(Backbone, Applications, Common, LoginModel, LoginView, DashboardModel, DashboardView, ApplicationsView, Logger) {
    'use strict';

    var MyRouter = Backbone.Router.extend({
        routes: {
            '': 'index',
            'dashboard': 'dashboard',
            'dashboard/applications': 'applications',
            'dashboard/users': 'users',
            'login': 'login'
        },
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

            this.dashboardView.render();
            Logger.i("Navigating Dashboard");
            if (this[page])
                this[page]();
            else
                this.dashboardView.navigateToSidebar("applications");
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
            Applications.add([{

                "id": "1",
                "name": "1",
                "createdAt": "1",
                "APP_TOKEN": "1"
            }, {

                "id": "2",
                "name": "2",
                "createdAt": "2",
                "APP_TOKEN": "2"
            }], {
                merge: true
            });

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
        }
    });

    return MyRouter;
});