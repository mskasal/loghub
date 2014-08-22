/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var FilterModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            APP_TOKENS: "",
            limit: "",
            sortedBy: "",
            keyword: "",
            level: "",
            newerThan: "",
            olderThan: ""
        },
        
        initialize: function() {

        }

    });

    return FilterModel;
});