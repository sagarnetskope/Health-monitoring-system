 $(document).ready(function(){
       $("#clear").click(function(){
        $("#center,#kilograms,#BMI,#feet,#inch,#pounds").val("")
            var chart = $('#container').highcharts();
                chart.series[0].setData([10]);
        $("label.error").hide();
        $(".error").removeClass("error");
             });


       $("#button2").click(function(){
      $("#fm2").hide(900)
      $("#fm1").show(900)
      $("#feet,#inch,#pounds,#BMI").val("")
      $("label.error").hide();
      $(".error").removeClass("error");
      });

     $("#button1").click(function(){
      $("#fm1").hide(1000)
      $("#fm2").show(1000)
      $("#center,#kilograms,#BMI").val("")
      $("label.error").hide();
      $(".error").removeClass("error");
      });

            $("#compute").click(function(){
        if ($("#feet").is(':visible')){
            if ($('#fm2').valid())
            {
            var feet =$("#feet").val();
            if ($("#inch").val() == "") {$("#inch").val("0");}
            var inch =$("#inch").val();
            var pounds =parseInt($("#pounds").val());
            var inch1=feet*12;
            var inch2=inch1+parseInt(inch);
            var pounds1=pounds*703
            var BMI1 = pounds1/(inch2*inch2);
            var BMIS = Math.round(BMI1*10)/10;
            var xx=1
            $("#BMI").val(BMIS);
            var chart = $('#container').highcharts();
            chart.series[0].setData([BMIS]);
            }}
        else if ($('#fm1').valid())
               {
               var centimeter = $("#center").val();
               var kilogram =  $("#kilograms").val();
               var BMI2 = kilogram/((centimeter/100)*(centimeter/100));
               var BMIM = Math.round(BMI2*10)/10;
               $("#BMI").val(BMIM);
               var chart = $('#container').highcharts();
                chart.series[0].setData([BMIM]);
             };




        });
     });