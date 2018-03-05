## CS 5100 Project Proposal
**Matthias Denu & Donald Hamnet**

### Description

```
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
```
### Platform
