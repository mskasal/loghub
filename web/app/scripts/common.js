/*global define*/
'use strict';

define([], function() {
    return {
        // What is the enter key constant?
        ENTER_KEY: 13,
        ESCAPE_KEY: 27,
        loggedIn : false,
        //  API URL
        apiURL: "http://loghub:8080",
        setItem: function(key, value){
        
        	this[key] = value;
        	return this[key];
        }
    };
});