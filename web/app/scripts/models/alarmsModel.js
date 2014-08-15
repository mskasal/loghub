/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var AlarmsModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            "id": "48cusrkravuqe50",
            "APP_TOKEN": "any",
            "active": 1,
            "name": "urgent internal problems",
            "keyword": "fatal error",
            "level": "any",
            "limit": 1,
            "receiver": ["sales@ domain.com", "technical@ domain.com"],
            "note": "please have a look at this ASAP",
        },
        initialize: function() {

        }

    });

    return AlarmsModel;
});