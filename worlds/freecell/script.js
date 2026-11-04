var solitaires={
    freecell:{
        name:"FreeCell",
        cardinfo:{
            viewmode:"up",  //default direction cards are placed
            cardcount:[13]  //hearts,clubs,diamonds,spades
        },
        generalinfo:{
            redeals:0,
            checks:"none",
            autoplace:true,
            maxstack:"freecell"   //standard FreeCell limit: (free cells + 1) * 2^(empty columns), see apMaxStack()
        },
        board:[[
        {vardef:{
            criteria:"any|same|asc|any"
        }},
        {type:"rest"},
        {type:"rest"},
        {type:"rest"},
        {type:"rest"},
        {vardef:{
            criteria:"0|same|asc|any"
        }},
        {type:"collection"},
        {type:"collection"},
        {type:"collection"},
        {type:"collection"}
        ],[
        {vardef:{
            criteria:"any|alternate|desc|any"
        }},
        {type:"heap",startsize:7},
        {type:"heap",startsize:7},
        {type:"heap",startsize:7},
        {type:"heap",startsize:7},
        {type:"heap",startsize:6},
        {type:"heap",startsize:6},
        {type:"heap",startsize:6},
        {type:"heap",startsize:6}
    ]]
  }
};

var cardSvg={
  hearts: [['l',10,-1],['l',-10,12],['l',-10,-12],['c',-5,-10,10,-10,10,-3],['c',0,-7,15,-7,10,3]],
  clubs: [['c',-15,-15,15,-15,0,0],['c',13,-15,13,15,0,0],['l',3,7],['l',-6,0],['l',3,-7],['c',-13,15,-13,-15,0,0]],
  diamonds: [['l',0,-11],['l',10,11],['l',-10,11],['l',-10,-11],['l',10,-11]],
  spades: [['c',-3,8,-14,4,-10,-2],['l',10,-10],['l',10,10],['c',4,6,-7,10,-10,2],['l',3,7],['l',-6,0],['l',3,-7]]
};

var cardDistribution=[
  [[],[0.2,0.8]],
  [[],[0.2,0.5,0.8]],
  [[0.2,0.8],[]],
  [[0.2,0.8],[0.5]],
  [[0.2,0.5,0.8],[]],
  [[0.2,0.5,0.8],[0.35]],
  [[0.2,0.5,0.8],[0.35,0.65]],
  [[0.2,0.4,0.6,0.8],[0.5]],
  [[0.2,0.4,0.6,0.8],[0.3,0.7]]
];

var cardSpacing=[0.3,0.5,0.7];

var cards=[],cardsPlaced=0,cardNo=52,maxDeal=Infinity;
var parentPile=null,moveElem=null,movedElem=false,noAction=false;
var pickupData={};

//runtime variables
var redeals=0,maxRedeals=0,time,tick=null,interruptTime,moves,thread=null,winCards;
var checks,maxStack,autoP,currentGame,hints=[],hintCount=0,hinting=false,zoomBasis;

var gameMode="FreeCell";

//=====================================================================
// Archipelago integration (game logic side)
// Networking and UI live in archipelago.js. When apState.enabled is
// false (offline play) every lock is open and nothing is sent.
//=====================================================================
var SUIT_NAMES=["Hearts","Clubs","Diamonds","Spades"];   //same order as the suit index used by the game

var apState={
  enabled:false,
  startFreeCells:1,      //free cells available without any item
  startTableau:4,        //tableau columns available without any item
  freeCellItems:0,       //"Free Cell" items received
  tableauItems:0,        //"Tableau Column" items received
  foundations:[false,false,false,false],   //hearts, clubs, diamonds, spades
  undo:false,            //"Undo" item received
  undoUsed:false,        //undo used during the current run of this deal
  score:0,               //current score of this deal (see apComputeScore)
  bestScore:0            //highest score reached in this deal
};
var apDealFlags={},moveHistory=[],apUndoPending=false;

function apFreeCells(){
  return apState.enabled?Math.min(4,apState.startFreeCells+apState.freeCellItems):4;
}

function apTableau(){
  return apState.enabled?Math.min(8,apState.startTableau+apState.tableauItems):8;
}

function apSuitUnlocked(suit){
  return !apState.enabled||apState.foundations[suit]===true;
}

function apUndoUnlocked(){
  return !apState.enabled||apState.undo;
}

function isLockedPile(pile){
  return !!pile&&pile.classList.contains("locked");
}

function setClass(elem,cls,on){
  if (!elem) return;
  if (on) elem.classList.add(cls);
  else elem.classList.remove(cls);
}

//Locks free cells and tableau columns that haven't been unlocked yet
function applyLocks(){
  var rests=document.querySelectorAll(".pile.rest"),fc=apFreeCells(),tb=apTableau();
  for (var i=0;i<rests.length;i++) setClass(rests[i],"locked",i>=fc);
  for (var i=0;i<8;i++) setClass(document.getElementById("heap_"+i),"locked",i>=tb);
  createUndoButton();
  setAllMovable();      //locked/unlocked free cells change the maximum block size
  updateUndoButton();
  getHints();
  apCheckProgress();    //unlocking a column can change the score
}

//---------------------------------------------------------------------
// Undo (unlocked by the "Undo" item). Moves are always single cards,
// so reversing a move is just moving that card back to where it came from.
//---------------------------------------------------------------------
function createUndoButton(){
  var wrap=document.getElementById("buttonwrapper");
  if (!wrap||document.getElementById("undobutton")) return;
  var btn=document.createElement("div");
  btn.id="undobutton";
  btn.className="btn";
  btn.setAttribute("data-title","Undo");
  btn.innerHTML='<svg viewBox="0 0 40 40"><path d="M17 12 l-6 6 l6 6"></path><path d="M11 18 l11 0 a6 6 0 0 1 0 12 l-5 0"></path></svg>';
  btn.addEventListener("click",undoMove);
  wrap.appendChild(btn);
}

