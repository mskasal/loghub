/*global define */
define([
    'underscore',
    'backbone',
    //'backboneLocalstorage',
    'models/model'
], function(_, Backbone, Model) {
    'use strict';

    var MyCollection = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: Model,
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {}

    });

    return new MyCollection({
        model: Model
    });
});