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
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function() {
                    that.render();
                }
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

        addOne: function(application) {
            var alarmView = new AlarmView({
                model: application
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

                success:function(response){
                    if (response.status.code == 20){
                        that.render();
                    }else
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