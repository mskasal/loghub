/*global define*/
define([
    'backbone',
    'text!templates/LogView.html',
    'text!templates/QueuViewTemplate.html',
    'models/logsModel',
    'views/alertifyView',
    'common',
    'mustache',
    'logger'
], function(Backbone, LogViewTemplate, QueuViewTemplate, LogsModel, AlertifyView, Common, Mustache, Logger) {
    'use strict';
    //view
    var LogView = Backbone.View.extend({

        template: LogViewTemplate,
        tagName: "a",
        className: "log-item list-group-item",

        initialize: function() {

        },

        render: function() {

            this.$el.html(this.mustacheTemplate(this.template, this.model.toJSON()));

            return this;
        },

        mustacheTemplate: function(template, JSON) {
            return Mustache.render(template, JSON);
        }
    });

    //view collection
    var QueuView = Backbone.View.extend({
        el: "#queu",

        initialize: function() {
            var that = this;

            Logger.i("Queu View initialized");
        },

        events:{

        },

        start: function() {
            var that = this;

            this.listenTo(this.collection, 'reset', this.addAll);
        },

        render: function() {

            this.addAll();

            Logger.i("Queu Rendered");

            return this;
        },

        addAll: function() {
            this.$("#queu-list").empty();
            this.collection.each(this.addOne, this);
        },

        addOne: function(log) {
            var logView = new LogView({
                model: log
            });
            this.$("#queu-list").prepend(logView.render().el);
        }
        
    });

    return QueuView;
});