function updateUndoButton(){
  var btn=document.getElementById("undobutton");
  if (!btn) return;
  var unlocked=apUndoUnlocked();
  setClass(btn,"disabled",!unlocked||moveHistory.length==0);
  btn.setAttribute("data-title",unlocked?"Undo ("+moveHistory.length+")":"Undo (locked)");
}

function undoMove(){
  if (noAction||moveElem) return;
  if (!apUndoUnlocked()){
    apToast("Undo is locked - find the Undo item!");
    return;
  }
  if (moveHistory.length==0) return;
  var h=moveHistory.pop(),card=h.card;
  var elem=card.parentElement.classList.contains("cardwrapper")?card.parentElement:card;
  apState.undoUsed=true;
  apUndoPending=true;      //makes appendCards skip recording this move
  relayAppend(h.from,elem,200,"sliding",true);
}

document.addEventListener("keydown",function(evt){
  if ((evt.ctrlKey||evt.metaKey)&&(evt.key=="z"||evt.key=="Z")){
    evt.preventDefault();
    undoMove();
  }
});

//---------------------------------------------------------------------
// Score and location checks. The locations are score thresholds inside the
// current deal. Every score 1..92 has a location id; the player's score step
// decides which of them exist (the client ignores the others).
//
//   1 point  for every card that is stacked on a fitting card in a column
//            (one rank lower, other colour)
//   1 point  for every card on a foundation
//   10 bonus for every suit that is complete (A to K) on a foundation
//
// The score is calculated from the board, so moving cards back and forth
// can't be farmed. Max: 52 + 40 = 92 points (= deal won).
//---------------------------------------------------------------------
var apScoreSteps=[];     //every possible score threshold; the server decides which ones exist (option score_step)
for (var st=1;st<=92;st++) apScoreSteps.push(st);

//b can be stacked on a in a column: one rank lower and the other colour
function isStackStep(a,b){
  return parseInt(a.getAttribute("data-value"))-1==parseInt(b.getAttribute("data-value"))
      &&parseInt(a.getAttribute("data-suit"))%2!=parseInt(b.getAttribute("data-suit"))%2;
}

function apComputeScore(){
  var cols=document.getElementsByClassName("collection"),per=[0,0,0,0],onFoundation=0,stacked=0,bonus=0;
  for (var i=0;i<cols.length;i++){
    var cs=cols[i].getElementsByClassName("card");
    for (var n=1;n<cs.length;n++){     //index 0 is the empty-pile placeholder
      per[parseInt(cs[n].getAttribute("data-suit"))]++;
      onFoundation++;
    }
  }
  for (var i=0;i<8;i++){
    var heap=document.getElementById("heap_"+i);
    if (!heap||isLockedPile(heap)) continue;     //locked columns don't score
    var cs=heap.getElementsByClassName("card");
    for (var n=2;n<cs.length;n++){
      if (isStackStep(cs[n-1],cs[n])) stacked++;
    }
  }
  for (var s=0;s<4;s++) if (per[s]==13) bonus+=10;
  return onFoundation+stacked+bonus;
}

function apCheckProgress(){
  apState.score=apComputeScore();
  if (apState.score>apState.bestScore) apState.bestScore=apState.score;
  if (window.AP&&AP.refresh) AP.refresh();
  if (!apState.enabled||!window.AP) return;
  for (var i=0;i<apScoreSteps.length;i++){
    apFlag("score_"+apScoreSteps[i],apState.bestScore>=apScoreSteps[i]);
  }
}

function apFlag(key,cond){
  if (!cond||apDealFlags[key]) return;
  apDealFlags[key]=true;
  AP.sendCheck(key);
}

//---------------------------------------------------------------------
// Small feedback helpers
//---------------------------------------------------------------------
function apToast(text){
  var box=document.getElementById("aptoasts");
  if (!box){
    box=document.createElement("div");
    box.id="aptoasts";
    document.body.appendChild(box);
  }
  var t=document.createElement("div");
  t.className="aptoast";
  t.textContent=text;
  box.appendChild(t);
  setTimeout(function(){t.classList.add("fade");},2200);
  setTimeout(function(){if (t.parentElement) t.parentElement.removeChild(t);},2800);
}

function apLockHint(pile,card){
  if (!apState.enabled||!pile||!card) return;
  if (pile.classList.contains("locked")){
    apToast(pile.classList.contains("rest")?"That free cell is still locked":"That column is still locked");
  }else if (pile.classList.contains("collection")){
    var suit=parseInt(card.getAttribute("data-suit"));
    if (!apSuitUnlocked(suit)) apToast("The "+SUIT_NAMES[suit]+" foundation is still locked");
  }
}



document.body.addEventListener("mousemove",function(event){
  moveCards(event);
});

document.body.addEventListener("touchmove",function(event){
  moveCards(event);
  event.preventDefault();
});

document.body.addEventListener("mouseup",function(event){
  dropCards(event);
  removeHints();
  hinting=false;
});

document.body.addEventListener("touchend",function(event){
  dropCards(event);
  removeHints();
  hinting=false;
});

var actionscr=document.getElementById("actionscreen"),noScroll=false;
actionscr.addEventListener("wheel",scrollMove);
actionscr.addEventListener("mousewheel",scrollMove);

function scrollMove(evt){
  if (!noScroll&&evt.deltaX!=0&&evt.deltaY==0){
    var item=document.getElementsByClassName("settingsitem selected")[0];
    while (item){
      item=evt.deltaX>0?item.nextElementSibling:item.previousElementSibling;
      if (!item||!item.classList.contains("hidden")) break;
    }
    if (item) item.click();
    noScroll=true;
    setTimeout(function(){
      noScroll=false;
    },600);
  }
}

window.onresize=setHeapSpacing;

