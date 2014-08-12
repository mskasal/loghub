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
            this.set({
                'CREDENTIAL_ID': localStorage.getItem('CREDENTIAL_ID')
            });
        },
        login: function() {
            var that = this;

            var url = Common.apiURL + '/API/v1/auth';

            return $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                contentType: "x-www-form-urlencoded",
                data: JSON.stringify({
                    email: that.get("email"),
                    password: that.get("password")
                })
            }).always(function(response) {
                response = {
                    "status": {
                        "code": 20,
                        "message": "successful"
                    },
                    "data": {
                        "email": "yoursexyemail@domain.com",
                        "registered_at": "2014-02-22 16:32:20",
                        "CREDENTIAL_ID": "g3b0hg4q48cusrkravuqe503g1"
                    }
                }

                Logger.i("Login request details: " + response.status.message);

                if (response.status.code == 20) {
                    // If not, send them back to the home page
                    that.setCREDENTIAL_ID(response.data.CREDENTIAL_ID);
                }
            });
        },

        onCREDENTIAL_IDChange: function(status, CREDENTIAL_ID) {
            this.set({
                'loggedIn': !!CREDENTIAL_ID
            });
        },

        setCREDENTIAL_ID: function(CREDENTIAL_ID) {
            localStorage.setItem('CREDENTIAL_ID', CREDENTIAL_ID)
            this.set({
                'CREDENTIAL_ID': CREDENTIAL_ID
            });
        }

    });

    return LoginStatus;
});