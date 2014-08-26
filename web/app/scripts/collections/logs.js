/*global define */
define([
    'backbone',
    'models/logsModel',
    'models/alertifyModel',
    'common'

], function(Backbone, LogModel, Alertify, Common) {
    'use strict';

    var Logs = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: LogModel,
        url: Common.apiURL + '/API/v1/logs',
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {},

        parse: function(response) {
            this.alertify = new Alertify({
                message: response.status.message,
                code: response.status.code
            });

            if (response.data) {
                return response.data.entries;
            }
            return response;
        }
    });

    return new Logs({
        model: LogModel
    });
});