/*global define*/
define([
    'backbone',
    'common',
    'logger'
], function (Backbone, Common, Logger) {
    'use strict';

    var UsersModel = Backbone.Model.extend({
        // Default attributes for the model
        defaults: {
            "email": "yoursexyemail@domain.com",
            "registered_at": "2014-02-22 16:32:20",
            "CREDENTIAL_ID": "g3b0hg4q48cusrkravuqe503g1"
        },
        initialize: function () {
            console.log(this.get("CREDENTIAL_ID"));
        }

    });

    return UsersModel;
});