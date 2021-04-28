jQuery(function($){

  // If mythological is True, the story_start_date field is disabled
  // If mythological is False, the story_start_date field is enabled

  let mythological_checkbox = $('#id_mythological');
  let start_date_input = $('#id_story_start_date');

  function update_start_date_input() {
    if (mythological_checkbox.is(':checked')) {
      start_date_input.prop('disabled', true);
      start_date_input.val('');
    }
    else {
      start_date_input.prop('disabled', false);
    }
  }

  mythological_checkbox.on('change', function() {
    update_start_date_input();
  });

  update_start_date_input();



  // If an item_part is selected, edition is null
  // If an edition is selected, item_part is null


  let operation;
  let initial_select;
  let initial_select_id;
  if ($('#id_item_part').val() == '' && $('#id_edition').val() == '') {
    operation = 'add';
  }
  else {
    operation = 'change';
    if ($('#id_item_part').val() != '') {
      initial_select = 'item_part';
      initial_select_id = $('#id_item_part').val();
    }
    else {
      initial_select = 'edition';
      initial_select_id = $('#id_edition').val();
    }
  }

  if (operation == 'add') {
    $('div.get_itempart_work').hide();
    $('div.get_itempart_currentitem').hide();
    $('div.get_edition_work').hide();
  }
  else {
    if ($('#id_item_part').val() == '') {
      $('div.get_itempart_work').hide();
      $('div.get_itempart_currentitem').hide();
    }
    else if ($('#id_edition').val() == '') {
      $('div.get_edition_work').hide();
    }
  }

  $('#id_item_part').on('change', function() {
    if ($('#id_item_part').val() != '') {
      if (initial_select == 'item_part' && $('#id_item_part').val() == initial_select_id) {
        $('div.get_itempart_work').show();
        $('div.get_itempart_currentitem').show();
      }
      else {
        $('div.get_itempart_work').hide();
        $('div.get_itempart_currentitem').hide();
      }

      $('#id_edition').val('');
      $('div.get_edition_work').hide();
    }
    else {
      $('div.get_itempart_work').hide();
      $('div.get_itempart_currentitem').hide();
    }
  });

  $('#id_edition').on('change', function() {
    if ($('#id_edition').val() != '') {
      if (initial_select == 'edition' && $('#id_edition').val() == initial_select_id) {
        $('div.get_edition_work').show();
      }
      else {
        $('div.get_edition_work').hide();
      }

      $('#id_item_part').val('');
      $('div.get_itempart_work').hide();
      $('div.get_itempart_currentitem').hide();
    }
    else {
      $('div.get_edition_work').hide();
    }
  });

});
