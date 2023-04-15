// let choose_img_Btn = document.querySelector(".choose_img button");
let choose_Input = document.querySelector(".choose_img input");
// let imgSrc = document.querySelector(".view_img img");
let filter_buttons = document.querySelectorAll(".icons_room button");
let slider = document.querySelector(".slider input");
let filter_name = document.querySelector(".filter_info .name");
let slider_value = document.querySelector(".filter_info .value");
let rotate_btns = document.querySelectorAll(".icons_room1 button");
let reset = document.querySelector(".reset");
let save = document.querySelector(".save");
let brightness = 100,
    contrast = 100,
    saturate = 100,
    invert = 0,
    blur = 0,
    rotate = 0,
    flip_x = 1,
    flip_y = 1;

// choose_img_Btn.addEventListener("click", () => choose_Input.click());
// choose_Input.addEventListener("change", () => {
//     let file = choose_Input.files[0];
//     if (!file) return;
//     imgSrc.src = URL.createObjectURL(file);
//     imgSrc.addEventListener("load", () => {
//         document.querySelector(".container").classList.remove("disabled");
//     });
// });

filter_buttons.forEach((element) => {
    element.addEventListener("click", () => {
        document.querySelector(".active").classList.remove("active");
        element.classList.add("active");
        filter_name.innerText = element.id;
        if (element.id === "brightness") {
            slider.max = "200";
            slider.value = brightness;
            slider_value.innerText = `${brightness}`;
        } else if (element.id === "contrast") {
            slider.max = "200";
            slider.value = contrast;
            slider_value.innerText = `${contrast}`;
        } else if (element.id === "contrast") {
            slider.max = "200";
            slider.value = saturate;
            slider_value.innerText = `${saturate}`;
        } else if (element.id === "invert") {
            slider.max = "100";
            slider.value = invert;
            slider_value.innerText = `${invert}`;
        } else if (element.id === "blur") {
            slider.max = "100";
            slider.value = blur;
            slider_value.innerText = `${blur}`;
        }
    });
});

slider.addEventListener("input", () => {
    slider_value.innerText = `${slider.value}%`;
    let sliderState = document.querySelector(".icons_room .active");
    if (sliderState.id === "brightness") {
        brightness = slider.value;
    } else if (sliderState.id === "contrast") {
        contrast = slider.value;
    } else if (sliderState.id === "saturate") {
        saturate = slider.value;
    } else if (sliderState.id === "invert") {
        invert = slider.value;
    } else if (sliderState.id === "blur") {
        blur = slider.value / 20;
    }
    imgSrc.style.filter = ` brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) invert(${invert}%) blur(${blur}px)`;
    mainImg.style.filter = `brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) invert(${invert}%) blur(${blur}px)`;

});

rotate_btns.forEach((element) => {
    element.addEventListener("click", () => {
        if (element.id === "rotate_left") {
            rotate -= 90;
        } else if (element.id === "rotate_right") {
            rotate += 90;
        } else if (element.id === "flip_x") {
            flip_x = flip_x === 1 ? -1 : 1;
        } else if (element.id === "flip_y") {
            flip_y = flip_y === 1 ? -1 : 1;
        }

        imgSrc.style.transform = `rotate(${rotate}deg) scale(${flip_x}, ${flip_y})`;

        mainImg.style.transform = `rotate(${rotate}deg) scale(${flip_x}, ${flip_y})`;
    });
});

reset.addEventListener("click", () => {
    brightness = "100";
    saturate = "100";
    contrast = "100";
    invert = "0";
    blur = "0";
    rotate = 0;
    flip_x = 1;
    flip_y = 1;
    imgSrc.style.transform = `rotate(${rotate}deg) scale(${flip_x}, ${flip_y})`;
    imgSrc.style.filter = `brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) invert(${invert}%) blur(${blur}px)`;
    mainImg.style.transform = `rotate(${rotate}deg) scale(${flip_x}, ${flip_y})`;
    mainImg.style.filter = `brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) invert(${invert}%) blur(${blur}px)`;

});

