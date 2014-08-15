/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function (Backbone, Common, Logger) {
    'use strict';

    var ApplicationsModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {

            "id": null,
            "name": null,
            "createdAt": null,
            "APP_TOKEN": null
        },
        initialize: function () {

        }

    });

    return ApplicationsModel;
});