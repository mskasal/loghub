/*global define*/
define([
    'backbone',
    'text!templates/LogView.html',
    'text!templates/LogsView.html',
    'models/logsModel',
    'common',
    'mustache',
    'logger'
], function (Backbone, LogViewTemplate, LogsViewTemplate, LogModel, Common, Mustache, Logger) {
    'use strict';
    //view
    var LogView = Backbone.View.extend({

        template: LogViewTemplate,
        tagName: "li",
        className: "log-item",

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
    var LogsView = Backbone.View.extend({
        el: "#logs",
        initialize: function () {},

        render: function () {
            this.addAll();
            return this;
        },

        addAll: function () {
            this.$el.empty();
            this.collection.each(this.addOne, this);
        },

        addOne: function (log) {
            var logView = new LogView({
                model: log
            });
            this.$el.prepend(logView.render().el);
        }
    });

    return LogsView;
});