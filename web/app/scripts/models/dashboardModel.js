/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var DashboardModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            title: ' Dashboard'
        },

        initialize: function() {
            Logger.i("Dashboard Model Initialize: " + this.defaults.title);

        },

        parse: function(response) {
            if (response.data) {
                return response.data;
            }
            return response;
        }

    });

    return DashboardModel;
});