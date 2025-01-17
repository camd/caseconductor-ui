/*jslint    browser:    true,
            indent:     4 */
/*global    ich, jQuery */

var CC = (function (CC, $) {

    'use strict';

    $(function () {
        // plugins
        $('.details:not(html)').html5accordion();
        $('#messages').messages({
            handleAjax: true,
            closeLink: '.message'
        });
        $('input[placeholder], textarea[placeholder]').placeholder();
        $('.selectruns').html5finder({
            loading: true,
            ellipsis: true,
            headerSelector: '.listordering',
            sectionSelector: '.col',
            sectionContentSelector: '.colcontent',
            sectionClasses: [
                'products',
                'cycles',
                'runs'
            ],
            sectionItemSelectors: [
                'input[name="product"]',
                'input[name="testcycle"]',
                'input[name="testrun"]'
            ],
            callback: function () {
                $('.selectruns + .environment').slideUp('fast');
            },
            lastChildCallback: function (choice) {
                var environments = $('.selectruns + .environment').css('min-height', '169px').slideDown('fast'),
                    ajaxUrl = $(choice).data("sub-url");
                environments.loadingOverlay();
                $.get(ajaxUrl, function (data) {
                    environments.loadingOverlay('remove');
                    environments.html(data.html);
                });
            }
        });
        $('.managedrill').html5finder({
            loading: true,
            horizontalScroll: true,
            scrollContainer: '.finder',
            ellipsis: true,
            headerSelector: '.listordering',
            sectionSelector: '.col',
            sectionContentSelector: '.colcontent',
            sectionClasses: [
                'products',
                'cycles',
                'runs',
                'suites'
            ],
            sectionItemSelectors: [
                'input[name="product"]',
                'input[name="testcycle"]',
                'input[name="testrun"]',
                'input[name="testsuite"]'
            ]
        });
        $('.resultsdrill').html5finder({
            loading: true,
            horizontalScroll: true,
            scrollContainer: '.finder',
            ellipsis: true,
            headerSelector: '.listordering',
            sectionSelector: '.col',
            sectionContentSelector: '.colcontent',
            sectionClasses: [
                'products',
                'cycles',
                'runs',
                'cases'
            ],
            sectionItemSelectors: [
                'input[name="product"]',
                'input[name="testcycle"]',
                'input[name="testrun"]',
                'input[name="testrunincludedtestcase"]'
            ]
        });

        // local.js
        CC.inputHadFocus();

        // manage-results.js
        CC.autoCompleteFiltering();
        CC.loadListItemDetails();
        CC.manageActionsAjax();
        CC.formOptionsFilter("#addsuite", "product-id", "#id_product", "#id_cases");
        CC.formOptionsFilter("#addrun", "product-id", "#id_test_cycle", "#id_suites");
        CC.autoCompleteCaseTags('#addcase');
        CC.testcaseAttachments('#single-case-form .attachments');
        CC.testcaseVersioning('#addcase');

        // manage-env.js
        CC.createEnvProfile();
        CC.editEnvProfile();

        // manage-tags.js
        CC.manageTags('#managetags');

        // runtests.js
        CC.hideEmptyRuntestsEnv();
        CC.autoFocus('.details.stepfail > .summary', '#run');
        CC.autoFocus('.details.testinvalid > .summary', '#run');
        CC.runTests("#run");
        CC.breadcrumb('.selectruns');
        CC.failedTestBug('#run');
    });

    $(window).load(function () {
        // manage-results.js
        CC.addEllipses();
        CC.openListItemDetails();
    });

    return CC;

}(CC || {}, jQuery));