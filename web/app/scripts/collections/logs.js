/*global define */
define([
    'backbone',
    'collections/queu',
    'models/logsModel',
    'models/alertifyModel',
    'common'

], function(Backbone, Queu, LogsModel, Alertify, Common) {
    'use strict';

    var Logs = Backbone.Collection.extend({
        // Reference to this collection's model.
        model: LogsModel,
        url: Common.apiURL + '/API/v1/logs',
        live: true,
        stream: false,
        // Save all of the items under the `"items"` namespace.
        //localStorage: new Store('items-backbone'),

        update: function(last) {
            var that = this;
            
            Queu.fetch({
                reset: true,
                data: {
                    newer_than: last,
                    page: that.total_page_count
                },
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                },
                success: function(res) {
                    if (Queu.models.length) {
                        console.log(last, Queu)
                    } else
                        console.log("nothing new")
                }
            })
        },

        mergeQueu: function() {
            this.fetch({
                reset: true,
                headers: {
                    'X-Authorization': 'CREDENTIAL_ID ' + localStorage.CREDENTIAL_ID
                }
            })
            Queu.reset();
        },

        initialize: function() {},

        parse: function(response) {
            this.alertify = new Alertify({
                message: response.status.message,
                code: response.status.code
            });

            if (response.data) {
                this.total_page_count = response.data.total_page_count;
                return response.data.entries;
            }
            return response;
        }
    });

    return new Logs({
        model: LogsModel
    });
});