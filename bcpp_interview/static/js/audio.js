function startRecording(e){
	e.preventDefault();
	$('#alert-saving').hide();
	$('#alert-saved').hide();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"start_recording",
		},
		success:function(json){
			$("#btn_record").removeClass( "btn-default" ).addClass( "btn-danger" );
			$("#btn_record").prop( "disabled", true );
			$("#btn_stop").prop( "disabled", false );
			console.log(json);
		}
	});
}

function stopRecording(e){
	e.preventDefault();
	$('#alert-saving').show();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"stop_recording",
		},
		success:function(json){
			$("#btn_record").removeClass( "btn-danger" ).addClass( "btn-default" );
			$("#btn_record").prop( "disabled", false );
			$("#btn_stop").prop( "disabled", true );
			$('#alert-saving').hide();
			$('#alert-saved').show();
			console.log(json);
		}
	});
}

/**(function poll() {
    $.ajax({
        url: "{% url 'record' app_label model_name pk %}",
        type: "GET",
        success: function(data) {
			action:"duration",
            console.log("polling");
        },
        dataType: "json",
        complete: setTimeout(function() {poll()}, 5000),
        timeout: 2000
    })
})();
**/