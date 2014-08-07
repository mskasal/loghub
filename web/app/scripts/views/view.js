/*global define*/
define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/viewTemp.html',
    'common'
], function($, _, Backbone, viewTemplate, Common) {
    'use strict';

    var MyView = Backbone.View.extend({

        tagName: 'li',
        initialize: function() {
            console.log("my view")
            console.log(this)
            this.$el.append(viewTemplate);
        }

    });

    return MyView;
});