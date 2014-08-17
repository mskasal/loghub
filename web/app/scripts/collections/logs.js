/*global define */
define([
    'backbone',
    'models/logsModel',
    'common'

], function(Backbone, LogModel, Common) {
    'use strict';

    var Logs = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: LogModel,
        url: Common.apiURL + '/API/v1/logs',
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {
        },

        parse: function(response) {
            return response.data;
        }

    });

    return new Logs({
        model: LogModel
    });
});