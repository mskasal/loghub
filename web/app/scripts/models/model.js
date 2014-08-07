/*global define*/
define([
    'underscore',
    'backbone'
], function(_, Backbone) {
    'use strict';

    var MyModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            title: 'model title'
        },
        initialize: function() {
            console.log(this.get("title"));
        }

    });

    return MyModel;
});