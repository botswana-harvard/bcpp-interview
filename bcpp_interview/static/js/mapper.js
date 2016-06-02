function setUpPage() {
    $('#id-button-cancel').click( function () {
        window.location = '{{ next_url }}';
    });
    $('#id-image-map').attr('src', '{% static src_image_zoom1 %}');
    $('#id-button-zoom1').click( function () {
        var image_map_path = '{% static src_image_zoom1 %}';
        $('#id-image-map').attr('src', image_map_path);
        $('#id-image-map-name').text(image_map_path);
        $('#id-button-zoom1').addClass('btn-primary');
        $('#id-button-zoom2').addClass('btn-default').removeClass('btn-primary');
        $('#id-button-zoom3').addClass('btn-default').removeClass('btn-primary');
        });
    $('#id-button-zoom2').click( function () {
        var image_map_path = '{{ MEDIA_URL }}{{ src_image_zoom2}}';
        $('#id-image-map').attr('src', image_map_path);
        $('#id-image-map-name').text(image_map_path);
        $('#id-button-zoom2').addClass('btn-primary');
        $('#id-button-zoom1').addClass('btn-default').removeClass('btn-primary');
        $('#id-button-zoom3').addClass('btn-default').removeClass('btn-primary');
        });
    $('#id-button-zoom3').click( function () {
        var image_map_path = '{{ MEDIA_URL }}{{ src_image_zoom3 }}';
        $('#id-image-map').attr('src', image_map_path);
        $('#id-image-map-name').text(image_map_path);
        $('#id-button-zoom3').addClass('btn-primary');
        $('#id-button-zoom1').addClass('btn-default').removeClass('btn-primary');
        $('#id-button-zoom2').addClass('btn-default').removeClass('btn-primary');
        });
    return true;
};
