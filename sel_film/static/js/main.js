$(document).ready(function () {
	"use strict"; // start of use strict

	/*==============================
	Menu
	==============================*/
	$('.header__btn').on('click', function() {
		$(this).toggleClass('header__btn--active');
		$('.header__nav').toggleClass('header__nav--active');
		$('.body').toggleClass('body--active');

		if ($('.header__search-btn').hasClass('active')) {
			$('.header__search-btn').toggleClass('active');
			$('.header__search').toggleClass('header__search--active');
		}
	});

	/*==============================
	Search
	==============================*/
	$('.header__search-btn').on('click', function() {
		$(this).toggleClass('active');
		$('.header__search').toggleClass('header__search--active');

		if ($('.header__btn').hasClass('header__btn--active')) {
			$('.header__btn').toggleClass('header__btn--active');
			$('.header__nav').toggleClass('header__nav--active');
			$('.body').toggleClass('body--active');
		}
	});

	/*==============================
	Home
	==============================*/
	$('.home__bg').owlCarousel({
		animateOut: 'fadeOut',
		animateIn: 'fadeIn',
		mouseDrag: false,
		touchDrag: false,
		items: 1,
		dots: false,
		loop: true,
		autoplay: false,
		smartSpeed: 700,
		margin: 0,
	});

	$('.home__cover').each( function() {
		if ($(this).attr("data-bg")){
			$(this).css({
				'background': 'url(' + $(this).data('bg') + ')',
				'background-position': 'center center',
				'background-repeat': 'no-repeat',
				'background-size': 'cover'
			});
		}
	});

	$('.home__carousel').owlCarousel({
		mouseDrag: false,
		touchDrag: false,
		dots: false,
		loop: true,
		autoplay: false,
		smartSpeed: 700,
		margin: 20,
		responsive : {
			0 : {
				items: 2,
			},
			576 : {
				items: 2,
			},
			768 : {
				items: 3,
				margin: 30,
			},
			992 : {
				items: 4,
				margin: 30,
			},
			1200 : {
				items: 4,
				margin: 40
			},
		}
	});

	$('.home__nav--next').on('click', function() {
		$('.home__carousel, .home__bg').trigger('next.owl.carousel');
	});
	$('.home__nav--prev').on('click', function() {
		$('.home__carousel, .home__bg').trigger('prev.owl.carousel');
	});

	$(window).on('resize', function() {
		var itemHeight = $('.home__bg').height();
		$('.home__bg .item').css("height", itemHeight + "px");
	});
	$(window).trigger('resize');

	/*==============================
	Tabs
	==============================*/
	$('.content__mobile-tabs-menu li').each( function() {
		$(this).attr('data-value', $(this).text().toLowerCase());
	});

	$('.content__mobile-tabs-menu li').on('click', function() {
		var text = $(this).text();
		var item = $(this);
		var id = item.closest('.content__mobile-tabs').attr('id');
		$('#'+id).find('.content__mobile-tabs-btn input').val(text);
	});

	/*==============================
	Section bg
	==============================*/
	$('.section--bg, .details__bg').each( function() {
		if ($(this).attr("data-bg")){
			$(this).css({
				'background': 'url(' + $(this).data('bg') + ')',
				'background-position': 'center center',
				'background-repeat': 'no-repeat',
				'background-size': 'cover'
			});
		}
	});

	/*==============================
	Filter
	==============================*/
	$('.filter__item-menu li').each( function() {
		$(this).attr('data-value', $(this).text().toLowerCase());
	});

	$('.filter__item-menu li').on('click', function() {
		var text = $(this).text();
		var item = $(this);
		var id = item.closest('.filter__item').attr('id');
		$('#'+id).find('.filter__item-btn input').val(text);

		if (id.slice(8) == 'genre') {
			if ($('#hidden_filter_genre').length == 0) {
				var input_el = $(`<input id="hidden_filter_genre" type="text" hidden="true" name="${id.slice(8)}">`).val(text);
				input_el.insertAfter($('#'+id).find('.filter__item-btn input'));
			} else {
				$('#hidden_filter_genre').val(text);
			};
		} else if (id.slice(8) == 'country') {
			if ($('#hidden_filter_country').length == 0) {
				var input_el = $(`<input id="hidden_filter_country" type="text" hidden="true" name="${id.slice(8)}">`).val(text);
				input_el.insertAfter($('#'+id).find('.filter__item-btn input'));
			} else {
				$('#hidden_filter_country').val(text);
			};
		};
	});

	/*==============================
	Scroll bar
	==============================*/
	$('.scrollbar-dropdown').mCustomScrollbar({
		axis: "y",
		scrollbarPosition: "outside",
		theme: "custom-bar"
	});

	$('.accordion').mCustomScrollbar({
		axis: "y",
		scrollbarPosition: "outside",
		theme: "custom-bar2"
	});

	$('.dashbox__table-wrap').mCustomScrollbar({
		axis: "x",
		scrollbarPosition: "outside",
		theme: "custom-bar3",
		advanced: {
			autoExpandHorizontalScroll: 2
		}
	});

	/*==============================
	Morelines
	==============================*/
	$('.card__description--details').moreLines({
		linecount: 5,
		baseclass: 'b-description',
		basejsclass: 'js-description',
		classspecific: '_readmore',
		buttontxtmore: "",
		buttontxtless: "",
		animationspeed: 400
	});

	/*==============================
	Gallery
	==============================*/
	var initPhotoSwipeFromDOM = function(gallerySelector) {

		// parse slide data (url, title, size ...) from DOM elements 
		// (children of gallerySelector)
		var parseThumbnailElements = function(el) {
			var thumbElements = el.childNodes,
				numNodes = thumbElements.length,
				items = [],
				figureEl,
				linkEl,
				size,
				item;

			for(var i = 0; i < numNodes; i++) {

				figureEl = thumbElements[i]; // <figure> element

				// include only element nodes 
				if(figureEl.nodeType !== 1) {
					continue;
				}

				linkEl = figureEl.children[0]; // <a> element

				size = linkEl.getAttribute('data-size').split('x');

				// create slide object
				item = {
					src: linkEl.getAttribute('href'),
					w: parseInt(size[0], 10),
					h: parseInt(size[1], 10)
				};



				if(figureEl.children.length > 1) {
					// <figcaption> content
					item.title = figureEl.children[1].innerHTML; 
				}

				if(linkEl.children.length > 0) {
					// <img> thumbnail element, retrieving thumbnail url
					item.msrc = linkEl.children[0].getAttribute('src');
				} 

				item.el = figureEl; // save link to element for getThumbBoundsFn
				items.push(item);
			}

			return items;
		};

		// find nearest parent element
		var closest = function closest(el, fn) {
			return el && ( fn(el) ? el : closest(el.parentNode, fn) );
		};

		// triggers when user clicks on thumbnail
		var onThumbnailsClick = function(e) {
			e = e || window.event;
			e.preventDefault ? e.preventDefault() : e.returnValue = false;

			var eTarget = e.target || e.srcElement;

			// find root element of slide
			var clickedListItem = closest(eTarget, function(el) {
				return (el.tagName && el.tagName.toUpperCase() === 'FIGURE');
			});

			if(!clickedListItem) {
				return;
			}

			// find index of clicked item by looping through all child nodes
			// alternatively, you may define index via data- attribute
			var clickedGallery = clickedListItem.parentNode,
				childNodes = clickedListItem.parentNode.childNodes,
				numChildNodes = childNodes.length,
				nodeIndex = 0,
				index;

			for (var i = 0; i < numChildNodes; i++) {
				if(childNodes[i].nodeType !== 1) { 
					continue; 
				}

				if(childNodes[i] === clickedListItem) {
					index = nodeIndex;
					break;
				}
				nodeIndex++;
			}



			if(index >= 0) {
				// open PhotoSwipe if valid index found
				openPhotoSwipe( index, clickedGallery );
			}
			return false;
		};

		// parse picture index and gallery index from URL (#&pid=1&gid=2)
		var photoswipeParseHash = function() {
			var hash = window.location.hash.substring(1),
			params = {};

			if(hash.length < 5) {
				return params;
			}

			var vars = hash.split('&');
			for (var i = 0; i < vars.length; i++) {
				if(!vars[i]) {
					continue;
				}
				var pair = vars[i].split('=');  
				if(pair.length < 2) {
					continue;
				}           
				params[pair[0]] = pair[1];
			}

			if(params.gid) {
				params.gid = parseInt(params.gid, 10);
			}

			return params;
		};

		var openPhotoSwipe = function(index, galleryElement, disableAnimation, fromURL) {
			var pswpElement = document.querySelectorAll('.pswp')[0],
				gallery,
				options,
				items;

			items = parseThumbnailElements(galleryElement);

			// define options (if needed)
			options = {

				// define gallery index (for URL)
				galleryUID: galleryElement.getAttribute('data-pswp-uid'),

				getThumbBoundsFn: function(index) {
					// See Options -> getThumbBoundsFn section of documentation for more info
					var thumbnail = items[index].el.getElementsByTagName('img')[0], // find thumbnail
						pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
						rect = thumbnail.getBoundingClientRect(); 

					return {x:rect.left, y:rect.top + pageYScroll, w:rect.width};
				}

			};

			// PhotoSwipe opened from URL
			if(fromURL) {
				if(options.galleryPIDs) {
					// parse real index when custom PIDs are used 
					// http://photoswipe.com/documentation/faq.html#custom-pid-in-url
					for(var j = 0; j < items.length; j++) {
						if(items[j].pid == index) {
							options.index = j;
							break;
						}
					}
				} else {
					// in URL indexes start from 1
					options.index = parseInt(index, 10) - 1;
				}
			} else {
				options.index = parseInt(index, 10);
			}

			// exit if index not found
			if( isNaN(options.index) ) {
				return;
			}

			if(disableAnimation) {
				options.showAnimationDuration = 0;
			}

			// Pass data to PhotoSwipe and initialize it
			gallery = new PhotoSwipe( pswpElement, PhotoSwipeUI_Default, items, options);
			gallery.init();
		};

		// loop through all gallery elements and bind events
		var galleryElements = document.querySelectorAll( gallerySelector );

		for(var i = 0, l = galleryElements.length; i < l; i++) {
			galleryElements[i].setAttribute('data-pswp-uid', i+1);
			galleryElements[i].onclick = onThumbnailsClick;
		}

		// Parse URL and open gallery if it contains #&pid=3&gid=1
		var hashData = photoswipeParseHash();
		if(hashData.pid && hashData.gid) {
			openPhotoSwipe( hashData.pid ,  galleryElements[ hashData.gid - 1 ], true, true );
		}
	};
	// execute above function
	initPhotoSwipeFromDOM('.gallery');

	/*==============================
	Player
	==============================*/
	function initializePlayer() {
		if ($('#player').length) {
			const player = new Plyr('#player');
		} else {
			return false;
		}
		return false;
	}
	$(window).on('load', initializePlayer());

	/*==============================
	Range sliders
	==============================*/
	/*1*/
	function initializeFirstSlider() {
		if ($('#filter__years').length) {
			var firstSlider = document.getElementById('filter__years');
			noUiSlider.create(firstSlider, {
				range: {
					'min': 1900,
					'max': 2021
				},
				step: 1,
				connect: true,
				start: [1900, 2021],
				format: wNumb({
					decimals: 0,
				})
			});
			var firstValues = [
				document.getElementById('filter__years-start'),
				document.getElementById('filter__years-end')
			];
			firstSlider.noUiSlider.on('update', function( values, handle ) {
				firstValues[handle].innerHTML = values[handle];

				var years_start = document.getElementById('filter__years-start').innerHTML;
				var years_end = document.getElementById('filter__years-end').innerHTML;

				if ($('#years_start').length == 0) {
					var years_start_el = $(`<input id="years_start" type="text" hidden="true" name="years_start">`).val(years_start);
					years_start_el.insertAfter(document.getElementById('filter__years-start'));
				} else {
					$('#years_start').val(years_start);
				};

				if ($('#years_end').length == 0) {
					var years_end_el = $(`<input id="years_end" type="text" hidden="true" name="years_end">`).val(years_end);
					years_end_el.insertAfter(document.getElementById('filter__years-end'));
				} else {
					$('#years_end').val(years_end);
				};
			});
		} else {
			return false;
		}
		return false;
	}
	$(window).on('load', initializeFirstSlider());

	/*2*/
	function initializeSecondSlider() {
		if ($('#filter__imbd').length) {
			var secondSlider = document.getElementById('filter__imbd');
			noUiSlider.create(secondSlider, {
				range: {
					'min': 0,
					'max': 10
				},
				step: 0.1,
				connect: true,
				start: [0.1, 9.9],
				format: wNumb({
					decimals: 1,
				})
			});

			var secondValues = [
				document.getElementById('filter__imbd-start'),
				document.getElementById('filter__imbd-end')
			];

			secondSlider.noUiSlider.on('update', function( values, handle ) {
				secondValues[handle].innerHTML = values[handle];

				var imbd_start = document.getElementById('filter__imbd-start').innerHTML;
				var imbd_end = document.getElementById('filter__imbd-end').innerHTML;

				if ($('#imbd_start').length == 0) {
					var imbd_start_el = $(`<input id="imbd_start" type="text" hidden="true" name="imbd_start">`).val(imbd_start);
					imbd_start_el.insertAfter(document.getElementById('filter__imbd-start'));
				} else {
					$('#imbd_start').val(imbd_start);
				};

				if ($('#imbd_end').length == 0) {
					var imbd_end_el = $(`<input id="imbd_end" type="text" hidden="true" name="imbd_end">`).val(imbd_end);
					imbd_end_el.insertAfter(document.getElementById('filter__imbd-end'));
				} else {
					$('#imbd_end').val(imbd_end);
				};
			});

			$('.filter__item-menu--range').on('click.bs.dropdown', function (e) {
				e.stopPropagation();
				e.preventDefault();
			});

		} else {
			return false;
		}
		return false;
	}
	$(window).on('load', initializeSecondSlider());

	/*3*/
	function initializeThirdSlider() {
		if ($('#slider__rating').length) {
			var thirdSlider = document.getElementById('slider__rating');
			noUiSlider.create(thirdSlider, {
				range: {
					'min': 0,
					'max': 10
				},
				connect: [true, false],
				step: 0.1,
				start: 8.6,
				format: wNumb({
					decimals: 1,
				})
			});

			var thirdValue = document.getElementById('form__slider-value');

			thirdSlider.noUiSlider.on('update', function( values, handle ) {
				thirdValue.innerHTML = values[handle];
				$('#hidden_rating_input').val(values[handle]);
			});
		} else {
			return false;
		}
		return false;
	}
	$(window).on('load', initializeThirdSlider());
	
	// Copy film title
	$('#copy__btn').on('click', function () {
		var copy_text = $('#copy__btn').closest('a').innerHTML;
		console.log(copy_text)
	})
});