/*global define*/
define([
    'backbone'
], function(Backbone) {
    'use strict';

    var DashboardModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            title: ' dashboard model title'
        },
        initialize: function() {
            console.log(this.get("title"));
        }

    });

    return DashboardModel;
});