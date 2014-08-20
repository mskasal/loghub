/*global define*/
define([
    'backbone',
    'text!templates/ApplicationView.html',
    'text!templates/ApplicationsView.html',
    'models/applicationsModel',
    'common',
    'mustache',
    'logger'
], function(Backbone, ApplicationViewTemplate, ApplicationsViewTemplate, ApplicationModel, Common, Mustache, Logger) {
    'use strict';
    //view
    var ApplicationView = Backbone.View.extend({

        template: ApplicationViewTemplate,
        tagName: "a",
        className: "app-item list-group-item",

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
    var ApplicationsView = Backbone.View.extend({
        el: "#applications",
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
            "click .add-new-application-button": "addNewApplication",
            "click .create-new-app": "createNewApplication"

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

        addNewApplication: function(event) {
            this.$(event.currentTarget).removeClass("btn-success add-new-application-button").addClass("btn-primary btn-xs create-new-app").text("Create")
            this.$('#application-name').removeClass("hidden");
        },

        createNewApplication: function() {
            var that = this;

            var applicationName = this.$("#application-name").val();
            console.log(applicationName)

            this.collection.create({
                name: that.applicationName
            }, {
                wait: true,
                headers: {
                    'Authorization': Common.CREDENTIAL_ID
                }
            })
        }
    });

    return ApplicationsView;
});