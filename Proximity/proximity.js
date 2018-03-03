var my = {};

function proximityMain(wd, ht) {
    this.version = '0.36';
    w = typeof wd !== 'undefined' ? wd : '500';
    h = typeof ht !== 'undefined' ? ht : '400';
    var ltBG = 'background: radial-gradient(#bbb 15%, transparent 16%) 0 0,radial-gradient(#bbb 15%, transparent 16%) 6px 6px,	radial-gradient(rgba(240,240,240,.1) 15%, transparent 20%) 0 1px,	radial-gradient(rgba(240,240,240,.1) 15%, transparent 20%) 6px 6px; background-color:#abc;	background-size:12px 12px;';
    players = [{
        name: 'Blue',
        clr: 'rgba(66,88,255,1)',
        ai: 1
    }, {
        name: 'Red',
        clr: 'rgba(255,0,0,1)',
        ai: 0
    }, {
        name: 'Green',
        clr: 'rgba(0,255,0,1)',
        ai: 1
    }];
    my.playerMax = 2;
    var s = "";
    s += '<div id="wrapper">';
    s += '<div id="main" style="position:absolute; border: none; ' + ltBG + ' ">';
    s += '<canvas id="can1" style="position: absolute; width:' + w + 'px; height:' + h + 'px; left: 0; top:0; border: none;"></canvas>';
    s += '<canvas id="can2" style="position: absolute; width:' + w + 'px; height:' + h + 'px; left: 0; top:0; border: none;"></canvas>';
    s += popHTML();
    s += '<div id="score" style="font: 23px Arial; position:absolute; right:10px; bottom:5px; text-align: right;">0</div>';
    s += '<div id="win" style="position:absolute; left:-500px; top:60px; width:380px; padding: 5px; border-radius: 9px; color: white; background-color: rgba(0,0,60,0.8); box-shadow: 5px 5px 3px 0px rgba(0,0,0,0.3); transition: all linear 0.3s; opacity:0; text-align: center; font: 24px Arial; ">';
    s += '<div id="winTxt">Completed</div>';
    s += '<button onclick="winClose()" style="float:right; font: 22px Arial;" class="togglebtn" >&#x2714;</button>';
    s += '</div>';
    s += '<button id="restart" style="position: absolute; bottom:14px; left:3px; font: 14px Arial; height:30px; vertical-align:middle; z-index: 10;" class="togglebtn" onclick="popOpen()" >New Game</button>';
    s += '<button id="resize" style="position: absolute; bottom:14px; left:93px; font: 14px Arial; height:30px; vertical-align:middle; z-index: 10;" class="togglebtn" onclick="sizeToggle()" >Resize</button>';
    s += '<div id="copyrt" style="font: 9px arial; color: white; position:absolute; left:10px; bottom:3px;">&copy; 2016 MathsIsFun.com  v' + this.version + '</div>';
    s += '</div>';
    s += '</div>';
    document.write(s);
    el = document.getElementById('can1');
    canResize(el, w, h);
    g = el.getContext("2d");
    el2 = document.getElementById('can2');
    canResize(el2, w, h);
    g2 = el2.getContext("2d");
    this.clrs = [
        ["Blue", '#0000FF'],
        ["Red", '#FF0000'],
        ["Black", '#000000'],
        ["Green", '#00cc00'],
        ["Violet", '#EE82EE'],
        ["Orange", '#FFA500'],
        ["Light Salmon", '#FFA07A'],
        ["Slate Blue", '#6A5ACD'],
        ["Yellow", '#FFFF00'],
        ["Aquamarine", '#7FFFD4'],
        ["Pink", '#FFC0CB'],
        ["Coral", '#FF7F50'],
        ["Lime", '#00FF00'],
        ["Pale Green", '#98FB98'],
        ["Spring Green", '#00FF7F'],
        ["Teal", '#008080'],
        ["Hot Pink", '#FF69B4'],
        ["Yellow", '#ffff00'],
        ["Aqua", '#00ffff'],
        ["Gold", '#ffd700'],
        ["Khaki", '#F0E68C'],
        ["Thistle", '#D8BFD8'],
        ["Med Purple", '#aa00aa'],
        ["Light Blue", '#ADD8E6'],
        ["Sky Blue", '#87CEEB'],
        ["Navy", '#000080'],
        ["Purple", '#800080'],
        ["Wheat", '#F5DEB3'],
        ["Tan", '#D2B48C'],
        ["Silver", '#C0C0C0']
    ];
    el2 = document.getElementById('can2');
    el2.addEventListener('touchstart', ontouchstart, false);
    el2.addEventListener('touchmove', ontouchmove, false);
    window.addEventListener('touchend', ontouchend, false);
    el2.addEventListener("mousedown", onMouseDown, false);
    el2.addEventListener("mousemove", onMouseMove, false);
    window.addEventListener("mouseup", onMouseUp, false);
    frames = 0;
    my.holesQ = false;
    r = (w - 15) / 18;
    turn = 0;
    turnQ = true;
    turns = [0, 0, 0];
    val = 19;
    b = new Board();
    my.maxQ = false;
    if (window.innerWidth < 500) {
        my.maxQ = true;
    }
    resize();
    window.addEventListener('resize', resize, false);
    window.addEventListener('orientationchange', resize, false);
    playerMaxChg(0, 0);
    popOpen();
}