function moveCards(evt){
  if (moveElem&&!noAction){
    var x=(evt.clientX || evt.touches[0].clientX),
        y=(evt.clientY || evt.touches[0].clientY);
    moveElem.style.left=(x-pickupData.offsX)+"px";
    moveElem.style.top=(y-pickupData.offsY)+"px";
    if (Math.hypot(x-pickupData.x-pickupData.offsX,y-pickupData.y-pickupData.offsY)>5) movedElem=true;
  }
}
function setupGame(type){
  var gc=document.getElementById("gamecontainer");
  gc.innerHTML="";
  
  //Archipelago: every game is a fresh random deal. Per-run flags are reset,
  //checks that were already sent stay checked.
  moveHistory=[];
  apUndoPending=false;
  apDealFlags={};
  apState.undoUsed=false;
  apState.score=0;
  apState.bestScore=0;
  var game=solitaires[type],critArr=[],deckInfo=null;
  
  //set variables to default
  redeals=0;
  moves=-1;
  var extraClass="",heapCount=0;
  
  //setup variables
  var viewup=game.cardinfo.viewmode=="up";
  maxRedeals=game.generalinfo.redeals;
  checks=game.generalinfo.checks;
  maxStack=game.generalinfo.maxstack || Infinity;
  autoP=game.generalinfo.autoplace&&settingsData.autoplace;
  zoomBasis=game.generalinfo.size || 1;
  document.getElementById("gamecontainer").style.fontSize=zoomBasis*settingsData.zoom+"em";
  
  //general setup
  document.getElementById("gamename").innerHTML=game.name;
  setupCards(game.cardinfo.cardcount);
  shuffleCards();
  incMoves();
  currentGame=type;
  setTick();
  
  //here be dragons
  for (var i=0;i<game.board.length;i++){
    var bar=document.createElement("div");
    bar.className="contentbar";
    var inner=document.createElement("div");
    inner.className="innerwrapper";
    extraClass="";
    for (var n=0;n<game.board[i].length;n++){
      var obj=game.board[i][n];
      var place=document.createElement("div");
      
      if (obj.vardef){
        for (var a in obj.vardef){
          if (a=="criteria") critArr=obj.vardef.criteria.split("|");
        }
        extraClass=obj.vardef.addclass || "";
        continue;
      }
      
      var tmpExtraClass=obj.addclass || extraClass;
      if (obj.type=="deck"||obj.type=="deckdump"||obj.type=="collection"){
        place.className="pile"
        if (obj.type=="deck"){
          deckInfo=obj;
          place.classList.add("deck","noplace");
          if (obj.mode=="packets") place.classList.add("packets");
          place.setAttribute("redealable",redeals<maxRedeals);
          var bc=createBottomCard();
          bc.innerHTML=document.getElementById("deckbuffer").innerHTML;
          place.appendChild(bc);
          (function(cm,dm){
            place.addEventListener("click",function(event){cyclePile(cm,dm,event)});
          })(obj.mode,(obj.dealcount||0));
        }
        else if (obj.type=="deckdump"){
          place.classList.add("dump","noplace");
          if (obj.display){
            var attr="";
            for (var m=2;m<=obj.display;m++){attr+=m;}
            place.setAttribute("display",attr);
          }
          place.appendChild(createBottomCard());
        }
        else if (obj.type=="collection"){
          place.classList.add("collection");
          var bottomCard=document.createElement("div");
          bottomCard.className="card bottom";
          var ca=obj.criteria?obj.criteria.split("|"):critArr;
          if (ca[4]=="auto"){place.classList.add("noplace","notake");}
          setCriteria(bottomCard,ca);
          place.appendChild(bottomCard);
        }
      }else if (obj.type=="heap"||obj.type=="rest"){
        place.className="cardwrapper base";
        var baseCard=createBottomCard();
        var ca=obj.criteria?obj.criteria.split("|"):critArr;
        setCriteria(baseCard,ca);
        place.appendChild(baseCard);
        if (obj.type=="heap"){
          addHeap(place,obj.startsize,!viewup,ca);
          place.id="heap_"+heapCount;
          heapCount++;
          bar.classList.add("heapspace");
        }else{
          place.className="pile rest";
        }
      }else if (obj.type=="invisible") place.className="invisible";
      
      if (tmpExtraClass) place.classList.add(tmpExtraClass);
      //inner.append(place);
      bar.appendChild(place);
    }
    gc.appendChild(bar);
  }
  
  //add rest of cards into deck
  var deck=document.getElementsByClassName("deck");
  if (deck.length>0&&deckInfo){
    //create packets of cards
    if (deckInfo.mode=="packets"){
      while (cardsPlaced<cardNo){
        var packet=document.createElement("div");
        packet.className="packet";
        for (var i=0;i<deckInfo.packetsize&&cardsPlaced<cardNo;i++){
          packet.appendChild(createCard(true,critArr));
        }
        packet.addEventListener("click",function(event){
          distributePacket(event);
        });
        deck[0].appendChild(packet);
      }
    }else{
      while (cardsPlaced<cardNo){
        deck[0].appendChild(createCard(true,critArr));
      }
    }
  }
  flipTopCards();
  setAllMovable();
  setHeapSpacing(true);
  applyLocks();   //also refreshes the hints
}

function createBottomCard(){
  var card=document.createElement("div");
  card.className="card bottom";
  return card;
}

function setCriteria(card,critArr){
  card.setAttribute("data-value",critArr[0]);
  card.setAttribute("data-order",critArr[1]);
  card.setAttribute("data-direction",critArr[2]);
  card.setAttribute("data-suit",critArr[3]);
}

function cloneCriteria(card,card2,pile){
  card.setAttribute("data-order",card2.getAttribute("data-order"));
  card.setAttribute("data-direction",card2.getAttribute("data-direction"));
}

function setupCards(deck){
  cardsPlaced=0;
  cardNo=0;
  cards=[];
  for (var i=0;i<4;i++){
    var count=deck[i]==undefined?deck[0]:deck[i];
    for (var n=0;n<count;n++){
      cards.push({
        suit:i,
        value:n%13+1
      });
      cardNo++;
    }
  }
}

function shuffleCards(){
  for (var i=0;i<cards.length;i++){
    var rand=Math.floor(Math.random()*cards.length);
    var tmp=cards[rand];
    cards[rand]=cards[i];
    cards[i]=tmp;
  }
}

