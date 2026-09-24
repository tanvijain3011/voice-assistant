// ============================================================
// COFFEE VOICE ASSISTANT - FRONTEND
// app.js
// ============================================================


// ELEMENT HELPERS
const $ = (id) => document.getElementById(id);

const log = $("log");
const state = $("state");
const mic = $("mic");


// WEBSITES
const SITES = {
    google: "https://www.google.com",
    youtube: "https://www.youtube.com",
    facebook: "https://www.facebook.com",
    instagram: "https://www.instagram.com",
    github: "https://github.com"
};


// QUICK COMMAND BUTTONS
const CHIPS = [
    "What's the time",
    "Tell me a joke",
    "Weather",
    "Latest news",
    "Wikipedia Albert Einstein",
    "Set alarm for 6:30 pm",
    "Timer 2 minutes",
    "Open Safari",
    "Volume up",
    "Take a screenshot",
    "Where am I",
    "Help"
];


let backendUp = false;


// UI FUNCTIONS
function add(text, cls) {

    const d = document.createElement("div");

    d.className = "m " + cls;

    d.textContent = text;

    log.appendChild(d);

    log.scrollTop = log.scrollHeight;

    return d;
}


// SPEAK ASSISTANT RESPONSE
function speak(text) {

    // Display response
    add(text, "bot");

    // If voice output is disabled, stop here
    if (
        !$("vox").checked ||
        !window.speechSynthesis
    ) {
        return;
    }

    // Stop previous speech
    speechSynthesis.cancel();

    const utterance =
        new SpeechSynthesisUtterance(text);

    utterance.lang = "en-IN";

    utterance.rate = 1;

    utterance.pitch = 1;

    utterance.volume = 1;

    speechSynthesis.speak(utterance);
}


// ALARM / TIMER BEEP
function beep() {

    try {

        const AudioCtx =
            window.AudioContext ||
            window.webkitAudioContext;

        const ctx = new AudioCtx();

        let count = 0;

        const interval = setInterval(() => {

            const oscillator =
                ctx.createOscillator();

            const gain =
                ctx.createGain();

            oscillator.connect(gain);

            gain.connect(ctx.destination);

            oscillator.frequency.value = 880;

            oscillator.start();

            oscillator.stop(
                ctx.currentTime + 0.25
            );

            count++;

            if (count > 8) {

                clearInterval(interval);

                setTimeout(() => {
                    ctx.close();
                }, 500);
            }

        }, 450);

    } catch (error) {

        console.error(
            "Beep error:",
            error
        );
    }
}


// OPEN WEBSITE
function openUrl(url) {

    const opened = window.open(
        url,
        "_blank",
        "noopener"
    );

    if (!opened) {

        add(
            "Popup blocked – allow popups for this page.",
            "sys"
        );
    }
}


// BACKEND CONNECTION
function setConn(ok) {

    backendUp = ok;

    $("dot").className =
        "dot " + (ok ? "ok" : "bad");

    $("conn").textContent =
        ok
            ? "Connected to Coffee server"
            : "Server offline – basic commands only";
}


// CHECK FLASK SERVER
async function checkHealth() {

    try {

        const response =
            await fetch("/api/health");

        setConn(response.ok);

    } catch (error) {

        console.error(
            "Health check failed:",
            error
        );

        setConn(false);
    }
}



