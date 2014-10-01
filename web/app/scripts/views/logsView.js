/*global define*/
define([
    'backbone',
    'text!templates/LogView.html',
    'text!templates/LogsView.html',
    'models/logsModel',
    'models/filterModel',
    'models/applicationsModel',
    'collections/applications',
    'collections/queu',
    'views/alertifyView',
    'views/queuView',
    'bootstrapSelect',
    'bootstrapDatepicker',
    'common',
    'mustache',
    'moment',
    'logger'
], function(Backbone, LogViewTemplate, LogsViewTemplate, LogModel, FilterModel, ApplicationsModel, Applications, Queu, AlertifyView, QueuView, Select, Datepicker, Common, Mustache, Moment, Logger) {
    'use strict';
    //view
    var LogView = Backbone.View.extend({

        template: LogViewTemplate,
        tagName: "a",
        className: "log-item list-group-item row",

        initialize: function() {
            this.applicationsModel = new ApplicationsModel();

            this.listenTo(this.applicationsModel, 'change', this.showApplicationDetail);
        },

        events: {
            "click":"toggleSelect"
        },

        render: function() {
            console.log(this.model.get('date'))
            this.model.set({date: Moment(this.model.get('date')).format('lll')})
            this.$el.html(this.mustacheTemplate(this.template, this.model.toJSON()));
            this.$applicationDetail = this.$(".application");
            this.getApplication();
            return this;
        },

        mustacheTemplate: function(template, JSON) {
            return Mustache.render(template, JSON);
        },

        getApplication: function() {
            var that = this;

            var app_token = this.model.get("APP_TOKEN");
            this.applicationsModel.url = Common.apiURL + '/API/v1/applications/' + app_token
            this.applicationsModel.fetch({
                wait: true,
                reset: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            })

        },

        showApplicationDetail: function(model) {
            var html = '<span class="name">[{{name}}]</span>';
            var html = Mustache.render(html, model.toJSON());
            this.$applicationDetail.html(html);
        },

        toggleSelect: function(){
            this.$el.toggleClass('selected');
            this.$('.log ul li i.glyphicon-ok').toggleClass('hidden');
        }
    });

    //view collection
    var LogsView = Backbone.View.extend({
        el: "#logs",

        initialize: function() {
            var that = this;

            this.applications = Applications;

            this.queuView = new QueuView({
                collection: Queu
            });

            this.filterModel = new FilterModel({});

            Logger.i("Logs View initialized");
        },

        start: function() {
            var that = this;


            this.$applicationSelect = this.$("#application-selected");

            this.collection.fetch({
                wait: true,
                reset: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function() {
                    that.render();
                }
            }).done(function() {

                var alertifyView = new AlertifyView({
                    model: that.collection.alertify
                })

                that.$el.append(alertifyView.render().el)
                if (this.interval)
                    clearInterval(this.interval)
                this.interval = setInterval(function() {
                    var lastItem = _.last(that.collection.models).toJSON().date;
                    that.collection.update(lastItem)
                }, 20000)
            });


            this.listenTo(this.applications, 'reset', this.setApplicationsSelect);
            this.listenTo(this.collection, 'reset', this.addAll);
            this.listenTo(this.collection, 'add', this.addAll);
            this.listenTo(this.filterModel, 'change', this.filter);
        },

        events: {
            "click .filter-toggle-button": "toggleFilter",
            "click #filter-submit-button": "setFilterParameters",
            "click .showqueu": "showQueu"
        },

        render: function() {

            this.addAll();
            this.getApplicationList();


            $('.logs-filter .selectpicker').selectpicker({
                width: "100%"
            });

            $('.logs-filter .input-daterange').datepicker({
                todayBtn: 'linked',
                autoclose: true
            });

            Logger.i("Logs Rendered");

            return this;
        },

        showQueu: function(){
            this.collection.mergeQueu();
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

            this.collection.fetch({
                data: this.filterModel.attributes,
                wait: true,
                reset: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            });
        },

        setFilterParameters: function() {

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
                reset: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            });
        },

        setApplicationsSelect: function(collection) {
            var that = this;
            this.$("#application-selected").empty();
            collection.each(this.renderOptionOfSelect, this);
        },

        renderOptionOfSelect: function(model) {

            var id = model.id;
            var name = model.get("name");
            var $option = $("<option />");

            $option.attr("data-token", id);
            $option.html(name);
            this.$("#application-selected").append($option[0].outerHTML).selectpicker("refresh")
        }
    });

    return LogsView;
});