function addHeap(elem,count,hidden,ca){
  for (var i=0;i<count;i++){
    var wrapper=document.createElement("div");
    wrapper.className="cardwrapper";
    var card=createCard(hidden,ca);
    if (!card) return;
    wrapper.appendChild(card);
    elem.appendChild(wrapper);
    elem=wrapper;
  }
}

function createCard(hidden,ca){
  if (cardsPlaced>=cardNo) return;
  var card=document.createElement("div");
  card.className="card";
  card.setAttribute("data-index",cardsPlaced++);
  setCriteria(card,ca);
  if (ca[5]) card.setAttribute(ca[5],ca[6]);
  if (hidden){
    flipBack(card);
    card.setAttribute("data-value",-1);
  }else{
    flipCard(card,true);
  }
  card.addEventListener("mousedown",function(event){pickupCard(event);});
  card.addEventListener("touchstart",function(event){pickupCard(event);});
  return card;
}
function flipCard(card,forceFlip){
  if (!card) return;
  if (card.classList.contains("hidden")||forceFlip){
    card.classList.remove("hidden");
    var obj=cards[card.getAttribute("data-index")];
    card.setAttribute("data-value",obj.value);
    card.setAttribute("data-suit",obj.suit);
    
    addCardContent(card,obj.value,obj.suit);
  }
}

function flipBack(card){
  if (!card) return;
  if (!card.classList.contains("hidden")){
    card.classList.add("hidden");
    card.innerHTML=document.getElementById("reversebuffer").innerHTML;
  }
}

function flipTopCards(){
  var heaps=document.getElementsByClassName("cardwrapper base");
  for (var i=0;i<heaps.length;i++){
    flipCard(getTopCard(heaps[i]));
  }
}

function addCardContent(card,value,suit){
  card.innerHTML="";
  var span=document.createElement("span");
  span.innerHTML=idToValue(value);
  card.appendChild(span);
  card.appendChild(span.cloneNode(true));
  var svg=document.createElementNS("http://www.w3.org/2000/svg","svg");
  svg.setAttribute("viewBox","0 0 70 100");
  if (value==1){
    svg.appendChild(addSuit(0.5,0.5,suit,2));
  }else if (value<11){
    var arr=cardDistribution[value-2];
    for (var i=0;i<arr.length;i++){
      for (var n=0;n<arr[i].length;n++){
        if (i==0){
          svg.appendChild(addSuit(cardSpacing[0],arr[i][n],suit,0.8));
          svg.appendChild(addSuit(cardSpacing[2],arr[i][n],suit,0.8));
        }else{
          svg.appendChild(addSuit(cardSpacing[i],arr[i][n],suit,0.8));
        }
      }
    }
  }else{
    svg.innerHTML=document.getElementById("powerbuffer_"+value).innerHTML;
  }
  svg.appendChild(addSuit(0.075,0.17,suit,0.35));
  svg.appendChild(addSuit(0.925,0.83,suit,0.35,true));
  card.appendChild(svg);
}

function idToValue(val){
  var vals=['A',2,3,4,5,6,7,8,9,10,'J','Q','K'];
  return vals[val-1];
}

function addSuit(x,y,suit,zoom,flip){
  var path=document.createElementNS("http://www.w3.org/2000/svg","path");
  var dir=flip?-1:1;
  var d="M"+round(70*x)+" "+round(100*y+(suit%2==1?2.2:0)*zoom*dir);
  var arr=cardSvg[Object.keys(cardSvg)[suit]];
  for (var i=0;i<arr.length;i++){
    d+=arr[i][0]+" ";
    for (var n=1;n<arr[i].length;n++){
      d+=round(arr[i][n]*zoom*(n%2==0?dir:1))+" ";
    }
  }
  path.setAttribute("d",d);
  return path;
}

function round(val){
  var roundTo=2,pow=Math.pow(10,roundTo);
  return Math.round(val*pow)/pow;
}

function pickupCard(evt){
  removeHints();
  if (moveElem||noAction) return;
  //Cards in locked piles/columns cannot be picked up
  if (isLockedPile(getParentPile(evt.target))) return;
  //Pick up card, and if it's bounded by a wrapper, pick that up.
  moveElem=evt.target.parentElement.classList.contains("cardwrapper")?evt.target.parentElement:evt.target;
  var bcr=moveElem.getBoundingClientRect();
  
  pickupData={
    x:bcr.left,
    y:bcr.top,
    offsX:(evt.clientX || evt.touches[0].clientX)-bcr.left,
    offsY:(evt.clientY || evt.touches[0].clientY)-bcr.top
  }
  //console.log(offsX+" - "+offsY);
  moveCards(evt);
  parentPile=getParentPile(moveElem);
  setHeapSpacing(true,parentPile);
  movedElem=false;
  moveElem.classList.add("moving");
  evt.stopPropagation();
}

function dropCards(evt){
  if (moveElem&&!noAction){
    var pp=getOverlappingPile(moveElem);
    if (pp&&pp!=parentPile){
      if (canPlace(getTopCard(pp),getBottomCard(moveElem))){
        relayAppend(pp,moveElem,200,"sliding");
        return;
      }
      apLockHint(pp,getBottomCard(moveElem));
    }else if (!movedElem){
      if (!autoPlace(evt)) slideBack();
      return;
    }
    slideBack();
  }
}

function slideBack(){
  noAction=true;
  moveElem.classList.add("sliding");
  setTimeout(function(){
    moveElem.style.left=pickupData.x+"px";
    moveElem.style.top=pickupData.y+"px";
  },10);
  setTimeout(function(){
    resetCardPos();
    noAction=false;
  },200);
}

function getOverlappingPile(elem){
  var maxPile=null,maxArea=0;
  var elements=optiElem(".pile",".cardwrapper.base");
  for (var i=0;i<elements.length;i++){
    if (elements[i]!=parentPile&&!elements[i].classList.contains("noplace")){
      var compareCard=getTopCard(elements[i]);
      if (!compareCard) continue;
      var area=overlap(compareCard,elem);
      if (area>maxArea){
        maxArea=area;
        maxPile=elements[i];
      }
    }
  }
  return maxPile;
}

