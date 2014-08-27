/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function(Backbone, Common, Logger) {
    'use strict';

    var LoginStatus = Backbone.Model.extend({

        defaults: {
            loggedIn: false,
            CREDENTIAL_ID: null,
            email: null,
            password: null
        },

        initialize: function() {

            this.bind('change:CREDENTIAL_ID', this.onCREDENTIAL_IDChange, this);
            
            if (localStorage.CREDENTIAL_ID) {

                this.set({
                    'CREDENTIAL_ID': localStorage.getItem('CREDENTIAL_ID')
                });

                Common.setItem('CREDENTIAL_ID', localStorage.CREDENTIAL_ID)
            }
        },

        login: function() {
            var that = this;

            var url = Common.apiURL + '/API/v1/user/' + 'email=' + that.get("email") + '&password=' + that.get("password");

            return $.ajax({
                url: url,
                type: 'GET',
                dataType: 'json',
                contentType: "x-www-form-urlencoded"
            }).done(function(response) {
                Logger.i("Login request details: " + response.status.message);

                if (response.status.code == 20) {
                    // If not, send them back to the home page
                    that.setCREDENTIAL_ID(response.data.credential_id);
                }
            });
        },

        onCREDENTIAL_IDChange: function(CREDENTIAL_ID) {

            this.set({
                'loggedIn': !!CREDENTIAL_ID
            });

            Common.setItem('loggedIn', !!CREDENTIAL_ID);
        },

        setCREDENTIAL_ID: function(CREDENTIAL_ID) {

            Common.setItem('CREDENTIAL_ID', CREDENTIAL_ID);

            localStorage.setItem('CREDENTIAL_ID', CREDENTIAL_ID);

            this.set({
                'CREDENTIAL_ID': CREDENTIAL_ID
            });
        }

    });

    return LoginStatus;
});