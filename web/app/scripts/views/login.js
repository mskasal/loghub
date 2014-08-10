/*global define*/
define([
    'backbone',
    'text!templates/Login.html',
    'common',
    'logger'
], function(Backbone, LoginTemplate, Common, Logger) {
    'use strict';

    var LoginView = Backbone.View.extend({
        tagName: "div",
        className: "login",
        initialize: function() {
            console.log('Initializing Login View');
            this.render();
            $("#mainContainer").html(this.el);

        },

        events: {
            "click #loginButton": "login"
        },

        render: function() {
            this.el = $(this.el).html(LoginTemplate);
            return this;
        },

        login: function(event) {
            var that = this;

            event.preventDefault();

            var formValues = {
                email: $('#inputEmail').val(),
                password: $('#inputPassword').val()
            };

            this.model.set(formValues);
            
            this.model.login().done(function() {
                if (that.model.get("loggedIn"))
                    Logger.i("Logged in") 
            });
        }
    });

    return LoginView;
});