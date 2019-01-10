function displayVals() {
  // When using jQuery 3:
  // var multipleValues = $( "#multiple" ).val();
  var singleValues = $( "#choices" ).val();
  if (singleValues == ''){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t1").hide();
    $("#m1").hide();
    $("#i1").hide();

  }
  if (singleValues == 'T'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t1").show();
    $("#m1").hide();
    $("#i1").hide();

  }
  if (singleValues == 'I'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t1").hide();
    $("#m1").hide();
    $("#i1").show();

  }
  if (singleValues == 'M'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t1").hide();
    $("#m1").show();
    $("#i1").hide();

  }
}

$( "#choices" ).change( displayVals );
displayVals();

function displayVals1() {
  var singleValues = $( "#choices1" ).val();
  // When using jQuery 3:
  // var multipleValues = $( "#multiple" ).val();
  if (singleValues == ''){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t2").hide();
    $("#m2").hide();
    $("#i2").hide();
  }
  if (singleValues == 'T'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t2").show();
    $("#m2").hide();
    $("#i2").hide();
  }
  if (singleValues == 'I'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t2").hide();
    $("#m2").hide();
    $("#i2").show();
  }
  if (singleValues == 'M'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t2").hide();
    $("#m2").show();
    $("#i2").hide();
  }
}

$( "#choices1" ).change( displayVals1 );
displayVals1();


function displayVals2() {
  var singleValues = $( "#choices2" ).val();
  // When using jQuery 3:
  // var multipleValues = $( "#multiple" ).val();
  if (singleValues == ''){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t3").hide();
    $("#m3").hide();
    $("#i3").hide();
  }
  if (singleValues == 'T'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t3").show();
    $("#m3").hide();
    $("#i3").hide();
  }
  if (singleValues == 'I'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t3").hide();
    $("#m3").hide();
    $("#i3").show();
  }
  if (singleValues == 'M'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t3").hide();
    $("#m3").show();
    $("#i3").hide();
  }
}

$( "#choices2" ).change( displayVals2 );
displayVals2();

function displayVals3() {
  var singleValues = $( "#choices3" ).val();
  // When using jQuery 3:
  // var multipleValues = $( "#multiple" ).val();
  if (singleValues == ''){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t4").hide();
    $("#m4").hide();
    $("#i4").hide();
  }
  if (singleValues == 'T'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t4").show();
    $("#m4").hide();
    $("#i4").hide();
  }
  if (singleValues == 'I'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t4").hide();
    $("#m4").hide();
    $("#i4").show();
  }
  if (singleValues == 'M'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t4").hide();
    $("#m4").show();
    $("#i4").hide();
  }
}

$( "#choices3" ).change( displayVals3 );
displayVals3();

function displayVals4() {
  var singleValues = $( "#choices4" ).val();
  // When using jQuery 3:
  // var multipleValues = $( "#multiple" ).val();
  if (singleValues == ''){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t5").hide();
    $("#m5").hide();
    $("#i5").hide();
  }
  if (singleValues == 'T'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t5").show();
    $("#m5").hide();
    $("#i5").hide();
  }
  if (singleValues == 'I'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t5").hide();
    $("#m5").hide();
    $("#i5").show();
  }
  if (singleValues == 'M'){
    $( "h5" ).html( "<b>Single:</b> " + singleValues  );
    $("#t5").hide();
    $("#m5").show();
    $("#i5").hide();
  }
}

$( "#choices4" ).change( displayVals4 );
displayVals4();


var i = 1
$( "#add" ).click(function() {
  $("#item"+i).show();
  $("#li"+i).show();
  if (i < 6){
    i = i +1;
    $('#add').prop('disabled', false);
    $('#minus').prop('disabled', false);
  }
  if (i == 6){
    $('#add').prop('disabled', true);
    $('#adds').prop('disabled', false);
  }

});

$( "#minus" ).click(function() {
  if (i >= 0){
    i = i -1;
    $('#minus').prop('disabled', false);
    $('#add').prop('disabled', false);
    $('#adds').prop('disabled', false);

  }
  $("#item"+i).hide();
  $("#li"+i).hide();

  if (i == 1){
    $('#minus').prop('disabled', true);

  }
});

var maxLength = 180;
$('#Identity1').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength-length;
  $('#chars').text(length);
});
$('#MC1').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength-length;
  $('#char').text(length);
});

$('#TF1').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength-length;
  $('#ch').text(length);
});


var maxLength1 = 180;
$('#Identity2').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength1-length;
  $('#chars1').text(length);
});

$('#MC2').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength1-length;
  $('#char1').text(length);
});

$('#TF2').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength1-length;
  $('#ch1').text(length);
});

var maxLength2 = 180;
$('#Identity3').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength2-length;
  $('#chars2').text(length);
});

$('#MC3').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength2-length;
  $('#char2').text(length);
});

$('#TF3').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength2-length;
  $('#cr2').text(length);
});

var maxLength3 = 180;
$('#Identity4').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength3-length;
  $('#chars3').text(length);
});

$('#MC4').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength3-length;
  $('#char3').text(length);
});

$('#TF4').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength3-length;
  $('#ch3').text(length);
});


var maxLength4 = 180;
$('#Identity5').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength4-length;
  $('#chars4').text(length);
});

$('#MC5').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength4-length;
  $('#char4').text(length);
});

$('#TF5').keyup(function() {
  var length = $(this).val().length;
  var length = maxLength4-length;
  $('#ch4').text(length);
});

