$(document).ready(function () {
    handle_sort_by_button();
 });


function handle_sort_by_button()
{
    default_paginate_by=10
    if(window.location.href.indexOf("order_by=") == -1 || window.location.href.indexOf("order_by=-publish_date") > -1) //no option was selected - therefore default value is checked
    {
        document.getElementById("orderRadioBtnDate").checked= true;
    }
    else
    {
        document.getElementById("orderRadioBtnAnswers").checked= true;
    }
}