function sizeToggle() {
    my.maxQ = !my.maxQ;
    resize();
}

function resize() {
    if (my.maxQ) {
        var aspect = 5 / 4;
        var wd = window.innerWidth - 10;
        var ht = window.innerHeight - 10;
        var newAspect = wd / ht;
        if (newAspect > aspect) {
            wd = ht * aspect;
        } else {
            ht = wd / aspect;
        }
    } else {
        var wd = 500;
        var ht = 400;
    }
    var lt = (window.innerWidth - wd) / 2;
    var tp = (window.innerHeight - ht) / 2;
    console.log("resize", lt, tp, wd, ht);
    var div = document.getElementById('main');
    div.style.left = lt + "px";
    div.style.width = wd + "px";
    div.style.height = ht + "px";
    var div = document.getElementById('wrapper');
    div.style.height = ht + "px";
    canResize(el, wd, ht);
    canResize(el2, wd, ht);
    r = wd / 18.5;
    b.lt = r;
    b.tp = r;
    b.redraw();
}

function canResize(can, w, h) {
    ratio = 2;
    can.width = w * ratio;
    can.height = h * ratio;
    can.style.width = w + "px";
    can.style.height = h + "px";
    can.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
}

function turnNext() {
    g2.clearRect(0, 0, el.width, el.height);
    if (b.getLeft() <= 0) {
        b.redraw();
        win();
        return;
    }
    turn = loop(turn, 0, my.playerMax - 1);
    var player = players[turn];
    val = player.rounds[player.roundN++];
    val = Math.max(1, Math.min(val, 20));
    turns[turn] += val;
    b.redraw();
    if (players[turn].ai == 1) {
        turnQ = false;
        setTimeout(aimove, 1000);
    }
}

function aimove() {
    b.aimove();
    turnQ = true;
}

