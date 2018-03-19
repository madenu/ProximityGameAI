// comprise game state from board fields (b.yadda, b.foo, b.cells, b.*)
// make a getSuccessors function
// make a simple eval function (heuristics or game score) (make higher order)
// generalize aimove to use different agents
// reflex, minimax, expectimax, alpha-beta
// make an expictimax, alpha-beta agent that goes to a reasonable depth
// integrate ML concepts

function aimove() {
    aimove_help();
    turnQ = true;
}

function aimove_help() {
    var orig = copy2d(b.cells);
    var bests = [];
    for (var i = 0; i < b.colMax; i++) {
        for (var j = 0; j < b.rowMax; j++) {
            b.cells = copy2d(orig);
            if (b.cells[i][j].typ != -1) continue;
            b.doCell(i, j);
            var diff = b.scoreGet();
            bests.push([diff, i, j]);
        }
    }
    bests.sort(function(a, b) {
        return b[0] - a[0]
    });
    var bestNo = randomInt(0, Math.min(3, bests.length - 1));
    var best = bests[bestNo];
    b.cells = copy2d(orig);
    b.doCell(best[1], best[2]);
    turnNext();
};