function canPlace(tc,bc){
  var tcp=getParentPile(tc),bcl=getPileLength(bc);
  //some no-no's
  if (!tc||!bc||tcp.classList.contains("noplace")||tc.classList.contains("hidden")) return false;
  //Archipelago locks: locked free cells/columns, and foundations of suits that aren't unlocked yet
  if (tcp.classList.contains("locked")) return false;
  if (tcp.classList.contains("collection")&&!apSuitUnlocked(parseInt(bc.getAttribute("data-suit")))) return false;
  if (bcl>1){
    if (!canCollapse(bc,tc)) return false;
  }
  
  //moving a block onto an empty column: that column can't be used as temporary space
  if (bcl>1&&maxStack==="freecell"&&tcp.classList.contains("base")&&tc.classList.contains("bottom")&&bcl>apMaxStack()/2) return false;
  
  //no rest piles may have more than one card in them
  if (tcp.classList.contains("rest")&&(tcp.children.length==2||bcl>1)) return false;
  
  var tcVal=parseInt(tc.getAttribute("data-value")),bcVal=parseInt(bc.getAttribute("data-value"));
  var tcSuit=tc.getAttribute("data-suit"),bcSuit=parseInt(bc.getAttribute("data-suit"));
  var dir=tc.getAttribute("data-direction"),ascending=dir=="asc";
  var order=tc.getAttribute("data-order");
  var alternating=order=="alternate";
  
  //assume that allowing a card of any value to be placed on a square/card means anything goes
  if (tc.getAttribute("data-value")=="any") return true;
  //check if the cards are directly in asc/desc order
  if (Math.abs(tcVal-bcVal)>1||tcVal==bcVal) return false;
  //check if cards are stacked in the correct order
  if (((tcVal<bcVal)^ascending)&&dir!="any") return false;
  //check if cards are alternating/have the same suit
  if (tcSuit=="any"||order=="consec"||tc.getAttribute("anysuit")=="true") return true;   
  //if the cards have passed all other tests up until this point, this must be true.
  if ((alternating&&tcSuit%2==bcSuit%2)||!alternating&&tcSuit!=bcSuit) return false;
  return true;
}

function canCollapse(tc,bc){
  //Concept: if there's a heap of cards where specific inherent properties are different
  //than the target pile's, that must mean the heap cannot be placed on the other.
  //Any details such as whether the card pattern will continue after appending will
  //be dealt with by canPlace.
  if (tc.getAttribute("data-order")!=bc.getAttribute("data-order")&&tc.getAttribute("data-order")!="consec") return false;
  if (tc.getAttribute("data-direction")!=bc.getAttribute("data-direction")) return false;
  return true;
}

function getPileLength(card){
  var parent=card.parentElement;
  return parent.classList.contains("pile")?1:parent.getElementsByClassName("card").length;
}

function getParentPile(elem){
  if (!elem) return null;
  while (elem.tagName!="BODY"){
    var cl=elem.classList;
    if (cl.contains("base")||cl.contains("pile")) return elem;
    elem=elem.parentElement;
  }
  return null;
}

function getTopCard(pile){
  var cards=pile.getElementsByClassName("card");
  return cards[cards.length-1] || pile;
}

function getBottomCard(pile){
  return pile.classList.contains("card")?pile:pile.getElementsByClassName("card")[0];
}

function relayAppend(target,cards,speed,extraClass,noSound){
  incMoves();
  noAction=true;
  cardToMoving(cards);
  speed=speed || 200;
  var dummy=document.createElement("div");
  dummy.className="card dummy";
  appendCards(target,dummy,true);
  var bcr=dummy.getBoundingClientRect();
  if (dummy.parentElement.classList.contains("cardwrapper")) dummy=dummy.parentElement;
  dummy.parentElement.removeChild(dummy);
  setTimeout(function(){
    if (extraClass) cards.classList.add(extraClass);
    cards.style.left=bcr.left+"px";
    cards.style.top=bcr.top+"px";
  },10);
  setTimeout(function(){
    noAction=false;
    appendCards(target,cards,false,noSound);
  },speed);
}

function appendCards(target,cards,noReset,noSound){
  var mElem=cards,pp,src=cards.parentElement;
  //find the moved card now: when a heap collapses onto a pile its wrapper is emptied/removed below
  var movedCard=mElem.classList.contains("card")?mElem:mElem.getElementsByClassName("card")[0];
  if (!noReset) pp=getParentPile(target);
  if (target.classList.contains("cardwrapper")){
    if (cards.classList.contains("card")){
      var wrapper=document.createElement("div");
      wrapper.className="cardwrapper";
      wrapper.appendChild(cards);
      cards=wrapper;
    }
    getTopCard(target).parentElement.appendChild(cards);
  }else{
    collapseHeap(target,cards);
  }
  if (noReset) return;
  
  //record the move for undo (a single card, since there are no supermoves)
  if (apUndoPending){
    apUndoPending=false;
  }else{
    moveHistory.push({card:movedCard,from:getParentPile(src),to:pp});
  }
  
  clonePile(target);
  flipTopCards();
  resetCardPos(mElem);
  apCheckProgress();
  checkCollectionFull();
  checkCards();
  setMovable(pp);
  setMovable(src);
  setAllMovable();      //the maximum block size depends on free cells/columns everywhere
  setHeapSpacing();
  getHints();
  updateUndoButton();
  if (!noSound) playEffect("place");
}

function setMovable(elem){
  var pp=getParentPile(elem),count=1,ms=getMaxStack();
  if (pp.classList.contains("pile")) return;
  var cards=[].slice.call(pp.getElementsByClassName("card"));
  cards.forEach(function(elm){
    elm.parentElement.classList.remove("cmovable");
  });
  for (var i=cards.length-1;i>0;i--){
    //look below to see what this does
    var block=isNaN(ms)?!checkConditions(cards[i-1],cards[i]):count>=ms;
    if (!canPlace(cards[i-1],cards[i])||block){
      cards[i-1].parentElement.classList.add("cmovable");
      return;
    }
    count++;
  }
  pp.classList.add("cmovable");
}

