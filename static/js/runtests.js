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
/*global    ich, jQuery */

var CC = (function (CC, $) {

    'use strict';

    // hide empty run-tests environments form on initial load
    CC.hideEmptyRuntestsEnv = function () {
        $('.selectruns + .environment.empty').hide();
    };

    // Add focus to ``invalid`` and ``fail`` textboxes when expanded
    CC.autoFocus = function (trigger) {
        $(trigger).click(function () {
            if ($(this).parent().hasClass('open')) {
                $(this).parent().find('textarea').focus();
            }
        });
    };

    // Open hierarchical navigation directly to clicked breadcrumb link
    CC.breadcrumb = function (context) {
        $(context).find('.colcontent').each(function () {
            $(this).data('originalHTML', $(this).html());
        });
        $('.runtests-nav .secondary .breadcrumb').click(function () {
            if (!$('.drilldown.details').hasClass('open')) {
                $('.drilldown.details > .summary').click();
            }
            $(context).find('.colcontent').each(function () {
                $(this).html($(this).data('originalHTML'));
            });
            $(context).find('#' + $(this).data('id')).click();
            return false;
        });
    };

    // Ajax submit runtest forms
    CC.testCaseButtons = function (context) {
        $(context).find("button").click(
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                var button = $(this),
                    testcase = button.closest(".item"),
                    container = button.closest("div.form"),
                    data = { action: button.data("action") },
                    inputs = container.find("input"),
                    post = true;
                testcase.loadingOverlay();
                container.find("textarea").add(inputs).each(function () {
                    var val = $(this).val();
                    if (val) {
                        data[$(this).attr("name")] = val;
                    } else {
                        $(this).siblings("ul.errorlist").remove();
                        $(this).before(ich.runtests_form_error());
                        testcase.loadingOverlay('remove');
                        post = false;
                    }
                });
                if (post) {
                    $.post(
                        testcase.data("action-url"),
                        data,
                        function (data) {
                            var id = testcase.attr("id"),
                                newCase;
                            testcase.replaceWith(data.html);
                            newCase = "#" + id;
                            $(newCase).find('.details').andSelf().html5accordion();
                            CC.testCaseButtons(newCase);
                            $(newCase).loadingOverlay('remove');
                            CC.autoFocus('.details.stepfail > .summary');
                            CC.autoFocus('.details.testinvalid > .summary');
                        }
                    );
                }
            }
        );
    };

    return CC;

}(CC || {}, jQuery));