/*global define */
define([
    'backbone',
    'models/applicationsModel',
    'common'

], function(Backbone, ApplicationModel, Common) {
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
            return response.data;
        }

    });

    return new Applications({
        model: ApplicationModel
    });
});