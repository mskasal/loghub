/*global define*/
define([
    'jquery',
    'backbone',
    'collections/collection',
    'common',
    'views/login'
], function($, Backbone, Collection, Common, LoginView) {
    'use strict';

    var MyRouter = Backbone.Router.extend({
        routes: {
            'dashboard': 'dashboard',
            'login': 'login'
        },
        initialize: function() {
            console.log("routing")
        },
        dashboard: function() {
            console.log("at dashboard")
        },
        login: function() {
            console.log('login')
            var loginView = new LoginView();
            $('#mainContainer').html(loginView.render().el);
        }
    });

    return MyRouter;
});