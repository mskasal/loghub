/*global define*/
define([
    'backbone',
    'text!templates/app.html',
    'common',
    'logger'
], function (Backbone, appTemplate, Common, Logger) {
    'use strict';

    // Our overall **AppView** is the top-level piece of UI.
    var AppView = Backbone.View.extend({

        // Instead of generating a new element, bind to the existing skeleton of
        // the App already present in the HTML.
        el: '#app',
        initialize: function () {
            Logger.i("App Initialized");
        }
    });

    return AppView;
});