/*global define*/
define([
    'backbone',
    'text!templates/AlarmsView.html',
    'models/alarmsModel',
    'common',
    'mustache',
    'logger'
], function(Backbone, AlarmsViewTemplate, AlarmsModel, Common, Mustache, Logger) {
    'use strict';
    //view
    var AlarmView = Backbone.View.extend({
        tagName: 'a',
        className: 'list-group-item alarm',
        template: AlarmsViewTemplate,

        initialize: function() {
            this.$el.attr("href", "#")
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
    var AlarmsView = Backbone.View.extend({
        el: "#alarms",
        notification: $("#alarms-notification"),
        initialize: function() {
            var that = this;
            this.collection.fetch({
                headers: {
                    'Authorization': 'CREDENTIAL_ID ' + Common.CREDENTIAL_ID
                },
                success: function() {
                    that.render();
                }
            });
        },

        render: function() {

            this.addAll();
            return this;
        },

        addAll: function() {

            if (this.popover) {
                this.popover.empty();
            } else
                this.popover = $("<ul/>", {
                    class: 'popoverContent list-group'
                });

            this.collection.each(this.addOne, this);

            this.notification.popover({
                trigger: "click",
                placement: "bottom",
                container: "body",
                content: this.popover.html(),
                html: true
            });

            this.$el.html(this.popover)
        },

        addOne: function(alarm) {
            var alarmView = new AlarmView({
                model: alarm
            });
            this.popover.append(alarmView.render().el);
        }
    });

    return AlarmsView;
});