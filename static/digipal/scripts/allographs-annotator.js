annotator.url_allographs = true;
annotator.url_annotations = '../annotations';
temporary_vectors = [];

if (annotator.hands_page == "True") {
	annotator.url_annotations = '/digipal/page/61/annotations/';
}
var request = $.getJSON(annotator.url_annotations, function(data) {

	annotator.annotations = data;
});

function style_select(select) {
	$(select).css({
		"float": "left",
		"margin": "0%",
		"margin-left": "3%",
		"margin-right": "3%",
		"margin-bottom": "3%",
		"margin-top": "2%"
	}).addClass('important_width');
}

var chained = request.then(function(data) {


	$('#id_allograph').change(function() {
		updateFeatureSelect();
	});

	var format = annotator.format;
	var layer = annotator.vectorLayer;
	var url_vectors = '../vectors/';
	if (annotator.hands_page == "True") {
		url_vectors = '/digipal/page/61/vectors/';
	}
	var features_request = $.getJSON(url_vectors);

	features_request.then(function(data) {
		var features = [];
		var annotations = annotator.annotations;
		var div = $('.loading-div');
		div.fadeOut().remove();
		div = null;
		for (var j in data) {
			var f = format.read(data[j])[0];
			f.id = j;
			for (var i in annotations) {
				var allograph = annotations[i]['feature'];
				var graph = annotations[i]['graph'];
				var features_list = annotations[i]['features'];
				if (f.id == annotations[i]['vector_id']) {
					f.feature = allograph;
					f.graph = graph;
					f.features = features_list;
				}
			}
			features.push(f);
		}
		// adds all the vectors to the vector layer
		layer.addFeatures(features); // zooms to the max extent of the map area
		var vectors = annotator.vectorLayer.features;

		var summary_shown = true;
		$('#show_summary').click(function() {
			if (summary_shown) {
				$("#summary").animate({
					'right': 0,
					'opacity': 0,
				}, 350, function() {
					$(this).css({
						'display': 'none'
					});
				});


				summary_shown = false;
				$(this).removeClass('active');
			} else {
				$("#summary").css({
					'display': 'block'
				});
				$("#summary").animate({
					'right': "35.4%",
					'opacity': 1
				}, 350);
				summary_shown = true;
				$(this).addClass('active');

			}
		});

		modal = false;
		current_feature = false;
		$("#modal_features").draggable();
		selectedAnnotations = {
			'allograph': null,
			'annotations': []
		};

		function clean_annotations(annotation) {
			var annotations = selectedAnnotations.annotations;
			var length_annotations = annotations.length;
			for (i = 0; i < length_annotations; i++) {
				if (annotations[i].vector_id == annotation.vector_id) {

					selectedAnnotations.annotations.splice(i, 1);
					break;
				}
			}
		}

		/*
		$('.check_all_allographs').click(function(event) {
			var parent = $(this).parent();
			var checkboxes = parent.find('input[type=checkbox]');
			checkboxes.attr('checked', true);
			checkboxes.trigger('click');
		});

		$('.uncheck_all_allographs').click(function(event) {
			var parent = $(this).parent();
			var checkboxes = parent.find('input[type=checkbox]');
			checkboxes.attr('checked', false);
			checkboxes.trigger('click');
		});
*/
		$('.annotation_li a').click(function(event) {
			event.stopPropagation();
		});
		$('.annotation_li').click(function(event) {
			var annotation = getFeatureById($(this).data('annotation'));
			var annotation_li = $(this);
			if (event.target.type != 'checkbox') {
				if (selectedAnnotations.allograph !== null && selectedAnnotations.allograph != annotation.feature) {
					selectedAnnotations.allograph = null;
					selectedAnnotations.annotations = [];
					$('.annotation_li').removeClass('selected');
					$('.annotation_li').data('selected', false);
					temporary_vectors = [];
				}
				if ($(this).data('selected')) {
					clean_annotations(annotation);
					$(this).data('selected', false);
					$(this).removeClass('selected');
					$(this).find('input').attr('checked', false);
				} else {
					temporary_vectors = [];
					selectedAnnotations.annotations = [];
					$('.annotation_li').data('selected', false).removeClass('selected');
					$('.annotation_li').find('input').attr('checked', false);
					selectedAnnotations.allograph = annotation.feature;
					selectedAnnotations.annotations.push(annotation);
					$(this).data('selected', true);
					$(this).addClass('selected');
					$(this).find('input').attr('checked', true);
					modal = true;
				}
			} else {
				var checkbox = $(this).children('p').children("input");
				var checkboxes = $('.select_annotation_checkbox');
				var a = selectedAnnotations.allograph;
				if (selectedAnnotations.allograph && selectedAnnotations.allograph != annotation.feature) {
					selectedAnnotations.allograph = null;
					selectedAnnotations.annotations = [];
					$('.annotation_li').removeClass('selected');
					$('.annotation_li').data('selected', false);
					temporary_vectors = [];
				}
				if (!checkbox.is(':checked')) {
					clean_annotations(annotation);
					annotation_li.data('selected', false);
					annotation_li.removeClass('selected');

				} else {
					selectedAnnotations.allograph = annotation.feature;
					selectedAnnotations.annotations.push(annotation);
					annotation_li.data('selected', true);
					annotation_li.addClass('selected');
					modal = true;
					$.each(checkboxes, function() {
						if ($(this).data('allograph') !== selectedAnnotations.allograph) {
							$(this).attr('checked', false);
						}
					});

				}

			}


			main();
		});

		var initialLoad = true;

		function main() {
			if (modal) {
				if (selectedAnnotations.annotations.length > 1) {
					$('.myModalLabel .label-modal-value').html(annotation.feature + " <span class='badge badge-important'>" + selectedAnnotations.annotations.length + "</span>");
				} else {
					$('.myModalLabel .label-modal-value').html(annotation.feature);
				}
			}

			modal = true;
			if (initialLoad) {
				$('#save').click(function() {
					var features = annotator.vectorLayer.features;
					var features_length = features.length;
					var selected_features = [];
					for (var i = 0; i < features_length; i++) {
						for (var j = 0; j < selectedAnnotations.annotations.length; j++) {
							if (features[i].graph == selectedAnnotations.annotations[j].graph) {
								selected_features.push(features[i]);
							}
						}
					}
					for (i = 0; i < selected_features.length; i++) {
						annotator.selectedFeature = selected_features[i];
						annotator.saveAnnotation();
					}
				});

				$('#delete').click(function(event) {
					var features = annotator.vectorLayer.features;
					var features_length = features.length;
					var selected_features = [];
					for (var i = 0; i < features_length; i++) {
						for (var j = 0; j < selectedAnnotations.annotations.length; j++) {
							if (features[i].graph == selectedAnnotations.annotations[j].graph) {
								selected_features.push(features[i]);
							}
						}
					}

					var j = 0;
					for (var i = 0; i < selected_features.length; i++) {
						annotator.deleteAnnotation(annotator.vectorLayer, selected_features[i], selected_features.length);
					}

				});
			}

			initialLoad = false;

			if (!selectedAnnotations.annotations.length) {
				$("#modal_features").fadeOut();
				return false;
			} else {
				$("#modal_features").fadeIn();
			}

			if (annotation) {
				if (selectedAnnotations.annotations.length > 1) {
					$('.myModalLabel .label-modal-value').html(annotation.feature + " <span class='badge badge-important'>" + selectedAnnotations.annotations.length + "</span>");
				} else {
					$('.myModalLabel .label-modal-value').html(annotation.feature);
				}
				$('#hidden_hand').val(annotation.hidden_hand);
				$('#id_hand').val(annotation.hidden_hand);
				$('#id_allograph').val(getKeyFromObjField(annotation, 'hidden_allograph'));
				$('#hidden_allograph').val(getKeyFromObjField(annotation, 'hidden_allograph'));
				$('#id_display_note').val(annotation.display_note);
				$('#id_internal_note').val(annotation.internal_note);
				$('select').trigger('liszt:updated');
				if (annotator.hands_page == "True") {
					url = '/digipal/graph/' + annotation.graph + '/features/';
				}
				var url = '../graph/' + annotation.graph + '/features/';
				var features_owned = $.ajax({
					url: url,
					dataType: 'json',
					cache: false,
					type: 'GET',
					async: false,
					error: function(xhr, status, error) {
						console.log('Error: ' + error);
					}
				});

				features_owned.done(function(f) {
					array_features_owned = [];
					if (temporary_vectors) {
						array_features_owned = array_features_owned.concat(temporary_vectors);
					}
					var f_length = f.length;
					for (var i = 0; i < f_length; i++) {
						for (var j = 0; j < f[i].feature.length; j++) {
							s = f[i].name;
							s += ':' + f[i].feature[j];
							array_features_owned.push(s);
						}
						s = '';
					}
				});

				$('#id_display_note').parent('p').hide();
				$('#id_internal_note').parent('p').hide();
				var url_features = "../graph/" + annotation.graph;
				if (annotator.hands_page == "True") {
					url_features = "/digipal/page/61/graph/" + annotation.graph;
				}

				var request = $.getJSON(url_features);
				var features = annotator.vectorLayer.features;
				var url2;
				request.done(function(data) {
					var allograph_id = data.id;
					url2 = '../allograph/' + data.id + '/features/';
					if (annotator.hands_page == "True") {
						url2 = "/digipal/page/61/allograph/" + data.id + '/features/';
					}
					var allographs = $.getJSON(url2);
					var s = "<div id='box_features_container'>";
					var string_summary = '';
					allographs.done(function(data) {
						$.each(data, function(idx) {
							component = data[idx].name;
							component_id = data[idx].id;
							var is_empty;
							var features = data[idx].features;
							string_summary += "<span class='component_summary'>" + data[idx].name + "</span>";

							s += "<p class='component_labels' data-id='component_" + component_id + "' style='border-bottom:1px solid #ccc'><b>" + component + " <span class='arrow_component icon-arrow-up'></span></b></p>";

							s += "<div class='checkboxes_div pull-right' style='margin: 1%;'><button data-component = '" + component_id + "' class='check_all btn btn-small'>All</button> <button data-component = '" + component_id + "' class='btn btn-small uncheck_all'>Clear</button></div><div>";

							s += "<div id='component_" + component_id + "' data-hidden='false' class='feature_containers'>";
							var n = 0;

							$.each(features, function(idx) {
								var value = component_id + '::' + features[idx].id;
								var names = component + ':' + features[idx].name;
								var f = selectedAnnotations.annotations;
								var al = '';
								var d = 0;
								var title = '';
								var ann;
								for (var k = 0; k < f.length; k++) {
									for (var j = 0; j < f[k].features.length; j++) {
										if (f[k].features[j] == component_id + '::' + features[idx].id && f[k].feature == annotation.feature) {
											ann = $('input[data-annotation="' + f[k].vector_id + '"]').next().text();
											d++;
											al += '<span class="label">' + ann + '</span> ';
											title += ann + ' ';
											temporary_vectors.push(names);
										}

									}
								}
								var id = component_id + '_' + features[idx].id;
								if (array_features_owned.indexOf(names) >= 0) {

									string_summary += "<span title='" + title + "' class='feature_summary'>" + features[idx].name + ' ' + al + "</span>";

									s += "<p><input checked = 'checked' type='checkbox' value='" + value + "' class='features_box' id='" + id + "' data-feature = '" + features[idx].id + "' /> <label style='font-size:12px;display:inline;vertical-align:bottom;' for='" + id + "'>" + features[idx].name + "</label></p>";
									n++;
								} else {
									s += "<p><input id='" + id + "' type='checkbox' value='" + value + "' class='features_box' data-feature = '" + features[idx].id + "'/> <label style='font-size:12px;display:inline;vertical-align:bottom;' for='" + id + "'>" + features[idx].name + "</label></p>";
								}

							});
							s += "</div>";
							if (!n) {
								string_summary += "<span class='feature_summary'>undefined</span>";
							}
						});
						s += "</div>";
						$("#summary").html(string_summary);
						$('#features_container').html(s);
						$('.check_all').click(function(event) {
							var component = $(this).data('component');
							var checkboxes = $('#component_' + component).find("input[type=checkbox]");
							checkboxes.attr('checked', true);
							event.stopPropagation();
						});
						$('.uncheck_all').click(function(event) {
							var component = $(this).data('component');
							var checkboxes = $('#component_' + component).find("input[type=checkbox]");
							checkboxes.attr('checked', false);
							event.stopPropagation();
						});
						$('.myModal select').chosen();

						var maximized = false;
						$('#maximize').click(function(event) {
							event.preventDefault();
							$('#summary').css("bottom", "67.3%").hide();
							if (!maximized) {
								$('.myModal').animate({
									'position': 'fixed',
									'top': "0px",
									'left': '59.5%',
									"width": '40%',
									"height": '100%'
								}, 200, function() {
									$('#summary').show();
									$('.modal-body').css("max-height", "100%");
								}).draggable("destroy");


								maximized = true;
							} else {
								$('#summary').css("bottom", "88%").hide();
								$('.myModal').animate({
									'position': 'fixed',
									'left': "55%",
									'top': "15%",
									'right': '',
									"width": '30%',
									"height": '60%'
								}, 200, function() {
									$('#summary').show();
									$('.modal-body').css("max-height", "");
								}).draggable();



								maximized = false;
							}
						});

						$('.component_labels').click(function() {
							var div = $("#" + $(this).data('id'));
							if (!div.data('hidden')) {
								$(this).next('.checkboxes_div').hide();
								div.slideUp().data('hidden', true);
								$(this).find('.arrow_component').removeClass('icon-arrow-up').addClass('icon-arrow-down');
							} else {
								div.slideDown().data('hidden', false);
								$(this).next('.checkboxes_div').show();
								$(this).find('.arrow_component').removeClass('icon-arrow-down').addClass('icon-arrow-up');
							}
						});

						//updateFeatureSelect(annotation.features, feature);
						$('#modal_features .close').click(function() {
							$("#modal_features").fadeOut();
							$('#status').html('-');
							modal = false;
							selectedAnnotations.allograph = null;
							selectedAnnotations.annotations = [];
							$('.annotation_li').removeClass('selected');
						});

					});
					$('select').on("liszt:ready", function() {
						style_select('#id_hand_chzn');
						style_select('#id_allograph_chzn');
					});
					$('select').chosen();



				});

			}

		}
	});
});