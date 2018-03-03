function dist(dx, dy) {
    return Math.sqrt(dx * dx + dy * dy);
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function loop(currNo, minNo, maxNo, incr) {
    if (incr === undefined) incr = 1;
    currNo += incr;
    var range = maxNo - minNo + 1;
    if (currNo < minNo) {
        currNo = maxNo - (-currNo + maxNo) % range;
    }
    if (currNo > maxNo) {
        currNo = minNo + (currNo - minNo) % range;
    }
    return currNo;
}

function constrain(min, val, max) {
    return (Math.min(Math.max(min, val), max));
}

function fmt(num, digits) {
    if (num == Number.POSITIVE_INFINITY) return "undefined";
    if (num == Number.NEGATIVE_INFINITY) return "undefined";
    num = Number(num.toPrecision(digits));
    if (Math.abs(num) < 1e-15) num = 0;
    return num;
}
Array.prototype.shuffle = function() {
    var counter = this.length,
        temp, index;
    while (counter > 0) {
        index = (Math.random() * counter--) | 0;
        temp = this[counter];
        this[counter] = this[index];
        this[index] = temp;
    }
};

function Pt(x, y) {
    this.x = x;
    this.y = y;
    return this;
};

function Line(a, b) {
    this.a = a;
    this.b = b;
    return this;
};

function Rect(lt, tp, wd, ht) {
    this.lt = lt;
    this.tp = lt;
    this.wd = wd;
    this.ht = ht;
    return this;
};
Rect.prototype.bt = function() {
    return this.tp + this.ht;
}
Rect.prototype.rt = function() {
    return this.lt + this.wd;
}
Rect.prototype.center = function() {
    return [this.lt + (this.wd / 2) | 0, this.tp + (this.ht / 2) | 0];
}
Rect.prototype.move = function(lt, tp) {
    return new Rect(this.lt + lt, this.tp + tp, this.wd, this.ht);
};
Rect.prototype.moveMe = function(lt, tp) {
    this.lt += lt;
    this.tp += tp;
    return;
};
Rect.prototype.clip = function(rect) {
    if (!this.collideRect(rect)) {
        return new Rect(0, 0, 0, 0);
    }
    var lt, tp, wd, ht;
    if ((this.lt >= rect.lt) && (this.lt < rect.rt)) {
        lt = this.lt;
    } else if ((rect.lt >= this.lt) && (rect.lt < this.rt)) {
        lt = rect.lt;
    }
    if ((this.rt > rect.lt) && (this.rt <= rect.rt)) {
        wd = this.rt - x;
    } else if ((rect.rt > this.lt) && (rect.rt <= this.rt)) {
        wd = rect.rt - x;
    }
    if ((this.tp >= rect.tp) && (this.tp < rect.bt)) {
        tp = this.tp;
    } else if ((rect.tp >= this.tp) && (rect.tp < this.bt)) {
        tp = rect.tp;
    }
    if ((this.bt > rect.tp) && (this.bt <= rect.bt)) {
        ht = this.bt - y;
    } else if ((rect.bt > this.tp) && (rect.bt <= this.bt)) {
        ht = rect.bt - y;
    }
    return new Rect(lt, tp, wd, ht);
};
Rect.prototype.union = function(rect) {
    var lt = Math.min(this.lt, rect.lt);
    var tp = Math.min(this.tp, rect.tp);
    var wd = Math.max(this.rt, rect.rt) - x;
    var ht = Math.max(this.bt, rect.bt) - y;
    return new Rect(lt, tp, wd, ht);
};
Rect.prototype.inflate = function(x, y) {
    var copy = this.clone();
    copy.inflateMe(x, y);
    return copy;
};
Rect.prototype.inflateMe = function(x, y) {
    this.lt -= Math.floor(x / 2);
    this.tp -= Math.floor(y / 2);
    this.wd += x;
    this.ht += y;
};
Rect.prototype.collidePoint = function(x, y) {
    return (this.lt <= x && x <= this.rt) && (this.tp <= y && y <= this.bt);
};
Rect.prototype.collideRect = function(rect) {
    return !(this.lt > rect.rt || this.rt < rect.lt || this.tp > rect.bt || this.bt < rect.tp);
};
Rect.prototype.collideLine = function(p1, p2) {
    var x1 = p1[0];
    var y1 = p1[1];
    var x2 = p2[0];
    var y2 = p2[1];

    function linePosition(point) {
        var x = point[0];
        var y = point[1];
        return (y2 - y1) * x + (x1 - x2) * y + (x2 * y1 - x1 * y2);
    }
    var relPoses = [
        [this.lt, this.tp],
        [this.lt, this.bt],
        [this.rt, this.tp],
        [this.rt, this.bt]
    ].map(linePosition);
    var noNegative = true;
    var noPositive = true;
    var noZero = true;
    relPoses.forEach(function(relPos) {
        if (relPos > 0) {
            noPositive = false;
        } else if (relPos < 0) {
            noNegative = false;
        } else if (relPos === 0) {
            noZero = false;
        }
    }, this);
    if ((noNegative || noPositive) && noZero) {
        return false;
    }
    return !((x1 > this.rt && x2 > this.rt) || (x1 < this.lt && x2 < this.lt) || (y1 < this.tp && y2 < this.tp) || (y1 > this.bt && y2 > this.bt));
};
Rect.prototype.toString = function() {
    return ["[", this.lt, ",", this.tp, "]", " [", this.wd, ",", this.ht, "]"].join("");
};
Rect.prototype.clone = function() {
    return new Rect(this.lt, this.tp, this.wd, this.ht);
};
