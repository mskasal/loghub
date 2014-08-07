/*global define*/
define([
    'jquery',
    'underscore',
    'backbone',
    'collections/collection',
    'views/view',
    'text!templates/template.html',
    'common'
], function($, _, Backbone, Collection, View, Template, Common) {
    'use strict';

    // Our overall **AppView** is the top-level piece of UI.
    var AppView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#mainContainer',
        initialize: function() {
            var view = new View({
                collection: Collection
            });
        }
    });

    return AppView;
});