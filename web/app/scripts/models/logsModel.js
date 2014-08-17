/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var LogsModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            "APP_TOKEN": "....",
            "message": "....",
            "level": "info",
            "date": "....",
            "metadata": "...."
          },
        initialize: function() {

        }

    });

    return LogsModel;
});