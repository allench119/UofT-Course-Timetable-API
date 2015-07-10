
    // Closes the sidebar menu
    $("#menu-close").click(function(e) {
        e.preventDefault();
        $("#sidebar-wrapper").toggleClass("active");
    });

    // Opens the sidebar menu
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#sidebar-wrapper").toggleClass("active");
    });
    
    // scrolling animation
    $(function() {
        
        $('a[href*=#]:not([href=#])').click(function() {
            console.log(this.pathname.replace(/^\//, ''))
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') || location.hostname == this.hostname) {

                var target = $(this.hash);
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    });
    
    /*
    //randomly change home background
    $(function() {
        var images = ['bg01.jpg', 'bg02.jpg', 'bg03.jpg'];

        $('.header').css({'background-image': 'url(/img/' + images[Math.floor(Math.random() * images.length)] + ')'});
    });*/

    //request photos from flickr and make it as the background 
    $(function() {
        var flickrURL = "https://api.flickr.com/services/rest/?" +
                        "method=flickr.people.getPhotos" +
                        "&api_key=8dc21c0ccf12456f0bc646fd0da94480" +
                        "&user_id=118407044@N07" +
                        "&format=json" +
                        "&jsoncallback=?";
        
        $.ajax({
                url: flickrURL,
                dataType: "jsonp",
                success: function(response){
                            if (response['stat'] == "ok"){  

                                console.log("flickr ajax succeed");
                                var total = response["photos"]["total"];
                                var photos = response["photos"]["photo"];
                                var size = "b";
                                var photo_selected = photos[Math.floor(Math.random() * total)];

                                var photoURL = "https://farm" + photo_selected.farm + ".staticflickr.com/" 
                                                + photo_selected.server + "/" + photo_selected.id 
                                                + "_" + photo_selected.secret + "_" + size + ".jpg";
                                $('.header').css({'background-image':
                                                    "linear-gradient(rgba(0, 0, 0, 0.1),rgba(0, 0, 0, 0.1))," +
                                                    "url(" + photoURL + ")"});

                                }else{
                                    console.log("flickr failed");
                                }
                             }
                })

    });











