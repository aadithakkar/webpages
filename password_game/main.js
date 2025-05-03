var rigged = 0;

var playing = true;

var tens = Math.floor(Math.random() * 5) + 5;
var totalSum = tens * 10 + Math.floor(tens + Math.random() * (10 - tens));
var numbers = Array(0);
numbers.push(Math.floor(Math.random() * totalSum / 2))
numbers.push(Math.floor(Math.random() * (totalSum - numbers[0])))
numbers.push(totalSum - numbers[0] - numbers[1])

// var numbers = Array(0);
// var totalSum = 0;
// for (var i = 0; i < 3; i++) {
//     var num = Math.floor(Math.random() * 500);
//     numbers.push(num);
//     totalSum += num;
// }

if (rigged) {
    totalSum = 1;
}

const countries = [
    "afghanistan", "albania", "america", "algeria", "andorra", "angola", "antigua and barbuda", "argentina",
    "armenia", "australia", "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados",
    "belarus", "belgium", "belize", "benin", "bhutan", "bolivia", "bosnia and herzegovina",
    "botswana", "brazil", "brunei", "bulgaria", "burkina faso", "burundi", "cabo verde", "cambodia",
    "cameroon", "canada", "central african republic", "chad", "chile", "china", "colombia", "comoros",
    "congo", "costa rica", "croatia", "cuba", "cyprus",
    "czech republic", "denmark", "djibouti", "dominica", "dominican republic", "ecuador", "egypt",
    "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji",
    "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana", "greece", "grenada",
    "guatemala", "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland",
    "india", "indonesia", "iran", "iraq", "ireland", "israel", "italy", "ivory coast", "jamaica",
    "japan", "jordan", "kazakhstan", "kenya", "kiribati", "korea, north", "korea, south", "kosovo",
    "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein",
    "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", "malta",
    "marshall islands", "mauritania", "mauritius", "mexico", "micronesia", "moldova", "monaco",
    "mongolia", "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nauru", "nepal",
    "netherlands", "new zealand", "nicaragua", "niger", "nigeria", "north macedonia", "norway",
    "oman", "pakistan", "palau", "palestine", "panama", "papua new guinea", "paraguay", "peru",
    "philippines", "poland", "portugal", "qatar", "romania", "russia", "rwanda", "saint kitts and nevis",
    "saint lucia", "saint vincent and the grenadines", "samoa", "san marino", "sao tome and principe",
    "saudi arabia", "senegal", "serbia", "seychelles", "sierra leone", "singapore", "slovakia",
    "slovenia", "solomon islands", "somalia", "south africa", "south sudan", "spain", "sri lanka",
    "sudan", "suriname", "sweden", "switzerland", "syria", "taiwan", "tajikistan", "tanzania",
    "thailand", "timor-leste", "togo", "tonga", "trinidad and tobago", "tunisia", "turkey",
    "turkmenistan", "tuvalu", "uganda", "ukraine", "united arab emirates", "united kingdom",
    "united states", "uruguay", "uzbekistan", "vanuatu", "vatican city", "venezuela", "vietnam", "wales",
    "yemen", "zambia", "zimbabwe"
  ];

  const elements = [
    "actinium", "aluminum", "americium", "antimony", "argon", "arsenic", "astatine", "barium",
    "berkelium", "beryllium", "bismuth", "bohrium", "boron", "bromine", "cadmium", "calcium",
    "californium", "carbon", "cerium", "cesium", "chlorine", "chromium", "cobalt", "copernicium",
    "copper", "curium", "darmstadtium", "dubnium", "dysprosium", "einsteinium", "erbium",
    "europium", "fermium", "flerovium", "fluorine", "francium", "gadolinium", "gallium",
    "germanium", "gold", "hafnium", "hassium", "helium", "holmium", "hydrogen", "indium", "iodine",
    "iridium", "iron", "krypton", "lanthanum", "lawrencium", "lead", "lithium", "livermorium",
    "lutetium", "magnesium", "manganese", "meitnerium", "mendelevium", "mercury", "molybdenum",
    "moscovium", "neodymium", "neon", "neptunium", "nickel", "nihonium", "niobium", "nitrogen",
    "nobelium", "oganesson", "osmium", "oxygen", "palladium", "phosphorus", "platinum", "plutonium",
    "polonium", "potassium", "praseodymium", "promethium", "protactinium", "radium", "radon",
    "rhenium", "rhodium", "roentgenium", "rubidium", "ruthenium", "rutherfordium", "samarium",
    "scandium", "seaborgium", "selenium", "silicon", "silver", "sodium", "strontium", "sulfur",
    "tantalum", "technetium", "tellurium", "tennessine", "terbium", "thallium", "thorium",
    "thulium", "tin", "titanium", "tungsten", "uranium", "vanadium", "xenon", "ytterbium",
    "yttrium", "zinc", "zirconium"
  ];

  const flags = [
    "🇦🇫", "🇦🇱", "🇺🇸", "🇩🇿", "🇦🇩", "🇦🇴", "🇦🇬", "🇦🇷", "🇦🇲", "🇦🇺",
    "🇦🇹", "🇦🇿", "🇧🇸", "🇧🇭", "🇧🇩", "🇧🇧", "🇧🇾", "🇧🇪", "🇧🇿", "🇧🇯",
    "🇧🇹", "🇧🇴", "🇧🇦", "🇧🇼", "🇧🇷", "🇧🇳", "🇧🇬", "🇧🇫", "🇧🇮", "🇨🇻",
    "🇰🇭", "🇨🇲", "🇨🇦", "🇨🇫", "🇹🇩", "🇨🇱", "🇨🇳", "🇨🇴", "🇰🇲", "🇨🇬",
    "🇨🇷", "🇭🇷", "🇨🇺", "🇨🇾", "🇨🇿", "🇩🇰", "🇩🇯", "🇩🇲", "🇩🇴", "🇪🇨",
    "🇪🇬", "🇸🇻", "🇬🇶", "🇪🇷", "🇪🇪", "🇸🇿", "🇪🇹", "🇫🇯", "🇫🇮", "🇫🇷",
    "🇬🇦", "🇬🇲", "🇬🇪", "🇩🇪", "🇬🇭", "🇬🇷", "🇬🇩", "🇬🇹", "🇬🇳", "🇬🇼",
    "🇬🇾", "🇭🇹", "🇭🇳", "🇭🇺", "🇮🇸", "🇮🇳", "🇮🇩", "🇮🇷", "🇮🇶", "🇮🇪",
    "🇮🇱", "🇮🇹", "🇨🇮", "🇯🇲", "🇯🇵", "🇯🇴", "🇰🇿", "🇰🇪", "🇰🇮", "🇰🇵",
    "🇰🇷", "🇽🇰", "🇰🇼", "🇰🇬", "🇱🇦", "🇱🇻", "🇱🇧", "🇱🇸", "🇱🇷", "🇱🇾",
    "🇱🇮", "🇱🇹", "🇱🇺", "🇲🇬", "🇲🇼", "🇲🇾", "🇲🇻", "🇲🇱", "🇲🇹", "🇲🇭",
    "🇲🇷", "🇲🇺", "🇲🇽", "🇫🇲", "🇲🇩", "🇲🇨", "🇲🇳", "🇲🇪", "🇲🇦", "🇲🇿",
    "🇲🇲", "🇳🇦", "🇳🇷", "🇳🇵", "🇳🇱", "🇳🇿", "🇳🇮", "🇳🇪", "🇳🇬", "🇲🇰",
    "🇳🇴", "🇴🇲", "🇵🇰", "🇵🇼", "🇵🇸", "🇵🇦", "🇵🇬", "🇵🇾", "🇵🇪", "🇵🇭",
    "🇵🇱", "🇵🇹", "🇶🇦", "🇷🇴", "🇷🇺", "🇷🇼", "🇰🇳", "🇱🇨", "🇻🇨", "🇼🇸",
    "🇸🇲", "🇸🇹", "🇸🇦", "🇸🇳", "🇷🇸", "🇸🇨", "🇸🇱", "🇸🇬", "🇸🇰", "🇸🇮",
    "🇸🇧", "🇸🇴", "🇿🇦", "🇸🇸", "🇪🇸", "🇱🇰", "🇸🇩", "🇸🇷", "🇸🇪", "🇨🇭",
    "🇸🇾", "🇹🇼", "🇹🇯", "🇹🇿", "🇹🇭", "🇹🇱", "🇹🇬", "🇹🇴", "🇹🇹", "🇹🇳",
    "🇹🇷", "🇹🇲", "🇹🇻", "🇺🇬", "🇺🇦", "🇦🇪", "🇬🇧", "🇺🇸", "🇺🇾", "🇺🇿",
    "🇻🇺", "🇻🇦", "🇻🇪", "🇻🇳", "🏴", "🇾🇪", "🇿🇲", "🇿🇼"
  ];
  

