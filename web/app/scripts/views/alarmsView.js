/*global define*/
define([
    'backbone',
    'text!templates/AlarmsView.html',
    'models/alarmsModel',
    'views/alertifyView',
    'common',
    'mustache',
    'logger'
], function(Backbone, AlarmsViewTemplate, AlarmsModel, AlertifyView, Common, Mustache, Logger) {
    'use strict';
    //view
    var AlarmView = Backbone.View.extend({
        tagName: 'a',
        className: 'list-group-item alarm',
        template: AlarmsViewTemplate,

        initialize: function() {},

        render: function() {

            this.$el.html(this.mustacheTemplate(this.template, this.model.toJSON()));

            return this;
        },

        events: {
            "click .delete-alarm": "deleteAlarm",
            "click .get-alarm": "getAlarm"
        },

        getAlarm: function(event) {
            var that = this;
            $(event.currentTarget).attr("disabled", "disabled");
            this.model.fetch({
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function(model, response) {
                    Logger.i("Alarm Get Request with : " + response.status.message);
                    Logger.i("Alarm Got: " + model.attributes.id);
                    that.$(".details").html(JSON.stringify(model.toJSON()))
                    $(event.currentTarget).removeAttr("disabled");
                },
                error: function() {
                    $(event.currentTarget).removeAttr("disabled");
                }
            })
        },

        deleteAlarm: function(event) {
            var that = this;
            $(event.currentTarget).attr("disabled", "disabled");
            this.model.destroy({
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function(model, response) {
                    Logger.i("Alarm Delete Request with : " + response.status.message);
                    Logger.i("Alarm Deleted: " + model.attributes.id);
                    that.$el.remove();
                },
                error: function() {
                    $(event.currentTarget).removeAttr("disabled");
                }
            })
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

            this.collection.bind('add', this.addOne, this);

        },

        events: {
            "click #create-alarm": "createAlarm"
        },

        render: function() {

            this.addAll();
            return this;
        },

        addAll: function() {
            this.$('#alarms-list').empty();
            this.collection.each(this.addOne, this);
        },

        addOne: function(alarm) {
            var alarmView = new AlarmView({
                model: alarm
            });

            this.$('#alarms-list').prepend(alarmView.render().el);
        },

        createAlarm: function() {
            var that = this;
            var params = this.getAlarmParameters();
            this.collection.create(params, {
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID,
                    'Content-Type': 'application/json'
                },

                wait: true,

                success: function(response) {
                    if (response.status.code == 20) {
                        that.render();
                    } else
                        return false;
                }
            })
        },

        getAlarmParameters: function() {
            var b = {}
            var $form = this.$(".create-alarm-form");
            var list = $form.find("input");

            for (var i in list) {
                var a = {

                }
                a[$(list[i]).attr("name")] = $(list[i]).val()
                b = $.extend(b, a);
                if (i == 4)
                    break;
            }

            return b;

        },

        inputSerialize: function(obj) {
            var a = {};
            var key = obj.attr("name") || "";

            a[key] = obj.text();
            return a;
        }
    });

    return AlarmsView;
});