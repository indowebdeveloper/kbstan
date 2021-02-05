(function($) {
	"use strict"

	// Mobile Nav toggle
	$('.menu-toggle > a').on('click', function (e) {
		e.preventDefault();
		$('#responsive-nav').toggleClass('active');
	})

	// Fix cart dropdown from closing
	$('.cart-dropdown').on('click', function (e) {
		e.stopPropagation();
	});

	/////////////////////////////////////////

	// Products Slick
	$('.products-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			slidesToShow: 4,
			slidesToScroll: 1,
			autoplay: true,
			infinite: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
			responsive: [{
	        breakpoint: 991,
	        settings: {
	          slidesToShow: 2,
	          slidesToScroll: 1,
	        }
	      },
	      {
	        breakpoint: 480,
	        settings: {
	          slidesToShow: 1,
	          slidesToScroll: 1,
	        }
	      },
	    ]
		});
	});

	// Products Widget Slick
	$('.products-widget-slick').each(function() {
		var $this = $(this),
				$nav = $this.attr('data-nav');

		$this.slick({
			infinite: true,
			autoplay: true,
			speed: 300,
			dots: false,
			arrows: true,
			appendArrows: $nav ? $nav : false,
		});
	});

	/////////////////////////////////////////

	

	/////////////////////////////////////////

})(jQuery);

$( document ).ready(function() {
	const initial_min_price = $('#filters_price_min').val(); // this field is populated by DJANGO and it holds the lowest price any product has
	const initial_max_price = $('#filters_price_max').val(); // this field is populated by DJANGO and it holds the highest price any product has

	// setup the price-range slider
	$(".js-range-slider").ionRangeSlider({
		type: "double",
		min: parseFloat(initial_min_price) /* prices divided by 1000 to enable our 'k'-postfix - Rupiah prices are really high! */,
		max: parseFloat(initial_max_price) /* prices divided by 1000 to enable our 'k'-postfix - Rupiah prices are really high! */,
		from: parseFloat(initial_min_price) /* prices divided by 1000 to enable our 'k'-postfix - Rupiah prices are really high! */,
		to: parseFloat(initial_max_price) /* prices divided by 1000 to enable our 'k'-postfix - Rupiah prices are really high! */,
		grid: true,
		postfix: '',
		prefix: 'Rp',
		grid_num: 5,
		onChange: function (data) {
			// Called every time handle position is changed
			$('#filters_price_min').val(data.from); // the input-field with this ID holds the real value of the price_min /// the *1000 is necessary, because above I divide by 1000 to enable our 'k'-postfix
			$('#filters_price_max').val(data.to); // the input-field with this ID holds the real value of the price_max /// the *1000 is necessary, because above I divide by 1000 to enable our 'k'-postfix
        }
	});

	// setup search field
	try {
		const searchTerm = window.location.href;
		const escaped_search = searchTerm.split("q=")[1]; // this is the search with all the "escaped" special characters (e.g. "good year" turns into "good%20year")
		if(escaped_search) { // sometimes, the "/?q=" is "undefined", but we shouldn't write that into the search field
			$('#search').val(unescape(escaped_search)); // because of the escaped search, we need to unescape() the string
		}
	}
	catch(err) {
		console.log(err);
	}
});

function showQuickview(el) {
	const name = $(el).attr('data-product-name');
	const price = $(el).attr('data-product-price');
	const description = $(el).siblings('.hidden-description').html();
	const productLink = $(el).attr('data-product-link');

	const previewImageNames = $(el).siblings('.hidden-qv-img').children('p');
	console.log(previewImageNames.length);

	const qvModal = $('#quickviewModal');
	$(qvModal).find('.qv-product-name').html(name);
	$(qvModal).find('.qv-product-name a').attr("href",productLink );
	$(qvModal).find('.qv-product-description').html(description);
	$(qvModal).find('.qv-price').html(price);
	
	$(qvModal).find('.carousel-inner').empty(); // remove all previous carousel elements to make it reusable
	
	if(previewImageNames.length == 0) { // if there is no images, hide the slow show
		$('#product-qv-slider').addClass('d-none'); 
	}
	for (let i = 0; i < previewImageNames.length; i++) {
		$('#product-qv-slider').removeClass('d-none'); // make slideshow visible in case the previously quickviewed product hid the slideshow cause it didnt have any images

		let newSlideEl = $(qvModal).find('#qv-image-template').clone();
		let name = $(previewImageNames[i]).html();
		$(newSlideEl).removeClass('d-none');
		$(newSlideEl).css('background-image','url(" '+ name +' ")');
		$(newSlideEl).attr('id','');
		if(i==0) {
			$(newSlideEl).addClass('active');
		}
		$(qvModal).find('.carousel-inner').append(newSlideEl);
		console.log('success');
	}

	$('#quickviewModal').modal('show')
}