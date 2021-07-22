$('.filter_motives_button').click(function(event) {

  // Remove the class 'btn-primary' to 'deselect' the three buttons
  $('.filter_motives_button').removeClass('btn-primary');
  // Add the class 'btn-primary' to the clicked button to 'select' it
  $(event.target).addClass('btn-primary');

  // If the clicked button is 'Only characters',
  // we look at the attribute 'is_story_character' of each option:
  // if 'is_story_character' is true, we show the option, else we hide it
  if (event.target.id == 'filter_by_only_characters') {
    $('select[name=allograph] option').each(function(index, option) {
      $(option).attr('is_story_character') == 'true' ? $(option).show() : $(option).hide();
    });
  }
  // If the clicked button is 'No characters',
  // we look at the attribute 'is_story_character' of each option:
  // if 'is_story_character' is true, we hide the option, else we show it
  else if (event.target.id == 'filter_by_no_characters') {
    $('select[name=allograph] option').each(function(index, option) {
      $(option).attr('is_story_character') == 'true' ? $(option).hide() : $(option).show();
    });
  }
  // If the clicked button is 'All', we show all the options
  else {
    $('select[name=allograph] option').each(function(index, option) {
      $(option).show();
    });
  }

  // The event 'liszt:updated' is triggered to update the options of the select
  $('select[name=allograph]').trigger('liszt:updated');
});
