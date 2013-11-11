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
					'right': "40.4%",
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
			annotation = getFeatureById($(this).data('annotation'));
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
						annotator.saveAnnotation(annotation);
					}

				});

				$('#delete').click(function(event) {
					var features = annotator.vectorLayer.features;
					var features_length = features.length;
					var selected_features = [];
					var vectors_list = [];
					for (var i = 0; i < features_length; i++) {
						for (var j = 0; j < selectedAnnotations.annotations.length; j++) {
							if (features[i].graph == selectedAnnotations.annotations[j].graph) {
								selected_features.push(features[i]);
								console.log(features[i])
							}
						}
					}

					var j = 0;
					for (var i = 0; i < selected_features.length; i++) {
						annotator.deleteAnnotation(annotator.vectorLayer, selected_features[i], selected_features.length);
						var element = $('.annotation_li[data-graph="' + selected_features[i].graph + '"]');
						element.fadeOut().remove();
					}

				});
			}

			initialLoad = false;

			if (!selectedAnnotations.annotations.length) {
				$("#modal_features").fadeOut();
				$('.select_annotation_checkbox').attr('checked', false);
				return false;
			} else {
				$("#modal_features").fadeIn();
			}

			load_annotations_allographs(annotation);

			var to_lightbox = $('.to_lightbox');
			to_lightbox.click(function() {
				var array = [];
				var annotations = selectedAnnotations.annotations;
				for (var j = 0; j < annotations.length; j++) {
					array.push(annotations[j].graph);
				}
				location.href = 'http://lightbox-dev.dighum.kcl.ac.uk/?annotations=[' + array.toString() + ']';
			});

		}
	});
});