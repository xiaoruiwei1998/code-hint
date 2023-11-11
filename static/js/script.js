var hints_buffer = null;
var hint_types = ["orientation", "instrumental", "worked_example", "bottom_out"];
var hint_index = 0;
var problem_info = null;
var editor = ace.edit("editor");
editor.setTheme("ace/theme/textmate");
editor.session.setMode("ace/mode/python");
getProblem(0);


function runCode() {
    const code = editor.getValue();
    fetch('/run_code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").textContent = data.output;
        document.getElementById("student-output").textContent = data.output;
        if (document.getElementById("student-output").textContent == document.getElementById("correct-output").textContent) {
            document.getElementById("submit").disabled = false;
        } else {
            document.getElementById("submit").disabled = true;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function stripHTML(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    return doc.body.textContent || "";
}

function getProblem(idx) {
    fetch('/get_problem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idx: idx }),
    })
    .then(response => response.json())
    .then(data => {
        problem_info = JSON.parse(data)
        document.getElementById('problemdescription').textContent = problem_info['problem_desc'];
        ace.edit('editor').setValue(problem_info['code']);
    })
    .catch(error => {
        console.error('Error fetching hint:', error);
    });
}

function generateHint() {
    showSpinner();
    document.getElementById("ask-hint").disabled = true;
    document.getElementById("prev-hint").disabled = true;
    document.getElementById("next-hint").disabled = true;
    hint_index = 0;
    const code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "")
    const problemDesc = document.getElementById('problemdescription').textContent;
    const problemDesc_plain_text = stripHTML(problemDesc).trim();
    fetch('/get_hint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: code, problemDesc: problemDesc_plain_text }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data['hints']);
        hints_buffer = JSON.parse(data['hints']);
        document.getElementById('hintType').textContent = hint_types[hint_index];
        wrap_worked_example(hints_buffer[hint_types[hint_index]]);
        document.getElementById("ask-hint").disabled = false;
        hideSpinner();
        document.getElementById("next-hint").disabled = false;
    })
    .catch(error => {
        console.error('Error fetching hint:', error);
        document.getElementById("ask-hint").disabled = false;
    });
}

function getPrevHint() {
    hint_index = (hint_index + hint_types.length-1) % hint_types.length;
    enablePrevNext(hint_index);
    document.getElementById('hintType').textContent = hint_types[hint_index];
    wrap_worked_example(hints_buffer[hint_types[hint_index]]);
    console.log(hints_buffer[hint_types[hint_index]]);
}

function getNextHint() {
    hint_index = (hint_index + hint_types.length+1) % hint_types.length;
    enablePrevNext(hint_index);
    document.getElementById('hintType').textContent = hint_types[hint_index];
    console.log(hints_buffer[hint_types[hint_index]]);
    wrap_worked_example(hints_buffer[hint_types[hint_index]]);
      
}

function wrap_worked_example(worked_example_str) {
    var editor = ace.edit("worked_example_editor");
    editor.setTheme("ace/theme/textmate");
    editor.session.setMode("ace/mode/python");
    editor.setValue(worked_example_str, -1); // -1 is for moving the cursor to the start
}

function showSpinner() {
    console.log("showSpinner");
    document.getElementById("loadingSpinner").style.display = "block";
}

function hideSpinner() {
    console.log("hideSpinner");
    document.getElementById("loadingSpinner").style.display = "none";
}

function enablePrevNext(hint_index) {
    if (hint_index == 0) {
        document.getElementById("prev-hint").disabled = true;
        document.getElementById("next-hint").disabled = false;
    } else if (hint_index < 3) {
        document.getElementById("prev-hint").disabled = false;
        document.getElementById("next-hint").disabled = false;
    } else {
        document.getElementById("prev-hint").disabled = false;
        document.getElementById("next-hint").disabled = true;
    }
}