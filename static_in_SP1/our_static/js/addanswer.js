var ctr = 0
$( "#answer1" ).click(function() {
    // alert( "Handler for .click() called." );
    ctr=ctr+1;
    $("#h1_"+ctr).show();
    if (ctr == 4){
        $('#answer1').prop('disabled', true);        
    }
    if (ctr == 0){
        $('#answer1').prop('disabled', false);        
        $('#mins1').prop('disabled', true);        
    }
    if (ctr >0){
        $('#mins1').prop('disabled', false);        
    }
    // alert( ctr );

  });

  $( "#mins1" ).click(function() {
    // alert( ctr );
    $("#h1_"+ctr).hide();
    ctr=ctr-1;

    if (ctr == 4){
        $('#answer1').prop('disabled', true);        
    }
    if (ctr == 0){
        $('#mins1').prop('disabled', true);        
    }
    if (ctr >0){
        $('#mins1').prop('disabled', false);        
    }
    if (ctr < 3){
        $('#answer1').prop('disabled', false);        
    }

  });

var ctr1 = 0
$( "#answer2" ).click(function() {
    // alert( "Handler for .click() called." );
    ctr1=ctr1+1;
    $("#h2_"+ctr1).show();
    if (ctr1 == 3){
        $('#answer2').prop('disabled', true);        
    }
    if (ctr1 == 0){
        $('#answer2').prop('disabled', false);        
        $('#mins2').prop('disabled', true);        
    }
    if (ctr1 >0){
        $('#mins2').prop('disabled', false);        
    }
    // alert( ctr );

  });

  $( "#mins2" ).click(function() {
    // alert( ctr );
    $("#h2_"+ctr1).hide();
    ctr1=ctr1-1;

    if (ctr1 == 3){
        $('#answer2').prop('disabled', true);        
    }
    if (ctr1 == 0){
        $('#mins2').prop('disabled', true);        
    }
    if (ctr1 >0){
        $('#mins2').prop('disabled', false);        
    }
    if (ctr1 < 3){
        $('#answer2').prop('disabled', false);        
    }

  });

var ctr2 = 0
$( "#answer3" ).click(function() {
    // alert( "Handler for .click() called." );
    ctr2=ctr2+1;
    $("#h3_"+ctr2).show();
    if (ctr2 == 3){
        $('#answer3').prop('disabled', true);        
    }
    if (ctr2 == 0){
        $('#answer3').prop('disabled', false);        
        $('#mins3').prop('disabled', true);        
    }
    if (ctr2 >0){
        $('#mins3').prop('disabled', false);        
    }
    // alert( ctr );

  });

  $( "#mins3" ).click(function() {
    // alert( ctr );
    $("#h3_"+ctr2).hide();
    ctr2=ctr2-1;

    if (ctr2 == 3){
        $('#answer3').prop('disabled', true);        
    }
    if (ctr2 == 0){
        $('#mins3').prop('disabled', true);        
    }
    if (ctr2 >0){
        $('#mins3').prop('disabled', false);        
    }
    if (ctr2 < 3){
        $('#answer3').prop('disabled', false);        
    }

  });
var ctr3 = 0
$( "#answer4" ).click(function() {
    // alert( "Handler for .click() called." );
    ctr3=ctr3+1;
    $("#h4_"+ctr3).show();
    if (ctr3 == 3){
        $('#answer4').prop('disabled', true);        
    }
    if (ctr3 == 0){
        $('#answer4').prop('disabled', false);        
        $('#mins4').prop('disabled', true);        
    }
    if (ctr3 >0){
        $('#mins4').prop('disabled', false);        
    }
    // alert( ctr );

  });

  $( "#mins4" ).click(function() {
    // alert( ctr );
    $("#h4_"+ctr3).hide();
    ctr3=ctr3-1;

    if (ctr3 == 3){
        $('#answer4').prop('disabled', true);        
    }
    if (ctr3 == 0){
        $('#mins4').prop('disabled', true);        
    }
    if (ctr3 >0){
        $('#mins4').prop('disabled', false);        
    }
    if (ctr3 < 3){
        $('#answer4').prop('disabled', false);        
    }

  });
var ctr4 = 0
$( "#answer5" ).click(function() {
    // alert( "Handler for .click() called." );
    ctr4=ctr4+1;
    $("#h5_"+ctr4).show();
    if (ctr4 == 3){
        $('#answer5').prop('disabled', true);        
    }
    if (ctr4 == 0){
        $('#answer5').prop('disabled', false);        
        $('#mins5').prop('disabled', true);        
    }
    if (ctr4 >0){
        $('#mins5').prop('disabled', false);        
    }
    // alert( ctr );

  });
$( "#mins5" ).click(function() {
    // alert( ctr );
    $("#h5_"+ctr4).hide();
    ctr4=ctr4-1;

    if (ctr4 == 4){
        $('#answer5').prop('disabled', true);        
    }
    if (ctr4 == 0){
        $('#mins5').prop('disabled', true);        
    }
    if (ctr4 >0){
        $('#mins5').prop('disabled', false);        
    }
    if (ctr4 < 4){
        $('#answer5').prop('disabled', false);        
    }

  });

  $(document).ready(function() {
    $('#dataTables-example').DataTable({
        responsive: true
    });
});