// LOCAL BROWSER COMMANDS
function handleLocal(q) {

    let m;
    
    // HELLO

    if (/\b(hello|hi|hey)\b/.test(q)) {

        speak("Oh, hello!");

        return true;
    }

    // THANK YOU

    if (/thank/.test(q)) {

        speak("No problem!");

        return true;
    }

    // HOW ARE YOU
    if (/how are you/.test(q)) {

        speak(
            "I am fine. How are you?"
        );

        return true;
    }
    
    // GOODBYE
    if (/\b(quit|goodbye|bye)\b/.test(q)) {

        speak(
            "Okay, call me when you want."
        );

        return true;
    }

    // HELP
    if (
        /\bhelp\b/.test(q) ||
        /what can you do/.test(q)
    ) {

        speak(
            "Try commands like: " +
            "what's the time, " +
            "tell me a joke, " +
            "weather, " +
            "latest news, " +
            "Wikipedia Albert Einstein, " +
            "set alarm for 6:30 PM, " +
            "timer 5 minutes, " +
            "open YouTube, " +
            "search Google for cats, " +
            "or calculate 12 times 7."
        );

        return true;
    }


    
    // ALARM
    // Examples:
    // set alarm for 6:30 pm
    // alarm 7 am
    m = q.match(
        /alarm.*?(\d{1,2})(?::|\.)?(\d{2})?\s*([ap])\.?\s?m/
    );

    if (m) {

        let hour = Number(m[1]);

        const minute =
            Number(m[2] || 0);

        const ampm = m[3];


        if (ampm === "p" && hour !== 12) {

            hour += 12;
        }


        if (ampm === "a" && hour === 12) {

            hour = 0;
        }


        const alarmTime =
            new Date();


        alarmTime.setHours(
            hour,
            minute,
            0,
            0
        );


        // If time already passed today, schedule for tomorrow

        if (
            alarmTime <= new Date()
        ) {

            alarmTime.setDate(
                alarmTime.getDate() + 1
            );
        }


        const delay =
            alarmTime.getTime() -
            Date.now();


        setTimeout(() => {

            speak(
                "Alarm! Time to go."
            );

            beep();

        }, delay);


        speak(
            `Done, alarm is set for ${
                alarmTime.toLocaleTimeString(
                    [],
                    {
                        hour: "numeric",
                        minute: "2-digit"
                    }
                )
            }. Keep this tab open.`
        );


        return true;
    }


    // TIMER
    // Examples:
    // timer 30 seconds
    // timer 2 minutes
    // timer 1 hour

    m = q.match(
        /timer.*?(\d+)\s*(second|seconds|sec|minute|minutes|min|hour|hours)/
    );


    if (m) {

        const number =
            Number(m[1]);

        const unit =
            m[2];


        let milliseconds;


        if (
            unit.startsWith("s")
        ) {

            milliseconds =
                number * 1000;

        } else if (
            unit.startsWith("m")
        ) {

            milliseconds =
                number * 60000;

        } else {

            milliseconds =
                number * 3600000;
        }


        setTimeout(() => {

            speak(
                "Your timer is done!"
            );

            beep();

        }, milliseconds);


        speak(
            `Timer set for ${number} ${unit}.`
        );


        return true;
    }

    
    // GOOGLE SEARCH
    // Examples:
    // search cats
    // search google for Python
    // search for Jaipur
   
    m = q.match(
        /search\s+(?:on\s+)?(?:google\s+)?(?:for\s+)?(.+)$/
    );


    if (
        m &&
        !/wikipedia/.test(q)
    ) {

        const query =
            m[1].trim();


        speak(
            `Searching Google for ${query}.`
        );


        openUrl(
            "https://www.google.com/search?q=" +
            encodeURIComponent(query)
        );


        return true;
    }


    // OPEN WEBSITE
    // Examples:
    // open youtube
    // open google
    // open github

    m = q.match(
        /\bopen\s+([a-z]+)\b/
    );


    if (
        m &&
        SITES[m[1]]
    ) {

        const site =
            m[1];


        speak(
            `Opening ${site}.`
        );


        openUrl(
            SITES[site]
        );


        return true;
    }

    
    // CALCULATOR
    // Examples:
    // 12 plus 5
    // 10 minus 2
    // 4 times 7
    // 20 divided by 5

    m = q.match(
        /(-?\d+(?:\.\d+)?)\s*(plus|minus|times|multiplied by|divided by|x|\+|-|\*|\/)\s*(-?\d+(?:\.\d+)?)/
    );


    if (m) {

        const a =
            Number(m[1]);

        const operator =
            m[2];

        const b =
            Number(m[3]);


        let result;


        if (
            operator === "plus" ||
            operator === "+"
        ) {

            result = a + b;

        } else if (
            operator === "minus" ||
            operator === "-"
        ) {

            result = a - b;

        } else if (
            operator === "times" ||
            operator === "multiplied by" ||
            operator === "x" ||
            operator === "*"
        ) {

            result = a * b;

        } else {

            if (b === 0) {

                speak(
                    "I cannot divide by zero."
                );

                return true;
            }

            result = a / b;
        }


        speak(
            `That's ${
                Number(result.toFixed(4))
            }.`
        );


        return true;
    }


    return false;
}


