/*global define*/
define([
    'jquery',
    'underscore',
    'backbone',
    'text!templates/Login.html',
    'common'
], function($, _, Backbone, LoginTemplate, Common) {
    'use strict';

    var LoginView = Backbone.View.extend({
        tagName: "div",
        className: "login",
        initialize: function() {
            console.log('Initializing Login View');
        },

        events: {
            "click #loginButton": "login"
        },

        render: function() {
            $(this.el).html(LoginTemplate);
            return this;
        },

        login: function(event) {
            event.preventDefault(); // Don't let this button submit the form
            $('.alert-error').hide(); // Hide any errors on a new submit
            var url = Common.apiURL + '/API/v1/users';

            console.log('Loggin in... ');
            var formValues = {
                email: $('#inputEmail').val(),
                password: $('#inputPassword').val()
            };

            $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                contentType: "x-www-form-urlencoded",
                data: JSON.stringify(formValues)
            }).always(function(response) {
                response = {
                    "status": {
                        "code": 20,
                        "message": "successful"
                    },
                    "data": []
                }
                console.log(["Login request details: ", response.status.message]);
                if (response.status.code !== 20) { // If there is an error, show the error messages
                    $('.alert-error').text(response.status.message).show();
                } else { // If not, send them back to the home page
                    console.log(response.status.message)
                    window.location.replace('#dashboard');
                }
            });
        }
    });

    return LoginView;
});