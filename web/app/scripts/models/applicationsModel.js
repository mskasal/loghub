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

            "id": "510Dasdwq0hg4q48cusr185RC",
            "name": "MyUberWebsite",
            "createdAt": "2014-03-18 20:16:32",
            "APP_TOKEN": "88KOBg4q48cusrkravuqe95TRH"
        },
        initialize: function () {

        }

    });

    return ApplicationsModel;
});