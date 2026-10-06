document.addEventListener(
    "DOMContentLoaded",
    function () {

        const subjectContainer =
            document.getElementById(
                "subjectsContainer"
            );

        const addSubjectButton =
            document.getElementById(
                "addSubject"
            );

        const semesterSelect =
            document.getElementById(
                "semester"
            );

        const customSemesterBox =
            document.getElementById(
                "customSemesterBox"
            );

        const customSemester =
            document.getElementById(
                "customSemester"
            );


        // =================================================
        // CUSTOM SEMESTER
        // =================================================

        function updateCustomSemester() {

            if (!semesterSelect) {
                return;
            }

            if (
                semesterSelect.value ===
                "Custom"
            ) {

                customSemesterBox.style.display =
                    "block";

                if (customSemester) {
                    customSemester.required = true;
                }

            } else {

                customSemesterBox.style.display =
                    "none";

                if (customSemester) {
                    customSemester.required = false;
                }
            }
        }


        if (semesterSelect) {

            semesterSelect.addEventListener(
                "change",
                updateCustomSemester
            );

            updateCustomSemester();
        }


        // =================================================
        // CALCULATE LIVE PREVIEW
        // =================================================

        function updatePreview() {

            if (!subjectContainer) {
                return;
            }

            const rows =
                subjectContainer.querySelectorAll(
                    ".subject-row"
                );

            let total = 0;

            let maximum = 0;


            rows.forEach(
                function (row) {

                    const marks =
                        parseFloat(
                            row.querySelector(
                                '[name="marks[]"]'
                            ).value
                        );

                    const maxMarks =
                        parseFloat(
                            row.querySelector(
                                '[name="max_marks[]"]'
                            ).value
                        );


                    if (
                        !isNaN(marks) &&
                        !isNaN(maxMarks) &&
                        maxMarks > 0
                    ) {

                        total += marks;

                        maximum += maxMarks;
                    }

                }
            );


            let percentage = 0;


            if (maximum > 0) {

                percentage =
                    (
                        total /
                        maximum
                    ) * 100;

            }


            let grade = "F";


            if (percentage >= 90) {

                grade = "A+";

            } else if (percentage >= 80) {

                grade = "A";

            } else if (percentage >= 70) {

                grade = "B+";

            } else if (percentage >= 60) {

                grade = "B";

            } else if (percentage >= 50) {

                grade = "C";

            } else if (percentage >= 40) {

                grade = "D";

            }


            const percentageElement =
                document.getElementById(
                    "previewPercentage"
                );

            const gradeElement =
                document.getElementById(
                    "previewGrade"
                );

            const subjectsElement =
                document.getElementById(
                    "previewSubjects"
                );


            if (percentageElement) {

                percentageElement.textContent =
                    percentage.toFixed(2) +
                    "%";

            }


            if (gradeElement) {

                gradeElement.textContent =
                    grade;

            }


            if (subjectsElement) {

                subjectsElement.textContent =
                    rows.length;

            }

        }


        // =================================================
        // SUBJECT ROW
        // =================================================

        function attachSubjectEvents(row) {

            const inputs =
                row.querySelectorAll(
                    "input"
                );


            inputs.forEach(
                function (input) {

                    input.addEventListener(
                        "input",
                        updatePreview
                    );

                }
            );


            const removeButton =
                row.querySelector(
                    ".remove-subject"
                );


            if (removeButton) {

                removeButton.addEventListener(
                    "click",
                    function () {

                        const rows =
                            subjectContainer
                                .querySelectorAll(
                                    ".subject-row"
                                );


                        if (rows.length <= 1) {

                            alert(
                                "At least one subject is required."
                            );

                            return;
                        }


                        row.remove();

                        updatePreview();

                    }
                );

            }

        }


        // =================================================
        // EXISTING SUBJECTS
        // =================================================

        if (subjectContainer) {

            subjectContainer
                .querySelectorAll(
                    ".subject-row"
                )
                .forEach(
                    attachSubjectEvents
                );

        }


        // =================================================
        // ADD NEW SUBJECT
        // =================================================

        if (addSubjectButton) {

            addSubjectButton.addEventListener(
                "click",
                function () {

                    const row =
                        document.createElement(
                            "div"
                        );


                    row.className =
                        "subject-row";


                    row.innerHTML = `

                        <div class="field">

                            <label>
                                Subject Name
                            </label>

                            <input
                                type="text"
                                name="subject_name[]"
                                required
                                placeholder="e.g. Artificial Intelligence"
                            >

                        </div>


                        <div class="field">

                            <label>
                                Obtained Marks
                            </label>

                            <input
                                type="number"
                                name="marks[]"
                                min="0"
                                step="0.01"
                                required
                            >

                        </div>


                        <div class="field">

                            <label>
                                Maximum Marks
                            </label>

                            <input
                                type="number"
                                name="max_marks[]"
                                min="1"
                                step="0.01"
                                value="100"
                                required
                            >

                        </div>


                        <button
                            type="button"
                            class="remove-subject"
                        >
                            ×
                        </button>

                    `;


                    subjectContainer.appendChild(
                        row
                    );


                    attachSubjectEvents(
                        row
                    );


                    updatePreview();

                }
            );

        }


        updatePreview();

    }
);