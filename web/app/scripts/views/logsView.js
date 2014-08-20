/*global define*/
define([
    'backbone',
    'text!templates/LogView.html',
    'text!templates/LogsView.html',
    'models/logsModel',
    'bootstrapSelect',
    'bootstrapDatepicker',
    'common',
    'mustache',
    'logger'
], function(Backbone, LogViewTemplate, LogsViewTemplate, Select, Datepicker, LogModel, Common, Mustache, Logger) {
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
    var LogsView = Backbone.View.extend({
        el: "#logs",

        initialize: function() {
            var that = this;
            this.collection.fetch({
                headers: {
                    'Authorization': Common.CREDENTIAL_ID
                },
                success: function() {
                    that.render();
                }
            });
        },

        events: {
            "click .filter-toggle-button": "toggleFilter"
        },

        render: function() {
            
            $('.logs-filter .selectpicker').selectpicker({
                width: "100%"
            });
            $('.logs-filter .input-daterange').datepicker({
                todayBtn: 'linked',
                autoclose: true
            });

            this.addAll();
            return this;
        },

        toggleFilter: function() {
            $('.logs-filter').toggleClass("open");
        },

        addAll: function() {
            this.$("#logs-list").empty();
            this.collection.each(this.addOne, this);
        },

        addOne: function(log) {
            var logView = new LogView({
                model: log
            });
            this.$("#logs-list").prepend(logView.render().el);
        },

        getFilterParameters : function(){
            
        }
    });

    return LogsView;
});