function Board() {
    this.colMax = 10;
    this.rowMax = 8;
    if (1 == 0) {
        this.colMax = 4;
        this.rowMax = 3;
    }
    this.lt = 25;
    this.tp = 25;
    this.cells = [];
    this.scores = [];
    this.restart();
    this.redraw();
}
Board.prototype.aimove = function() {
    var orig = copy2d(this.cells);
    var bests = [];
    for (var i = 0; i < this.colMax; i++) {
        for (var j = 0; j < this.rowMax; j++) {
            this.cells = copy2d(orig);
            if (this.cells[i][j].typ != -1) continue;
            this.doCell(i, j);
            var diff = this.scoreGet();
            bests.push([diff, i, j]);
        }
    }
    bests.sort(function(a, b) {
        return b[0] - a[0]
    });
    var bestNo = randomInt(0, Math.min(3, bests.length - 1));
    var best = bests[bestNo];
    this.cells = copy2d(orig);
    this.doCell(best[1], best[2]);
    turnNext();
};
Board.prototype.getLeft = function() {
    var n = 0;
    for (var i = 0; i < this.colMax; i++) {
        for (var j = 0; j < this.rowMax; j++) {
            var typ = this.cells[i][j].typ;
            if (typ == -1) {
                n++;
            }
        }
    }
    return n;
};
Board.prototype.scoreGet = function(typ) {
    var x = 0;
    for (var i = 0; i < this.colMax; i++) {
        for (var j = 0; j < this.rowMax; j++) {
            var cell = this.cells[i][j]
            if (cell.typ == turn) x += cell.val;
        }
    }
    return x;
};
Board.prototype.hiCell = function(xc, yc) {
    xc -= this.lt;
    yc -= this.tp;
    yn = (yc / (r * 1.5) + 0.5) << 0;
    xn = (xc / (r * 2 * 0.866) + 0.5) << 0;
    if (yn % 2) {
        xn = (xc / (r * 2 * 0.866)) << 0;
    } else {}
    this.hilite(xn, yn);
};
Board.prototype.click = function(xc, yc) {
    xc -= this.lt;
    yc -= this.tp;
    yn = (yc / (r * 1.5) + 0.5) << 0;
    xn = (xc / (r * 2 * 0.866) + 0.5) << 0;
    if (yn % 2) {
        xn = (xc / (r * 2 * 0.866)) << 0;
    } else {}
    if (xn < 0) return;
    if (yn < 0) return;
    if (xn >= this.colMax) return;
    if (yn >= this.rowMax) return;
    if (this.cells[xn][yn].typ != -1) return;
    this.doCell(xn, yn);
    turnNext();
};
Board.prototype.doCell = function(xn, yn) {
    this.cells[xn][yn] = {
        typ: turn,
        val: val
    };
    var nbors = this.getNbors(xn, yn);
    for (var i = 0; i < nbors.length; i++) {
        var nbor = nbors[i];
        var cell = this.cells[nbor[0]][nbor[1]];
        if (cell.typ >= 0) {
            if (cell.typ == turn) {
                this.cells[nbor[0]][nbor[1]] = {
                    typ: turn,
                    val: (cell.val + 1)
                };
            } else {
                if (cell.val < val) {
                    this.cells[nbor[0]][nbor[1]] = {
                        typ: turn,
                        val: cell.val
                    };
                }
            }
        }
    }
};
Board.prototype.inq = function(xn, yn) {
    if (xn < 0) return false;
    if (yn < 0) return false;
    if (xn >= this.colMax) return false;
    if (yn >= this.rowMax) return false;
    return true;
};
Board.prototype.hilite = function(xn, yn) {
    g2.clearRect(0, 0, el2.width, el2.height);
    if (!this.inq(xn, yn)) return;
    if (this.cells[xn][yn].typ != -1) return;
    g2.strokeStyle = 'yellow';
    g2.lineWidth = 3;
    if (turn == 0) {
        g2.fillStyle = 'rgba(0,0,255,0.6)';
    } else {
        g2.fillStyle = 'rgba(255,0,0,0.6)';
    }
    this.drawCell(g2, xn, yn, val.toString());
};
Board.prototype.getNbors = function(xn, yn) {
    var maybes = [
        [xn - 1, yn],
        [xn + 1, yn]
    ];
    var inc = yn % 2 ? 1 : 0;
    maybes.push([xn - 1 + inc, yn - 1]);
    maybes.push([xn + inc, yn - 1]);
    maybes.push([xn - 1 + inc, yn + 1]);
    maybes.push([xn + inc, yn + 1]);
    var nbors = [];
    for (var i = 0; i < maybes.length; i++) {
        var maybe = maybes[i];
        if (this.inq(maybe[0], maybe[1])) {
            nbors.push(maybe);
        }
    }
    return nbors;
};
Board.prototype.restart = function() {
    this.cells = [];
    for (var i = 0; i < this.colMax; i++) {
        row = [];
        for (var j = 0; j < this.rowMax; j++) {
            var c = {
                typ: -1,
                val: 0
            };
            if (my.holesQ) {
                if (Math.random() < 0.1) {
                    c.typ = -2;
                }
            }
            row.push(c);
        }
        this.cells.push(row)
    }
    this.scores = [0, 0];
};
Board.prototype.redraw = function() {
    g.clearRect(0, 0, el.width, el.height);
    this.scores = [0, 0, 0];
    for (var i = 0; i < this.colMax; i++) {
        for (var j = 0; j < this.rowMax; j++) {
            var s = '';
            var typ = this.cells[i][j].typ;
            g.strokeStyle = '#99a';
            if (typ >= 0) {
                g.lineWidth = 1;
                g.fillStyle = players[typ].clr;
                s = this.cells[i][j].val.toString();
                this.scores[typ] += this.cells[i][j].val;
            }
            if (typ == -1) {
                g.lineWidth = 1;
                g.fillStyle = '#eec';
            }
            if (typ == -2) {
                g.lineWidth = 0;
                g.strokeStyle = 'transparent';
                g.fillStyle = 'transparent';
            }
            this.drawCell(g, i, j, s);
        }
    }
    s = '<div style="background-color:rgba(88,88,255,0.2); padding:2px 6px; border-radius:5px;">';
    for (var i = 0; i < my.playerMax; i++) {
        if (i > 0) s += '<span style="color:grey"> vs </span>';
        s += '<span style="color:' + players[i].clr + '">' + this.scores[i] + '</span>';
    }
    s += '</div>';
    document.getElementById('score').innerHTML = s;
    g.strokeStyle = 'yellow';
    g.lineWidth = 3;
    g.fillStyle = players[turn].clr
    this.drawCell(g, this.colMax / 2 - 0.5, this.rowMax + 0.3, val.toString());
};
Board.prototype.drawCell = function(g, xn, yn, s) {
    var jig = 0;
    if (yn % 2) jig = r * (0.866);
    var xc = xn * r * 2 * 0.866 + jig;
    var yc = yn * r * 1.5;
    var endClr = g.fillStyle;
    for (var i = 0; i < 1; i++) {
        clr = endClr.replace('1)', '0.1)');
        g.fillStyle = clr;
        drawHex(g, this.lt + xc, this.tp + yc, r - i);
        g.fill();
        g.stroke();
    }
    if (s.length > 0) {
        g.textAlign = 'center';
        g.font = (r << 0) + 'px Arial';
        g.fillStyle = 'black';
        g.fillText(s, this.lt + xc, this.tp + yc + r * 0.3);
    }
};

