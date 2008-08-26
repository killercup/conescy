/*
 * Some cool Ajax Stuff for the Django Admin Panel
 * You need to load jQuery to make this work.
 * for the table sorting ou need tablesorter http://tablesorter.com/
 */

/*
 *  GENERAL
 */

function error() {
    $("#container ul.errorlist").remove();
    $("#container .breadcrumbs").after('<ul class="errorlist"><li>Could not load that page.</li></ul>').find("ul.errorlist").hide().slideDown(500);
    all();
}

/*
 *  LIST VIEW
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
                ).hide().fadeIn(400);
                all();
            },
            error: function(){
                error();
            },
        });

    });
}

function ajaxpagination() {
    // ajax for pagination bar
    $("#changelist .paginator a").click(function(ev) {
        ev.preventDefault();
        $.ajax({
            url: this.href,
            type: "GET",
            dataType: "html",
            success: function(data, status) {
                $("#changelist").fadeOut(200).remove();
                $("div#container div#content-main").append(
                    $("<div/>").append(data.replace(/<script(.|\s)*?\/script>/g, "")).find("div#container div#content-main div#changelist")
                ).hide().fadeIn(400);
                all();
            },
            error: function(){
                error();
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
                ).hide().fadeIn(400);
                all();
            },
            error: function(){
                error();
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
                ).hide().fadeIn(400);
                all();
            },
            error: function(){
                error();
            },
        });
    });
}

/*
 *  DETAIL VIEW
 */

function ajaxhistory() {
    // load the history (table of changes made to an object via admin panel) with ajax
    // todo: second execution causes complete bullshit
    $("div#content-main a.historylink").click(function(ev) {
        ev.preventDefault();
        $("div.ajaxhistory").slideUp(400, function(){
                $(this).remove();
        });
        $.ajax({
            url: this.href,
            type: "GET",
            dataType: "html",
            success: function(data, status) {
                $("div#container div#content div#content-main ul.object-tools").after(
                    $("<div/>")
                        .empty()
                        .append(data.replace(/<script(.|\s)*?\/script>/g, ""))
                        .find("div#container div#content")
                        .css({'display': 'none', 'background': '#ffc', 'padding': '5px'})
                        .addClass("ajaxhistory")
                        .find("h1")
                        .prepend('<a href="#close" class="deletelink historyclose" style="float: right">&nbsp;</a>')
                        .parent()
                ).find("+ div").hide().slideDown(400);
                
                // close ajax history!
                $("div#container div#content div#content-main a.historyclose").click(function(ev) {
                    ev.preventDefault();
                    $("div.ajaxhistory").slideUp(400, function(){
                        $(this).remove();
                    });
                });
                
                all();
            },
            error: function(){
                error();
            },
        });
        // }
    });
}

function fieldvalidation() {
    /* Tries to validate the fields.
     * Currently it does nothing, but I try to implement some functionality soon.
     * My plan was to analyse the fields by use of model definitions via JSON.
     */
}

function authorselection() {
    /* If there is an author field, and it is set to a user, hide the selection
     * and let the user have to click on "change" to change it. This takes one
     * decision to make form the user, but keeps functionality.
     */
    if (!($("div#content-main select[name='author'] option[@selected]").text() == "---------")) {
        // $("div#content-main select[name='author']").hide();
        $("div#content-main select[name='author'], div#content-main select[name='author'] + a#add_id_author").hide().parent().append(
            '<p class="authorchangereplace"><strong>'
             + $("div#content-main select[name='author'] option[@selected]").text()
             + '</strong> <a href="#changeauthor" class="changeauthor">(Change)</a></p>'
        );
    }
    
    $("div#content-main a.changeauthor").click(function(ev){
        ev.preventDefault();
        $(this).parent().remove();
        $("div#content-main select[name='author'], div#content-main select[name='author'] + a#add_id_author").fadeIn(300);
    });
}

/*
 *  LAUNCH THE FUNCTIONS
 */

function all() {
    ajaxfilter();
    ajaxpagination();
    ajaxsearch();
    ajaxsearchbacklinks();
    $("div#changelist table").tablesorter({'cssAsc': 'sorted ascending', 'cssDesc': 'sorted descending', 'cssHeader': '',});
    
    ajaxhistory();
    authorselection();
}

$(document).ready(function() {
    all();
});
