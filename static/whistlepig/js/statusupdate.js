$(document).ready(function(){
    location_split = location.href.split(/\//);
    last_split_element = location_split[location_split.length-2];
    if(last_split_element != 'add'){
        $('[name="_addanother"]').before("<input type='submit' id='_send_outage_notification' value='Send Outage Notification' />");

        $('#_send_outage_notification').click(function(){
            id = last_split_element;
            var left  = ($(window).width()/2)-(900/2),
                top   = ($(window).height()/2)-(600/2);
            window.open("/admin/statusupdate/sendoutagenotification/" + id + "/", "Send Notification Email", "scrollbars=yes,resizeable,width=900, height=600");
            return false;
        });

    }
});
