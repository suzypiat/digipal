jQuery(function($){

  // If original_version is True, the translator field is disabled
  // If original_version is False, the translator field is enabled and required

  let original_version_checkbox = $('#id_original_version');
  let translator_select = $('#id_translator');

  function update_translator_select() {
    if (original_version_checkbox.is(':checked')) {
      translator_select.prop('disabled', true);
      translator_select.val('');
    }
    else {
      translator_select.prop('disabled', false);
    }
  }

  original_version_checkbox.on('change', function() {
    update_translator_select();
  });

  update_translator_select();

});
