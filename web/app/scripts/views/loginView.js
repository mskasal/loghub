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

            Logger.i('Initialized Login View');

            if (Common.loggedIn) {
                /**
                 * If loggedIn success navigate to Dashboard
                 */
                setTimeout(function() {
                    Backbone.history.navigate("dashboard", {
                        trigger: true,
                        replace: true
                    });
                }, 1000);

            }
        },

        events: {
            "click #loginButton": "login"
        },

        render: function() {
            this.el = $(this.el).html(LoginTemplate);
            $("#app").html(this.el);

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

            this.model.login().always(function() {
                if (that.model.get("loggedIn")) {
                    Logger.i("Logged in");

                    /**
                     * If loggedIn success navigate to Dashboard
                     */
                    Backbone.history.navigate("dashboard", {
                        trigger: true,
                        replace: true
                    });
                }
            });
        }
    });

    return LoginView;
});