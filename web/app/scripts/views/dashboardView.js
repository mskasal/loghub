/*global define*/
define([
    'backbone',
    'text!templates/Dashboard.html',
    'views/alarmsView',
    'collections/alarms',
    'common',
    'logger'
], function(Backbone, dashboardTemplate, AlarmsView, Alarms, Common, Logger) {
    'use strict';

    var Dashboard = Backbone.View.extend({

        tagName: 'div',
        className: 'maincontainer',
        id: 'maincontainer',

        initialize: function() {
            Logger.i("Dashboard View Initialized");
        },

        render: function(page) {
            this.$el.html(dashboardTemplate);
            $("#app").html(this.$el);
            this.sidebar = this.$el.find("#sidebar");
            this.bind();
        },

        bind: function() {
            var that = this;
            this.sidebar.find("li a").click(function(e) {
                e.preventDefault();
                var id = $(this).data("navigate");
                that.navigateToSidebar(id);

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

            var alarmsView = new AlarmsView({
                collection: Alarms
            });
            alarmsView.render();

        },

        navigateToSidebar: function(page) {
            this.sidebar.find("a[data-navigate=" + page + "]").tab("show");
            Backbone.history.navigate("dashboard/" + page, {
                trigger: true
            })
        }

    });

    return Dashboard;
});