const chemNames = [["propane", "C3H8"], ["propene", "C3H6"], ["propyne", "C3H4"], ["butane", "C4H10"], ["butene", "C4H8"]]
var chemName = chemNames[Math.floor(Math.random() * chemNames.length)]

if (rigged) {
    chemName = ["butane", "C4H10"]
}

const songs = [["ode to joy", "E-E-F-G-G-F-E-D-C-C-D-E-E-D-D"], ["twinkle twinkle little star", "C-C-G-G-A-A-G-F-F-E-E-D-D-C"], ["mary had a little lamb", "E-D-C-D-E-E-E-D-D-D-E-G-G"], ["happy birthday", "C-C-D-C-F-E-C-C-D-C-G-F"]]
var song = songs[Math.floor(Math.random() * songs.length)]

const parallels = hints = [
    "",
    "The First Level",
    "Gravity Falls",
    "Flappy Bird?",
    "Before You Leap",
    "The Grand Illusion",
    "Danger Zone",
    "Through the Portal",
    "Timeless",
    "Curse of Vanishing",
    "Curse of Everything Vanishing",
    "Back and There Again",
    "Recharged",
    "A Vulnerable World",
    "Disguised",
    "A New World",
    "Creative Mode",
    "Think Fast",
    "All Under Control",
    "kcabyalP",
    "Leader and Follower",
    "The End"
]
var parallel = Math.floor(Math.random() * 20) + 1

