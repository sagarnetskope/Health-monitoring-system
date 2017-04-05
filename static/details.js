//var disable== ("calculate");
//song.attr('disabled', true);
//$("#calculate").attr('disabled', true);
//document.getElementById("calculate").disabled = true;
$(document).ready(function() {//$("#calculate").attr('disabled', true);
   $('.input-group input[required], .input-group textarea[required], .input-group select[required]').on('keyup, change', function() {
        var $group = $(this).closest('.input-group'),
			$addon = $group.find('.input-group-addon'),
			$icon = $addon.find('span'),
			state = false;

    	if (!$group.data('validate')) {
			state = $(this).val() ? true : false;
		}else if ($group.data('validate') == "email") {
			state = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($(this).val())
		}else if($group.data('validate') == 'phone') {
			state = /^[(]{0,1}[0-9]{3}[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/.test($(this).val())
            a++;
		}else if ($group.data('validate') == "length") {
			state = $(this).val().length >= $group.data('length') ? true : false;
		}else if ($group.data('validate') == "number") {
			state = !isNaN(parseFloat($(this).val())) && isFinite($(this).val());
		}
		if (state) {
				$addon.removeClass('danger');
				$addon.addClass('success');
				$icon.attr('class', 'glyphicon glyphicon-ok');
		}else{
				$addon.removeClass('success');
				$addon.addClass('danger');
				$icon.attr('class', 'glyphicon glyphicon-remove');
    	}
 });

});


/*	function b(a){
		var b=$("#gain_loss_amount");
		b.empty();$.each(a,function(a,c){
			var d={value:c};
			0===c&&(d.selected="selected");
			b.append($("<option></option>").attr(d).text(a))
		})}
		var a={"Lose 2 Pounds per Week":-1000,"Lose 1.5 Pounds per Week":-750,"Lose 1 Pounds per Week":-500,"Lose 0.5 Pounds per Week":-250,"Stay the Same Weight":0,"Gain 0.5 Pound per Week":250,"Gain 1 Pound per Week":500,"Gain 1.5 Pounds per Week":750,"Gain 2 Pounds per Week":1E3},
		var c={"Lose 1 Kg per Week":-1100,"Lose 0.75 Kg per Week":-825,"Lose 0.5 Kg per Week":-550,"Lose 0.25 Kg per Week":-275,"Stay the Same Weight":0,"Gain 0.25 Kg per Week":275,"Gain 0.5 Kg per Week":550,"Gain 0.75 Kg per Week":825,"Gain 1 Kg per Week":1100};
			});
*/

/* function validateDailyCalsValues(b){
	var a="";$.isNumeric($("#age").val())||(a+="Age value must be a number\n");
	$.isNumeric($("#weight").val())||(a+="Weight value must be a number\n");
	$.isNumeric($("#inches").val())||(a=a+(b?"Feet ":"Height ")+"value must be a number\n");
//    (!$("activity_level").val())(a="balls")
//	var c=$("#inches").val();b&&(!$.isNumeric(c)&&!(12>parseFloat(c)))&&(a+="Inches value must be a number less than 12\n");
	return a
}
*/
function calcDailyCals(){
	//var b="standard"===$("input[name='units']:checked").val(),
//    a=validateDailyCalsValues(b);
//	if(a)alert(a);
    //if(state)alert("Fill in all values");
//  if(a)alert("Fill in all fields!");
//	else{
		var a=parseFloat($("#weight").val());
		b=(a*=0.453592);
		//var c=parseFloat($("#feet_cm").val());
        var c=parseFloat($("#inches").val());
		b=(c=2.54*c);
		var d=parseFloat($("#age").val()),e=$("input[name='sex']:checked").val(),b=$("#activity_level").val(),
		a="male"==e?88.362+13.397*a+4.799*c-5.677*d:447.593+9.247*a+3.098*c-4.33*d;
		"no"===b?a*=1.2:"light"===b?a*=1.375:"moderate"===b?a*=1.55:"heavy"===b?a*=1.725:"extreme"===b&&(a*=1.9);
		a=Math.round(a+parseInt($("#gain_loss_amount").val()));
        $("#calAmount").text(500<a?a:0);
		$("#dc_results").show();
        //if(a>0)
         //   $("#recommendations").show();

}//}

function resetForm(){
    $(':input').not(':button, :submit, :reset, :hidden, :checkbox, :radio').val('');
    $(':checkbox, :radio').prop('checked', false);
    location.reload();
}
