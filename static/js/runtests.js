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
    CC.autoFocus = function (trigger, context) {
        $(context).find(trigger).click(function () {
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
    CC.runTests = function (container) {
        var context = $(container),
            tests = context.find('.item.action-ajax-replace'),
            ajaxFormsInit = function (test) {
                var forms = test.find('form');

                forms.ajaxForm({
                    beforeSubmit: function (arr, form, options) {
                        test.loadingOverlay();
                    },
                    success: function (response) {
                        var newTest = $(response.html);
                        test.loadingOverlay('remove');
                        if (response.html) {
                            test.replaceWith(newTest);
                            ajaxFormsInit(newTest);
                            newTest.find('.details').andSelf().html5accordion();
                            CC.autoFocus('.details.stepfail > .summary', newTest);
                            CC.autoFocus('.details.testinvalid > .summary', newTest);
                        }
                    }
                });
            };

        tests.each(function () {
            var thisTest = $(this);
            ajaxFormsInit(thisTest);
        });
    };

    CC.failedTestBug = function (container) {
        var context = $(container);

        context.delegate('.item .stepfail input[type="radio"][name="bugs"]', 'change', function () {
            var thisList = $(this).closest('.stepfail'),
                newBug = thisList.find('input[type="radio"].newbug'),
                newBugInput = thisList.find('input[type="url"][name="related_bug"]');

            if (newBug.is(':checked')) {
                newBugInput.removeAttr('disabled');
            } else {
                newBugInput.attr('disabled', true);
            }
        });
    };

    return CC;

}(CC || {}, jQuery));