function drawHex(g, xc, yc, r) {
    g.beginPath();
    for (var i = 0; i < 6; i++) {
        a = (i + 0.5) * Math.PI / 3;
        x = Math.cos(a) * r;
        y = Math.sin(a) * r;
        if (i == 0) {
            g.moveTo(xc + x, yc + y);
        } else {
            g.lineTo(xc + x, yc + y);
        }
    }
    g.closePath();
}

function ontouchstart(evt) {
    var touch = evt.targetTouches[0];
    evt.clientX = touch.clientX;
    evt.clientY = touch.clientY;
    evt.touchQ = true;
    onMouseDown(evt)
}

function ontouchmove(evt) {
    var touch = evt.targetTouches[0];
    evt.clientX = touch.clientX;
    evt.clientY = touch.clientY;
    evt.touchQ = true;
    onMouseMove(evt)
}

function ontouchend() {
    draggingQ = false;
}

function onMouseDown(evt) {
    var bRect = el.getBoundingClientRect();
    mouseX = (evt.clientX - bRect.left) * (el.width / ratio / bRect.width);
    mouseY = (evt.clientY - bRect.top) * (el.height / ratio / bRect.height);
    if (turnQ)
        b.click(mouseX, mouseY);
    draggingQ = true;
    frames = 0;
    if (evt.preventDefault) {
        evt.preventDefault();
    }
    return false;
}

function onMouseMove(evt) {
    var bRect = el.getBoundingClientRect();
    mouseX = (evt.clientX - bRect.left) * (el.width / ratio / bRect.width);
    mouseY = (evt.clientY - bRect.top) * (el.height / ratio / bRect.height);
    if (turnQ) b.hiCell(mouseX, mouseY);
    if (evt.preventDefault) {
        evt.preventDefault();
    }
    return false;
}

function onMouseUp() {
    draggingQ = false;
}

function holesToggle() {
    my.holesQ = !my.holesQ;
    btnToggle("holesBtn", my.holesQ);
}

function btnToggle(btn, onq) {
    if (onq) {
        document.getElementById(btn).classList.add("hi");
        document.getElementById(btn).classList.remove("lo");
    } else {
        document.getElementById(btn).classList.add("lo");
        document.getElementById(btn).classList.remove("hi");
    }
}

function popHTML() {
    var s = '';
    s += '<div id="optpop" style="position:absolute; left:-450px; top:10px; width:380px; padding: 5px; border-radius: 9px; background-color: #88aaff; box-shadow: 10px 10px 5px 0px rgba(40,40,40,0.75); transition: all linear 0.3s; opacity:0; text-align: center; ">';
    s += '<button id="holesBtn" onclick="holesToggle()" style="z-index:2;" class="togglebtn lo" >Holes</button>';
    s += '<div style="font: 16px Arial;">';
    s += '<br>';
    s += radioHTML('Players:', 'playerCount', [2, 3], 'playerMaxChg', 0, my.playerMax - 2);
    s += '<br>';
    s += '</div>';
    s += '<div style="font: 16px Arial; width:280px; margin-top:10px;">';
    for (var i = 0; i < players.length; i++) {
        var p = players[i];
        s += '<div id="player' + i + '" style="color:' + p.clr + ';  text-align:right;">';
        s += radioHTML(p.name + ':', 'player' + i, ['human', 'AI'], 'playerTypChg', i, p.ai);
        s += '</div>';
    }
    s += '</div>';
    s += '<p>&nbsp;</p>'
    s += '<div style="text-align:center;">';
    s += '<button onclick="popYes()" style="z-index:2; font: 22px Arial;" class="togglebtn" >&#x2714;</button>';
    s += '</div>';
    s += '</div>';
    return s;
}

