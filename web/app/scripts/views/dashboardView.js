/*global define*/
define([
    'backbone',
    'text!templates/Dashboard.html',
    'views/alarmsView',
    'collections/alarms',
    'collections/applications',
    'views/applicationsView',
    'common',
    'logger'
], function(Backbone, dashboardTemplate, AlarmsView, Alarms, Applications, ApplicationsView, Common, Logger) {
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
            this.bind();
        },
        events: {
            "click .addapp": "openAddApp"
        },

        bind: function() {
            var that = this;

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

            var alarmsView = new AlarmsView({
                collection: Alarms
            });
            alarmsView.render();

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
        },

        openAddApp: function(event) {
            event.preventDefault();
            Backbone.history.navigate("dashboard/applications", {
                trigger: true
            })
        }

    });

    return Dashboard;
});