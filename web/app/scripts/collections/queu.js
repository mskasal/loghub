/*global define */
define([
    'backbone',
    'models/logsModel',
    'common'

], function(Backbone, LogsModel, Common) {
    'use strict';

    var Queu = Backbone.Collection.extend({
        // Reference to this collection's model.
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),

        url: Common.apiURL + '/API/v1/logs',
        model: LogsModel,

        initialize: function() {},

        parse: function(response) {

            if (response.data) {
                return response.data.entries;
            }
            return response;
        }
    });

    return new Queu({
        model: LogsModel
    });
});