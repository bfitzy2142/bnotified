$(document).ready(function () {

  var response;
  var status = 'False';

  $("#ping").click(function () {
    $('#image').attr("src",'static/peter.gif');
    $('#ping').prop('disabled',true).css('opacity',0.5);
    $('#button_feedback').text('Waiting for response!')
    startTimer();
  })

  //Prepare/Send request
  function startTimer() {
    var xhr = new XMLHttpRequest();
    if (xhr) {


      // open( method, location, isAsynchronous )
      xhr.open("GET", "/set-true", true);
      xhr.send();

      setInterval(function () {
        if (status == 'True' && $('#button_feedback').text() == 'Waiting for response!') {
          xhr.open("GET", '/data');
          xhr.send();
        }
      }, 2000);


      setTimeout(function () {
        status = 'False';
        xhr.open("GET", '/set-false');
        xhr.send();
        $('#button_feedback').text('')
        $('#ping').prop('disabled',false).css('opacity',1);
        $('#image').attr("src",'static/tenor.gif');
      }, 20000);

      xhr.onload = function () {

        //call script to wait for Rpi response here

        if (xhr.responseText == 'True' || xhr.responseText == 'False') {
          status = xhr.responseText;
        }

        var response = jQuery.parseJSON(xhr.responseText);
        if (typeof response == 'object') {
          audio_name = $.parseJSON(xhr.responseText)
          $('#button_feedback').text("Now Playing: " + audio_name['playing'])
        }
      };
    }
  }





})