var startTime;

if (rigged) {
    parallel = 8;
}

var level = 0;

var countryTime;

// var countrySat = 0;

var elementTime;

// var elementSat = 0;

var freqPrefix = "";

var satisfiedRules = [];

const alpha = "abcdefghijklmnopqrstuvwyz";

const chemAlpha = "abcdefghiklmnoprstuvxyz";

var letters = []
for (var i = 0; i < 10; i++) {
    letters.push(alpha[Math.floor(Math.random() * alpha.length)])
}

letters[3] = chemAlpha[Math.floor(Math.random() * chemAlpha.length)]

if (rigged) {
    letters = ["a", "a", "a", "a", "a"]
}

const requirements = ["Your password must contain at least 6 characters", "Your password must contain a number", "Your password must contain Aadi's name", `Your password must contain the sum: ${numbers[0]} + ${numbers[1]} + ${numbers[2]}`, "Your password must contain the name of the compound " + chemName[1], "Your password must contain the name of level " + parallel + " of Parallel", `Your password must contain a 7 letter word starting with '${letters[0].toUpperCase()}' and containing '${letters[1].toUpperCase()}'`, "Your password must contain the phrase 'Pura Vida.'", "Your password must contain the best move for white in this complex position", `Your password must contain a country starting with the letter ${letters[2].toUpperCase()}`, "Your password must be exactly 20% vowels", "This is Dia: 🦥 Please put Dia in your password", `Your password must contain the song that goes: ${song[1]}`, `Your password must contain a chemical element starting with the letter ${letters[3].toUpperCase()}`, "Dia is very hungry. Feed her 3 🌴 every minute.", "Your password must contian the flags of each of the following scrambled countries: ", "All of the monkeys in your password must be red.", "Your password must contain the sum of its digits.", "Please give Dia a more filling meal - she happens to love Costa Rican cuisine", "Digits in your password must be in increasing order.", "The frequency of each non-emoji character in your password must be a power of 2", "Your password must contain the product of its digits", "Your password must contain the seconds passed since you started playing", "Your password must contain the square root of its length", "You win!"];

