/*
 * Some cool Ajax Stuff for the Django Admin Panel
 */

function ajaxfilter() {
    // ajax for filters bar in list view
    $("#changelist-filter ul li a").click(function(ev) {
        ev.preventDefault();
        $.ajax({
            url: this.href,
            type: "GET",
            dataType: "html",
            success: function(data, status) {
                $("#changelist").fadeOut(200).remove();
                $("div#container div#content-main").append(
                    $("<div/>").append(data.replace(/<script(.|\s)*?\/script>/g, "")).find("div#container div#content-main div#changelist")
                ).fadeIn(400);
                all();
            },
            error: function() {
                $("#container .breadcrumbs").after('<ul class="errorlist"><li>Could not load that page.</li></ul>').hide().fadeIn(500);
                all();
            },
        });

    });
}

function ajaxsearch() {
    // search form on top of list
    $("form#changelist-search").submit(function(ev){
        ev.preventDefault();
        $.ajax({
            url: this.action,
            type: "GET",
            dataType: "html",
            data: $("form#changelist-search").serialize(),
            success: function(data, status) {
                $("#changelist").fadeOut(200).remove();
                $("div#container div#content-main").append(
                    $("<div/>").append(data.replace(/<script(.|\s)*?\/script>/g, "")).find("div#container div#content-main div#changelist")
                ).fadeIn(400);
                all();
            },
            error: function() {
                $("#container .breadcrumbs").after('<ul class="errorlist"><li>Could not load that page.</li></ul>').hide().fadeIn(500);
                all();
            },
        });
    });
}

function ajaxsearchbacklinks() {
    // This adds ajax for the backlinks on search results pages. ("2 Results (_show all_)")
    $("form#changelist-search span a").click(function(ev){
        ev.preventDefault();
        $.ajax({
            url: this.href,
            type: "GET",
            dataType: "html",
            success: function(data, status) {
                $("#changelist").fadeOut(200).remove();
                $("div#container div#content-main").append(
                    $("<div/>").append(data.replace(/<script(.|\s)*?\/script>/g, "")).find("div#container div#content-main div#changelist")
                ).fadeIn(400);
                all();
            },
            error: function() {
                $("#container .breadcrumbs").after('<ul class="errorlist"><li>Could not load that page.</li></ul>').hide().fadeIn(500);
                all();
            },
        });
    });
}

function all() {
    ajaxfilter();
    ajaxsearch();
    ajaxsearchbacklinks();
    $("div#container div#content-main div#changelist table").tablesorter({'cssAsc': 'sorted ascending', 'cssDesc': 'sorted descending', 'cssHeader': '',}); 
}

$(document).ready(function() {
    all();
});
