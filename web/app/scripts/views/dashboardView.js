/*global define*/
define([
    'backbone',
    'text!templates/Dashboard.html',
    'common',
    'logger'
], function (Backbone, dashboardTemplate, Common, Logger) {
    'use strict';

    var Dashboard = Backbone.View.extend({

        tagName: 'div',
        initialize: function () {
            Logger.i("Dashboard View Initialized");
        },
        render: function (page) {
            this.$el.html(dashboardTemplate);
            $("#app").html(this.$el);
            this.sidebar = this.$el.find("#sidebar");
            this.bind();
        },
        bind: function () {
            var that = this;
            this.sidebar.find("li a").click(function (e) {
                e.preventDefault();
                var id = $(this).data("navigate");
                that.navigateToSidebar(id);

            })
        },
        navigateToSidebar: function (page) {
            this.sidebar.find("a[data-navigate=" + page + "]").tab("show");
            Backbone.history.navigate("dashboard/" + page, {
                trigger: true
            })
        }

    });

    return Dashboard;
});