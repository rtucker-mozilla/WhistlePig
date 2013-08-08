$(document).ready(function() {
    
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $('#calendar').fullCalendar({
        theme: true,
        header: {
            left: '',
            center: 'title',
            //right: 'today,month,agendaWeek,agendaDay'
            //left: 'month'
            right: 'prev,next'
        },
        //eventSources: [
        //    {
        //        url: '/en-US/event_feed' // use the `url` property
        //    }
        //],
        events: function(start, end, callback) {
            // do some asynchronous ajax
            contentType:"application/json; charset=utf-8",
            $.getJSON("/en-US/event_feed",
                    {
                        start: start.getTime() / 1000,
                        end: end.getTime() / 1000
                    },
                    function(result) {
                            if(result != null)
                            {
                                for (i in result) {
                                    var calEvent = result[i];
                                    start_int = parseInt(result[i]['start'].replace(/"/g,'')) * 1000;
                                    calEvent.date = new Date(start_int);
                                    calEvent.start = new Date(start_int);
                                    calEvent.end = new Date(start_int);
                                    //calEvent.date = new Date(parseInt(calEvent.date.replace("/Date(", "").replace(")/", ""), 10));
                                    //calEvent.start = new Date(parseInt(calEvent.start.replace("/Date(", "").replace(")/", ""), 10));
                                    //calEvent.end = new Date(parseInt(calEvent.end.replace("/Date(", "").replace(")/", ""), 10));
                                }
                            }

                            var calevents = result;
                            // then, pass the CalEvent array to the callback
                            callback(calevents);

                    });

        },
        editable: false
    });

});
