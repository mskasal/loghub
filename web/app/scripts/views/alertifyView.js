/*global define*/
define([
    'backbone',
    'text!templates/AlertifyView.html',
    'models/alertifyModel',
    'common',
    'mustache',
    'logger'
], function(Backbone, AlertifyViewTemplate, AlertifyModel, Common, Mustache, Logger) {
    'use strict';
    //view
    var AlertifyView = Backbone.View.extend({
        tagName: 'div',
        className: 'alert',
        template: AlertifyViewTemplate,

        initialize: function() {},

        render: function() {

            var code = this.model.get("code");

            if (code === 20)
                this.$el.addClass("alert-success");
            else if (code === -1)
                this.$el.addClass("alert-danger");
            else
                this.$el.addClass("alert-warning");



            this.$el.html(this.mustacheTemplate(this.template, this.model.toJSON()));

            return this;
        },

        mustacheTemplate: function(template, JSON) {
            return Mustache.render(template, JSON);
        },

        hide: function(){
            this.$el.hide();
        },

        destroy: function(){
            this.$el.remove();
        }
    });

    return AlertifyView;
});