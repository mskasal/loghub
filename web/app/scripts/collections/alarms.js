/*global define */
define([
    'backbone',
    'models/alarmsModel',
    'common'

], function(Backbone, AlarmsModel, Common) {
    'use strict';

    var Alarms = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: AlarmsModel,
        url: Common.apiURL + '/API/v1/alarms',
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),
        initialize: function() {
        },

        parse: function(response) {
            return response.data;
        }

    });

    return new Alarms();
});