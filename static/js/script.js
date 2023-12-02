var problem_idx = 2;
var hints_buffer = null;
var hint_types = [];
var input_links= ['','','https://drive.google.com/file/d/1PwdGBOo6yAGjdtH8l0l8ouqv2QZktb34/view?usp=sharing', 'https://drive.google.com/file/d/1SaSHFmafOA7iH4alC06eiOGXnU-j_pew/view?usp=sharing', 'https://drive.google.com/file/d/1g7qyswgmiSing-nyr3WVZpyf5CfVbbyn/view?usp=sharing']
var display_hint_types = ["What to do next", "How to do next", "Example demonstration", "Solution for the next step", "Summary"];
var hint_index = 4;
var problem_info = null;
var editor = ace.edit("editor");
editor.setTheme("ace/theme/textmate");
editor.session.setMode("ace/mode/python");
getProblem(problem_idx);


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
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function stripHTML(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    return doc.body.textContent || "";
}

function getProblem() {
    fetch('/get_problem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idx: problem_idx }),
    })
    .then(response => response.json())
    .then(data => {
        problem_info = JSON.parse(data)
        document.getElementById('problemdescription').textContent = problem_info['problem_desc'];
        ace.edit('editor').setValue(problem_info['code']);
        document.getElementById('problem-title').textContent = problem_info['problem_title'];
        document.getElementById('example-input').innerHTML = '<a href="' + input_links[problem_idx] + '">A csv file</a>';
        document.getElementById('example-output').textContent = problem_info['output'];
        document.getElementById('correct-output').textContent = problem_info['output'];

        if (problem_idx >= 4) {
            document.getElementById("submit").disabled = false;
        } else {
            document.getElementById("submit").disabled = false;
            problem_idx = problem_idx + 1;
        }
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
        document.getElementById('hintType').textContent = display_hint_types[hint_index];
        hint_type = data['hint_type']
        if (hint_type == "summative") {
            hint_types = ["summative"];
            wrap_worked_example(hints_buffer['summative'], "summative");
        } else if (hint_type="multilevel") {
            hint_types = ["orientation", "instrumental", "worked_example", "bottom_out", "summative"];
            wrap_worked_example(hints_buffer[hint_types[hint_index]], "multilevel");
        }

        document.getElementById("ask-hint").disabled = false;
        hideSpinner();
        document.getElementById("next-hint").disabled = false;
        document.getElementById("survey").disabled = false;

        var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
        send_log('ask-hint', hints_buffer, code);
        send_log(hint_types[hint_index], hints_buffer[hint_types[hint_index]], code);

    })
    .catch(error => {
        console.error('Error fetching hint:', error);
        document.getElementById("ask-hint").disabled = false;
    });
}

function getPrevHint() {
    hint_index = (hint_index + hint_types.length-1) % hint_types.length;
    enablePrevNext(hint_index);
    document.getElementById('hintType').textContent = display_hint_types[hint_index];
    wrap_worked_example(hints_buffer[hint_types[hint_index]], "multilevel");
    console.log(hints_buffer[hint_types[hint_index]]);

    // send log
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
    send_log(hint_types[hint_index], hints_buffer[hint_types[hint_index]], code);
}

function getNextHint() {
    hint_index = (hint_index + hint_types.length+1) % hint_types.length;
    enablePrevNext(hint_index);
    document.getElementById('hintType').textContent = display_hint_types[hint_index];
    console.log(hints_buffer[hint_types[hint_index]]);
    wrap_worked_example(hints_buffer[hint_types[hint_index]], "multilevel");
      
    // send log
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
    send_log(hint_types[hint_index], hints_buffer[hint_types[hint_index]], code);
}

function wrap_worked_example(worked_example_str, hint_type) {
    var editor = ace.edit("worked_example_editor");
    editor.setTheme("ace/theme/textmate");
    if (hint_index >= 2 || hint_type == "summative") {
        editor.session.setMode("ace/mode/python");
    } else {
        editor.session.setMode("ace/mode/text");
        worked_example_str = plaintext_formatter(worked_example_str);
    }
    editor.setValue(worked_example_str, -1); // -1 is for moving the cursor to the start
}

function plaintext_formatter(worked_example_str) {
    let CHARACTER_LIMIT = 85;
    var words = worked_example_str.split(' ');

    var formatted_str = '';
    var current_line = '';

    words.forEach(function(word) {
        if ((current_line + word).length > CHARACTER_LIMIT) {
            formatted_str += current_line + '\n';
            current_line = word + ' ';
        } else {
            current_line += word + ' ';
        }
    });

    formatted_str += current_line;
    return formatted_str;
    return worked_example_str;
}


function showSpinner() {
    document.getElementById("loadingSpinner").style.display = "block";
}

function hideSpinner() {
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

// copy
document.addEventListener('copy', function(e) {
    e.preventDefault();
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "")
    var copiedText = e.clipboardData.getData('text/plain');
    console.log('Copied content:', copiedText);
    send_log('copy', copiedText, code);
});

// paste
document.addEventListener('paste', function(e) {
    e.preventDefault();
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "")
    var pastedText = e.clipboardData.getData('text/plain');
    console.log('Copied content:', copiedText);
    send_log('paste', pastedText, code);
});

// run 
document.getElementById("run").addEventListener('click', function(e) {
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
    var output = document.getElementById('student-output').textContent;
    send_log('run', output, code);
});

// generate hint
document.getElementById("ask-hint").addEventListener('click', function(e) {
    document.getElementById("survey").disabled = false;

    const radioButtons = document.querySelectorAll('input[type="radio"]');
    // Iterate through each radio button and set checked to false
    radioButtons.forEach(radio => {
        radio.checked = false;
    });
});

// next question
document.getElementById("submit").addEventListener('click', function(e) {
    var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
    send_log('submit', "correct", code);
    document.getElementById("survey").disabled = true;
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    // Iterate through each radio button and set checked to false
    radioButtons.forEach(radio => {
        radio.checked = false;
    });
});

document.getElementById("next-hint").addEventListener('click', function(e){
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    // Iterate through each radio button and set checked to false
    radioButtons.forEach(radio => {
        radio.checked = false;
    });
});

document.getElementById("prev-hint").addEventListener('click', function(e){
    const radioButtons = document.querySelectorAll('input[type="radio"]');

    // Iterate through each radio button and set checked to false
    radioButtons.forEach(radio => {
        radio.checked = false;
    });
});

// next question
document.addEventListener('DOMContentLoaded', () => {
    // Select all radio buttons with the name 'satisfaction'
    const radios = document.querySelectorAll('input');

    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            var code = document.getElementsByClassName('ace_text-layer')[0].textContent.replace("ה", "");
            
            // Get all input elements of type checkbox
            var checkboxes = document.querySelectorAll('input[type="radio"]');
            // Loop through all checkboxes to see which is checked
            checkboxes.forEach(function(checkbox) {
                if(checkbox.checked) {
                    send_log(checkbox.id, hints_buffer, code);
                }
            });
        });
    });
});


function send_log(event_type, event_log, code) {
    fetch('/log_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ event_type: event_type, pid: problem_idx, sid: 1, code:code, event_log:event_log, timestamp: Date.now() })
    });
}