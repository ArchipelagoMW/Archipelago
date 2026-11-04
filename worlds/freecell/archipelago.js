//=====================================================================
// Archipelago client for FreeCell (browser, no dependencies)
// Load AFTER script.js:  <script src="./archipelago.js"></script>
//
// Every game is a fresh random deal; the locations are score thresholds
// that can be reached inside a deal and stay checked once earned.
//
// IDs must match items.py / locations.py:
//   item id     = ITEM_BASE_ID + item code
//   location id = LOCATION_BASE_ID + score          (score 1..92)
//=====================================================================
(function(){
  var GAME="FreeCell";
  var ITEM_BASE_ID=7700000, LOCATION_BASE_ID=7700000;

  //one possible check per score 1..92 (apScoreSteps comes from script.js); the slot's score_step decides
  //which locations really exist - the server tells us in Connected, everything else is ignored
  var CHECK_KEYS=[],CHECK_LABELS={};
  apScoreSteps.forEach(function(step){
    CHECK_KEYS.push("score_"+step);
    CHECK_LABELS["score_"+step]="Score "+step;
  });
  var GOAL_KEY="score_"+apScoreSteps[apScoreSteps.length-1];   //perfect deal = all cards on the foundations

  var ITEM_NAMES={1:"Free Cell",2:"Tableau Column",3:"Undo",10:"Hearts Foundation",11:"Clubs Foundation",
                  12:"Diamonds Foundation",13:"Spades Foundation",100:"Filler Card"};

  var socket=null,connected=false,syncDone=false,goalSent=false;
  var receivedItems=[];
  var allLocations={},checkedLocations={};   //id -> true
  var pendingChecks={};                      //checks made while disconnected, resent on reconnect
  var els={};

  //-------------------------------------------------------------------
  // Networking
  //-------------------------------------------------------------------
  function send(packets){
    if (socket&&socket.readyState===1) socket.send(JSON.stringify(packets));
  }

  function connect(address,slot,password){
    disconnect(true);
    var url=/^wss?:\/\//.test(address)?address:((location.protocol==="https:"?"wss://":"ws://")+address);
    setStatus("Connecting...","warn");
    try{
      socket=new WebSocket(url);
    }catch(e){
      setStatus("Invalid address","bad");
      return;
    }
    socket.onmessage=function(evt){
      var packets=JSON.parse(evt.data);
      for (var i=0;i<packets.length;i++) onPacket(packets[i],slot,password);
    };
    socket.onerror=function(){ setStatus("Connection error","bad"); };
    socket.onclose=function(){
      var was=connected;
      connected=false;
      if (was) setStatus("Disconnected (checks are kept, reconnect to continue)","bad");
      render();
    };
  }

  function disconnect(silent){
    if (socket){
      socket.onclose=null;
      try{socket.close();}catch(e){}
      socket=null;
    }
    connected=false;
    if (!silent){
      setStatus("Disconnected","bad");
      render();
    }
  }

  function onPacket(p,slot,password){
    switch (p.cmd){
      case "RoomInfo":
        send([{cmd:"Connect",password:password||"",game:GAME,name:slot,uuid:getUuid(),
               version:{major:0,minor:5,build:0,"class":"Version"},
               items_handling:7,tags:[],slot_data:true}]);
        break;
      case "ConnectionRefused":
        setStatus("Refused: "+(p.errors||["unknown error"]).join(", "),"bad");
        break;
      case "Connected":
        onConnected(p);
        break;
      case "ReceivedItems":
        onReceivedItems(p);
        break;
      case "RoomUpdate":
        if (p.checked_locations) markChecked(p.checked_locations);
        render();
        break;
    }
  }

  function onConnected(p){
    var sd=p.slot_data||{};
    connected=true;
    syncDone=false;
    goalSent=false;
    apState.enabled=true;
    apState.startFreeCells=sd.start_free_cells!=null?sd.start_free_cells:1;
    apState.startTableau=sd.start_tableau!=null?sd.start_tableau:4;
    allLocations={};
    checkedLocations={};
    (p.checked_locations||[]).forEach(function(id){allLocations[id]=true;checkedLocations[id]=true;});
    (p.missing_locations||[]).forEach(function(id){allLocations[id]=true;});
    setStatus("Connected","good");
    saveSettings();

    //resend checks that were made while offline
    var pend=Object.keys(pendingChecks).map(Number);
    if (pend.length){
      send([{cmd:"LocationChecks",locations:pend}]);
      markChecked(pend);
    }
    newDeal();
    checkGoal();
  }

  function onReceivedItems(p){
    var fresh=p.items||[];
    if (p.index===0) receivedItems=fresh.slice();
    else receivedItems=receivedItems.slice(0,p.index).concat(fresh);

    if (syncDone&&p.index>0){
      fresh.forEach(function(it){
        apToast("Received: "+(ITEM_NAMES[it.item-ITEM_BASE_ID]||("item "+it.item)));
      });
    }
    syncDone=true;
    recomputeItems();
  }

  function recomputeItems(){
    var fc=0,tb=0,undo=false,f=[false,false,false,false];
    receivedItems.forEach(function(it){
      var code=it.item-ITEM_BASE_ID;
      if (code===1) fc++;
      else if (code===2) tb++;
      else if (code===3) undo=true;
      else if (code>=10&&code<=13) f[code-10]=true;
    });
    apState.freeCellItems=fc;
    apState.tableauItems=tb;
    apState.undo=undo;
    apState.foundations=f;
    applyLocks();      //defined in script.js; calls AP.refresh()
  }

  //-------------------------------------------------------------------
  // Checks
  //-------------------------------------------------------------------
  function locId(key){ return LOCATION_BASE_ID+parseInt(key.slice(6)); }   //"score_25" -> base + 25

  function markChecked(ids){
    ids.forEach(function(id){ allLocations[id]=true; checkedLocations[id]=true; });
  }

  function sendCheck(key){
    var id=locId(key);
    if (!allLocations[id]||checkedLocations[id]) return;   //unknown/disabled/already done
    checkedLocations[id]=true;
    pendingChecks[id]=true;
    send([{cmd:"LocationChecks",locations:[id]}]);
    apToast("Check: "+CHECK_LABELS[key]);
    checkGoal();
    render();
  }

  function checkGoal(){
    if (goalSent||!checkedLocations[locId(GOAL_KEY)]) return;
    goalSent=true;
    send([{cmd:"StatusUpdate",status:30}]);   //CLIENT_GOAL
    apToast("Goal complete!");
  }

  //a new random deal; earned checks are kept
  function newDeal(){
    setupGame("freecell");     //script.js
    render();
  }

  //-------------------------------------------------------------------
  // UI
  //-------------------------------------------------------------------
  function getUuid(){
    var id=null;
    try{id=localStorage.getItem("ap_uuid");}catch(e){}
    if (!id){
      id="fc-"+Math.random().toString(36).slice(2)+Date.now().toString(36);
      try{localStorage.setItem("ap_uuid",id);}catch(e){}
    }
    return id;
  }

  function saveSettings(){
    try{
      localStorage.setItem("ap_conn",JSON.stringify({address:els.address.value,slot:els.slot.value}));
    }catch(e){}
  }

  function loadSettings(){
    try{return JSON.parse(localStorage.getItem("ap_conn"))||{};}catch(e){return {};}
  }

  function setStatus(text,level){
    if (!els.status) return;
    els.status.textContent=text;
    els.status.className="apstatus "+(level||"");
  }

  function mk(tag,cls,text,parent){
    var e=document.createElement(tag);
    if (cls) e.className=cls;
    if (text) e.textContent=text;
    if (parent) parent.appendChild(e);
    return e;
  }

  function buildPanel(){
    var saved=loadSettings();
    var panel=mk("div","",null,document.body);
    panel.id="appanel";
    els.panel=panel;

    var head=mk("div","aphead","Archipelago",panel);
    head.addEventListener("click",function(){ panel.classList.toggle("collapsed"); });
    els.status=mk("div","apstatus","Not connected",panel);

    //connection form
    var form=mk("div","apform",null,panel);
    els.form=form;
    els.address=mk("input","",null,form);
    els.address.placeholder="server:port";
    els.address.value=saved.address||"archipelago.gg:38281";
    els.slot=mk("input","",null,form);
    els.slot.placeholder="slot name";
    els.slot.value=saved.slot||"";
    els.password=mk("input","",null,form);
    els.password.placeholder="password (optional)";
    els.password.type="password";
    var go=mk("button","","Connect",form);
    go.addEventListener("click",function(){
      if (!els.slot.value) return setStatus("Enter a slot name","bad");
      connect(els.address.value.trim(),els.slot.value.trim(),els.password.value);
    });

    //in-game info
    var info=mk("div","apinfo",null,panel);
    els.info=info;
    els.items=mk("div","apitems",null,info);
    els.progress=mk("div","approg",null,info);
    var nd=mk("button","","New random deal",info);
    nd.addEventListener("click",newDeal);
    var dc=mk("button","apsmall","Disconnect",info);
    dc.addEventListener("click",function(){
      disconnect(false);
      apState.enabled=false;     //back to offline free play
      setupGame("freecell");
      render();
    });
    render();
  }

  function itemChip(parent,label,on){
    mk("span","apchip"+(on?" on":""),label,parent);
  }

  function render(){
    if (!els.panel) return;
    els.form.style.display=connected?"none":"block";
    els.info.style.display=connected?"block":"none";
    if (!connected) return;

    els.items.innerHTML="";
    var line=mk("div","",null,els.items);
    itemChip(line,"Free cells "+apFreeCells()+"/4",apFreeCells()>0);
    itemChip(line,"Columns "+apTableau()+"/8",true);
    itemChip(line,"Undo",apState.undo);
    var suits=mk("div","",null,els.items);
    var sym=["\u2665","\u2663","\u2666","\u2660"];
    for (var s=0;s<4;s++){
      var c=mk("span","apchip suit"+(s%2==0?" red":"")+(apState.foundations[s]?" on":""),sym[s],suits);
      c.title=SUIT_NAMES[s]+" Foundation"+(apState.foundations[s]?"":" (locked)");
    }

    var total=0,done=0;
    for (var id in allLocations){
      total++;
      if (checkedLocations[id]) done++;
    }
    els.progress.textContent="Score: "+apState.score+" (best "+apState.bestScore+")  |  Checks: "+done+" / "+total;
  }

  window.AP={
    connect:connect,
    disconnect:disconnect,
    sendCheck:sendCheck,
    refresh:render,
    newDeal:newDeal
  };

  buildPanel();
})();
