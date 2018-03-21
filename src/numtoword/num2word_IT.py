# coding=utf-8


from __future__ import division 
import num2word_EU

    
class Num2Word_IT(num2word_EU.Num2Word_EU):
    def set_high_numwords(self, high):
        mx = 3 + 3*len(high)
        for word, n in zip(high, range(mx, 3, -3)):
            self.cards[10**n] = word + "ilioni"

    def setup(self):
        self.negword = "meno "
        self.pointword = "virgola"
        self.errmsg_nonnum = "Solo i numeri possono essere convertiti in parole."
        self.exclude_title = ["e", "virgola", "meno"]


        self.mid_numwords = [(1000, "mila"), (100, "cento"),
                             (90, "novanta"), (80, "ottanta"), (70, "settanta"),
                             (60, "sessanta"), (50, "cinquanta"), (40, "quaranta"),
                             (30, "trenta")]
        self.low_numwords = ["venti", "diciannove", "diciotto", "diciassette",
                             "sedici", "quindici", "quattordici", "tredici",
                             "dodici", "undici", "dieci", "nove", "otto",
                             "sette", "sei", "cinque", "quattro", "tre", "due",
                             "uno", "zero"]
        self.ords = { "uno"         : "primo",
                      "due"         : "secondo",
                      "tre"         : "terzo",
                      "quattro"     : "quarto",
                      "cinque"      : "quinto",
                      "sei"         : "sesto",
                      "sette"       : "settimo",
                      "otto"        : "ottavo",
                      "nove"        : "nono",
                      "dieci"       : "decimo" }



    def merge(self, curr, xnext):
        ctext, cnum, ntext, nnum = curr + xnext

        if cnum == 1 and nnum < 100:
            return xnext
        elif 100 > cnum > nnum :
            return ("%s%s"%(ctext, ntext), cnum + nnum)
        elif cnum >= 100 > nnum:
            return ("%s e %s"%(ctext, ntext), cnum + nnum)
        elif nnum > cnum:
            return ("%s%s"%(ctext, ntext), cnum * nnum)
        return ("%s, %s"%(ctext, ntext), cnum + nnum)


    def to_ordinal(self, value):
        self.verify_ordinal(value)
        outwords = self.to_cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        
        if (value < 11):
            lastword = self.ords[lastword]
        else:
            if (lastword[:-1] == 'a'):
                lastword = lastword[:-2] + "esimo"
            elif (lastword[:-1] == 'i'):
                lastword = lastword[:-2] + "esimo"
            elif (lastword[:-1] == 'e'):
                lastword = lastword[:-2] + "esimo"
            else:
                lastword = lastword[:-1] + "esimo"

        lastwords[-1] = self.title(lastword) 
        outwords[-1] = "".join(lastwords)
        return " ".join(outwords)


    def to_ordinal_num(self, value):
        self.verify_ordinal(value)
        return "%s%s"%(value, self.to_ordinal(value)[-2:])


    def to_year(self, val, longval=True):
        if not (val//100)%10:
            return self.to_cardinal(val)
        return self.to_splitnum(val, hightxt="centinaia", jointxt="e",
                                longval=longval)

    def to_currency(self, val, longval=True):
        return self.to_splitnum(val, hightxt="euro/o", lowtxt="centesimo/i",
                                jointxt="e", longval=longval)


n2w = Num2Word_IT()
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
                     
