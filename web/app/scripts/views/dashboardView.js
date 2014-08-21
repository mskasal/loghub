/*global define*/
define([
    'backbone',
    'text!templates/Dashboard.html',
    'common',
    'logger'
], function(Backbone, dashboardTemplate, Common, Logger) {
    'use strict';

    var Dashboard = Backbone.View.extend({

        tagName: 'div',
        className: 'container',
        id: 'maincontainer',

        initialize: function() {

            Logger.i("Dashboard View Initialized");
        },

        render: function(page) {

            this.$el.html(dashboardTemplate);

            $("#app").html(this.$el);

            Backbone.history.navigate("dashboard/logs", {
                trigger: true
            });

            this.bind();
        },
        
        events: {
            "click .addapp": "openAddApp"
        },

        bind: function() {
            var that = this;

            $('#dashboard-nav a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
                var target = e.target.hash.split("#")[1];

                Backbone.history.navigate("dashboard/" + target, {
                    trigger: true
                })
            })
        },

        initializeAddApp: function(event) {
            event.preventDefault();

        },

        initializeNotification: function(event) {
            event.preventDefault();

        },

        initializeSettings: function(event) {
            event.preventDefault();

        }

    });

    return Dashboard;
});