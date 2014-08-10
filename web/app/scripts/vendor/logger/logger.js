/*global define*/
'use strict';

define([], function() {

    return {
        mute: true,
        listeners: [],
        start: function(){
            this.mute = false;
        },
        stop: function(){
            this.mute = true;
        },
        i: function(message){
            this.write('Info', message)
        },
        e: function(message){
            this.write('Error', message)
        },
        write: function(level, message){
            if (this.mute)
                return;

            if (console){
                if (level == 'error')
                    console.error(level + ": " + message);
                else
                    console.log(level + ": " + message);
            }
            else
                alert("Logger says: " +level + ": " + message);

            for (var i in this.listeners)
                this.listeners[i](level, message)
        },
        addListener: function(f){
            this.listeners.push(f);
        }
    }
});

