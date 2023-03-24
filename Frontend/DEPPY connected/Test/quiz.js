const start = document.getElementById("start");
const quiz = document.getElementById("quiz");
const question = document.getElementById("question");
const qImg = document.getElementById("qImg");
//const counter = document.getElementById("counter");
//const timeGauge = document.getElementById("timeGauge");
const progress = document.getElementById("progress");
const scoreDiv = document.getElementById("scoreContainer");

// create questions
let questions = [
    {
        question : "what is your name?",
        imgSrc : "img/logo.png",
       
    },{
        question : "How old are you?",
        imgSrc : "img/logo.png",
        
    },{
        question : "In which country did you spend most of your life?",
        imgSrc : "img/logo.png",
        
      },{
        question : "What's something you have achieved that you are most proud of and why?",
        imgSrc : "img/logo.png",
       
      },{
        question : "Who are some of your top role models, why do they inspire you?",
        imgSrc : "img/logo.png",
       
      },{
        question:  "How do you celebrate success?",
        imgSrc : "img/logo.png",
       
      },{
        question:  "What kind of behaviour makes you angry/annoyed?",
        imgSrc : "img/logo.png",
        
      },{
        question:  "Compare to your collagues or friends, do you consider yourself happier than most of them?",
        imgSrc : "img/logo.png",
       
      },{
        question:  "How do you recover from failure?",
        imgSrc : "img/logo.png",
       
      },{
        question:  "Do you have any other concerns that you would like to mention?",
        imgSrc : "img/logo.png",
       
    }
];

// create some variables

const lastQuestion = questions.length - 1;
let runningQuestion = 0;
let count = 0;
//const questionTime = 300; // 5min
//const gaugeWidth = 150; // 150px
//const gaugeUnit = gaugeWidth / questionTime;
//let TIMER;
//let score = 0;

// render a question
function renderQuestion(){
    let q = questions[runningQuestion];

    question.innerHTML = "<p>"+ q.question +"</p>";
    qImg.innerHTML = "<img src="+ q.imgSrc +">";
	
}

start.addEventListener("click",startQuiz);

// start quiz
function startQuiz(){
    start.style.display = "none";
    renderQuestion();
    quiz.style.display = "block";
    renderProgress();
    //renderCounter();
    //TIMER = setInterval(renderCounter,1000); // 1000ms = 1s
}
pro.addEventListener("click",renderCounter);


function renderCounter(){
              
        if(runningQuestion < lastQuestion){
            runningQuestion++;
            renderQuestion();
        }else{
            //clearInterval(TIMER);
            scoreRender();
        }
    
}


// score render
function scoreRender(){
    scoreContainer.style.display = "block";
	quiz.style.display="none";
	clo.addEventListener("onclick",window.close());

		
}

