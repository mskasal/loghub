/*global define */
define([
    'backbone',
    'models/alarmsModel',
    'models/alertifyModel',
    'common'

], function(Backbone, AlarmsModel, Alertify, Common) {
    'use strict';

    var Alarms = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: AlarmsModel,
        url: Common.apiURL + '/API/v1/alarms',
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {},

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

    return new Alarms();
});