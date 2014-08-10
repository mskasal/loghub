/*global define*/
define([
    'backbone',
    'collections/collection',
    'common',
    'models/loginStatus',
    'views/login',
    'models/dashboardModel',
    'views/dashboard',
    'logger'
], function(Backbone, Collection, Common, LoginStatusModel, LoginView, DashboardModel, DashboardView, Logger) {
    'use strict';

    var MyRouter = Backbone.Router.extend({
        routes: {
            '': 'index',
            'dashboard': 'dashboard',
            'login': 'login'
        },
        initialize: function() {
            console.log("routing")
        },
        /**
         * Navigating dashboard, callback
         */
        dashboard: function() {
            Logger.i("Navigating Dashboard")
            console.log("at dashboard")
            var dashboardView = new DashboardView({
                model: new DashboardModel()
            });
        },
        index: function() {
            console.log("index")
        },

        /**
         * Navigating to login page,callback
         */
        login: function() {
            console.log('login')
            var loginView = new LoginView({
                model: new LoginStatusModel()
            });
        }
    });

    return MyRouter;
});