$(document).ready(  function() {
    function log( message ) {
      $( "<div>" ).text( message ).prependTo( "#log" );
      $( "#log" ).scrollTop( 0 );
    }
    console.log("mmm")
    $( "#birds" ).autocomplete({
      source: "item_names.json",
      minLength: 2,
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.label );
      }
    });
  } );