save.addEventListener("click", () => {
    let canvas = document.createElement("canvas");
    let ctx = canvas.getContext("2d");
    canvas.width = imgSrc.naturalWidth;
    canvas.height = imgSrc.naturalHeight;
    ctx.filter = `brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) invert(${invert}%) blur(${blur}px)`;
    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.scale(flip_x, flip_y);
    ctx.drawImage(
        imgSrc, -canvas.width / 2, -canvas.height / 2,
        canvas.width,
        canvas.height
    );
    const link = document.createElement("a");
    link.download = "image.jpg";
    link.href = canvas.toDataURL();
    link.click();
});

// text editors

let optionsButtons = document.querySelectorAll(".option-button");
let advancedOptionButton = document.querySelectorAll(".adv-option-button");
let fontName = document.getElementById("fontName");
let fontSizeRef = document.getElementById("fontSize");
let writingArea = document.getElementById("text-input");
let linkButton = document.getElementById("createLink");
let alignButtons = document.querySelectorAll(".align");
let spacingButtons = document.querySelectorAll(".spacing");
let formatButtons = document.querySelectorAll(".format");
let scriptButtons = document.querySelectorAll(".script");

//List of fontlist
let fontList = [
    "Arial",
    "Verdana",
    "Times New Roman",
    "Garamond",
    "Georgia",
    "Courier New",
    "cursive",
    "Fantasy",
    "Slab Serif",
    "Script",
    "Decorative",
    "Tangerine"

];

//Initial Settings
const initializer = () => {
    //function calls for highlighting buttons
    //No highlights for link, unlink,lists, undo,redo since they are one time operations
    highlighter(alignButtons, true);
    highlighter(spacingButtons, true);
    highlighter(formatButtons, false);
    highlighter(scriptButtons, true);

    //create options for font names
    fontList.map((value) => {
        let option = document.createElement("option");
        option.value = value;
        option.innerHTML = value;
        fontName.appendChild(option);
    });


    //fontSize allows only till 
    for (let i = 1; i <= 7; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.innerHTML = i;
        fontSizeRef.appendChild(option);
    }

    //default size
    fontSizeRef.value = 3;
};

//main logic
const modifyText = (command, defaultUi, value) => {
    //execCommand executes command on selected text
    document.execCommand(command, defaultUi, value);
};

//For basic operations which don't need value parameter
optionsButtons.forEach((button) => {
    button.addEventListener("click", () => {
        modifyText(button.id, false, null);
    });
});

//options that require value parameter (e.g colors, fonts)
advancedOptionButton.forEach((button) => {
    button.addEventListener("change", () => {
        modifyText(button.id, false, button.value);
    });
});

//link
linkButton.addEventListener("click", () => {
    let userLink = prompt("Enter a URL");
    //if link has http then pass directly else add https
    if (/http/i.test(userLink)) {
        modifyText(linkButton.id, false, userLink);
    } else {
        userLink = "http://" + userLink;
        modifyText(linkButton.id, false, userLink);
    }
});

//Highlight clicked button
const highlighter = (className, needsRemoval) => {
    className.forEach((button) => {
        button.addEventListener("click", () => {
            //needsRemoval = true means only one button should be highlight and other would be normal
            if (needsRemoval) {
                let alreadyActive = false;

                //If currently clicked button is already active
                if (button.classList.contains("active")) {
                    alreadyActive = true;
                }

                //Remove highlight from other buttons
                highlighterRemover(className);
                if (!alreadyActive) {
                    //highlight clicked button
                    button.classList.add("active");
                }
            } else {
                //if other buttons can be highlighted
                button.classList.toggle("active");
            }
        });
    });
};

const highlighterRemover = (className) => {
    className.forEach((button) => {
        button.classList.remove("active");
    });
};

window.onload = initializer();

// text editors