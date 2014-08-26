/*global define*/
define([
    'backbone',
    'text!templates/LogView.html',
    'text!templates/LogsView.html',
    'models/logsModel',
    'models/filterModel',
    'collections/applications',
    'views/alertifyView',
    'bootstrapSelect',
    'bootstrapDatepicker',
    'common',
    'mustache',
    'logger'
], function(Backbone, LogViewTemplate, LogsViewTemplate, LogModel, FilterModel, Applications, AlertifyView, Select, Datepicker, Common, Mustache, Logger) {
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
            Logger.i("Logs View initialized");
            this.applications = Applications;
            this.$applicationSelect = this.$("#application-selected");

            this.collection.fetch({
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function() {
                    that.render();
                }
            }).done(function() {

                console.log(that.collection.alertify);
                var alertifyView = new AlertifyView({
                    model: that.collection.alertify
                })

                that.$el.append(alertifyView.render().el)
            });

            this.getApplicationList();
            this.filterModel = new FilterModel({});
            this.listenTo(this.filterModel, 'change', this.filter);
        },

        events: {
            "click .filter-toggle-button": "toggleFilter",
            "click #filter-submit-button": "setFilterParameters"
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

            Logger.i("Logs Rendered");

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

        filter: function() {
            var that = this;

            this.setFilterParameters();

            this.collection.fetch({
                data: this.filterModel.attributes,
                wait: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function(response) {
                    that.addAll();
                }
            });
        },

        setFilterParameters: function(a) {

            var $filter = this.$(".logs-filter");

            var applicationsList = [];

            $filter.find("#application-selected").find(":selected").each(function() {
                var token = $(this).data("token");

                applicationsList.push(token);
            });

            var applications = applicationsList || "",
                limit = $filter.find("#logs-limit").val(),
                sortedBy = $filter.find("#logs-sort").val(),
                keyword = $filter.find("#logs-contain").val(),
                level = $filter.find("#logs-level").val() || "",
                olderThan = $filter.find("#datepicker-logs-date-range").datepicker('getDate') | "",
                newerThan = $filter.find("#datepicker-logs-date-range").datepicker('getDate') | "";

            this.filterModel.set({
                APP_TOKENS: applications.toString(),
                limit: limit,
                sortedBy: "",
                keyword: keyword,
                level: level.toString(),
                newerThan: "",
                olderThan: ""
            });
        },

        getApplicationList: function() {
            var that = this;

            this.applications.fetch({
                wait: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            }).done(function() {
                that.applications.each(that.setApplicationsSelect, that);
            });

        },

        setApplicationsSelect: function(model) {

            var id = model.id;
            var name = model.get("name");
            var $option = $("<option />");

            $option.attr("data-token", id);
            $option.html(name);
            $option.appendTo(this.$applicationSelect);
        }
    });

    return LogsView;
});