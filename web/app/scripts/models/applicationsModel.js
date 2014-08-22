/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var ApplicationsModel = Backbone.Model.extend({
        // Default attributes for the model
        idAttribute: "APP_TOKEN",
        initialize: function() {

        },

        parse: function(response) {
            this.status = response.status;
            if (response.data) {
                return response.data;
            }
            return response;
        }

    });

    return ApplicationsModel;
});