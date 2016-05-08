function startRecording(e){
	e.preventDefault();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"start_recording",
		},
		success:function(json){
			$("#btn_record").removeClass( "btn-default" ).addClass( "btn-success" );
			$("#btn_record").html("<span class='glyphicon glyphicon-record'></span>Recording...");
			$("#btn_record").attr("color", "white;");
			$("#btn_stop").prop( "disabled", false );;
			console.log(json);
		}
	});
}

function stopRecording(e){
	e.preventDefault();
	$.ajax({
		type:'GET',
		url:"{% url 'record' app_label model_name pk %}",
		data:{
			action:"stop_recording",
		},
		success:function(json){
			$("#btn_record").attr("style", "background-color:white;");
			$("#btn_record").html("<span class='glyphicon glyphicon-record'></span>Record");
			console.log(json);
		}
	});
}