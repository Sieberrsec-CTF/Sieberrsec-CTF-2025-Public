// ==UserScript==
// @name         Google Form Autofill
// @version      2025-07-16
// @description  Based on client side input validation
// @author       Enxgmatic
// @match        https://docs.google.com/forms/d/e/*
// @grant        none
// @icon         https://www.google.com/s2/favicons?sz=64&domain=google.com
// @run-at       document-idle
// @require      https://gist.github.com/Enxgmatic/9d91534565a95b5628af6639c8a6ab94/raw/7c9935c59b4a8f52f9db24e2d9a87211f81ba784/randexp.min.js
// ==/UserScript==

/* globals RandExp */
// adapted from https://github.com/zerodytrash/Google-Forms-Quiz-Solver/blob/main/Google-Forms-Quiz-Solver.user.js

(function() {
    'use strict';

    window.fillForm = () => {

        // skip form if already filled by url params
        if(location.href.indexOf("?entry.") > 0) return;

        var inputAreas = document.querySelectorAll("div[data-params]");
        var urlPrefillParams = new URLSearchParams();

        inputAreas.forEach((inputArea) => {
            try {

                var areaParams = inputArea.getAttribute("data-params");
                var decodedAreaParams = JSON.parse("[" + areaParams.substr(areaParams.indexOf("["), areaParams.length));
                var questionParams = decodedAreaParams[0][4][0];
                var questionEntryId = questionParams[0];
                var validationParams = questionParams[4];

                // if validation disabled
                if(validationParams.length === 0) return;

                var validationRule = validationParams[0];
                var valueToFill = null;

                // type: short answer, number && match: equal to
                if(validationRule[0] === 1 && validationRule[1] === 5) {
                    valueToFill = validationRule[2][0];
                }

                // type: short answer, number && match: less than
                if(validationRule[0] === 1 && validationRule[1] === 3) {
                    valueToFill = '' + Number(validationRule[2][0]) - 1;
                }

                // type: short answer, number && match: greater than
                if(validationRule[0] === 1 && validationRule[1] === 1) {
                    valueToFill = '' + Number(validationRule[2][0]) + 1;
                }

                // type: short answer, number && match: between
                if(validationRule[0] === 1 && validationRule[1] === 7) {
                    valueToFill = Math.random() * (Number(validationRule[2][1]) - Number(validationRule[2][0])) + Number(validationRule[2][0]) + '';
                }

                // type: short answer, text && match: contains
                if(validationRule[0] === 2 && validationRule[1] === 100) {
                    valueToFill = validationRule[2][0];
                }

                // type: short answer, text && match: min length
                if(validationRule[0] === 6 && validationRule[1] === 203) {
                    valueToFill = 'A'.repeat(Number(validationRule[2][0]));
                }

                // type: text && match: regex
                if(validationRule[0] === 4 && validationRule[1] === 301) {
                    valueToFill = new RandExp(validationRule[2][0]).gen();
                }

                // type: long answer, text && match: contains
                if(validationRule[0] === 4 && validationRule[1] === 299) {
                    valueToFill = validationRule[2][0];
                }

                console.log(valueToFill);

                if(valueToFill !== null) urlPrefillParams.set("entry." + questionEntryId, valueToFill);

            } catch(ex) {
                console.error("Param decoding failed", ex, inputArea);
            }
        });

        if(Array.from(urlPrefillParams).length > 0) {
            if(confirm("Found " + Array.from(urlPrefillParams).length + " exact values in form validation. Prefill form?")) {
                location.search = urlPrefillParams;
            }
        }
    }

    document.querySelector('body').addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            window.fillForm();
        }
    });
})();