//Maximum number of cards that can be moved at once
function getMaxStack(){
  return maxStack==="freecell"?apMaxStack():maxStack;
}

//Standard FreeCell rule: every empty free cell adds one card, every empty column doubles the amount.
//Locked free cells and columns don't count.
function apMaxStack(){
  var free=0,empty=0,rests=document.querySelectorAll(".pile.rest");
  for (var i=0;i<rests.length;i++){
    if (!isLockedPile(rests[i])&&rests[i].getElementsByClassName("card").length==1) free++;
  }
  for (var i=0;i<8;i++){
    var heap=document.getElementById("heap_"+i);
    if (heap&&!isLockedPile(heap)&&heap.getElementsByClassName("card").length==1) empty++;
  }
  return (free+1)*Math.pow(2,empty);
}

//Checks additional conditions with visible cards, i.e. if two cards share specific properties, such
//as same suit. Makes it so that decisions can be made whether a valid movable block can be made out of a 
//sequence of cards.
function checkConditions(c1,c2){
  for (var key in maxStack){
    var check=maxStack[key],same=key=="same";
    for (var i=0;i<check.length;i++){
      if ((c1.getAttribute("data-"+check[i])==c2.getAttribute("data-"+check[i]))^same) return false;
    }
  }
  return true;
}

function setAllMovable(){
  var heaps=document.getElementsByClassName("cardwrapper base");
  for (var i=0;i<heaps.length;i++){
    setMovable(heaps[i]);
  }
}

function setHeapSpacing(noAnim,defaultPile){
  var heaps=document.getElementsByClassName("cardwrapper base");
  if (defaultPile) defaultPile=defaultPile.getElementsByClassName("card").length-2;
  if (heaps.length==0) return;
  var cardHeight=document.getElementsByClassName("card")[0].offsetHeight,marginSpace=heaps[0].parentElement.offsetHeight-cardHeight;
  if (!noAnim) document.body.classList.add("slideheap");
  var css="";
  for (var i=0;i<heaps.length;i++){
    var cardCount=heaps[i].getElementsByClassName("card").length-2;
    if (cardCount<1) cardCount=defaultPile || 1;
    var margin=Math.min(Math.max(Math.floor(marginSpace/cardCount),10),cardHeight/3);
    css+="#heap_"+i+" > .cardwrapper .cardwrapper {";
    css+="margin-top:"+margin+"px";
    css+="}\n";
  }
  document.getElementById("customstyle").innerHTML=css;
  setTimeout(function(){
    document.body.classList.remove("slideheap");
  },200);
}

function resetCardPos(cards){
  cards=cards || moveElem;
  if (cards){
    cards.classList.remove("moving");
    cards.removeAttribute("style");
    cards.classList.remove("sliding");
    cards.classList.remove("collapse");
    moveElem=null;
    parentPile=null;
  }
}

function checkCollectionFull(){
  var collections=document.getElementsByClassName("collection"),count=0;
  for (var i=0;i<collections.length;i++){
    count+=(collections[i].children.length-1);
  }
  if (count==cardNo) animateWin();
}

function animateWin(){
  clearInterval(tick);
  tick=null;
  var cards=document.querySelectorAll(".card:not(.bottom)");
  var padding=cards[0].offsetHeight/2;
  winCards=[];
  for (var i=0;i<cards.length;i++){
    cardToMoving(cards[i]);
    var bcr=cards[i].getBoundingClientRect();
    winCards.push({
      dom:cards[i],
      top:bcr.top,
      left:bcr.left,
      dx:(Math.random()>0.5?-1:1)*(Math.random()*10+5),
      dy:Math.random()*-15,
      delay:(cards.length-i)*2
    });
  }
  
  setTimeout(function(){
    thread=setInterval(moveWinCards,25);
  },500);
  /*setTimeout(function(){
    for (var i=0;i<cards.length;i++){
      cards[i].classList.add("winning");
      cards[i].style.left=Math.floor(Math.random()*(window.innerWidth-padding*2)+padding)+"px";
      cards[i].style.top=Math.floor(Math.random()*(window.innerHeight-padding*2)+padding)+"px";
      cards[i].style.transform="rotate("+(Math.random()*180-90)+"deg";
      cards[i].style.transitionDelay=i*50+"ms";
    }
  },500);*/
}

function moveWinCards(){
  var bcr=winCards[0].dom.getBoundingClientRect();
  var bounce=window.innerHeight-bcr.height;
  for (var i=winCards.length-1;i>=0;i--){
    var crd=winCards[i];
    crd.delay--;
    if (crd.delay>0) continue;
    if (crd.delay==0) crd.dom.classList.add("winning");
    crd.top+=crd.dy;
    crd.left+=crd.dx;
    crd.dy++;
    if (crd.top>bounce){
      crd.top=bounce;
      crd.dy*=-0.8;
    }
    if (crd.left>window.innerWidth||crd.left<-bcr.width){
      crd.dom.style.display="none";
      crd.dom.classList.remove("moving");
      winCards.splice(i,1);
    }
    crd.dom.style.top=crd.top+"px";
    crd.dom.style.left=crd.left+"px";
  }
  if (winCards.length==0) clearInterval(thread);
}

function cardToMoving(card){
  var bcr=card.getBoundingClientRect();
  card.classList.add("moving");
  card.style.left=Math.floor(bcr.left)+"px";
  card.style.top=Math.floor(bcr.top)+"px";
}

function checkCards(){
  if (checks=="none") return;
  //First atrocity: 
  if (checks=="flush"){
    var heaps=document.getElementsByClassName("cardwrapper base");
    
    main:
    for (var i=0;i<heaps.length;i++){
      var cards=heaps[i].getElementsByClassName("card");
      if (cards.length>13){
        var val=1,count=13;
        for (var n=cards.length-1;n>0;n--){
          if (cards[n].getAttribute("data-value")!=val) continue main;
          val++;
          count--;
          if (count==0){
            moveElem=cards[n].parentElement;
            break;
          }
        }
        var collections=document.getElementsByClassName("collection");
        for (var n=0;n<collections.length;n++){
          if (collections[n].children.length==1){
            cardToMoving(moveElem);
            relayAppend(collections[n],moveElem,450,"collapse");
            return;
          }
        }
      }
    }
  }
}

