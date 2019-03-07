i = true;

function myFunction() {
    title_elem = document.getElementById("title_elem");
    if (i == true) {
        title_elem.innerHTML = "Le";
        i = false;
    } else {
        title_elem.innerHTML = "Meme";
        i = true;
    }
}

setInterval(myFunction, 2000);

// JQuery & AJAX Section
$(document).ready(function () {

    // Back to Top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 200) {
            $('#BacktoTop').fadeIn();
        } else {
            $('#BacktoTop').fadeOut();
        }
    });

    $("#BacktoTop").click(function () {
        //1 second of animation time
        //html works for FFX but not Chrome
        //body works for Chrome but not FFX
        //This strange selector seems to work universally
        $("html, body").animate({scrollTop: 0}, 500,);
    });

     $('[data-toggle="popover"]').popover(
     ).on('mouseenter', function () {
         var _this = this;
         $(this).popover('show');
         $('.popover').on('mouseleave', function () {
             $(_this).popover('hide');
         });
     }).on('mouseleave', function () {
         var _this = this;
         setTimeout(function () {
             if (!$('.popover:hover').length) {
                 $(_this).popover('hide');
             }
         }, 300);
     });

    // Prepare the preview for profile picture
    $("#id_image").change(function () {
        readURL(this);
    });
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#ImagePreview').attr('src', e.target.result).fadeIn('slow');
        }
        reader.readAsDataURL(input.files[0]);
    }
}


// AJAX for commenting
function create_comment() {
    console.log("create comment is working!"); // sanity check
    var url = $("#comment_form").attr('action') + '/add_comment/';
    console.log(url);
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        data: {comment_text: $('#comment-text').val()}, // data sent with the post request

        // handle a successful response
        success: function (json) {
            $('#comment-text').val(''); // remove the value from the input

            // obtain values from json object
            var user = json["user"];
            var date = json["created"];
            var user_pic_url = json["user_pic_url"];
            var text = json["text"];
            var comment_count = json["number_of_comments"];

            // generate the new comment's html using the values above
            var new_comment = "<div class=\"card\">\n" +
                "\t\t\t<div class=\"card-body\">\n" +
                "\t\t\t\t<div class=\"media\">\n" +
                "\t\t\t\t\t<a href=\"/lememe/user/" + user + "\">\n" +
                "\t\t\t\t\t\t<img class=\"d-flex mr-3 image-cropper\" \n" +
                "\t\t\t\t\t\t\tsrc=\"" + user_pic_url + "\"\n" +
                "\t\t\t\t\t\t\tonerror=\"this.src='/static/images/placeholder_profile.png' %}'\"\n" +
                "\t\t\t\t\t\t\talt=\"Generic placeholder image\">\n" +
                "\t\t\t\t\t</a>\n" +
                "\t\t\t\t\t<div class=\"media-body\">\n" +
                "\t\t\t\t\t\t<div class=\"mt-0 text-left\">\n" +
                "\t\t\t\t\t\t\t<a href=\"/lememe/user/" + user + "\">" + user + "</a> -\n" +
                "\n" +
                "\t\t\t\t\t\t\t<span class=\"card-subtitle mb-2 text-muted\">" + date + "</span>\n" +
                "\t\t\t\t\t\t\t</div>\n" +
                "\t\t\t\t\t\t\t<p class=\"card-text text-left\">\n" +
                "\t\t\t\t\t\t\t\t" + text + "\n" +
                "\t\t\t\t\t\t\t</p>\n" +
                "\t\t\t\t\t\t</div>\n" +
                "\t\t\t\t\t</div>\n" +
                "\t\t\t\t</div>\n" +
                "\t\t\t</div>\n" +
                "\t\t</div>";

            // Insert new comment and update comment count
            document.getElementById("all_comments").innerHTML = new_comment + document.getElementById("all_comments").innerHTML;
            document.getElementById("number_of_comments").innerHTML = comment_count;
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


// Submit post on submit
$('#comment_form').on('submit', function (event) {
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_comment();
});