// SEND COMMAND TO PYTHON / FLASK SERVER

async function askServer(text) {

    // Check server if currently offline
    if (!backendUp) {

        await checkHealth();
    }


    if (!backendUp) {

        speak(
            "I can't reach the Coffee server. " +
            "Make sure python server.py is running."
        );

        return;
    }


    const wait =
        add(
            "Thinking…",
            "bot pending"
        );


    try {

        const response =
            await fetch(
                "/api/command",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            text: text
                        })
                }
            );


        let data;


        try {

            data =
                await response.json();

        } catch {

            data = {};
        }


        wait.remove();


        if (!response.ok) {

            speak(
                data.error ||
                "The server returned an error."
            );

            return;
        }


        speak(
            data.reply ||
            data.error ||
            "Hmm, I got an empty answer."
        );


    } catch (error) {

        console.error(
            "Server error:",
            error
        );


        wait.remove();


        setConn(false);


        speak(
            "I lost the connection to the Coffee server."
        );
    }
}


// HANDLE COMMAND

async function handle(raw) {

    const text =
        raw.trim();


    if (!text) {

        return;
    }


    // Display user's command

    add(
        text,
        "me"
    );


    // First check local commands

    const handledLocally =
        handleLocal(
            text.toLowerCase()
        );


    if (handledLocally) {

        return;
    }


    // Otherwise send to Python server

    await askServer(text);
}


// SPEECH RECOGNITION

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;


let recognition = null;

let listening = false;

let finalTranscript = "";

let commandSubmitted = false;


// UPDATE MICROPHONE UI

function setListening(
    isListening,
    message
) {

    listening =
        isListening;


    mic.classList.toggle(
        "on",
        isListening
    );


    state.textContent =
        message;
}


// SET UP SPEECH RECOGNITION

if (SpeechRecognition) {

    recognition =
        new SpeechRecognition();


    recognition.lang =
        "en-IN";


    /*
       Keep recognition active while the user is speaking.
    */

    recognition.continuous =
        true;


    /*
       Show partial text while the user speaks.
    */

    recognition.interimResults =
        true;


    recognition.maxAlternatives =
        1;

    
    // START
    recognition.onstart = () => {

        finalTranscript = "";

        commandSubmitted = false;


        setListening(
            true,
            "Listening… Speak now"
        );


        console.log(
            "Speech recognition started"
        );
    };


    // AUDIO START
    recognition.onaudiostart = () => {

        console.log(
            "Microphone audio started"
        );
    };
    

    // SOUND DETECTED
    recognition.onsoundstart = () => {

        console.log(
            "Sound detected"
        );
    };


    // SPEECH DETECTED
    recognition.onspeechstart = () => {

        state.textContent =
            "I can hear you…";


        console.log(
            "Speech detected"
        );
    };


    // SPEECH RESULT
    recognition.onresult =
        (event) => {


            let interimTranscript =
                "";


            for (
                let i =
                    event.resultIndex;

                i <
                event.results.length;

                i++
            ) {

                const result =
                    event.results[i];


                const transcript =
                    result[0].transcript;


                if (
                    result.isFinal
                ) {

                    finalTranscript +=
                        transcript + " ";

                } else {

                    interimTranscript +=
                        transcript;
                }
            }


            // Show live words

            if (
                interimTranscript
            ) {

                state.textContent =
                    interimTranscript;
            }


            // Final command received

            if (
                finalTranscript.trim() &&
                !commandSubmitted
            ) {

                commandSubmitted =
                    true;


                const command =
                    finalTranscript.trim();


                state.textContent =
                    command;


                console.log(
                    "Recognized command:",
                    command
                );


                /*
                  Stop recognition. Command will be handled in onend.
                */

                try {

                    recognition.stop();

                } catch (error) {

                    console.error(
                        error
                    );
                }
            }
        };


    // ERROR
    recognition.onerror =
        (event) => {


            console.error(
                "Speech recognition error:",
                event.error
            );


            if (
                event.error ===
                    "not-allowed" ||
                event.error ===
                    "service-not-allowed"
            ) {

                setListening(
                    false,
                    "Microphone blocked – allow microphone access in Chrome."
                );

                return;
            }


            if (
                event.error ===
                "audio-capture"
            ) {

                setListening(
                    false,
                    "No microphone detected. Check Windows microphone settings."
                );

                return;
            }


            if (
                event.error ===
                "no-speech"
            ) {

                setListening(
                    false,
                    "I couldn't hear anything. Tap the mic and try again."
                );

                return;
            }


            if (
                event.error ===
                "network"
            ) {

                setListening(
                    false,
                    "Speech recognition network error. Check your internet connection."
                );

                return;
            }


            if (
                event.error ===
                "aborted"
            ) {

                setListening(
                    false,
                    "Tap the mic and speak"
                );

                return;
            }


            setListening(
                false,
                "Microphone error: " +
                event.error
            );
        };


    // END
    recognition.onend = () => {


        console.log(
            "Speech recognition ended"
        );


        setListening(
            false,
            "Tap the mic and speak"
        );


        const command =
            finalTranscript.trim();


        finalTranscript = "";


        if (command) {

            handle(command);
        }
    };


} else {

    state.textContent =
        "Voice recognition isn't supported in this browser. Please use Google Chrome.";
}


