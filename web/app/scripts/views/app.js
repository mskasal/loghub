/*global define*/
define([
    'backbone',
    'collections/collection',
    'common'
], function(Backbone, Collection, Common) {
    'use strict';

    // Our overall **AppView** is the top-level piece of UI.
    var AppView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#app',
        initialize: function() {
            console.log("app view loaded")
        }
    });

    return AppView;
});