function collapseHeap(target,wrapper){
  if (wrapper.classList.contains("card")){
    target.appendChild(wrapper);
  }else{
    var toDelete=wrapper;
    while (true){
      target.appendChild(wrapper.getElementsByClassName("card")[0]);
      wrapper=wrapper.getElementsByClassName("cardwrapper")[0];
      if (!wrapper) break;
    }
    toDelete.parentElement.removeChild(toDelete);
  }
  clonePile(target);
}

function clonePile(elem){
  var pile=getParentPile(elem);
  var cards=pile.getElementsByClassName("card");
  for (var i=1;i<cards.length;i++){
    cloneCriteria(cards[i],cards[0],pile);
  }
}

function overlap(elem,elem2){
  var rect=elem.getBoundingClientRect(),rect2=elem2.getBoundingClientRect();
  var top=Math.max(rect.top,rect2.top),bottom=Math.min(rect.bottom,rect2.bottom);
  var left=Math.max(rect.left,rect2.left),right=Math.min(rect.right,rect2.right);
  if (top>bottom||left>right) return 0;
  return (right-left)*(bottom-top);
}

function cyclePile(cm,dc,evt){
  if (noAction) return;
  var deck=evt.target,
      isEmpty=deck.querySelectorAll(".card:not(.moving)").length==1;
  var dump=document.getElementsByClassName("dump")[0];
  if (cm=="heap"){
    dump=document.getElementsByClassName("collection")[0];
    cm="normal";
  }
  if (cm=="normal"){
    var card=deck.children[1];
    if (!card){
      if (redeals>=maxRedeals) return;
      var cards=dump.children,len=cards.length;
      for (var i=1;i<len;i++){
        flipBack(cards[1]);
        deck.appendChild(cards[1]);
      }
      redeals++;
      deck.setAttribute("redealable",redeals<maxRedeals);
    }
    for (var i=0;i<dc;i++){
      card=deck.children[i+1];
      if (!card) break;
      flipCard(card);
      relayAppend(dump,card,270,"sliding",true);
    }
  }
  var crds=optiElem(".deck .card + .card",".dump .card + .card").length;
  if (crds) playEffect(isEmpty?"collapse":"flip");
}

function distributePacket(evt){
  var packet=evt.target;
  packet.style.cssText="box-shadow:none !important";
  var cards=[].slice.call(packet.children);
  cards.forEach(function(card){   //no arrow notation because IE
    flipCard(card);
  });
  var heaps=document.getElementsByClassName("cardwrapper base");
  for (var i=0;i<cards.length;i++){
    relayAppend(heaps[i%heaps.length],cards[i],430,"collapse");
  }
  setTimeout(function(){
    if (packet.parentElement) packet.parentElement.removeChild(packet);
  },450);
}

function autoPlace(evt){
  if (!autoP) return false;
  var cards=evt.target,actElem=null;
  
  var tmpIndex=(hints.length+hintCount-1)%hints.length,dest=null;
  if (hints.length>0&&cards==hints[tmpIndex][0]&&hinting) dest=hints[tmpIndex][1];
    
  //cards is ALWAYS a .card element. If it's not, this will break.
  if (cards.parentElement.classList.contains("cardwrapper")) cards=cards.parentElement;
  
  if (dest){
    relayAppend(dest.parentElement,cards,200,"sliding");
    evt.stopPropagation();
    return true;
  }
  
  var bc=getBottomCard(cards);
  var elems=getPriorityList();
  
  for (var i=0;i<elems.length;i++){
    if (canPlace(getTopCard(elems[i]),bc)){
      if (!actElem||actElem.classList.contains("collection")) actElem=elems[i];
      if (elems[i].children.length>1||elems[i].classList.contains("collection")) break;
    }
  }
  if (actElem){
    relayAppend(actElem,cards,200,"sliding");
    evt.stopPropagation();
    return true;
  }
  return false;
}

function getPriorityList(){
  //This creates an array of elements ordered in decreasing priority.
  return optiElem(".collection",".cardwrapper.base .cardwrapper",".cardwrapper.base",".rest");
}

function getHints(){
  hints=[];
  hintCount=0;
  
  //add class to first empty heap
  var heaps=document.getElementsByClassName("cardwrapper base"),
      addedClass=false;
  for (var i=0;i<heaps.length;i++){
    heaps[i].classList.remove("fe");
    if (!addedClass&&heaps[i].children.length==1){
      heaps[i].classList.add("fe");
      addedClass=true;
    }
  }
  
  heaps=optiElem(".collection div:last-of-type",".cardwrapper.base > .cardwrapper",".cardwrapper.fe",".rest div:last-of-type"),topCards=[];
  for (var i=0;i<heaps.length;i++){
    topCards.push(getTopCard(heaps[i]));
  }
  
  var movables=optiElem(".cmovable > .cardwrapper > .card",".cmovable > .cardwrapper .cardwrapper .card",".rest .card + .card",".dump div:last-of-type:not(.bottom)");
  
  for (var i=0;i<topCards.length;i++){
    var pm=getParentPile(topCards[i]);
    for (var n=0;n<movables.length;n++){
      if (canPlace(topCards[i],movables[n])&&getParentPile(movables[n])!=pm&&!isLockedPile(getParentPile(movables[n]))){
        hints.push([movables[n],topCards[i]]);
      }
    }
  }
  
  var decks=document.getElementsByClassName("deck");
  var dealCards=optiElem(".deck .card + .card",".dump .card + .card").length;
  //console.log(dealCards);
  for (var i=0;i<decks.length;i++){
    if (dealCards>0&&(decks[i].getElementsByClassName("card").length>1||decks[i].getAttribute("redealable")=="true")){
      hints.push([decks[i].lastChild]);
    }
  }
  
  document.getElementById("hintbutton").setAttribute("data-title",hints.length>0?"Get hint (1/"+hints.length+")":"No hints available");
  document.getElementById("hintbutton").setAttribute("data-hints",hints.length);
  if (hints.length==0){
    clearInterval(tick);
    tick=null;
  }
}

