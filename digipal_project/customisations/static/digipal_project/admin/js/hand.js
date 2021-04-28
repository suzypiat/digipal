jQuery(function($){

  // API request to get all contributor records
  function getContributors() {
    let res;
    $.ajax({
      async: false,
      url: '/digipal/api/scribe/',
      method: 'GET',
      success: function(data) {
        res = data.results;
      }
    })
    return res;
  };
  contributors = getContributors();

  // API request to get a contributor by id
  function getContributor(id) {
    let res;
    let url = `/digipal/api/scribe/${id}/`;
    $.ajax({
      async: false,
      url: url,
      method: 'GET',
      success: function(data) {
        res = data.results[0];
      }
    })
    return res;
  };

  // API request to get all contributor type records
  function getContributorTypes() {
    let res;
    $.ajax({
      async: false,
      url: '/digipal/api/bonhum_contributortype/',
      method: 'GET',
      success: function(data) {
        res = data.results;
      }
    })
    return res;
  };
  contributor_types = getContributorTypes();

  // The contributor_type_select is filled with the values sent by the API
  fillContributorTypeSelect();

  let initial_type_id;

  // If the select for the contributor field is empty,
  // we are adding a new hand
  if ($('#id_scribe').val() == '') {
    // We get the first type that appears in the contributor_type_select
    initial_type_id = $('#id_contributor_type').val();
  }
  // If the select for the contributor field is not empty,
  // we are changing an existing hand and we need to know the type of the contributor
  else {
    // We get the contributor associated to the hand from the values sent by the API
    let contributor = contributors.find(contrib => contrib.id == $('#id_scribe').val());
    if (contributor) {
      // We get the id of the type this contributor belongs to
      initial_type_id = contributor.type__id;
      // We select the corresponding type in the contributor_type_select
      $('#id_contributor_type').val(initial_type_id);
    }
  }

  // The contributor_select is updated in order to display
  // only contributors whose type matches the selected type
  updateContributorSelect(initial_type_id);
  // Hide or show the fields related to a scribe
  toggleScribeFields(initial_type_id);

  // Each time the user changes the value of contributor_type_select
  $('#id_contributor_type').on('change', function() {
    // We store the type selected by the user
    let selected_type_id = $('#id_contributor_type').val();
    // The contributor_select is updated in order to display
    // only contributors whose type matches the selected type
    updateContributorSelect(selected_type_id);
    // Hide or show the fields related to a scribe
    toggleScribeFields(selected_type_id);
  });

  // The contributor_type_select is filled with the values sent by the API
  function fillContributorTypeSelect() {
    let options = {};
    contributor_types.forEach((result) => {
      options[result.id] = result.str;
    });
    $.each(options, function(id, str) {
      $('#id_contributor_type').append($('<option></option>').attr('value', id).text(str));
    });
  }

  // The contributor_select is filtered according
  // to the selected contributor_type (given as parameter)
  function updateContributorSelect(type_id) {
    // If there was already a contributor selected, we store it
    let selected_before = $('#id_scribe').val();
    let selected_after;
    $('#id_scribe option:gt(0)').each(function(index) {
      let contributor = contributors.find(contrib => contrib.id == $(this).val());
      if (contributor) {
        contributor.type__id != type_id ? $(this).hide() : $(this).show();
        if ($(this).val() == selected_before && contributor.type__id == type_id) {
          selected_after = $(this).val();
        }
      }
      else {
        // If the contributor is not in the list, it is because it has been added
        // dynamically by the user; we get it with an API request and push it
        // to the list of contributors
        new_contributor = getContributor($(this).val());
        contributors.push(new_contributor);
        new_contributor.type__id != type_id ? $(this).hide() : $(this).show();
        if ($(this).val() == selected_before && new_contributor.type__id == type_id) {
          selected_after = $(this).val();
        }
      }
    });
    // If there was already a contributor selected before,
    // and its type is the selected one, we re-select the contributor
    selected_after ? $('#id_scribe').val(selected_after) : $('#id_scribe').val('');
  }

  // We look at the name of the selected contributor_type (given as parameter):
  // if it is 'painter', the fields related to a scribe are hidden,
  // else they are shown
  function toggleScribeFields(type_id) {
    let type = contributor_types.find(contrib_type => contrib_type.id == type_id);
    let scribe_fields = $('fieldset.module:nth-child(6)');
    if (type) {      
      type.name.toLowerCase() == 'peintre' ? scribe_fields.hide() : scribe_fields.show();
    }
  }

});
