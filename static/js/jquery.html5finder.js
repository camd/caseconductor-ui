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
            indent:     4,
            confusion:  true */
/*global    jQuery */

/**
 * jQuery html5finder 0.1
 *
 * Copyright (c) 2011, Jonny Gerig Meyer
 * All rights reserved.
 *
 * Licensed under the New BSD License
 * See: http://www.opensource.org/licenses/bsd-license.php
 */
(function ($) {

    'use strict';

    $.fn.html5finder = function (opts) {
        var options = $.extend({}, $.fn.html5finder.defaults, opts),
            context = $(this),
            numberCols = options.sectionClasses.length,
            sections = context.find(options.sectionSelector),
            i,

            // Set the width of each section to account for vertical scroll-bars
            headers = context.find(options.headerSelector).each(function () {
                var scrollbarWidth = $(this).closest(options.sectionSelector).css('width') - $(this).children('li').css('width');
                $(this).css('right', scrollbarWidth);
            }),

            // We want to be able to treat already-selected items differently
            markSelected = function () {
                context.find(options.selected).data('selected', true);
                context.find(options.notSelected).data('selected', false);
            },

            // Define the function for updating ellipses on long text
            updateEllipsis = function () {
                if (options.ellipsis === true) {
                    var target = context.find(options.sectionContentSelector + ' ' + options.ellipsisTarget);
                    $.doTimeout('updateEllipsis', 300, function () {
                        target.ellipsis();
                    });
                    $(window).resize(function () {
                        $.doTimeout('resize', 300, function () {
                            target.ellipsis();
                        });
                    });
                }
            },

            // Define the function for horizontal scrolling:
            // Scrolls to the previous section (so that the active section is centered)
            horzScroll = function () {
                if (options.horizontalScroll === true) {
                    var scrollTarget,
                        currentScroll = context.find(options.scrollContainer).scrollLeft();
                    if (context.find(options.sectionSelector + '.focus').is(':first-child')) {
                        scrollTarget = 0;
                    } else {
                        scrollTarget = currentScroll + context.find(options.sectionSelector + '.focus').prev(options.sectionSelector).position().left;
                    }
                    context.find(options.scrollContainer).animate({scrollLeft: scrollTarget});
                }
            },

            itemClick = function (i) {
                context.find(options.sectionItemSelectors[i]).live('click', function () {
                    var thisItem = $(this),
                        container = thisItem.closest(options.sectionSelector),
                        ajaxUrl = thisItem.data('sub-url'),
                        target = container.next(options.sectionSelector);
                    // Clicking an already-selected input only scrolls (if applicable), adds focus, and empties subsequent sections
                    if (thisItem.data('selected') === true && !container.hasClass('focus')) {
                        container.addClass('focus').siblings(options.sectionSelector).removeClass('focus');
                        container.next(options.sectionSelector).find('input:checked').removeAttr('checked').data('selected', false);
                        container.next(options.sectionSelector).nextAll(options.sectionSelector).children('ul').empty();
                        horzScroll();
                        updateEllipsis();
                        if (!container.is(':last-child') && options.callback) {
                            options.callback();
                        }
                    } else {
                        // Last-child section only receives focus on-click by default
                        if (container.is(':last-child')) {
                            if (options.lastChildCallback) {
                                options.lastChildCallback(this);
                            }
                        } else {
                            // Add a loading screen while waiting for the Ajax call to return data
                            if (options.loading === true) {
                                target.loadingOverlay();
                            }
                            // Add returned data to the next section
                            $.get(
                                ajaxUrl,
                                function (response) {
                                    container.next(options.sectionSelector).children(options.sectionContentSelector).html(response.html);
                                    container.next(options.sectionSelector).loadingOverlay('remove');
                                    updateEllipsis();
                                }
                            );
                            container.removeClass('focus').prevAll(options.sectionSelector).removeClass('focus');
                            container.next(options.sectionSelector).addClass('focus').children('ul').empty();
                            container.next(options.sectionSelector).nextAll(options.sectionSelector).removeClass('focus').children('ul').empty();
                            horzScroll();
                            if (options.callback) {
                                options.callback();
                            }
                        }
                        markSelected();
                    }
                });
            };

        context.find('.finder').data('cols', numberCols);
        markSelected();
        updateEllipsis();

        // Enable headers to engage section focus, and sort column if section already has focus
        // Sorting requires jQuery Element Sorter plugin ( http://plugins.jquery.com/project/ElementSort )
        headers.find('a').live('click', function () {
            var container = $(this).closest(options.sectionSelector),
                list = container.find(options.sectionContentSelector),
                selectorClass = $(this).parent().attr('class').substring(2),
                type = $(this).parent().data('sort'),
                direction;
            if (container.hasClass('focus')) {
                if ($(this).hasClass('asc') || $(this).hasClass('desc')) {
                    $(this).toggleClass('asc').toggleClass('desc');
                    $(this).parent().siblings().find('a').removeClass('asc').removeClass('desc');
                } else {
                    $(this).addClass('asc');
                    $(this).parent().siblings().find('a').removeClass('asc').removeClass('desc');
                }
                if ($(this).hasClass('asc')) {
                    direction = 'asc';
                }
                if ($(this).hasClass('desc')) {
                    direction = 'desc';
                }
                if (type === 'number') {
                    selectorClass = selectorClass + ' .number';
                }
                if (type === 'date') {
                    list.sort({
                        sortOn: '.' + selectorClass,
                        direction: direction,
                        sortType: 'string'
                    });
                }
                list.sort({
                    sortOn: '.' + selectorClass,
                    direction: direction,
                    sortType: type
                });
            } else {
                context.find(options.sectionSelector).removeClass('focus');
                container.addClass('focus');
                updateEllipsis();
                horzScroll();
            }
            $(this).blur();
            return false;
        });

        for (i = 0; i < numberCols; i = i + 1) {
            itemClick(i);
        }
    };

    /* Setup plugin defaults */
    $.fn.html5finder.defaults = {
        loading: false,                     // If true, adds a loading overlay while waiting for Ajax response
        horizontalScroll: false,            // If true, automatically scrolls to center the active section
        scrollContainer: null,              // The container (window) to be automatically scrolled
        scrollSpeed: 500,                   // Speed of the scroll (in ms)
        ellipsis: false,                    // If true, adds ellipsis to long text
                                                // [This requires the jquery.text-overflow.js plugin by default]
        ellipsisTarget: '.title',           // The target text to be shortened
        selected: 'input:checked',          // A selected element
        notSelected: 'input:not(:checked)', // An unselected element
        headerSelector: 'header',           // Section headers
        sectionSelector: 'section',         // Sections
        sectionContentSelector: 'ul',       // Content to be replaced by Ajax function
        sectionClasses: [                   // Classes for each section
            'section1',
            'section2',
            'section3'
        ],
        sectionItemSelectors: [             // Selectors for items in each section
            'input[name="section1"]',
            'input[name="section2"]',
            'input[name="section3"]'
        ],
        callback: null,                     // Callback function, currently runs after input in any section (except lastChild) is selected
        lastChildCallback: null             // Callback function, currently runs after input in last section is selected
    };
}(jQuery));