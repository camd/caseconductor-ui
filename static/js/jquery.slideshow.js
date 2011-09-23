/*
Case Conductor is a Test Case Management system.
Copyright (C) 2011 uTest Inc.

This file is part of Case Conductor.

Case Conductor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Case Conductor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.

*/
/*jslint    browser:    true,
            indent:     4 */
/*global    jQuery */

/**
 * jQuery slideshow 0.1
 *
 * Copyright (c) 2011, Jonny Gerig Meyer
 * All rights reserved.
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */
(function ($) {

    'use strict';

    $.fn.slideshow = function (opts) {
        var options = $.extend({}, $.fn.slideshow.defaults, opts),
            hash,
            context = $(this),
            slides = context.find(options.slidesSelector),
            slideLinks = context.find(options.slideLinksSelector),
            showSlide = function (slide) {
                var thisLink = slideLinks.filter('a[href="#' + $(slide).attr('id') + '"]');
                $(slide).addClass('active-slide').removeClass('inactive-slide');
                $(slide).siblings(options.slidesSelector).removeClass('active-slide').addClass('inactive-slide').fadeOut('fast', function () {
                    $(slide).fadeIn('fast', options.callback);
                });
                slideLinks.removeClass('active');
                thisLink.addClass('active');
            };

        slideLinks.click(function (e) {
            e.preventDefault();
            showSlide($(this).attr('href'));
            $(this).blur();
        });

        if (window.location.hash) {
            hash = window.location.hash.substring(1);
            if (slides.filter('[id^="' + hash + '"]').length) {
                showSlide(slides.filter('[id^="' + hash + '"]'));
            }
        }
    };

    /* Setup plugin defaults */
    $.fn.slideshow.defaults = {
        slidesSelector: '.slide',           // Selector for slides
        slideLinksSelector: '.slideLink',   // Selector for links to slides
        callback: null                      // Function to be called after each slide transition
    };
}(jQuery));