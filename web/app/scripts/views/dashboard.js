/*global define*/
define([
    'backbone',
    'text!templates/Dashboard.html',
    'common'
], function(Backbone, dashboardTemplate, Common) {
    'use strict';

    var Dashboard = Backbone.View.extend({

        tagName: 'div',
        initialize: function() {
            console.log("Dashboard")
            this.$el.append(dashboardTemplate);
        }

    });

    return Dashboard;
});