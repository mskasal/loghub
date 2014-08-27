/*global define*/
define([
    'backbone',
    'text!templates/ApplicationView.html',
    'text!templates/ApplicationsView.html',
    'models/applicationsModel',
    'views/alertifyView',
    'common',
    'mustache',
    'logger'
], function(Backbone, ApplicationViewTemplate, ApplicationsViewTemplate, ApplicationModel, AlertifyView, Common, Mustache, Logger) {
    'use strict';
    //view
    var ApplicationView = Backbone.View.extend({

        template: ApplicationViewTemplate,
        tagName: "a",
        className: "app-item list-group-item",

        initialize: function() {

        },

        events: {
            "click .delete-application": "deleteApplication"
        },

        deleteApplication: function(event) {
            var that = this;
            $(event.currentTarget).attr("disabled", "disabled");
            this.model.destroy({
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function(model, response) {
                    Logger.i("Application Delete Request with : " + response.status.message);
                    Logger.i("Application Deleted: " + model.attributes.APP_TOKEN);
                    that.$el.remove();
                },
                error: function() {
                    $(event.currentTarget).removeAttr("disabled");
                }
            })
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
    var ApplicationsView = Backbone.View.extend({

        el: "#applications",

        initialize: function() {
            var that = this;

            Logger.i("Applications View initialized");

            this.collection.fetch({
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
            });

            this.collection.bind('add', this.addOne, this);
            this.collection.bind('remove', function(a) {

            }, this);
        },

        events: {
            "click .add-new-application-button": "addNewApplication",
            "click .create-new-app": "createNewApplication",
            "keyup #application-search": "filterApp"

        },

        render: function() {

            this.addAll();
            return this;
        },

        addAll: function() {
            this.$('#application-list').empty();
            this.collection.each(this.addOne, this);
        },

        addOne: function(application) {
            var applicationView = new ApplicationView({
                model: application
            });
            this.$('#application-list').prepend(applicationView.render().el);
        },

        filterApp: function(event) {
            this.$('#application-list').empty();
            var keyword = $(event.currentTarget).val();
            var models = this.collection.models;
            for (var i in models) {
                if (models[i].attributes.name.indexOf(keyword) !== -1) {
                    this.addOne(models[i])
                }
            }
        },

        addNewApplication: function(event) {
            this.$(event.currentTarget).removeClass("btn-success add-new-application-button").addClass("btn-primary btn-xs create-new-app").text("Create")
            this.$('#application-name').removeClass("hidden");
        },

        createNewApplication: function() {
            var that = this;

            var applicationName = this.$("#application-name").val();

            this.collection.create({
                name: applicationName
            }, {
                wait: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            })
        }
    });

    return ApplicationsView;
});