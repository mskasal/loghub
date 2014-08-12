/*global define*/
define([
    'backbone'
], function(Backbone) {
    'use strict';

    var MyModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            title: 'model title'
        },
        initialize: function() {
        }

    });

    return MyModel;
});