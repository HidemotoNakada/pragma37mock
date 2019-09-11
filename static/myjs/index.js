
function init_listgroups() {
    $('.list-group-item').on('click', function (e) {
        //alert(this.id + " pressed");
        var kids = $(this).parent().children('.list-group-item');
        kids.removeClass("active");
        $(this).addClass("active");
    });
}
function init_launchButton() {
    $('#launch').on('click', function (e) {
        var selected = {};
        var allselected = true;
        $('.list-group').each(function (index, element) {
            //alert("test")
            var id = getActive(this);
            console.log("id = " + id);
            selected[this.id] = id;
        });
        for (var k in selected) {
            if (selected[k] == null) {
                alert(k + ' is null');
                allselected = false;
            }
        }
        if (allselected) {
            console.log(selected);
            $.post("launch", selected, function (data) {
                $(".result").html(data);
            });   
        }
    });
}

function getActive(node) {
    var activeone = null;
    $(node).children().each(function () {
        if ($(this).hasClass("active")) {
            activeone = this.id;
        }
    });
    return activeone;
}

function set_periodic() {
    setInterval("update_table();", 10000); 
}

function shutdown(id) {
    $.post("shutdown", {"id":id});
}


function notebook_str(obj) {
    var closebutton = "";
    var urlbutton = "";

    if (obj.status == "RUNNING") {
        closebutton = "<img src=\"/static/img/close.png\" onclick=\"shutdown('" +   
            obj.id +
            "')\" width=\"20pt\" > ";

        urlbutton = "<img src=\"/static/img/open.png\" width=\"25pt\"> ";
    }
    console.log(closebutton);
    return "<tr>" +
        "<td>" + obj.id + "</td>" +
        "<td>" + obj.time + "</td> " +      
        "<td><a href=\"" + obj.url + "\" target=\"_blank\">" + urlbutton + "</td> " +      
        "<td>" + obj.status + "</td> " + 
        "<td>" + closebutton + "</td> " + 
        "</tr>"
    }


function update_table() {
    $.get("notebooks", function (data) {
//        console.log(data);
        $("#notebooklist").children().remove();
        $.each(data, function() {
            $("#notebooklist").append(notebook_str(this));
        });
    });
}

window.onload = function () {
    init_listgroups();
    init_launchButton();
    set_periodic();
}
