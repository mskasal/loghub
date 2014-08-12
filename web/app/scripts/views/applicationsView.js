/*global define*/
define([
    'backbone',
    'text!templates/ApplicationView.html',
    'models/applicationsModel',
    'common',
    'mustache',
    'logger'
], function (Backbone, ApplicationViewTemplate, ApplicationModel, Common, Mustache, Logger) {
    'use strict';
    //view
    var ApplicationView = Backbone.View.extend({

        template: ApplicationViewTemplate,
        tagName: "li",
        className: "app-item",

        initialize: function () {

        },

        render: function () {

            this.$el.html(this.mustacheTemplate(this.template, this.model.toJSON()));

            return this;
        },

        mustacheTemplate: function (template, JSON) {
            return Mustache.render(template, JSON);
        }
    });

    //view collection
    var ApplicationsView = Backbone.View.extend({
        el: "#applications",
        initialize: function () {},

        render: function () {
            this.addAll();
            return this;
        },

        addAll: function () {
            this.$el.empty();
            this.collection.forEach(this.addOne, this);
        },

        addOne: function () {
            var applicationView = new ApplicationView({
                model: new ApplicationModel()
            });
            this.$el.prepend(applicationView.render().el);
        }
    });

    return ApplicationsView;
});