function popOpen() {
    console.log("optpop");
    var pop = document.getElementById('optpop');
    pop.style.transitionDuration = "0.3s";
    pop.style.opacity = 1;
    pop.style.zIndex = 12;
    pop.style.left = (w - 380) / 2 + 'px';
}

function popYes() {
    var pop = document.getElementById('optpop');
    pop.style.opacity = 0;
    pop.style.zIndex = 1;
    pop.style.left = '-999px';
    gameNew();
}

function radioHTML(prompt, id, lbls, func, n, checkN) {
    var s = '';
    s += '<div style="display:inline-block; border: 1px solid white; border-radius:5px; padding:4px; margin:3px; background-color:rgba(255,255,255,0.2);">';
    s += prompt;
    for (var i = 0; i < lbls.length; i++) {
        var idi = id + i;
        var lbl = lbls[i];
        if (n === undefined) {
            funcStr = func + '(' + i + ')';
        } else {
            funcStr = func + '(' + n + ',' + i + ')';
        }
        var checkStr = '';
        if (checkN != undefined) {
            if (i == checkN) checkStr = ' checked ';
        }
        s += '<input type="radio" name="' + id + '" value="' + lbl + '" onclick="' + funcStr + ';"' + checkStr + ' autocomplete="off" />';
        s += '<label for="' + idi + '">' + lbl + ' </label>';
    }
    s += '</div>';
    return s;
}

function playerTypChg(n, i) {
    console.log("playerTyp", n, i);
    players[n].ai = i;
}

function playerMaxChg(n, i) {
    console.log("playerMaxChg", i);
    my.playerMax = i + 2;
    for (var i = 0; i < players.length; i++) {
        var div = document.getElementById('player2');
        if (i < my.playerMax) {
            div.style.visibility = 'visible';
        } else {
            div.style.visibility = 'hidden';
        }
    }
}

function gameNew() {
    g.clearRect(0, 0, el.width, el.height);
    g2.clearRect(0, 0, el.width, el.height);
    winClose();
    b.restart();
    turn = 0;
    turns = [0, 0, 0];
    roundsNew();
    turnNext();
}

function roundsNew() {
    var roundN = b.getLeft() / my.playerMax;
    var rounds = [];
    for (var i = 1; i <= roundN; i++) {
        var n = Math.ceil(20 * i / roundN);
        rounds.push(n);
    }
    for (var i = 0; i < my.playerMax; i++) {
        var p = players[i];
        var rs = rounds.slice();
        rs.shuffle();
        rs.push(randomInt(1, 5));
        p.rounds = rs;
        p.roundN = 0;
        console.log("player", i, p);
    }
}

function win() {
    var div = document.getElementById('win');
    div.style.opacity = 1;
    var dadDiv = document.getElementById('main');
    div.style.left = (parseInt(dadDiv.style.width) - parseInt(div.style.width)) / 2 + 'px';
    var scores = b.scores;
    var scoreMax = -1;
    var scoreMaxi = -1;
    for (var i = 0; i < scores.length; i++) {
        if (scores[i] > scoreMax) {
            scoreMax = scores[i];
            scoreMaxi = i;
        }
    }
    var atMaxN = 0;
    for (var i = 0; i < scores.length; i++) {
        if (scores[i] == scoreMax) {
            atMaxN++;
        }
    }
    var s = '';
    s += '<div style="margin-top:10px;">';
    if (atMaxN > 1) {
        s += 'A Draw!'
    } else {
        s += '<span style="color:' + players[scoreMaxi].clr + '">' + players[scoreMaxi].name + ' Wins' + '</span>';
    }
    s += '</div>';
    s += '<div style="margin-top:10px;">';
    for (var i = 0; i < my.playerMax; i++) {
        if (i > 0) s += '<span style="color:grey"> vs </span>';
        s += '<span style="color:' + players[i].clr + '">' + scores[i] + '</span>';
    }
    s += '</div>';
    s += '<br>';
    s += '<span style="font-size: 60%">';
    s += '(Given ';
    for (var i = 0; i < my.playerMax; i++) {
        if (i > 0) s += '<span style="color:grey"> vs </span>';
        s += '<span style="color:' + players[i].clr + '">' + turns[i] + '</span>';
    }
    s += ')';
    s += '<span>';
    document.getElementById('winTxt').innerHTML = s;
}

function winClose() {
    div = document.getElementById('win');
    div.style.opacity = 0;
    div.style.left = '-999px';
}

function copy2d(a) {
    var b = [];
    for (var i = 0; i < a.length; i++)
        b[i] = a[i].slice();
    return b;
}
