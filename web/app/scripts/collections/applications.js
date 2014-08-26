/*global define */
define([
    'backbone',
    'models/applicationsModel',
    'models/alertifyModel',
    'common'

], function(Backbone, ApplicationModel, Alertify, Common) {
    'use strict';

    var Applications = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: ApplicationModel,
        url: Common.apiURL + '/API/v1/applications',
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {

        },

        parse: function(response) {
            this.alertify = new Alertify({
                message: response.status.message,
                code: response.status.code
            });

            if (response.data) {
                return response.data;
            }
            return response;
        }
    });

    return new Applications({
        model: ApplicationModel
    });
});