function countrySubset(letter, arr) {
    var start = -1
    for (var i = 0; i < arr.length; i++) {
        if (start == -1 && arr[i][0] == letter) {
            start = i
        } else if (start != -1 && arr [i][0] != letter) {
            return arr.slice(start, i)
        }
    }
    return countries.slice(start, countries.length)
}

var countrySubarr = countrySubset(letters[2], countries);

var elementSubarr = countrySubset(letters[3], elements);

function scramble(words) {
    words = words.split(" ");
    var newString = ""
    for (var i = 0; i < words.length; i++) {
        var word = words[i].split("");
        length = word.length
        for (var j = 0; j < length; j++) {
            var char = word[Math.floor(Math.random() * word.length)]
            newString += char
            word.splice(word.indexOf(char), 1)
        }
        newString += " ".slice(0, -1)
    }
    return newString
}

function scrambled(length) {
    var indices = [];
    var scram = [];
    var num;
    for (var i = 0; i < length; i++) {
        do {
            num = Math.floor(Math.random() * countries.length);
        } while (indices.includes(num))
        indices.push(num);
        var country = countries[num];
        scram.push(scramble(country))
    }
    return [indices, scram]
}

scrambledCountries = scrambled(3);

function end_game(message) {
    if (playing) {
        playing = false
        var screen = document.createElement('div')
        screen.classList.add("deathscreen")
        screen.innerHTML = `
        <div class="deathbanner">${message}</div>
        `
        document.body.appendChild(screen)
    }
}