// MICROPHONE BUTTON
mic.onclick = async () => {


    if (!recognition) {

        state.textContent =
            "Speech recognition isn't available in this browser.";

        return;
    }


    // STOP IF ALREADY LISTENING
    if (listening) {

        try {

            recognition.stop();

        } catch (error) {

            console.error(
                error
            );
        }

        return;
    }


    // STOP COFFEE FROM SPEAKING
    if (
        window.speechSynthesis
    ) {

        speechSynthesis.cancel();
    }


    // REQUEST MICROPHONE ACCESS
    try {


        if (
            !navigator.mediaDevices ||
            !navigator.mediaDevices.getUserMedia
        ) {

            state.textContent =
                "Microphone access isn't available. Open Coffee through http://127.0.0.1:5000 in Chrome.";

            return;
        }


        state.textContent =
            "Checking microphone…";


        const stream =
            await navigator.mediaDevices
                .getUserMedia({
                    audio: true
                });


        /*
          Permission has been confirmed.

          Release getUserMedia's stream.
          SpeechRecognition will access the microphone itself.
        */

        stream
            .getTracks()
            .forEach(
                (track) =>
                    track.stop()
            );


        finalTranscript = "";

        commandSubmitted = false;


        state.textContent =
            "Starting microphone…";


        /*
          Small delay helps Chrome after releasing the getUserMedia stream.
        */

        setTimeout(() => {

            try {

                recognition.start();

            } catch (error) {

                console.error(
                    "Recognition start error:",
                    error
                );


                setListening(
                    false,
                    "Could not start microphone. Please try again."
                );
            }

        }, 250);


    } catch (error) {


        console.error(
            "Microphone permission error:",
            error
        );


        if (
            error.name ===
            "NotAllowedError"
        ) {

            setListening(
                false,
                "Microphone permission is blocked. Allow it in Chrome."
            );

        } else if (
            error.name ===
            "NotFoundError"
        ) {

            setListening(
                false,
                "No microphone was found."
            );

        } else {

            setListening(
                false,
                "Could not access microphone: " +
                error.message
            );
        }
    }
};


// TEXT COMMAND FORM

$("f").onsubmit =
    (event) => {


        event.preventDefault();


        const input =
            $("txt");


        const value =
            input.value;


        input.value =
            "";


        handle(value);
    };


// QUICK COMMAND CHIPS
CHIPS.forEach(
    (command) => {


        const button =
            document.createElement(
                "button"
            );


        button.type =
            "button";


        button.className =
            "chip";


        button.textContent =
            command;


        button.onclick =
            () => handle(command);


        $("chips")
            .appendChild(button);
    }
);


// START COFFEE
async function init() {


    // Check Python backend

    await checkHealth();


    // Check every 15 seconds

    setInterval(
        checkHealth,
        15000
    );


    add(
        "Tap the mic to talk, or use the shortcuts below.",
        "sys"
    );


    // GREETING
    const hour =
        new Date().getHours();


    let greeting;


    if (hour < 12) {

        greeting =
            "morning";

    } else if (
        hour < 18
    ) {

        greeting =
            "afternoon";

    } else {

        greeting =
            "evening";
    }


    speak(
        `Good ${greeting}. I am Coffee. How may I help you?`
    );
}


// Start application

init();