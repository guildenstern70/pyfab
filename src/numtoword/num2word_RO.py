# coding=utf-8


from __future__ import division 
import num2word_EU

    
class Num2Word_RO(num2word_EU.Num2Word_EU):
    def set_high_numwords(self, high):
        mx = 3 + 3*len(high)
        for word, n in zip(high, range(mx, 3, -3)):
            self.cards[10**n] = word + "ilioane"

    def setup(self):
        self.negword = "minus "
        self.pointword = "punct"
        self.errmsg_nonnum = "Numai numerele se pot transforma în cuvinte."
        self.exclude_title = ["și", "punct", "minus"]


        self.mid_numwords = [(1000, "o mie"), (100, "o sută"),
                             (90, "nouăzeci"), (80, "optzeci"), (70, "șaptezeci"),
                             (60, "șaizeci"), (50, "cincizeci"), (40, "patruzeci"),
                             (30, "treizeci")]
        self.low_numwords = ["douăzeci", "nouăsprezece", "optsprezece", "șaptisprezece",
                             "șaisprezece", "cincisprezece", "paisprezece", "treisprezece",
                             "doisprezece", "unsprezece", "zece", "nouă", "opt",
                             "șapte", "șase", "cinci", "patru", "trei", "doi",
                             "unu", "zero"]
        self.ords = { "unu"         : "primul",
                      "doi"         : "al doilea",
                      "trei"        : "al treilea",
                      "patru"       : "al patrulea",
                      "cinci"       : "al cincilea",
                      "șase"        : "al șaselea",
                      "șapte"       : "al șaptelea",
                      "opt"         : "al optulea",
                      "nouă"        : "al nouălea",
                      "doisprezece" : "al doisprezecelea" }


    def merge(self, curr, xnext):
        ctext, cnum, ntext, nnum = curr + xnext

        if cnum == 1 and nnum < 100:
            return xnext
        elif 100 > cnum > nnum :
            return ("%s-%s"%(ctext, ntext), cnum + nnum)
        elif cnum >= 100 > nnum:
            return ("%s and %s"%(ctext, ntext), cnum + nnum)
        elif nnum > cnum:
            return ("%s %s"%(ctext, ntext), cnum * nnum)
        return ("%s, %s"%(ctext, ntext), cnum + nnum)


    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == "y":
                lastword = lastword[:-1] + "ie" 
            lastword += "ea"
        lastwords[-1] = self.title(lastword) 
        outwords[-1] = "-".join(lastwords)
        return " ".join(outwords)


    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s"%(value, self.to_ordinal(value)[-2:])


    def to_year(self, val, longval=True):
        if not (val//100)%10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="hundred", jointxt="and",
                                longval=longval)

    def to_currency(self, val, longval=True):
        return self.to_splitnum(val, hightxt="dollar/s", lowtxt="cent/s",
                                jointxt="and", longval=longval)


n2w = Num2Word_RO()
to_card = n2w.to_cardinal
to_ord = n2w.to_ordinal
to_ordnum = n2w.to_ordinal_num
to_year = n2w.to_year

def main():
    print
    print '-- TEST NUMBERS --'
    for val in [ 1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1500, 1701, 3000,
             8280, 8291, 150000, 500000, 1000000, 2000000, 2000001,
             -21212121211221211111, -2.121212, -1.0000100]:
        n2w.test(val)
    print
    print '-- TEST YEARS --'
    for val in [1,120,1000,1120,1800, 1976,2000,2010,2099,2171]:
        print val, "is", n2w.to_year(val)
    

if __name__ == "__main__":
    main()