async function isWord(word) {
    const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${word}`;
    const response = await fetch(url);
    return (response["status"] == 200)
}

async function satisfied(rule, password) {
    var passwordLow = password.toLowerCase()
    if (satisfiedRules.includes(rule)) {
        return true
    }
    // if (rule < 22) {
    //     return true
    // }
    switch (rule) {
        case 1:
            return password.length >= 6;
        case 2:
            return containsAny(password, "1234567890");
        case 3:
            return passwordLow.includes("aadi");
        case 4:
            return password.includes(totalSum);
        case 5:
            return password.includes(chemName[0])
        case 6:
            var list = parallels[parallel].toLowerCase().split(" ")
            for (var i = 0; i < list.length; i++) {
                if (!passwordLow.includes(list[i])) {
                    return false
                }
            }
            return true
        case 7:
            var firstLetter = letters[0];
            for (var i = 0; i < password.length - 6; i++) {
                if (firstLetter == passwordLow[i]) {
                    var potentialWord = passwordLow.substring(i, i + 7);
                    if (!potentialWord.includes(' ') && potentialWord.includes(letters[1]) && await isWord(potentialWord)) {
                        if (!satisfiedRules.includes(rule)) {
                            satisfiedRules.push(rule)
                        }
                        return true
                    }
                }
            }
            return false
        case 8:
            return passwordLow.includes("pura") && passwordLow.includes("vida");
        case 9:
            return password.includes("Qh5#")
        case 10:
            for (var i = 0; i < countrySubarr.length; i++) {
                if (passwordLow.includes(countrySubarr[i])) {
                    if (!satisfiedRules.includes(rule)) {
                        satisfiedRules.push(rule)
                    }
                    return true
                }
            }
            return false
        case 11:
            return Math.abs(vowelFreq(passwordLow) / password.length - 0.2) < 0.0001
        case 12:
            return password.includes("🦥")
        case 13:
            var list = song[0].toLowerCase().split(" ")
            for (var i = 0; i < list.length; i++) {
                if (!passwordLow.includes(list[i])) {
                    return false
                }
            }
            return true
        case 14:
            for (var i = 0; i < elementSubarr.length; i++) {
                if (passwordLow.includes(elementSubarr[i])) {
                    if (!satisfiedRules.includes(rule)) {
                        satisfiedRules.push(rule)
                    }
                    return true
                }
            }
            return false
        case 15:
            if (password.includes('🌴')) {
                if (!satisfiedRules.includes(rule)) {
                    satisfiedRules.push(rule)
                }
                return true
            }
            return false
        case 16:
            for (var i = 0; i < 3; i++) {
                if (!password.includes(flags[scrambledCountries[0][i]])) {
                    return false
                }
            }
            return true
        case 17:
            return !password.includes('monkey')
        case 18:
            var sum = 0
            for (var i = 0; i < password.length; i++) {
                if (!isNaN(password[i])) {
                    sum += parseInt(password[i])
                }
            }
            return password.includes(sum)
        case 19:
            return password.includes('🍚') && password.includes('🫘')
        case 20:
            var max = 0;
            for (var i = 0; i < password.length; i++) {
                if (!isNaN(password[i])) {
                    if (parseInt(password[i]) < max) {
                        return false
                    }
                    max = parseInt(password[i])
                }
            }
            return true
        case 21:
            var chars = [];
            var freqs = [];
            var emojiLess = password.replace(/\p{Emoji_Presentation}|\p{Emoji}\uFE0F/gu, '')
            for (var i = 0; i < emojiLess.length; i++) {
                var item = emojiLess[i];
                if (chars.includes(item)) {
                    freqs[chars.indexOf(item)] += 1
                } else if (true) {
                    chars.push(item)
                    freqs.push(1)
                }
            }
            for (var i = 0; i < freqs.length; i++) {
                var freq = freqs[i];
                if (!(Math.floor(Math.log(freq)/Math.log(2)) == Math.ceil(Math.log(freq)/Math.log(2)))) {
                    freqPrefix = ` ('${chars[i].toUpperCase()}' x${freqs[i]})`
                    return false
                }
            }
            freqPrefix = ""
            return true
        case 22:
            return password.includes('0')
        case 23:
            return password.includes(Math.floor((Date.now() - startTime) / 1000))
        case 24:
            var sqrt = Math.sqrt(password.length)
            return Math.floor(sqrt) == Math.ceil(sqrt) && password.includes(parseInt(sqrt))
    }
}

function containsAny(string, options) {
    for (var i = 0; i < options.length; i ++) {
        if (string.includes(options[i])) {
            return true
        }
    }
    return false
}

function vowelFreq(password) {
    freq = 0
    for (var i = 0; i < password.length; i++) {
        if ("aeiou".includes(password[i])) {
            freq += 1
        }
    }
    return freq
}

function updateTimer() {
    if (playing) {
        if (level == 10 && !satisfiedRules.includes(14)) {
            document.getElementById('r10').innerText = rulePrefix(10);
            if ((Date.now() - countryTime) > 9500) {
                end_game("YOU FAILED GEOGRAPHY")
            }
        } else if (level == 14 && !satisfiedRules.includes(14)) {
            document.getElementById('r14').innerText = rulePrefix(14);
            if ((Date.now() - elementTime) > 14500) {
                end_game("YOU FAILED CHEMISTRY")
            }
        }
    }
}

function updateFood() {
    if (playing) {
        var password = document.getElementById('textbox').value;
        if (password.includes('🌴')) {
            if (password.length - password.split('🌴').join('').length > 16) {
                end_game("DIA WAS OVERFED")
            }
            document.getElementById('textbox').value = password.replace('🌴', '')
        } else {
            end_game("DIA HAS STARVED")
        }
    }
}

function rulePrefix(rule, password=null) {
    var prefix = requirements[rule - 1]
    if (!satisfiedRules.includes(10) && rule == 10) {
        prefix += ` (${10 - Math.floor((Date.now() - countryTime) / 1000)}s)`
    } else if (rule == 11) {
        prefix += ` (currently ${vowelFreq(password)})`
    } else if (!satisfiedRules.includes(14) && rule == 14) {
        prefix += ` (${15 - Math.floor((Date.now() - elementTime) / 1000)}s)`
    } else if (rule == 16) {
        prefix += `${scrambledCountries[1][0].toUpperCase()}, ${scrambledCountries[1][1].toUpperCase()}, ${scrambledCountries[1][2].toUpperCase()}`
    } else if (rule == 21) {
        prefix += freqPrefix
    } else if (rule == 23) {
        prefix += ` ${Math.floor((Date.now() - startTime) / 1000)} seconds ago`
    }
    return prefix
}

async function update() {
    if (!playing) {
        return false
    }
    var tbox = document.getElementById('textbox');
    var password = tbox.value;
    var completed = true;
    var maxSat = 1;
    var topMost = 1;
    tbox.style.height = 'auto';
    tbox.style.height = tbox.scrollHeight + "px";
    document.getElementById('header').innerText = `Length: ${password.length}`;
    for (var rule = 1; rule < level + 1; rule ++) {
        ruleElement = document.getElementById(`r${rule}`);
        divElement = document.getElementById(`d${rule}`);
        headerElement = document.getElementById(`h${rule}`);
        if (await satisfied(rule, password)) {
            if (rule != 9) {
                ruleElement.innerText = rulePrefix(rule, password.toLowerCase());
            }
            // if (rule != 1) {
            //     document.body.insertBefore(divElement, document.getElementById(`d${maxSat}`));
            //     if (maxSat == topMost) {
            //         topMost = rule;
            //     }
            //     maxSat = rule;
            // }
            // ruleElement.style.color = "rgb(0, 150, 0)"
            // divElement.style.background = "rgb(0, 150, 0)"
            // divElement.style.borderColor = "rgb(0, 75, 0)"
            divElement.style.borderColor = "rgb(64, 121, 57)"
            headerElement.style.backgroundColor = "rgb(190, 240, 180)"
            ruleElement.style.backgroundColor = "rgb(232, 254, 229)"
        } else {
            completed = false;
            if (rule != 9) {
                ruleElement.innerText = rulePrefix(rule, password.toLowerCase());
            }
            // document.body.insertBefore(divElement, document.getElementById(`d${topMost}`));
            // topMost = rule;
            // ruleElement.style.color = "rgb(150, 0, 0)"
            // divElement.style.background = "rgb(255, 113, 113)";
            // divElement.style.borderColor = "rgb(220, 75, 75)"
            divElement.style.borderColor = "rgb(234, 51, 35)"
            headerElement.style.backgroundColor = "rgb(246, 201, 200)"
            ruleElement.style.backgroundColor = "rgb(252, 236, 236)"
        }
    }
    if (completed) {
        level += 1;
        if (level == 1) {
            startTime = Date.now()
            // setInterval(update, 3000)
        } else if (level == 25) {
            var newDiv = document.createElement("div");
            newDiv.classList.add("winbanner");
            newDiv.innerText = "YOU WIN";
            document.body.appendChild(newDiv)
            playing = false;
            return null;
        }
        var newDiv = document.createElement("div")
        newDiv.id = `d${level}`;
        newDiv.classList.add("rulebox")
        newDiv.innerHTML = `
            <div class="ruleheader" id="h${level}">Rule ${level}</div>
            <div class="rulebody" id="r${level}"></div>
        `
        // var newElement = document.createElement("p");
        // newElement.id = `r${level}`;
        // newDiv.appendChild(newElement)
        // console.log(newElement);
        if (level == 1) {
            document.body.appendChild(newDiv)
        } else {
            document.body.insertBefore(newDiv, document.getElementById(`d${level - 1}`))
        }
        if (level == 9) {
            // newElement = document.createElement("img");
            // newElement.src = "Screenshot 2025-04-24 193224.png"
            // newElement.width = "300"
            // document.getElementById("r9").innerText = rulePrefix(9)
            // document.getElementById("r9").appendChild(newElement)
            newDiv.innerHTML = `
            <div class="ruleheader" id="h${level}">Rule ${level}</div>
            <div class="rulebody" id="r${level}">
            <p>${rulePrefix(9)}</p>
            <img src="Screenshot 2025-04-24 193224.png" width=300></img>
            </div>
            `
        } else if (level == 10) {
            countryTime = Date.now();
            setInterval(updateTimer, 1000)
        } else if (level == 14) {
            elementTime = Date.now();
        } else if (level == 16) {
            setInterval(updateFood, 20000)
        } else if (level == 23) {
            setInterval(update, 1000)
        }
        // if (level == 2) {
        //     newElement = document.createElement("p")
        //     newElement.innerText = "hii"
        //     document.body.insertBefore(newElement, document.getElementById('r1'))
        // }
        update();
    }
    if (level > 12 && !password.includes('🦥')) {
        end_game("DIA HAS BEEN ERADICATED")
    }
    // console.log("checking" + isWord(password))
    // if (isWord(password)) {
    //     console.log("success")
    // }
}

