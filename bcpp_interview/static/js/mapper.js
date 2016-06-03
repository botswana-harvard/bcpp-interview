function imageViewReady(jsonData) {

    var djContext = jsonData;
    
    djContext = JSON.parse(djContext);
    
    var zoomLevels = djContext.zoom_levels;
    var imageFileNames = djContext.image_filenames;

    if ( imageFileNames != null ) {

        $( '#id-button-add-point' ).click( function () {
            window.location = djContext.add_point_url;
        });
        $( '#id-button-back-call' ).click( function () {
            window.location = djContext.back_call_url;
        });
        $( '#id-button-back-subject' ).click( function () {
            window.location = djContext.back_subject_url;
        });
        // setup images and zoom buttons
        $.each( imageFileNames, function( zoomLevel, imageFilename ) {
            var imageId = 'id-image-map-' + zoomLevel;
            var buttonId = 'id-button-zoom-' + zoomLevel;
            // set the image src for each image 
            makeImg( 'div-image-maps-container', imageId, imageFilename );
            // make and append Zoom buttons
            makeDefaultButton( 'div-zoom-buttons-container', buttonId, 'Zoom ' + zoomLevel );
            // set click function for each Zoom button
            $( '#' + 'id-button-zoom-' + zoomLevel ).click( function() {
                $.each( zoomLevels, function( i, val ) {
                    $( '#id-image-map-' + val ).hide();  // hide all images
                    $( '#id-button-zoom-' + val ).removeClass( 'btn-primary' ).addClass( 'btn-default' ); // set all buttons to default
                });  //each            
                // this button has focus
                $( '#id-button-zoom-' + zoomLevel).removeClass( 'btn-default' ).addClass( 'btn-primary' );
                displayImageOrAlert(zoomLevel);
            });
        });

        $( '#div-missing-image-alert' ).text( '' ).hide();
        $( '#div-landmarks' ).show();
        $( '#id-button-zoom-' + zoomLevels[0] ).click();

    } else {
        // or show the missing image alert
        $( '#div-missing-image-alert' ).text( 'No image maps are available for this location' ).show();
    };
}

function makeDefaultButton ( divId, buttonId, label ) {
    var cssClass = 'btn btn-sm btn-default';
    var button = '<button id="' + buttonId + '" type="button" class="' + cssClass + '">' + label + '</button>';
    $('#' + divId).append(button);
};

function makeImg ( divId, imageId, imageFilename ) {
    var cssClass = 'img-rounded img-responsive';
    var img = '<img id="' + imageId + '" class="' + cssClass + '"/>';
    $('#' + divId).append(img);
    $( '#' + imageId ).attr( 'src', imageFilename ).attr( 'title', imageFilename ).hide();
}

function displayImageOrAlert( zoomLevel ) {
    //check if the image exists, otherwise show alert
    $.ajax({
        url: $( '#id-image-map-'+ zoomLevel ).attr( 'src' ),
        type:'HEAD',
        error: function () {
            $( '#id-image-map-' + zoomLevel ).hide();
            $( '#div-missing-image-alert' ).text( 'Image is not available at this zoom level' ).show();
        },
        success: function () {
            $( '#id-image-map-' + zoomLevel ).show();
            $( '#div-missing-image-alert' ).text( '' ).hide();
        },
    });    
}