function optiElem(selector){
  var out=[];
  for (var i=0;i<arguments.length;i++){
    var elems=[].slice.call(document.querySelectorAll(arguments[i]));
    var empties=0;
    for (var n=0;n<elems.length;n++){
      empties+=isBottom=elems[n].classList.contains("bottom");
      if (empties>1){
        elems.splice(n,1);
        n--;
      }
    }
    out=out.concat(elems);
  }
  return out;
}

function playEffect(type){
  var audio=document.getElementById(type+"sound");
  if (!audio) return;     //no sound elements in the page: stay silent
  audio.volume=settingsData.globalVol;
  audio.currentTime=0;
  var p=audio.play();
  if (p&&p.catch) p.catch(function(){});
}
//UI stuff
function setTick(){
  clearInterval(tick);
  tick=null;
  time=new Date().getTime();
  tick=setInterval(timeCount,1000);
  timeCount();
}

function timeCount(){
  var timeOut="",newTime=(new Date().getTime()-time)/1000;
  if (newTime>=3600){
    timeOut=addZeroes(newTime/3600)+":";
    newTime%=3600;
  }
  timeOut+=addZeroes(newTime/60)+":";
  newTime%=60;
  timeOut+=addZeroes(newTime);
  document.getElementById("time").innerHTML=timeOut;
}

function addZeroes(inp){
  inp=Math.floor(inp)
  return inp<10?"0"+inp:inp;
}

function incMoves(){
  moves++;
  document.getElementById("movecount").innerHTML=moves;
}

function toggleAction(){
  var expanded=document.body.getAttribute("expanded")=="true";
  if (expanded){
    if (tick){
      time+=(new Date().getTime()-interruptTime);
      timeCount();
    }
    setTimeout(function(){
      slideSettings(document.getElementsByClassName("settingsitem")[0],0);
      var si=[].slice.call(document.getElementsByClassName("actionwrapper"));
      si.forEach(function(e){
        e.scrollTop=0;
      });
    },500);
  }else{
    interruptTime=new Date().getTime();
  }
  document.body.setAttribute("expanded",!expanded);
}

function fillShowcase(){
  var sc=document.getElementById("showcase"),counter=0;
  for (var key in solitaires){
    var sci=document.createElement("div");
    sci.className="showcaseitem";
    var st=document.createElement("div");
    st.className="solitairethumb";
    st.style.backgroundPosition=-100*(counter%2)+"% "+20*Math.floor(counter/2)+"%";
    var p=document.createElement("p");
    p.innerHTML=solitaires[key].name || "Untitled Solitaire";
    sci.appendChild(st);
    sci.appendChild(p);
    sc.appendChild(sci);
    (function(k){
      sci.addEventListener("click",function(){
        relaySetupGame(k);
      });
    })(key);
    counter++;
  }
}

function relaySetupGame(type){
  toggleAction();
  setupGame(type);
}

function markHints(){
  removeHints();
  if (hints.length==0) return;
  hinting=true;
  hints[hintCount][0].classList.add("hint");
  if (hints[hintCount][1]) hints[hintCount][1].classList.add("hint");
  hintCount=(hintCount+1)%hints.length;
  document.getElementById("hintbutton").setAttribute("data-title","Get hint ("+(hintCount+1)+"/"+hints.length+")");
}

function removeHints(){
  var hnts=document.getElementsByClassName("hint");
  for (var i=hnts.length-1;i>=0;i--){
    hnts[i].classList.remove("hint");
  }
}

function slideSettings(elem,id){
  var si=[].slice.call(document.getElementsByClassName("settingsitem"));
  si.forEach(function(e){
    e.classList.remove("selected");
  });
  elem.classList.add("selected");
  document.getElementsByClassName("actionwrapper")[0].style.marginLeft="-"+id*100+"%";
}

function showAndSlide(id){
  slideSettings(document.getElementsByClassName("settingsitem")[id],id);
}

var inputs=[
  ["boolean","hintbutton","Hint mode",0,[0,"show hints",1,"hide hint count",2,"no hints"],setAttribute],
  ["boolean","autoplace","Autoplace",true,[true,"on",false,"off"],setAP],
  [
    ["slider","zoom","Zoom",1,0.7,1.3,0.02,setZoom],
    ["boolean","",[1,"Default"]]
  ],
  [
    ["slider","globalVol","Volume",1,0,1,0.02,setVol],
    ["boolean","",[0,"Mute"]]
  ]
];

var settingsData=JSON.parse(localStorage.getItem("settings")) || {zoom:1,autoplace:true,globalVol:1};
function injectInputs(){
  for (var i=0;i<inputs.length;i++){
    var arr=Array.isArray(inputs[i][0])?inputs[i][0]:inputs[i];
    if (settingsData.hasOwnProperty(arr[1])) arr[3]=settingsData[arr[1]];
  }
}
injectInputs();

generateForm(inputs,document.getElementById("inputarea"));
for (var key in inputData){
  var obj=inputData[key];
  if (obj.changeCallback) obj.changeCallback(obj);
}

document.body.addEventListener("inputchange",function(evt){
  localStorage.setItem("settings",JSON.stringify(settingsData));
  console.log(evt);
});

function setAttribute(obj){
  document.getElementById(obj.name).setAttribute("data-level",obj.value);
  settingsData[obj.name]=obj.getValue();
}

function setZoom(obj){
  settingsData.zoom=obj.getValue();
  document.getElementById("gamecontainer").style.fontSize=zoomBasis*settingsData.zoom+"em";
  setHeapSpacing(true);
}

function setVol(obj){
  settingsData.globalVol=obj.getValue();
}

function setAP(obj){
  settingsData.autoplace=obj.getValue();
  autoP=settingsData.autoplace;
}

Math.hypot=function(a,b){
  return Math.sqrt(a*a+b*b);
};

fillShowcase();
setupGame("freecell");
