import unittest
from worlds.ff6wc.Options import verify_flagstring

standard_flagstring = (
    " -cg -oa 2.2.2.2.6.6.4.9.9 -ob 3.1.1.2.9.9.4.12.12.10.22.22 -oc 30.8.8.1.1.11.8 -od 59.1.1.11.31 "
    "-sc1 random -sc2 random -sc3 random -sal -eu -csrp 80 125 -fst -brl -slr 6 10 -lmprp 75 125 -lel "
    "-srr 25 35 -rnl -rnc -sdr 3 4 -das -dda -dns -sch -scis -com 98989898989898989898989898 -rec1 28 "
    "-rec2 27 -xpm 3 -mpm 5 -gpm 5 -nxppd -lsced 2 -hmced 2 -xgced 2 -ase 2 -msl 40 -sed -bbs -drloc "
    "shuffle -stloc mix -be -bnu -res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 2 5 -elrt -ebr 82 "
    "-emprp 75 125 -nm1 random -rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 "
    "-sto 1 -ieor 33 -ieror 33 -ir stronger -csb 7 15 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 5 -npi "
    "-sebr -snsb -snee -snil -ccsr 20 -chrm 0 0 -cms -frw -wmhc -cor 100 -crr 100 -crvr 100 120 -crm -ari "
    "-anca -adeh -ame 1 -nmc -noshoes -u254 -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -rr -etn "
)


class TestVerifyFlags(unittest.TestCase):
    def test_ok_flags(self) -> None:
        verify_flagstring(["-i", "x"])
        verify_flagstring([])
        verify_flagstring(["-i", standard_flagstring])
        verify_flagstring([
            "-i",
            "-cg -oa 2.6.6.3.r.3.r.3.r.5.r.5.r.5.r -ob 3.0.0 -oc 21.10.10.0.0 -od 22.5.5.0.0 -oe 23.5.5.0.0 -sc1 "
            "random -sc2 random -sal -eu -csrp 80 125 -fst -brl -slr 3 5 -lmprp 75 125 -lel -srr 25 35 -rnl -rnc "
            "-sdr 1 2 -das -dda -dns -sch -scis -com 98989898989898989898989898 -rec1 28 -rec2 97 -xpm 1 -mpm 5 "
            "-gpm 5 -nxppd -lsc 1 -hmc 1 -xgc 1 -ase 0.5 -msl 50 -sed -bbs -drloc shuffle -stloc mix -be -bnu "
            "-res -fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -elr -ebr 100 -emprp 75 125 -emi -nm1 random "
            "-rnl1 -rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 5000 -smc 3 -sws 0 -sto 1 -ieor 33 "
            "-ieror 33 -ir standard -csb 10 20 -mca -stra -saw -sisr 20 -sprp 75 125 -sdm 4 -npi -sebr -snsb "
            "-snee -snil -ccsr 20 -cms -frw -wmhc -cor -crr -crvr 255 255 -crm -cnee -cnil -ari -anca -adeh -nmc "
            "-nee -noshoes -nu -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -rr -rc -warp -move bd -etn -yremove"
        ])
        verify_flagstring([
            "-i",
            "-cg -oa 2.6.6.3.r.3.r.3.r.5.r.5.r.5.r -ob 3.0.0 -oc 21.10.10.0.0 -od 22.5.5.0.0 -oe 23.5.5.0.0 "
            "-sc1 random -sc2 random -sal -eu -csrp 80 125 -fst -brl -slr 3 5 -lmprp 75 125 -lel -srr 25 35 -rnl "
            "-rnc -sdr 1 2 -das -dda -dns -sch -scis -com 98989898989898989898989898 -rec1 28 -rec2 97 -xpm 1 -mpm 5 "
            "-gpm 5 -nxppd -lsc 1 -hmc 1 -xgc 1 -ase 0.5 -msl 50 -sed -bbs -drloc shuffle -stloc mix -be -bnu -res "
            "-fer 0 -escr 100 -dgne -wnz -mmnu -cmd -esr 1 5 -elr -ebr 100 -emprp 75 125 -emi -nm1 random -rnl1 "
            "-rns1 -nm2 random -rnl2 -rns2 -nmmi -mmprp 75 125 -gp 500000 -smc 3 -sws 0 -sto 1 -ieor 33 -ieror 33 "
            "-ir standard -csb 10 20 -mca -stra -saw -sisr 5 -sprv 0 0 -sdm 4 -npi -snbr -snes -snsb -snee -snil "
            "-ccsr 20 -cms -frw -wmhc -cor -crr -crvr 255 255 -crm -cnee -cnil -ari -anca -adeh -nmc -nee -noshoes "
            "-nu -nfps -fs -fe -fvd -fr -fj -fbs -fedc -fc -ond -rr -rc -warp -move bd -etn -yremove"
        ])

    def test_new_flags(self) -> None:
        """ some new flags from Worlds Collide 1.4.2 """
        verify_flagstring(["-i", "x", "-chrm", "0", "0"])

    def test_bad_flags(self) -> None:
        self.assertRaises(ValueError, verify_flagstring, ["-i", "x", "-bkbkb00"])
        # for these objective tests, see https://github.com/beauxq/Archipelago/pull/8 for more info

        # NOTE: for some reason, the ArgParse parser method is rejecting the entire flagstring,
        # and I'm not sure why...we are getting ValueError,
        # but not from the correct part of the code that is being reached when doing Generate.py
        # Bad Objective Result number (current values are 0-73)
        # self.assertRaises(KeyError, verify_flagstring, ["-i", "x", standardflagstring, " -oe 83.1.1.11.31 "])

        # Bad Objective Range, in this example:
        # Add 18-155 Enemy Levels for 1 random objective (max is 99)
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -oe 21.18.155.1.1.1.r "
        ])

        # Bad Objective Range, in this example:
        # Update MagPwr stat between -234 and +23 for 1-2 dragon kills (range -99 to 99)
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -oe 45.-234.23.1.1.6.1.2 "
        ])

        # Bad Objective Conditions min/max, in this example:
        # Ribbon for completing 2 of 1 conditions
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -oe 42.2.1.9.15.4.5.10.3.2 "
        ])
        # Bad Objective Condition Type (current range 0-12)
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -oe 65.1.1.22.31 "
        ])

        # Bad Objective Condition Value Range, in this example using random as a max
        # self.assertRaises(TypeError, verify_flagstring, [standardflagstring] + [" -oe 35.2.2.2.1.9.r "])

        # Bad Objective Condition Value Range, in this example missing the max condition
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -oe 8.4.4.3.1.3.3.3.3.3.5.5.5.8.12 "
        ])
        # Bad Objective Condition Value, it's missing from this one
        self.assertRaises(ValueError, verify_flagstring, [
            "-i", "x", standard_flagstring, " -of 40.4.4.3.6.3.3.0.9.2.5.16.12 "
        ])
